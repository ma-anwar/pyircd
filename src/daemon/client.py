"""This module represents a client and defines client message handlers"""
import logging
from selectors import SelectorKey
from typing import Callable

import channel
import config
import constants
from constants import IRC_COMMANDS, IRC_ERRORS, IRC_REPLIES
from message import Message


class Client:
    """Class responsible for handling messages related to client connections
    channel_name is stored in lowercase for both `channels` and `joined_channels`
    The actual Channel.name is not stored in lowercase
    """

    registered_nicks = []
    channels = {}  # Key: channel_name, Value=Channel()

    def __init__(self, address: tuple, key: SelectorKey, unregister_callback: Callable):
        self._logger = logging.getLogger(__name__)
        self._is_registered = False
        self._nick = ""
        self._realname = ""
        self._username = ""
        self._key = key
        self.address = address
        self._unregister_callback = unregister_callback
        self._handlers = {
            IRC_COMMANDS.PING: self._handle_ping,
            IRC_COMMANDS.USER: self._handle_user,
            IRC_COMMANDS.NICK: self._handle_nick,
            IRC_COMMANDS.QUIT: self._handle_quit,
            IRC_COMMANDS.JOIN: self._handle_join
            # TODO: Implement _handle_part
            IRC_COMMANDS.LUSERS: self._handle_lusers,
        }
        self.joined_channels = {}  # Key=channel_name, Value=broadcast:callable

    @property
    def is_registered(self):
        """Get value of _is_registered"""
        return self._is_registered

    @is_registered.setter
    def is_registered(self, is_registered):
        """Set value of is_registered, call success handler if is_registered"""
        self._is_registered = is_registered
        if is_registered:
            self._send_registration_success()
            Client.registered_nicks.append(self._nick)

    def _send_registration_success(self):
        """Complete the registration flow as per IRC spec

        https://modern.ircdocs.horse/#connection-registration
        """
        self.send_message(IRC_REPLIES.WELCOME, f":Welcome to {config.SERVER_NAME}")
        self.send_message(IRC_REPLIES.YOURHOST, ":This daemon is being developed.")
        self.send_message(IRC_REPLIES.CREATED, ":This server was started recently")
        self.send_message(IRC_REPLIES.MYINFO, f":{config.SERVER_NAME} More info sooon!")

    def handle_message(self, message: Message):
        """Handle message by invoking registration flow"""
        self._logger.debug(f"{self.address} - {message}")

        if not self.is_registered:
            self._handle_registration_flow(message)
            return

        if message.command in self._handlers.keys():
            handler = self._handlers[message.command]
            handler(message)

    def _handle_registration_flow(self, message: Message):
        """Handle registration state and ultimately send reply on success WIP"""
        if message.command == IRC_COMMANDS.NICK:
            self._handle_nick(message)

        if message.command == IRC_COMMANDS.USER:
            self._handle_user(message)

        # user_name implies realname is present
        if self._username and self._nick:
            self.is_registered = True

    def _handle_nick(self, message: Message):
        """Handle NICK command"""
        if self._is_registered:
            return

        candidate_nick = message.parameters[0] if len(message.parameters) > 0 else None

        if not candidate_nick:
            self.send_message(IRC_ERRORS.NO_NICKNAME_GIVEN, ":No nickname given")
            return

        if candidate_nick in Client.registered_nicks:
            self.send_message(
                IRC_ERRORS.NICKNAME_IN_USE,
                f"{candidate_nick}:Nickname is already in use",
            )
            return

        self._nick = candidate_nick

    def _handle_user(self, message: Message):
        """Handle USER command"""
        if self.is_registered:
            self.send_message(
                IRC_ERRORS.ALREADY_REGISTERED,
                ":Unauthorized command (already registered)",
            )
            return

        if len(message.parameters) < 4:
            self.send_message(
                IRC_ERRORS.NEED_MORE_PARAMS, "USER :Not enough parameters"
            )
            return

        candidate_username = message.parameters[0]
        candidate_realname = message.parameters[3]

        if candidate_username == "" or candidate_realname == "":
            self.send_message(
                IRC_ERRORS.NEED_MORE_PARAMS,
                "USER :username or realname not long enough",
            )
            return

        self._username = candidate_username
        self._realname = candidate_realname

    def _handle_ping(self, message: Message):
        """Handle PING command"""
        if not len(message.parameters) or not len(message.parameters[0]):
            self.send_message(IRC_ERRORS.NEED_MORE_PARAMS, "PING :a token must be sent")
            return

        token = message.parameters[0]
        self.send_message(
            IRC_COMMANDS.PONG, f"{config.SERVER_NAME} {token}", include_nick=False
        )

    def _handle_quit(self, message: Message):
        """Handle QUIT command"""
        reason = message.parameters[0] if message.parameters else ""
        self.send_message(IRC_COMMANDS.ERROR, f"QUIT: {reason}")

        # Signal to Server to unregister after sending QUIT
        self._key.data.unregister_socket = True
        # Unregister from message_bus
        self._unregister_callback()

    def _handle_join(self, message: Message):
        """Handle JOIN command"""
        if len(message.parameters) < 1:  # Error case
            self.send_message(IRC_ERRORS.NEED_MORE_PARAMS, ":Not enough parameters")
            return

        elif (
            len(message.parameters) > 1
        ):  # Recursive case for processing multiple channels
            parameters = message.parameters
            for param in parameters:
                message.parameters = [param]
                self._handle_join(message)

        else:  # Base case
            channel_name = message.parameters[0]

            if channel_name.lower() in self.joined_channels:
                return
            if len(channel_name) < 1 or channel_name[0] != "#":
                return
            if channel_name not in Client.channels:  # If not exists, create new channel
                for x in constants.FORBIDDEN_CHANNELNAME_CHARS:
                    if x in channel_name:
                        self.send_message(
                            IRC_ERRORS.BADCHANMASK, "Invalid channel name!"
                        )
                        return
                new_channel = channel.Channel(channel_name)
                Client.channels[channel_name.lower()] = new_channel

            # Check whether client is already in channel
            if (
                self.address
                in Client.channels[channel_name.lower()].get_client_addresses()
            ):
                self.send_message(
                    numeric=constants.IRC_ERRORS.USERONCHANNEL,
                    message=f" \
                        {Client.channels[channel_name.lower()].get_channel_name()} \
                        :is already on channel",
                    include_nick=True,
                )
                return

            # Register and get broadcast function from channel
            broadcast = Client.channels[channel_name.lower()].register(
                self.address, self.send_message, self._nick
            )

            # Add channel to joined_channels with broadcast function as value
            self.joined_channels[channel_name.lower()] = broadcast

            # Send JOIN message to channel members and client
            self.broadcast_arrival(broadcast, channel_name)

            # Send topic in reply only if there is a topic
            self.send_topic(channel_name)

            # Send list of users in channel
            members = Client.channels[channel_name.lower()].get_members()
            members_str = ", ".join(members)
            self.send_message(
                IRC_REPLIES.NAMREPLY,
                message=f"={channel_name} :{members_str}",
                include_nick=True,
            )
            self.send_message(IRC_REPLIES.ENDOFNAMES, message=":End of /NAMES list")

    def broadcast_arrival(self, broadcast: callable, channel_name: str):
        """Send JOIN messages announcing that user has arrived"""
        # Send JOIN message to channel
        broadcast(
            numeric="JOIN", message=f"{self._nick} {channel_name}", include_nick=False
        )
        # Send JOIN message to client
        self.send_message("JOIN", message=f"{channel_name}")

    def send_topic(self, channel_name):
        """Send topic to client"""
        topic = Client.channels[channel_name.lower()].get_topic()
        if topic != "":
            topic_code = IRC_REPLIES.TOPIC
            self.send_message(topic_code, message=f": {topic}", include_nick=False)
    def _handle_lusers(self, message: Message):
        """Handle LUSERS command"""
        # Check if error checking needed for extra params and stuff.
        # figure out user name
        # document why 0 for both
        num_users = len(self.registered_nicks)
        self.send_message(
            numeric=IRC_REPLIES.LUSERCLIENT,
            message=f":There are {num_users} users and 0 invisible on 0 servers",
            include_nick=True,
        )
        self.send_message(
            numeric=IRC_REPLIES.LUSERME,
            message=f":I have {num_users} clients and 0 servers",
            include_nick=True,
        )

    def send_message(self, numeric: str, message: str, include_nick: bool = True):
        """Write message to the out buffer of this client instance

        Constructs message according to spec below
        https://modern.ircdocs.horse/#numeric-replies
        numeric: 3 digit code per docs
        message: utf-8 string, optionally terminated with \r\n
        """
        if include_nick:
            constructed_messsage = (
                f"{constants.MESSAGE_PREFIX} {numeric} {self._nick} {message}"
            )
        else:
            constructed_messsage = f"{constants.MESSAGE_PREFIX} {numeric} {message}"

        message_as_bytes = constructed_messsage.encode()

        if not message_as_bytes.endswith(constants.IRC_TERMINATION_DELIMITER):
            message_as_bytes += constants.IRC_TERMINATION_DELIMITER

        self._key.data.out_buffer += message_as_bytes
