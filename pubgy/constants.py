SHARD_LIST = ["steam", "kakao", "tournament", "psn", "xbox", "console", "stadia"]
PLATFORM_REGION = ["pc-as", "pc-eu", "pc-jp", "pc-kakao", "pc-krjp"]
DEFAULT_SHARD = SHARD_LIST[0]
BASE_URL = "https://api.pubg.com/shards/"
DEBUG_URL = "https://api.pubg.com/status"
MATCHES_ROUTE = "matches"
PLAYERNAME_ROUTE = "players?filter[playerNames]="
PLAYERID_ROUTE = "players"
PLAYERIDLIST = "players?filter[playerIds]="
SAMPLE_ROUTE = "samples"
MATCH_TYPES = ["arcade", "custom", "event", "official", "training"]
TEL_REF = {"Desert_Main": "Miramar",
           "DihorOtok_Main": "Vikendi",
           "Erangel_Main": "Erangel",
           "Baltic_Main": "Erangel (Remastered)",
           "Range_Main": "Camp Jackal",
           "Savage_Main": "Sanhok",
           "Summerland_Main": "Karakin"}
STATS = {
    "all": "lifetime"
}