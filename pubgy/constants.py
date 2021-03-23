"""
Copyright (c) 2018-2021 Discordian

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Some of the contents from this file comes from https://github.com/pubg/api-assets
"""
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
MAP_LIST = {
    "Desert_Main": "Miramar",
    "DihorOtok_Main": "Vikendi",
    "Erangel_Main": "Erangel",
    "Baltic_Main": "Erangel (Remastered)",
    "Range_Main": "Camp Jackal",
    "Savage_Main": "Sanhok",
    "Summerland_Main": "Karakin",
    "Heaven_Main": "Heaven"
}
GAME_MODES = {
    "duo": "Duo TPP",
    "duo-fpp": "Duo FPP",
    "solo": "Solo TPP",
    "solo-fpp": "Solo FPP",
    "squad": "Squad TPP",
    "squad-fpp": "Squad FPP",
    "conquest-duo": "Conquest Duo TPP",
    "conquest-duo-fpp": "Conquest Duo FPP",
    "conquest-solo": "Conquest Solo TPP",
    "conquest-solo-fpp": "Conquest Solo FPP",
    "conquest-squad": "Conquest Squad TPP",
    "conquest-squad-fpp": "Conquest Squad FPP",
    "esports-duo": "Esports Duo TPP",
    "esports-duo-fpp": "Esports Duo FPP",
    "esports-solo": "Esports Solo TPP",
    "esports-solo-fpp": "Esports Solo FPP",
    "esports-squad": "Esports Squad TPP",
    "esports-squad-fpp": "Esports Squad FPP",
    "normal-duo": "Duo TPP",
    "normal-duo-fpp": "Duo FPP",
    "normal-solo": "Solo TPP",
    "normal-solo-fpp": "Solo FPP",
    "normal-squad": "Squad TPP",
    "normal-squad-fpp": "Squad FPP",
    "war-duo": "War Duo TPP",
    "war-duo-fpp": "War Duo FPP",
    "war-solo": "War Solo TPP",
    "war-solo-fpp": "War Solo FPP",
    "war-squad": "Squad TPP",
    "war-squad-fpp": "War Squad FPP",
    "zombie-duo": "Zombie Duo TPP",
    "zombie-duo-fpp":"Zombie Duo FPP",
    "zombie-solo": "Zombie Solo TPP",
    "zombie-solo-fpp": "Zombie Solo FPP",
    "zombie-squad": "Zombie Squad TPP",
    "zombie-squad-fpp": "Zombie Squad FPP",
    "lab-tpp": "Lab TPP",
    "lab-fpp": "Lab FPP",
    "tdm": "Team Deathmatch"
}
STATS = {
    "all": "lifetime"
}