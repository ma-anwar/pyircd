"""This module holds constants used throughout the daemon"""

NICK_COMMAND = b"NICK"
USER_COMMAND = b"USER"
IRC_TERMINATION_DELIMITER = b"\r\n"
EMPTY_STRING = b""
# Most IRC servers limit messages to 512 bytes in length
# https://modern.ircdocs.horse/#message-format
RECEIVE_LENGTH = 1024
MAX_LINE_LENGTH = 512

# +1 for \n since find gives us index of \r
# +1 bc end index is not inclusive
DELIMITER_END_INDEX = 2

NOT_FOUND = -1
LOCAL_HOST = "127.0.0.1"
DEFAULT_PORT = 6667

ACCEPTED_ACTIONS = ["PARSE", "PASS", "NICK", "USER", "PING", "PONG", "QUIT"]

# Based on https://modern.ircdocs.horse/#client-messages
VALID_ALPHA_COMMANDS = [
    "CAP",
    "AUTHENTICATE",
    "PASS",
    "NICK",
    "USER",
    "PING",
    "PONG",
    "OPER",
    "QUIT",
    "ERROR",
    "JOIN",
    "PART",
    "TOPIC",
    "NAMES",
    "LIST",
    "INVITE",
    "KICK",
    "MOTD",
    "VERSION",
    "ADMIN",
    "CONNECT",
    "TIME",
    "STATS",
    "HELP",
    "INFO",
    "MODE",
    "PRIVMSG",
    "NOTICE",
    "WHO",
    "WHOIS",
    "WHOWAS",
    "KILL",
    "REHASH",
    "RESTART",
    "SQUIT",
    "AWAY",
    "LINKS",
    "USERHOST",
    "WALLOPS",
]

# Based on https://www.alien.net.au/irc/irc2numerics.html
VALID_NUMERIC_COMMANDS = [
    "001",
    "002",
    "003",
    "004",
    "005",
    "006",
    "007",
    "008",
    "009",
    "010",
    "014",
    "015",
    "016",
    "017",
    "042",
    "043",
    "050",
    "051",
    "200",
    "201",
    "202",
    "203",
    "204",
    "205",
    "206",
    "207",
    "208",
    "209",
    "210",
    "211",
    "212",
    "213",
    "214",
    "215",
    "216",
    "217",
    "218",
    "219",
    "220",
    "221",
    "222",
    "223",
    "224",
    "225",
    "226",
    "227",
    "228",
    "231",
    "232",
    "233",
    "234",
    "235",
    "236",
    "237",
    "238",
    "239",
    "240",
    "241",
    "242",
    "243",
    "244",
    "245",
    "246",
    "247",
    "248",
    "249",
    "250",
    "251",
    "252",
    "253",
    "254",
    "255",
    "256",
    "257",
    "258",
    "259",
    "261",
    "262",
    "263",
    "265",
    "266",
    "267",
    "268",
    "269",
    "270",
    "271",
    "272",
    "273",
    "274",
    "275",
    "276",
    "277",
    "278",
    "280",
    "281",
    "282",
    "283",
    "284",
    "285",
    "286",
    "287",
    "288",
    "289",
    "290",
    "291",
    "292",
    "293",
    "294",
    "295",
    "296",
    "299",
    "300",
    "301",
    "302",
    "303",
    "304",
    "305",
    "306",
    "307",
    "308",
    "309",
    "310",
    "311",
    "312",
    "313",
    "314",
    "315",
    "316",
    "317",
    "318",
    "319",
    "320",
    "321",
    "322",
    "323",
    "324",
    "325",
    "326",
    "327",
    "328",
    "329",
    "330",
    "331",
    "332",
    "333",
    "334",
    "335",
    "338",
    "339",
    "340",
    "341",
    "342",
    "345",
    "346",
    "347",
    "348",
    "349",
    "351",
    "352",
    "353",
    "354",
    "355",
    "357",
    "358",
    "359",
    "361",
    "362",
    "363",
    "364",
    "365",
    "366",
    "367",
    "368",
    "369",
    "371",
    "372",
    "373",
    "374",
    "375",
    "376",
    "377",
    "378",
    "379",
    "380",
    "381",
    "382",
    "383",
    "384",
    "385",
    "386",
    "387",
    "388",
    "389",
    "391",
    "392",
    "393",
    "394",
    "395",
    "396",
    "400",
    "401",
    "402",
    "403",
    "404",
    "405",
    "406",
    "407",
    "408",
    "409",
    "411",
    "412",
    "413",
    "414",
    "415",
    "416",
    "419",
    "421",
    "422",
    "423",
    "424",
    "425",
    "429",
    "430",
    "431",
    "432",
    "433",
    "434",
    "435",
    "436",
    "437",
    "438",
    "439",
    "440",
    "441",
    "442",
    "443",
    "444",
    "445",
    "446",
    "447",
    "449",
    "451",
    "452",
    "453",
    "455",
    "456",
    "457",
    "458",
    "459",
    "460",
    "461",
    "462",
    "463",
    "464",
    "465",
    "466",
    "467",
    "468",
    "469",
    "470",
    "471",
    "472",
    "473",
    "474",
    "475",
    "476",
    "477",
    "478",
    "479",
    "480",
    "481",
    "482",
    "483",
    "484",
    "485",
    "486",
    "487",
    "488",
    "489",
    "491",
    "492",
    "493",
    "494",
    "495",
    "496",
    "497",
    "498",
    "499",
    "501",
    "502",
    "503",
    "504",
    "511",
    "512",
    "513",
    "514",
    "515",
    "516",
    "517",
    "518",
    "519",
    "520",
    "521",
    "522",
    "523",
    "524",
    "525",
    "526",
    "550",
    "551",
    "552",
    "553",
    "600",
    "601",
    "602",
    "603",
    "604",
    "605",
    "606",
    "607",
    "608",
    "610",
    "611",
    "612",
    "613",
    "615",
    "616",
    "617",
    "618",
    "619",
    "620",
    "621",
    "622",
    "623",
    "624",
    "625",
    "626",
    "630",
    "631",
    "640",
    "641",
    "642",
    "660",
    "661",
    "662",
    "663",
    "664",
    "665",
    "666",
    "670",
    "671",
    "672",
    "673",
    "678",
    "679",
    "682",
    "687",
    "688",
    "689",
    "690",
    "702",
    "703",
    "704",
    "705",
    "706",
    "708",
    "709",
    "710",
    "711",
    "712",
    "713",
    "714",
    "715",
    "716",
    "717",
    "718",
    "720",
    "721",
    "722",
    "723",
    "724",
    "725",
    "726",
    "771",
    "773",
    "774",
    "972",
    "973",
    "974",
    "975",
    "976",
    "977",
    "979",
    "980",
    "981",
    "982",
    "983",
    "999",
]
