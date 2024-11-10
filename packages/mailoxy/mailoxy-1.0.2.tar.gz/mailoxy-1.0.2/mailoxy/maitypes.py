from datetime import datetime
from random import randint
from time import time
from typing import List, Dict, Annotated

from orjson import dumps
from pydantic import BaseModel, field_serializer, AfterValidator, PlainSerializer, WithJsonSchema, ValidationError

from mailoxy.db_types import PydanticIcon, PydanticPlate, PydanticTitle, PydanticPartner, PydanticMap, PydanticFrame, PydanticChara, PydanticTicket, PydanticCourse, RegionEnum, PydanticMusic, PydanticLoginBonus, DifficultyEnum, ScoreEnum, SyncEnum, ComboEnum, LogoutTypeEnum, other_db
from mailoxy.dmr import NotesInfo, PlayModeEnum, ActivityCodeEnum, ItemKindEnum, Music
from mailoxy.divingfish import DivingFishMusicDetail

plaet_name_list = ["真", "超", "檄", "橙", "暁", "桃", "櫻", "紫", "菫", "白", "雪", "輝", "舞", "熊&華", "爽&煌", "宙&星", "祭&祝"]


def isToday(timestamp: int):
    return datetime.fromtimestamp(timestamp).date() == datetime.now().date()


def get_nameplate_music_list(name: str) -> List[Music]:
    for n in plaet_name_list:
        if name in n:
            name = n
    for i in other_db.get_dict('MusicGroup_dict').values():
        if name == i.name.name:
            return [other_db.get_dict('Music_dict')[k.ID] for k in i.MusicIds]
    return []


def random_deluxscore_max(notes_max: int, star_num: int) -> int:
    match star_num:
        case 0:
            return randint(int(notes_max * 3 * 0.8), int(notes_max * 3 * 0.85))
        case 1:
            return randint(int(notes_max * 3 * 0.85), int(notes_max * 3 * 0.90))
        case 2:
            return randint(int(notes_max * 3 * 0.90), int(notes_max * 3 * 0.93))
        case 3:
            return randint(int(notes_max * 3 * 0.93), int(notes_max * 3 * 0.95))
        case 4:
            return randint(int(notes_max * 3 * 0.95), int(notes_max * 3 * 0.97))
        case 5:
            return int(notes_max * 3 * 0.97) + 1
    return randint(int(notes_max * 3 * 0.8), int(notes_max * 3 * 0.85))


def new_music_version_int() -> int:
    return max(other_db.db_module.MusicVersion_dict.keys())


def is_new_music(this) -> bool:
    return this.musicId.AddVersion.ID == new_music_version_int()


def calculate_rating(ds: float, achievement: float) -> int:
    if ds > 15.9 or ds < 0:
        raise ValueError("Invalid ds value")
    if achievement > 101.0000 or achievement < 0:
        raise ValueError("Invalid achievement value")
    achievement_list = [100.5000, 100.4999, 100.0000,
                        99.9999, 99.5000, 99.0000, 98.9999,
                        98.0000, 97.0000, 96.9999, 94.0000,
                        90.0000, 80.0000, 79.9999, 75.0000,
                        70.0000, 60.0000, 50.0000, 40.0000,
                        30.0000, 20.0000, 10.0000, 0]
    multiplier_list = [0.224, 0.222, 0.216,
                       0.214, 0.211, 0.208, 0.206,
                       0.203, 0.2, 0.176, 0.168,
                       0.152, 0.136, 0.128, 0.12,
                       0.112, 0.096, 0.08, 0.064,
                       0.048, 0.032, 0.016, 0]
    for i in range(len(achievement_list)):
        if achievement >= achievement_list[i]:
            multiplier = multiplier_list[i]
            break
    if achievement >= 100.5000:
        achievement = 100.5000
    return int(ds * achievement * multiplier)


def calculate_scoreRank(achievement: float) -> ScoreEnum:
    if achievement > 101.0000 or achievement < 0:
        raise ValueError("Invalid achievement value")
    achievement_list = [100.5000, 100.0000,
                        99.5000, 99.0000,
                        98.0000, 97.0000,
                        94.0000, 90.0000, 80.0000,
                        75.0000, 70.0000, 60.0000,
                        50.0000, 0]
    for i in range(len(achievement_list)):
        if achievement >= achievement_list[i]:
            return ScoreEnum(len(achievement_list) - 1 - i)


def make_0_time(timestamp: int | float) -> str:
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S') + ".0"


def from_0_time(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')


def after(value: str | datetime | int | float) -> datetime:
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    elif isinstance(value, datetime):
        return value
    elif isinstance(value, int) or isinstance(value, float):
        return datetime.fromtimestamp(value)
    raise ValueError()


def plain_datetime(value: str | datetime | int | float) -> str:
    if isinstance(value, str):
        return value
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, int) or isinstance(value, float):
        return datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
    raise ValueError()


def plain_date(value: str | datetime | int | float) -> str:
    if isinstance(value, str):
        return value
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, int) or isinstance(value, float):
        return datetime.fromtimestamp(value).strftime("%Y-%m-%d")
    raise ValueError()


MaiDatetime = Annotated[
    str | int | float | datetime,
    AfterValidator(after),
    PlainSerializer(plain_datetime, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
MaiDate = Annotated[
    str | int | float | datetime,
    AfterValidator(after),
    PlainSerializer(plain_datetime, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


class MaiConfig(BaseModel):
    mai2_salt: str
    aes_key: bytes
    aes_iv: bytes
    chime_salt: str
    region: RegionEnum
    place_name: str
    place_id: int
    keychip: str
    rom_version: str
    data_version: str
    proxy: str = ''
    https_verify: bool = False
    retry: int = 3

    @property
    def romVersionInt(self) -> int:
        return int(self.rom_version.replace(".", "0"))

    @property
    def dataVersionInt(self) -> int:
        return int(self.data_version.replace(".", "0"))

    @property
    def client_id(self) -> str:
        return self.keychip[:4] + self.keychip[5:12]


class UserId(BaseModel):
    userId: int

    def extend(self, **kwargs):
        res = self.model_dump()
        res.update(**kwargs)
        return dumps(res).decode()


class UpsertClientTestmodePacket(BaseModel):
    placeId: int
    clientId: str
    trackSingle: int = 1
    trackMulti: int = 0
    trackEvent: int = 4
    totalMachine: int = 5
    satelliteId: int = 5
    cameraPosition: int = 1


class UpsertClientTestmodeOuterPacket(BaseModel):
    clientTestmode: UpsertClientTestmodePacket


class UserPreview(BaseModel):
    userId: int
    userName: str
    isLogin: bool
    lastGameId: str | None
    lastRomVersion: str
    lastDataVersion: str
    lastLoginDate: MaiDatetime
    lastPlayDate: MaiDatetime
    playerRating: int
    nameplateId: int
    iconId: int
    trophyId: int
    isNetMember: int
    isInherit: bool
    totalAwake: int
    dispRate: int
    dailyBonusDate: MaiDatetime
    headPhoneVolume: int | None
    banState: int


class UserLoginPacket(BaseModel):
    userId: int
    accessCode: str = ""
    regionId: RegionEnum
    placeId: int
    clientId: str
    dateTime: int
    isContinue: bool = False
    genericFlag: int = 0


class UserLogin(BaseModel):
    returnCode: int
    lastLoginDate: MaiDatetime | None
    loginCount: int | None
    consecutiveLoginCount: int | None
    loginId: int | None


class UserData(BaseModel):
    accessCode: str = ""
    userName: str
    isNetMember: int
    iconId: PydanticIcon
    plateId: PydanticPlate
    titleId: PydanticTitle
    partnerId: PydanticPartner
    frameId: PydanticFrame
    selectMapId: PydanticMap
    totalAwake: int
    gradeRating: int
    musicRating: int
    playerRating: int
    highestRating: int
    gradeRank: int
    classRank: int
    courseRank: int
    charaSlot: List[PydanticChara]
    charaLockSlot: List[PydanticChara]
    contentBit: int
    playCount: int
    currentPlayCount: int
    renameCredit: int
    mapStock: int
    eventWatchedDate: str
    lastGameId: str | None
    lastRomVersion: str
    lastDataVersion: str
    lastLoginDate: str
    lastPlayDate: str
    lastPlayCredit: int
    lastPlayMode: int
    lastPlaceId: int
    lastPlaceName: str | None
    lastAllNetId: int
    lastRegionId: RegionEnum
    lastRegionName: str
    lastClientId: str | None
    lastCountryCode: str
    lastSelectEMoney: int
    lastSelectTicket: PydanticTicket
    lastSelectCourse: PydanticCourse
    lastCountCourse: int
    firstGameId: str
    firstRomVersion: str
    firstDataVersion: str
    firstPlayDate: MaiDatetime
    compatibleCmVersion: str
    dailyBonusDate: MaiDatetime
    dailyCourseBonusDate: MaiDatetime
    lastPairLoginDate: MaiDatetime
    lastTrialPlayDate: MaiDatetime
    playVsCount: int
    playSyncCount: int
    winCount: int
    helpCount: int
    comboCount: int
    totalDeluxscore: int
    totalBasicDeluxscore: int
    totalAdvancedDeluxscore: int
    totalExpertDeluxscore: int
    totalMasterDeluxscore: int
    totalReMasterDeluxscore: int
    totalSync: int
    totalBasicSync: int
    totalAdvancedSync: int
    totalExpertSync: int
    totalMasterSync: int
    totalReMasterSync: int
    totalAchievement: int
    totalBasicAchievement: int
    totalAdvancedAchievement: int
    totalExpertAchievement: int
    totalMasterAchievement: int
    totalReMasterAchievement: int
    playerOldRating: int
    playerNewRating: int
    banState: int
    dateTime: int | None
    # "nameplateId": 0,
    # "trophyId": 0,
    # friendCode: int
    # cmLastEmoneyCredit: int
    # cmLastEmoneyBrand: int


class UserCharacter(BaseModel):
    characterId: PydanticChara
    level: int = 1
    awakening: int = 0
    useCount: int = 0


class UserItem(BaseModel):
    itemKind: ItemKindEnum
    itemId: int
    stock: int = 1
    isValid: bool = True


class UserPlate(UserItem):
    itemId: PydanticPlate


class UserTitle(UserItem):
    itemId: PydanticTitle


class UserIcon(UserItem):
    itemId: PydanticIcon


class UserMusic(UserItem):
    itemId: PydanticMusic


class UserChara(UserItem):
    itemId: PydanticChara


class UserPartner(UserItem):
    itemId: PydanticPartner


class UserFrame(UserItem):
    itemId: PydanticFrame


class UserTicket(UserItem):
    itemId: PydanticTicket


class UserCourse(BaseModel):
    courseId: PydanticCourse
    isLastClear: bool
    totalRestlife: int
    totalAchievement: int
    totalDeluxscore: int
    bestAchievement: int
    bestDeluxscore: int
    bestAchievementDate: MaiDatetime
    bestDeluxscoreDate: MaiDatetime
    playCount: int
    clearDate: MaiDatetime | None
    lastPlayDate: MaiDatetime
    extNum1: int


class UserChargelog(BaseModel):
    chargeId: PydanticTicket
    price: int
    purchaseDate: str
    playCount: int
    playerRating: int
    placeId: int
    regionId: RegionEnum
    clientId: str


class UserCharge(BaseModel):
    chargeId: PydanticTicket
    stock: int
    purchaseDate: MaiDatetime
    validDate: MaiDatetime


class UserChargeP(UserCharge):
    purchaseDate: str


class UserMap(BaseModel):
    mapId: PydanticMap
    distance: int
    isLock: bool
    isClear: bool
    isComplete: bool
    unlockFlag: int


class UserLoginBonus(BaseModel):
    bonusId: PydanticLoginBonus
    point: int
    isCurrent: bool
    isComplete: bool


class UserRegion(BaseModel):
    regionId: RegionEnum
    playCount: int
    created: MaiDatetime


class UserOption(BaseModel):
    optionKind: int
    noteSpeed: int
    slideSpeed: int
    touchSpeed: int
    tapDesign: int
    holdDesign: int
    slideDesign: int
    starType: int
    outlineDesign: int
    noteSize: int
    slideSize: int
    touchSize: int
    tapDesign: int
    starRotate: int
    dispCenter: int
    outFrameType: int
    dispChain: int
    dispRate: int
    dispBar: int
    touchEffect: int
    submonitorAnimation: int
    submonitorAppeal: int
    submonitorAchive: int
    matching: int
    trackSkip: int
    brightness: int
    mirrorMode: int
    dispJudge: int
    dispJudgePos: int
    dispJudgeTouchPos: int
    adjustTiming: int
    judgeTiming: int
    ansVolume: int
    tapHoldVolume: int
    criticalSe: int
    tapSe: int
    breakSe: int
    breakVolume: int
    exSe: int
    exVolume: int
    slideSe: int
    slideVolume: int
    breakSlideVolume: int
    touchVolume: int
    touchHoldVolume: int
    damageSeVolume: int
    headPhoneVolume: int
    sortTab: int
    sortMusic: int

    # tempoVolume: int
    @property
    def isCriticalDisp(self) -> bool:
        return self.dispJudge >= 5

    @property
    def isHLPerfectDisp(self) -> bool:
        return self.dispJudge >= 10


class UserExtend(BaseModel):
    selectMusicId: int
    selectDifficultyId: int
    categoryIndex: int
    musicIndex: int
    extraFlag: int
    selectScoreType: int
    extendContentBit: int
    isPhotoAgree: bool = False
    isGotoCodeRead: bool = False
    selectResultDetails: bool
    selectResultScoreViewType: int
    sortCategorySetting: int
    sortMusicSetting: int
    playStatusSetting: int
    selectedCardList: List[int | None]
    encountMapNpcList: List[Dict[str, int] | None]

    @field_serializer('selectedCardList')
    def serialize_scl(self, selectedCardList: List[int | None], _info):
        return []

    @field_serializer('encountMapNpcList')
    def serialize_emnl(self, encountMapNpcList: List[Dict[str, int] | None], _info):
        return []


class MusicRecord(BaseModel):
    musicId: PydanticMusic
    level: DifficultyEnum
    romVersion: int
    achievement: int

    @property
    def rating(self) -> int:
        return calculate_rating(self.musicId.notes[self.level.value].ds, self.achievement / 1_0000)


class UdemaeRecord(BaseModel):
    rate: int
    maxRate: int
    classValue: int
    maxClassValue: int
    totalWinNum: int
    totalLoseNum: int
    maxWinNum: int
    maxLoseNum: int
    winNum: int
    loseNum: int
    npcTotalWinNum: int
    npcTotalLoseNum: int
    npcMaxWinNum: int
    npcMaxLoseNum: int
    npcWinNum: int
    npcLoseNum: int


class MusicDetail(BaseModel):
    musicId: PydanticMusic
    level: DifficultyEnum
    playCount: int = 0
    achievement: int = 0
    comboStatus: ComboEnum = ComboEnum.NULL
    syncStatus: SyncEnum = SyncEnum.NULL
    deluxscoreMax: int = 0
    scoreRank: ScoreEnum = ScoreEnum.d
    extNum1: int = 0  # > 1010000

    def to_diving_fish(self) -> DivingFishMusicDetail:
        return DivingFishMusicDetail(
            achievements=self.achievement / 1_0000,
            ds=self.musicId.notes[self.level.value].ds,
            dxScore=self.deluxscoreMax,
            fc=self.comboStatus.name if self.comboStatus.value else "",
            fs=self.syncStatus.name if self.syncStatus.value else "",
            level=self.musicId.notes[self.level.value].level,
            level_index=self.level,
            level_label=self.level.name if self.level != DifficultyEnum.ReMaster else "Re:Master",
            ra=calculate_rating(self.musicId.notes[self.level.value].ds, self.achievement / 1_0000),
            rate=self.scoreRank.name,
            song_id=self.musicId.name.ID,
            title=self.musicId.name.name,
            type="DX" if self.musicId.name.ID > 1_0000 else "SD"
        )

    def to_music_record(self) -> MusicRecord:
        return MusicRecord(
            musicId=self.musicId,
            level=self.level,
            romVersion=self.musicId.version,
            achievement=self.achievement
        )

    def update(self, md: 'MusicDetail') -> 'MusicDetail':
        self.playCount = md.playCount
        self.achievement = md.achievement if md.achievement > self.achievement else self.achievement
        self.comboStatus = md.comboStatus if md.comboStatus.value > self.comboStatus.value else self.comboStatus
        self.syncStatus = md.syncStatus if md.syncStatus.value > self.syncStatus.value else self.syncStatus
        self.deluxscoreMax = md.deluxscoreMax if md.deluxscoreMax > self.deluxscoreMax else self.deluxscoreMax
        self.scoreRank = md.scoreRank if md.scoreRank.value > self.scoreRank.value else self.scoreRank
        return self

    @property
    def rating(self) -> int:
        return calculate_rating(self.musicId.notes[self.level.value].ds, self.achievement / 1_0000)

    @property
    def current_notes(self) -> NotesInfo:
        if isinstance(self.musicId, int):
            raise ValueError()
        return self.musicId.notes[self.level.value]


class MusicDetailRecord(BaseModel):
    musicId: PydanticMusic
    level: DifficultyEnum
    tapCriticalPerfect: int
    tapPerfect: int
    tapGreat: int
    tapGood: int
    tapMiss: int
    holdCriticalPerfect: int
    holdPerfect: int
    holdGreat: int
    holdGood: int
    holdMiss: int
    slideCriticalPerfect: int
    slidePerfect: int
    slideGreat: int
    slideGood: int
    slideMiss: int
    touchCriticalPerfect: int
    touchPerfect: int
    touchGreat: int
    touchGood: int
    touchMiss: int
    breakCriticalPerfect: int
    breakPerfect: int
    breakGreat: int
    breakGood: int
    breakMiss: int
    comboStatus: ComboEnum = ComboEnum.NULL
    syncStatus: SyncEnum = SyncEnum.NULL

    def __init__(self, **data):
        super().__init__(**data)
        if self.slidePerfect > 0:
            raise ValidationError("slidePerfect should be 0")
        if self.breakCriticalPerfect + self.breakPerfect + self.breakGreat + self.breakGood + self.breakMiss != self.current_notes.notes_detail.BRK:
            raise ValidationError("break num is not match")
        if self.tapCriticalPerfect + self.tapPerfect + self.tapGreat + self.tapGood + self.tapMiss != self.current_notes.notes_detail.TAP:
            raise ValidationError("tap num is not match")
        if self.holdCriticalPerfect + self.holdPerfect + self.holdGreat + self.holdGood + self.holdMiss != self.current_notes.notes_detail.HLD:
            raise ValidationError("hold num is not match")
        if self.slideCriticalPerfect + self.slidePerfect + self.slideGreat + self.slideGood + self.slideMiss != self.current_notes.notes_detail.SLD:
            raise ValidationError("slide num is not match")
        if self.touchCriticalPerfect + self.touchPerfect + self.touchGreat + self.touchGood + self.touchMiss != self.current_notes.notes_detail.TTP:
            raise ValidationError("touch num is not match")
        if self.achievement_rate == 101:
            self.comboStatus = ComboEnum.app
        elif self.breakMiss + self.tapMiss + self.holdMiss + self.slideMiss + self.touchMiss == 0:
            self.comboStatus = ComboEnum.fc
            if self.breakGood + self.tapGood + self.holdGood + self.slideGood + self.touchGood == 0:
                self.comboStatus = ComboEnum.fcp
                if self.breakGreat + self.tapGreat + self.holdGreat + self.slideGreat + self.touchGreat == 0:
                    self.comboStatus = ComboEnum.ap

    @property
    def current_notes(self) -> NotesInfo:
        if isinstance(self.musicId, int):
            raise ValueError()
        return self.musicId.notes[self.level.value]

    def isTap(self) -> bool:
        return self.tapCriticalPerfect + self.tapPerfect + self.tapGreat + self.tapGood + self.tapMiss > 0

    def isHold(self) -> bool:
        return self.holdCriticalPerfect + self.holdPerfect + self.holdGreat + self.holdGood + self.holdMiss > 0

    def isSlide(self) -> bool:
        return self.slideCriticalPerfect + self.slidePerfect + self.slideGreat + self.slideGood + self.slideMiss > 0

    def isTouch(self) -> bool:
        return self.touchCriticalPerfect + self.touchPerfect + self.touchGreat + self.touchGood + self.touchMiss > 0

    def isBreak(self) -> bool:
        return self.breakCriticalPerfect + self.breakPerfect + self.breakGreat + self.breakGood + self.breakMiss > 0

    def deluxscore(self) -> int:
        return (self.breakCriticalPerfect * 3 + self.breakPerfect * 2 + self.breakGreat +
                self.slideCriticalPerfect * 3 + self.slidePerfect * 2 + self.slideGreat +
                self.tapCriticalPerfect * 3 + self.tapPerfect * 2 + self.tapGreat +
                self.holdCriticalPerfect * 3 + self.holdPerfect * 2 + self.holdGreat +
                self.touchCriticalPerfect * 3 + self.touchPerfect * 2 + self.touchGreat)

    def maxdeluxscore(self) -> int:
        return self.current_notes.max_notes * 3

    def missNum(self) -> int:
        return self.breakMiss + self.tapMiss + self.holdMiss + self.slideMiss + self.touchMiss

    def notCPNum(self) -> int:
        return self.current_notes.max_notes - self.breakCriticalPerfect - self.tapCriticalPerfect - self.holdCriticalPerfect - self.slideCriticalPerfect - self.touchCriticalPerfect - self.missNum()

    def notPNum(self) -> int:
        return self.notCPNum() - self.breakPerfect - self.tapPerfect - self.holdPerfect - self.slidePerfect - self.touchPerfect

    def notMissNum(self) -> int:
        return self.current_notes.max_notes - self.missNum()

    @property
    def scr_base(self) -> int:
        return ((self.tapCriticalPerfect + self.tapPerfect) * 500 + self.tapGreat * 400 + self.tapGood * 250 +
                (self.holdCriticalPerfect + self.holdPerfect) * 1000 + self.holdGreat * 800 + self.holdGood * 500 +
                (self.slideCriticalPerfect + self.slidePerfect) * 1500 + self.slideGreat * 1200 + self.slideGood * 750 +
                (self.breakCriticalPerfect + self.breakPerfect) * 2500 + self.breakGreat * 2000 + self.breakGood * 1250)

    @property
    def scr_ultra(self) -> int:
        return self.breakCriticalPerfect * 100 + self.breakPerfect * 75 + self.breakGreat * 40 + self.breakGood * 30

    @property
    def achievement_rate(self) -> float:
        return (self.scr_base / self.current_notes.notes_detail.SCR_BASE) * 100 + (self.scr_ultra / self.current_notes.notes_detail.SCR_BRK_EXC) * 1

    @property
    def achievement(self) -> int:
        return int(self.achievement_rate * 1_0000)

    @property
    def scoreRank(self) -> int:
        return calculate_scoreRank(self.achievement_rate)

    def isClear(self) -> bool:
        return self.achievement_rate > 80

    @property
    def rating(self) -> int:
        return calculate_rating(self.current_notes.ds, self.achievement_rate)

    def to_music_record(self) -> MusicRecord:
        return MusicRecord(
            musicId=self.musicId,
            level=self.level,
            romVersion=self.musicId.version,
            achievement=self.achievement
        )

    def to_music_detail(self, playCount: int = 0) -> MusicDetail:
        return MusicDetail(
            musicId=self.musicId,
            level=self.level,
            playCount=playCount + 1,
            achievement=self.achievement,
            comboStatus=self.comboStatus,
            syncStatus=self.syncStatus,
            deluxscoreMax=self.deluxscore(),
            scoreRank=self.scoreRank,
            extNum1=0
        ).model_copy(deep=True)


class MusicDetailRecordIn(MusicDetailRecord):
    breakHPerfect: int
    breakLPerfect: int
    breakHGreat: int
    breakMGreat: int
    breakLGreat: int

    def __init__(self, **data):
        super().__init__(**data)
        if self.breakHPerfect + self.breakLPerfect != self.breakPerfect:
            raise ValidationError("breakPerfect num is not match")
        if self.breakHGreat + self.breakMGreat + self.breakLGreat != self.breakGreat:
            raise ValidationError("breakGreat num is not match")

    def to_music_detail_record(self) -> MusicDetailRecord:
        return MusicDetailRecord(**self.model_dump())

    @property
    def scr_base(self) -> int:
        return ((self.tapCriticalPerfect + self.tapPerfect) * 500 + self.tapGreat * 400 + self.tapGood * 250 +
                (self.holdCriticalPerfect + self.holdPerfect) * 1000 + self.holdGreat * 800 + self.holdGood * 500 +
                (self.slideCriticalPerfect + self.slidePerfect) * 1500 + self.slideGreat * 1200 + self.slideGood * 750 +
                (self.touchCriticalPerfect + self.touchPerfect) * 500 + self.touchGreat * 400 + self.touchGood * 250 +
                (self.breakCriticalPerfect + self.breakPerfect) * 2500 + self.breakHGreat * 2000 + self.breakMGreat * 1500 + self.breakLGreat * 1250 + self.breakGood * 1000)

    @property
    def scr_ultra(self) -> int:
        return self.breakCriticalPerfect * 100 + self.breakHPerfect * 75 + self.breakLPerfect * 50 + self.breakGreat * 40 + self.breakGood * 30

    @staticmethod
    def generate_from_default(musicId: int | Music, level: int | DifficultyEnum, achievement: float = 0, combo: int = ComboEnum.NULL) -> 'MusicDetailRecordIn':
        musicId = other_db.get_dict("Music_dict")[musicId] if isinstance(musicId, int) else musicId
        note = musicId.notes[level] if isinstance(level, int) else musicId.notes[level.value]
        note_detail = note.notes_detail
        tapCP, tapP, tapGreat, tapGood, tapMiss = 0, 0, 0, 0, 0
        holdCP, holdP, holdGreat, holdGood, holdMiss = 0, 0, 0, 0, 0
        slideCP, slideP, slideGreat, slideGood, slideMiss = 0, 0, 0, 0, 0
        touchCP, touchP, touchGreat, touchGood, touchMiss = 0, 0, 0, 0, 0
        breakCP, breakP, breakGreat, breakGood, breakMiss = 0, 0, 0, 0, 0
        breakHP, breakLP, breakHGreat, breakMGreat, breakLGreat = 0, 0, 0, 0, 0
        if achievement == 0:
            tapMiss = note_detail.TAP
            holdMiss = note_detail.HLD
            slideMiss = note_detail.SLD
            touchMiss = note_detail.TTP
            breakMiss = note_detail.BRK
        elif achievement == 101 or combo == ComboEnum.app or combo == ComboEnum.ap:
            tapP, holdCP, slideCP, touchCP, breakCP = note_detail.TAP, note_detail.HLD, note_detail.SLD, note_detail.TTP, note_detail.BRK
            if combo == ComboEnum.ap:
                breakHP = breakP = breakCP - 1
                breakLP = 1
                breakCP = 0
        else:
            ca = 101

            def calculate(source, target, num, ca):
                targetDecrease = num / note_detail.SCR_BASE * 100
                while source:
                    if ca - targetDecrease < achievement:
                        break
                    source -= 1
                    target += 1
                    ca -= targetDecrease
                return source, target, ca

            tapCP, holdP, slideCP, touchP, breakCP = note_detail.TAP, note_detail.HLD, note_detail.SLD, note_detail.TTP, note_detail.BRK
            if combo == ComboEnum.fcp:
                slideCP, slideGreat, ca = calculate(slideCP, slideGreat, 300, ca)
                holdCP, holdGreat, ca = calculate(holdCP, holdGreat, 200, ca)
                tapCP, tapGreat, ca = calculate(tapCP, tapGreat, 100, ca)
            elif combo == ComboEnum.fc:
                slideCP, slideGood, ca = calculate(slideCP, slideGood, 750, ca)
                holdCP, holdGood, ca = calculate(holdCP, holdGood, 500, ca)
                tapCP, tapGood, ca = calculate(tapCP, tapGood, 250, ca)
            else:
                tapCP, tapMiss, ca = calculate(tapCP, tapMiss, 500, ca)
                tapCP, tapGood, ca = calculate(tapCP, tapGood, 250, ca)
                tapCP, tapGreat, ca = calculate(tapCP, tapGreat, 100, ca)

        mdri = MusicDetailRecordIn(
            musicId=musicId,
            level=level,
            tapCriticalPerfect=tapCP, tapPerfect=tapP, tapGreat=tapGreat, tapGood=tapGood, tapMiss=tapMiss,
            holdCriticalPerfect=holdCP, holdPerfect=holdP, holdGreat=holdGreat, holdGood=holdGood, holdMiss=holdMiss,
            slideCriticalPerfect=slideCP, slidePerfect=slideP, slideGreat=slideGreat, slideGood=slideGood, slideMiss=slideMiss,
            touchCriticalPerfect=touchCP, touchPerfect=touchP, touchGreat=touchGreat, touchGood=touchGood, touchMiss=touchMiss,
            breakCriticalPerfect=breakCP, breakPerfect=breakP, breakGreat=breakGreat, breakGood=breakGood, breakMiss=breakMiss,
            breakHPerfect=breakHP, breakLPerfect=breakLP, breakHGreat=breakHGreat, breakMGreat=breakMGreat, breakLGreat=breakLGreat,
        )
        return mdri


class UserRating(BaseModel):
    rating: int
    ratingList: List[MusicRecord]
    newRatingList: List[MusicRecord]
    nextRatingList: List[MusicRecord]
    nextNewRatingList: List[MusicRecord]
    udemae: UdemaeRecord

    @property
    def oldratingTotal(self) -> int:
        return sum(r.rating for r in self.ratingList)

    @property
    def newRatingTotal(self) -> int:
        return sum(r.rating for r in self.newRatingList)

    @property
    def userRatingTotal(self) -> int:
        return self.oldratingTotal + self.newRatingTotal

    def add_music_record(self, record: MusicRecord | MusicDetailRecord | MusicDetail) -> bool:
        pre_rating = self.userRatingTotal
        if is_new_music(record):
            b25 = self.newRatingList + self.nextNewRatingList
            current_music = [r for r in b25 if r.musicId.name.ID == record.musicId.name.ID and r.level == record.level]
            if len(current_music) != 0:
                b25.remove(current_music[0])
            b25.append(record)
            b25.sort(key=lambda r: str(999 - r.rating) + str(r.musicId.name.ID).zfill(6))
            self.newRatingList = b25[:15]
            self.nextNewRatingList = b25[15:25]
        else:
            b45 = self.ratingList + self.nextRatingList
            current_music = [r for r in b45 if r.musicId.name.ID == record.musicId.name.ID and r.level == record.level]
            if len(current_music) != 0:
                b45.remove(current_music[0])
            b45.append(record.to_music_record())
            b45.sort(key=lambda r: str(999 - r.rating) + str(r.musicId.name.ID).zfill(6))
            self.ratingList = b45[:35]
            self.nextRatingList = b45[35:45]
        if self.userRatingTotal > pre_rating:
            return True
        return False


class ActivityDetail(BaseModel):
    kind: int
    id: int
    sortNumber: int = int(time())
    param1: int = 0
    param2: int = 0
    param3: int = 0
    param4: int = 0


class UserActivity(BaseModel):
    playList: List[ActivityDetail]
    musicList: List[ActivityDetail]

    def _PlayMusic(self, musicId: int):
        self.musicList = [x for x in self.musicList if x.id != musicId]
        self.musicList.append(ActivityDetail(kind=2, id=musicId))
        if len(self.musicList) > 10:
            self.musicList = self.musicList[len(self.musicList) - 10:]

    def __addPlayList(self, activityDetail: ActivityDetail):
        self.playList.append(activityDetail)
        if len(self.playList) > 15:
            self.playList = self.playList[len(self.playList) - 15:]

    def __UpsertPlayList(self, activityDetail: ActivityDetail):
        self.playList = [x for x in self.playList if x.id != activityDetail.id and not isToday(x.sortNumber)]
        self.__addPlayList(activityDetail)

    def PlayMaimaiDx(self):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.PlayDX))

    def _MusicAchievement(self, acode: int, musicId: int, difficulty: int, level: int):
        if len([x for x in self.playList if x.id // 10 == acode // 10 and isToday(x.sortNumber)]) == 0:
            self.__addPlayList(ActivityDetail(kind=1, id=acode, param1=musicId, param2=difficulty, param3=level))
            return
        tempPlayList = [x for x in self.playList if x.id != acode and not isToday(x.sortNumber) and
                        x.id < acode or (x.id == acode and x.param3 < level)]
        if len(tempPlayList) < len(self.playList):
            self.playList = tempPlayList
            self.__addPlayList(ActivityDetail(kind=1, id=acode, param1=musicId, param2=difficulty, param3=level))

    def music_result(self, music_detail: MusicDetailRecord | MusicDetail):
        scoreCode = music_detail.scoreRank + 12
        comboCode = music_detail.comboStatus + 29
        syncCode = music_detail.syncStatus + 39
        if syncCode >= ActivityCodeEnum.FullSync:
            self._MusicAchievement(syncCode, music_detail.musicId.name.ID, music_detail.level, int(music_detail.current_notes.ds * 10))
        if comboCode >= ActivityCodeEnum.FullCombo:
            self._MusicAchievement(comboCode, music_detail.musicId.name.ID, music_detail.level, int(music_detail.current_notes.ds * 10))
        if scoreCode >= ActivityCodeEnum.RankS:
            self._MusicAchievement(scoreCode, music_detail.musicId.name.ID, music_detail.level, int(music_detail.current_notes.ds * 10))
        self._PlayMusic(music_detail.musicId.name.ID)

    def DxRate(self, dxRate: int):
        self.playList = [x for x in self.playList if x.id != ActivityCodeEnum.DxRate]
        self.__addPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.DxRate, param1=dxRate))

    def AwakeMaxChara(self, charaId: int):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.AwakeMax, param1=charaId))

    def AwakePreMaxChara(self, combo: int):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.AwakePreMax, param1=combo))

    def MapComplete(self, mapId: int):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.MapComplete, param1=mapId))

    def MapFound(self, mapId: int):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.MapFound, param1=mapId))

    def TransmissionMusicGet(self, musicId: int):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.TransmissionMusic, param1=musicId))

    def TaskMusicClear(self, musicId: int, level: int):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.TaskMusicClear, param1=musicId, param2=level))

    def ChallengeMusicClear(self, musicId: int, level: int):
        self.__UpsertPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.ChallengeMusicClear, param1=musicId, param2=level))

    def RankUp(self, rankId: int):
        tempPlayList = [x for x in self.playList if x.id != ActivityCodeEnum.RankUp and x.param1 >= rankId]
        morePlayList = [x for x in self.playList if x.id == ActivityCodeEnum.RankUp]
        if len(morePlayList) == 0 or len(tempPlayList) < len(self.playList):
            self.playList = tempPlayList
            self.__addPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.RankUp, param1=rankId))

    def ClassUp(self, classId: int):
        tempPlayList = [x for x in self.playList if x.id != ActivityCodeEnum.ClassUp and x.param1 >= classId]
        morePlayList = [x for x in self.playList if x.id == ActivityCodeEnum.ClassUp]
        if len(morePlayList) == 0 or len(tempPlayList) < len(self.playList):
            self.playList = tempPlayList
            self.__addPlayList(ActivityDetail(kind=1, id=ActivityCodeEnum.ClassUp, param1=classId))


class UserGamePlaylog(BaseModel):
    playlogId: int
    version: str
    playDate: str = make_0_time(time())
    playMode: int
    useTicketId: PydanticTicket = -1
    playCredit: int = 1
    playTrack: int
    clientId: str
    isPlayTutorial: bool
    isEventMode: bool
    isNewFree: bool
    playCount: int
    playSpecial: int
    playOtherUserId: int


class User2pPlaylog(BaseModel):
    userId1: int = 0
    userId2: int = 0
    userName1: str = ''
    userName2: str = ''
    regionId: int = 0
    placeId: int = 0
    user2pPlaylogDetailList: List[UserGamePlaylog | None] = []


class UserPlaylogPacket(BaseModel):
    userId: int = 0
    orderId: int = 0
    playlogId: int
    version: int
    placeId: int
    placeName: str
    loginDate: int
    playDate: MaiDate = datetime.now().strftime('%Y-%m-%d')
    userPlayDate: str = make_0_time(time())
    type: int = 0
    musicId: PydanticMusic
    level: DifficultyEnum
    trackNo: int
    vsMode: int = 0
    vsUserName: str = ""
    vsStatus: int = 0
    vsUserRating: int = 0
    vsUserAchievement: int = 0
    vsUserGradeRank: int = 0
    vsRank: int = 0
    playerNum: int = 1
    playedUserId1: int = 0
    playedUserName1: str = ""
    playedMusicLevel1: int = 0
    playedUserId2: int = 0
    playedUserName2: str = ""
    playedMusicLevel2: int = 0
    playedUserId3: int = 0
    playedUserName3: str = ""
    playedMusicLevel3: int = 0
    characterId1: PydanticChara
    characterLevel1: int
    characterAwakening1: int
    characterId2: PydanticChara
    characterLevel2: int
    characterAwakening2: int
    characterId3: PydanticChara
    characterLevel3: int
    characterAwakening3: int
    characterId4: PydanticChara
    characterLevel4: int
    characterAwakening4: int
    characterId5: PydanticChara
    characterLevel5: int
    characterAwakening5: int
    achievement: int
    deluxscore: int
    scoreRank: ScoreEnum
    maxCombo: int
    totalCombo: int
    maxSync: int
    totalSync: int = 0
    tapCriticalPerfect: int
    tapPerfect: int
    tapGreat: int
    tapGood: int
    tapMiss: int
    holdCriticalPerfect: int
    holdPerfect: int
    holdGreat: int
    holdGood: int
    holdMiss: int
    slideCriticalPerfect: int
    slidePerfect: int
    slideGreat: int
    slideGood: int
    slideMiss: int
    touchCriticalPerfect: int
    touchPerfect: int
    touchGreat: int
    touchGood: int
    touchMiss: int
    breakCriticalPerfect: int
    breakPerfect: int
    breakGreat: int
    breakGood: int
    breakMiss: int
    isTap: bool
    isHold: bool
    isSlide: bool
    isTouch: bool
    isBreak: bool
    isCriticalDisp: bool
    isFastLateDisp: bool = True
    fastCount: int
    lateCount: int
    isAchieveNewRecord: bool
    isDeluxscoreNewRecord: bool
    comboStatus: ComboEnum
    syncStatus: SyncEnum
    isClear: bool
    beforeRating: int
    afterRating: int
    beforeGrade: int
    afterGrade: int
    afterGradeRank: int
    beforeDeluxRating: int
    afterDeluxRating: int
    isPlayTutorial: bool = False
    isEventMode: bool = False
    isFreedomMode: bool = False
    playMode: PlayModeEnum = PlayModeEnum.Normal
    isNewFree: bool = False
    trialPlayAchievement: int = -1
    extNum1: int = 0  # startlife * 10000 + endlife
    extNum2: int = 0  # courseID
    extNum4: int
    extBool1: bool = False  # 宴谱


class UserAllPacket(BaseModel):
    userData: List[UserData]
    userExtend: List[UserExtend]
    userOption: List[UserOption]
    userCharacterList: List[UserCharacter]
    userGhost: List
    userMapList: List[UserMap]
    userLoginBonusList: List[UserLoginBonus | None]
    userRatingList: List[UserRating]
    userItemList: List[UserItem]
    userMusicDetailList: List[MusicDetail]
    userCourseList: List[UserCourse | None]
    userFriendSeasonRankingList: List
    userChargeList: List[UserCharge | None]
    userFavoriteList: List
    userActivityList: List[UserActivity]
    userGamePlaylogList: List[UserGamePlaylog]
    user2pPlaylog: User2pPlaylog
    isNewCharacterList: str
    isNewMapList: str
    isNewLoginBonusList: str
    isNewItemList: str
    isNewMusicDetailList: str
    isNewCourseList: str
    isNewFavoriteList: str
    isNewFriendSeasonRankingList: str


class UpsertUserAllPacket(BaseModel):
    userId: int
    playlogId: int
    isEventMode: bool
    isFreePlay: bool
    upsertUserAll: UserAllPacket


class UserLogoutPacket(BaseModel):
    userId: int
    accessCode: str = ""
    regionId: RegionEnum
    placeId: int = 0
    clientId: str
    dateTime: int
    type: LogoutTypeEnum
