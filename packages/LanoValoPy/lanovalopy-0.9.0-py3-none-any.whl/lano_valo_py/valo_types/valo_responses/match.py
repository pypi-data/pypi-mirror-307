# --- Metadata models ---
from typing import List, Optional

from pydantic import BaseModel


class MatchOSModel(BaseModel):
    name: str
    version: str


class MatchPlatformModel(BaseModel):
    type: str
    os: MatchOSModel


class MatchSessionPlaytimeModel(BaseModel):
    minutes: int
    seconds: int
    milliseconds: int


class MatchAssetsCardModel(BaseModel):
    small: str
    large: str
    wide: str


class MatchAssetsAgentModel(BaseModel):
    small: str
    full: str
    bust: str
    killfeed: str


class MatchAssetsModel(BaseModel):
    card: MatchAssetsCardModel
    agent: MatchAssetsAgentModel


class MatchFriendlyFireModel(BaseModel):
    incoming: int
    outgoing: int


class MatchBehaviourModel(BaseModel):
    afk_rounds: int
    friendly_fire: MatchFriendlyFireModel
    rounds_in_spawn: int


class MatchAbilityCastsModel(BaseModel):
    c_cast: int
    q_cast: int
    e_cast: int
    x_cast: int


class MatchStatsModel(BaseModel):
    score: int
    kills: int
    deaths: int
    assists: int
    bodyshots: int
    headshots: int
    legshots: int


class MatchEconomySpentModel(BaseModel):
    overall: float
    average: float


class MatchEconomyLoadoutValueModel(BaseModel):
    overall: float
    average: float


class MatchEconomyModel(BaseModel):
    spent: MatchEconomySpentModel
    loadout_value: MatchEconomyLoadoutValueModel


class MatchPlayerModel(BaseModel):
    puuid: Optional[str] = None
    name: str
    tag: str
    team: str
    level: int
    character: str
    currenttier: int
    currenttier_patched: str
    player_card: str
    player_title: str
    party_id: str
    session_playtime: MatchSessionPlaytimeModel
    assets: MatchAssetsModel
    behaviour: Optional[MatchBehaviourModel] = None
    platform: MatchPlatformModel
    ability_casts: MatchAbilityCastsModel
    stats: MatchStatsModel
    economy: MatchEconomyModel
    damage_made: int
    damage_received: int


# --- Team Models ---
class MatchTeamModel(BaseModel):
    has_won: bool
    rounds_won: int
    rounds_lost: int


# --- Main Models ---


class MachPremierInfoModel(BaseModel):
    tournament_id: Optional[str]
    matchup_id: Optional[str]


class MatchMetadataModel(BaseModel):
    map: str
    game_version: str
    game_length: int
    game_start: int
    game_start_patched: str
    rounds_played: int
    mode: str
    mode_id: str
    queue: str
    season_id: str
    platform: str
    matchid: str
    premier_info: Optional[MachPremierInfoModel]
    region: str
    cluster: str


class MatchPlayersModel(BaseModel):
    all_players: List[MatchPlayerModel]
    red: List[MatchPlayerModel]
    blue: List[MatchPlayerModel]


class MatchObserversModel(BaseModel):
    puuid: str
    name: str
    tag: str
    platform: MatchPlatformModel
    session_playtime: MatchSessionPlaytimeModel
    team: str
    level: int
    player_card: str
    player_title: str
    party_id: str


class MatchCoachesModel(BaseModel):
    puuid: str
    team: str


class MatchTeamsModel(BaseModel):
    red: MatchTeamModel
    blue: MatchTeamModel


class MatchResponseModel(BaseModel):
    metadata: MatchMetadataModel
    players: MatchPlayersModel
    observers: List[MatchObserversModel]
    coaches: List[MatchCoachesModel]
    teams: MatchTeamsModel
