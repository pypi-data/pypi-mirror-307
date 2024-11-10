from dataclasses import dataclass
from enum import IntEnum, StrEnum
from os import listdir
from os.path import dirname, exists
from pathlib import Path
from typing import List, Dict
from xml.etree import ElementTree as etree

import UnityPy
from pydantic import BaseModel

current_path = Path(dirname(dirname(__file__)))
base_path = current_path / "maiResource" / "SDGB"


def get_assests_path(dir_name: str, file_name: str) -> List[Path]:
    res_list = []
    for part in listdir(base_path):
        part_dir = base_path / part
        part_path = part_dir / dir_name
        if not exists(part_path):
            continue
        for dirs in listdir(part_path):
            xml_path = part_path / dirs / file_name
            if exists(xml_path):
                res_list.append(xml_path)
    return res_list


class DBManager:
    db_module = None

    def get_dict(self, dict_name):
        return getattr(self.db_module, dict_name)


se1 = set()


class IntEnumType(IntEnum):

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class StrEnumType(StrEnum):

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class ActivityCodeEnum(IntEnumType):
    PlayDX = 10
    RankS = 20
    RankSP = 21
    RankSS = 22
    RankSSP = 23
    RankSSS = 24
    RankSSSP = 25
    FullCombo = 30
    FullComboP = 31
    AllPerfect = 32
    AllPerfectP = 33
    FullSync = 40,
    FullSyncP = 41
    FullSyncDx = 42
    FullSyncDxP = 43
    Sync = 44
    ClassUp_old = 50
    DxRate = 60
    AwakeMax = 70
    AwakePreMax = 71
    MapComplete = 80
    MapFound = 90
    TransmissionMusic = 100
    TaskMusicClear = 110
    ChallengeMusicClear = 120
    RankUp = 130
    ClassUp = 140


class BonusTypeEnum(StrEnumType):
    Frame = 'Frame'
    Icon = 'Icon'
    MusicNew = 'MusicNew'
    Partner = 'Partner'
    Plate = 'Plate'
    Ticket = 'Ticket'


class CondKindCreditEnum(StrEnumType):
    SATELLITE = 'SATELLITE'
    MUSIC_GROUP = 'MUSIC_GROUP'
    MUSIC = 'MUSIC'
    CLEAR_GRADE = 'CLEAR_GRADE'
    PEOPLE = 'PEOPLE'
    CHARASET = 'CHARASET'


class CondKindTotalEnum(StrEnumType):
    MUSIC_GROUP = 'MUSIC_GROUP'
    MUSIC = 'MUSIC'
    TOTAL_CHARA_KAKUSEI = 'TOTAL_CHARA_KAKUSEI'
    MAI2DX_N_PLAY = 'MAI2DX_N_PLAY'
    MAP_CHARA_KAKUSEI = 'MAP_CHARA_KAKUSEI'
    LOGIN_RUIKEI = 'LOGIN_RUIKEI'
    ZENKOKU_OTOMODACHI_N_WIN = 'ZENKOKU_OTOMODACHI_N_WIN'
    LOGIN_RENZOKU = 'LOGIN_RENZOKU'
    FULLCOMBO_COUNT = 'FULLCOMBO_COUNT'
    ZENKOKU_OTOMODACHI_N_REN_WIN = 'ZENKOKU_OTOMODACHI_N_REN_WIN'
    MAP_KYORI = 'MAP_KYORI'
    CHARA_KAKUSEI = 'CHARA_KAKUSEI'


class CondKindTrackEnum(StrEnumType):
    FULLCOMBO = 'FULLCOMBO'
    ICON = 'ICON'
    SYNC = 'SYNC'
    MUSIC = 'MUSIC'
    TRACK_SKIP = 'TRACK_SKIP'
    RATING = 'RATING'
    MISS = 'MISS'
    MIRROR_MODE = 'MIRROR_MODE'
    TAP_SPEED1_SONIC = 'TAP_SPEED1_SONIC'
    DELUXE_SCORE = 'DELUXE_SCORE'
    TITLESET_DP = 'TITLESET_DP'
    RANK_WIN = 'RANK_WIN'
    MUSIC_GENRE_SELECTED = 'MUSIC_GENRE_SELECTED'
    MATCHING_FOR_TITLESETPLAYER = 'MATCHING_FOR_TITLESETPLAYER'
    SATELLITE = 'SATELLITE'
    RANK = 'RANK'
    PEOPLE = 'PEOPLE'
    RANK_LOSE = 'RANK_LOSE'
    PARTNER = 'PARTNER'
    MOVIE_BRIGHTNESS = 'MOVIE_BRIGHTNESS'


class ComboEnum(IntEnumType):
    NULL = 0
    fc = 1
    fcp = 2
    ap = 3
    app = 4


class DifficultyEnum(IntEnumType):
    Basic = 0
    Advanced = 1
    Expert = 2
    Master = 3
    ReMaster = 4
    Y = 10


class ItemKindEnum(IntEnumType):
    plate = 1
    title = 2
    icon = 3
    present = 4
    music = 5
    master = 6
    remaster = 7
    musicSrg = 8
    chara = 9
    partner = 10
    frame = 11
    ticket = 12


class LockTypeEnum(IntEnumType):
    default = 0
    no = 1
    perfect = 2
    legend = 3

    def __repr__(self):
        return str(self.value)


class LogoutTypeEnum(IntEnumType):
    normal = 1
    exit = 2


class PlayModeEnum(IntEnumType):
    Normal = 0
    Freedom = 1
    Course = 2


class RareTypeEnum(StrEnumType):
    Normal = 'Normal'
    Bronze = 'Bronze'
    Silver = 'Silver'
    Gold = 'Gold'
    Rainbow = 'Rainbow'


class RegionEnum(IntEnumType):
    北京 = 1
    重庆 = 2
    上海 = 3
    天津 = 4
    安徽 = 5
    福建 = 6
    甘肃 = 7
    广东 = 8
    贵州 = 9
    海南 = 10
    河北 = 11
    黑龙江 = 12
    河南 = 13
    湖北 = 14
    湖南 = 15
    江苏 = 16
    江西 = 17
    吉林 = 18
    辽宁 = 19
    青海 = 20
    陕西 = 21
    山东 = 22
    山西 = 23
    四川 = 24
    台湾 = 25
    云南 = 26
    浙江 = 27
    广西 = 28
    内蒙古 = 29
    宁夏 = 30
    新疆 = 31
    西藏 = 32

    def __repr__(self):
        return str(self.value)


class ScoreEnum(IntEnumType):
    d = 0
    c = 1
    b = 2
    bb = 3
    bbb = 4
    a = 5
    aa = 6
    aaa = 7
    s = 8
    sp = 9
    ss = 10
    ssp = 11
    sss = 12
    sssp = 13


class SubLockTypeEnum(IntEnumType):
    _1 = 0
    _2 = 1

    def __repr__(self):
        return str(self.value)


class SyncEnum(IntEnumType):
    NULL = 0
    fs = 1
    fsp = 2
    fsd = 3
    fsdp = 4
    sync = 5


class TreasureTypeEnum(StrEnumType):
    Challenge = 'Challenge'
    Character = 'Character'
    Frame = 'Frame'
    Icon = 'Icon'
    MapTaskMusic = 'MapTaskMusic'
    MusicNew = 'MusicNew'
    NamePlate = 'NamePlate'
    Title = 'Title'


class IDName(BaseModel):
    ID: int
    name: str

    def __hash__(self):
        return hash(self.ID)

    def __repr__(self):
        return f"{self.name}({self.ID})"


class BaseItem(BaseModel):
    dataName: str
    path: Path | None = None
    name: IDName

    def __repr__(self):
        return repr(self.name)


class Condition(BaseModel):
    Category: str
    kindTrack: CondKindTrackEnum | None
    kindCredit: CondKindCreditEnum | None
    kindTotal: CondKindTotalEnum | None

    partnerId: IDName
    titleId: IDName
    plateId: IDName
    iconId: IDName
    frameId: IDName
    charaId: IDName
    mapId: IDName
    musicId: IDName
    musicGroupId: IDName
    musicGenreId: IDName
    hiSpeedTapTouchId: str
    hiSpeedSlideId: str
    oldGradeId: str
    gradeId: str
    rankId: str
    satelliteId: str
    difficultyId: str
    todohukenId: str
    param: str
    fcId: str
    syncId: str
    deluxeScoreId: str
    moviebrightnessID: str
    allEquipTitles: List = []
    matchingUserTitle: IDName
    boolParam: bool

    def is_null(self):
        return self.kindTotal is None and self.kindCredit is None and self.kindTrack is None


class Conditions(BaseModel):
    category: str
    conditions: List[Condition]


class Item(BaseItem):
    normText: str

    netOpenName: IDName
    releaseTagName: IDName
    genre: IDName
    eventName: IDName
    relConds: Conditions


class MusicAndDifficulty(BaseModel):
    musicId: IDName
    difficulty: int


class NotesDetail(BaseModel):
    TTP: int = 0
    TAP: int
    BRK: int
    HLD: int
    SLD: int

    @property
    def SCR_TAP(self):
        return (self.TAP + self.TTP) * 500

    @property
    def SCR_BRK_BAS(self):
        return self.BRK * 2500

    @property
    def SCR_BRK_EXC(self):
        return self.BRK * 100

    @property
    def SCR_BRK(self):
        return self.BRK * 2600

    @property
    def SCR_HLD(self):
        return self.HLD * 1000

    @property
    def SCR_SLD(self):
        return self.SLD * 1500

    @property
    def SCR_BASE(self):
        return self.SCR_TAP + self.SCR_BRK_BAS + self.SCR_HLD + self.SCR_SLD

    @property
    def SCR_ALL(self):
        return self.SCR_TAP + self.SCR_BRK + self.SCR_HLD + self.SCR_SLD

    def __add__(self, other):
        return NotesDetail(TTP=self.TTP + other.TTP, TAP=self.TAP + other.TAP, BRK=self.BRK + other.BRK, HLD=self.HLD + other.HLD, SLD=self.SLD + other.SLD)


class NotesInfo(BaseModel):
    ds: float
    max_notes: int
    level: str
    designer: IDName
    notes_detail: NotesDetail


class NoteParser(BaseModel):
    TAP: int = 0
    XTP: int = 0
    NMTAP: int = 0
    EXTAP: int = 0

    TTP: int = 0
    NMTTP: int = 0

    HLD: int = 0
    XHO: int = 0
    NMHLD: int = 0
    EXHLD: int = 0

    THO: int = 0
    NMTHO: int = 0

    STR: int = 0
    XST: int = 0
    NMSTR: int = 0
    EXSTR: int = 0

    SCL: int = 0  # 圆形星星
    SCR: int = 0  # 圆形星星
    SUL: int = 0  # 气球星星
    SUR: int = 0  # 气球星星
    SLL: int = 0  # 折线星星
    SLR: int = 0  # 折线星星
    SXL: int = 0  # 中间绕一圈星星
    SXR: int = 0  # 中间绕一下不转圈的星星
    SSL: int = 0  # 折线星星
    SSR: int = 0
    SF_: int = 0  # wifi星星
    SV_: int = 0  # 山形星星
    SI_: int = 0  # 直线星星
    NMSCL: int = 0
    NMSCR: int = 0
    NMSLL: int = 0
    NMSLR: int = 0
    NMSUL: int = 0
    NMSUR: int = 0
    NMSXL: int = 0
    NMSXR: int = 0
    NMSSL: int = 0
    NMSSR: int = 0
    NMSI_: int = 0
    NMSV_: int = 0
    NMSF_: int = 0
    CNSCR: int = 0
    CNSCL: int = 0
    CNSLL: int = 0
    CNSLR: int = 0
    CNSUR: int = 0
    CNSUL: int = 0
    CNSXL: int = 0
    CNSXR: int = 0
    CNSSL: int = 0
    CNSSR: int = 0
    CNSV_: int = 0
    CNSI_: int = 0
    CNSF_: int = 0

    BRK: int = 0
    BST: int = 0
    BRTAP: int = 0
    BXTAP: int = 0
    BRSTR: int = 0
    BXSTR: int = 0
    BRHLD: int = 0
    BXHLD: int = 0
    BRSCL: int = 0
    BRSCR: int = 0
    BRSF_: int = 0
    BRSI_: int = 0
    BRSLL: int = 0
    BRSXL: int = 0
    BRSLR: int = 0
    BRSSR: int = 0
    BRSSL: int = 0
    BRSUR: int = 0
    BRSV_: int = 0
    BRSUL: int = 0
    BRSXR: int = 0

    def parse(self, file_path: str | Path):
        with open(file_path, 'r', encoding='utf-8') as f:
            res = f.read()
        for i in self.__dict__.keys():
            self.__dict__[i] = res.count('\n' + i + '\t')
            # count = 0
            # for i in f.readlines():
            #     if i == '\n':
            #         count += 1
            #         continue
            #     if count != 2:
            #         continue
            #     if count == 2:
            #         name = i.strip().split("\t", 1)[0]
            #         self.__setattr__(name, self.__getattribute__(name) + 1)

    def tap_num(self):
        return sum([self.TAP, self.XTP, self.NMTAP, self.EXTAP]) + sum([self.STR, self.XST, self.NMSTR, self.EXSTR])

    def touch_num(self):
        return sum([self.TTP, self.NMTTP])

    def hold_num(self):
        return sum([self.HLD, self.XHO, self.NMHLD, self.EXHLD]) + sum([self.THO, self.NMTHO])

    def slide_num(self):
        return sum([
            self.SCL, self.SCR, self.SUL, self.SUR, self.SLL, self.SLR, self.SXL, self.SXR,
            self.SSL, self.SSR, self.SF_, self.SV_, self.SI_,
            self.NMSCL, self.NMSCR, self.NMSLL, self.NMSLR, self.NMSUL, self.NMSUR, self.NMSXL, self.NMSXR,
            self.NMSSL, self.NMSSR, self.NMSI_, self.NMSV_, self.NMSF_,
        ])

    def break_num(self):
        return sum([
            self.BRK, self.BST, self.BRTAP, self.BXTAP,
            self.BRSTR, self.BXSTR, self.BRHLD, self.BXHLD,
            self.BRSCL, self.BRSCR, self.BRSF_, self.BRSI_, self.BRSLL, self.BRSXL,
            self.BRSLR, self.BRSSR, self.BRSSL, self.BRSUR, self.BRSV_, self.BRSUL, self.BRSXR
        ])

    def total_num(self):
        return self.tap_num() + self.touch_num() + self.hold_num() + self.slide_num() + self.break_num()


class Challenge(BaseItem):
    music: IDName


class Chara(BaseItem):
    color: IDName
    genre: IDName
    netOpenName: IDName


class CharaGenre(BaseItem):
    genreName: str
    FileName: str


class Class(BaseItem):
    startPoint: int
    classdownStartPoint: int
    classupPoint: int
    winSameClass: int
    loseSameClass: int
    winUpperClass: int
    loseUpperClass: int
    winLowerClass: int
    loseLowerClass: int

    classBoss: IDName
    npcBaseMusicByBoss: IDName


class CollectionGenre(BaseItem):
    genreName: str
    FileName: str


class Course(BaseItem):
    isRandom: bool
    lowerLevel: int
    upperLevel: int
    life: int
    recover: int

    baseDaniId: IDName
    baseCourseId: IDName
    eventId: IDName
    netOpenName: IDName
    conditionsUnlockCourse: IDName

    courseMusicData: List[MusicAndDifficulty]


class Event(BaseItem):
    pass


class Frame(Item):
    pass


class Icon(Item):
    pass


class LoginBonus(BaseItem):
    itemID: int
    BonusType: BonusTypeEnum
    maxPoint: int

    PartnerId: IDName
    CharacterId: IDName
    MusicId: IDName
    TitleId: IDName
    PlateId: IDName
    IconId: IDName
    FrameId: IDName
    TicketId: IDName
    OpenEventId: IDName
    netOpenName: IDName


class Map(BaseItem):
    IsCollabo: bool
    IsInfinity: bool

    IslandId: IDName
    ColorId: IDName
    BonusMusicId: IDName
    OpenEventId: IDName
    netOpenName: IDName

    TreasureExDatas: Dict[int, IDName]


class MapBonusMusic(BaseItem):
    MusicIds: List[IDName]


class MapColor(BaseItem):
    ColorGroupId: IDName


class MapTreasure(BaseItem):
    itemID: int
    TreasureType: TreasureTypeEnum

    CharacterId: IDName
    MusicId: IDName
    NamePlate: IDName
    Frame: IDName
    Title: IDName
    Icon: IDName
    Challenge: IDName


class Music(BaseItem):
    sortName: str
    bpm: int
    version: str
    lockType: LockTypeEnum

    utageKanjiName: str | None

    eventName: List[IDName] | None
    netOpenName: IDName
    releaseTagName: IDName
    artistName: IDName
    genreName: IDName
    AddVersion: IDName

    notes: Dict[int, NotesInfo | None]


class MusicGroup(BaseItem):
    MusicIds: List[IDName]


class MusicVersion(BaseItem):
    genreName: str
    version: int
    FileName: str


class Ticket(BaseItem):
    areaPercent: int
    charaMagnification: int
    detail: str
    filename: str


class Title(Item):
    rareType: RareTypeEnum
    disable: bool


class Partner(BaseItem):
    normText: str

    eventName: IDName
    netOpenName: IDName
    releaseTagName: IDName
    genre: IDName
    naviChara: IDName


class Plate(Item):
    pass


class Parser:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.xml_tree = etree.parse(file_path)

    def text(self, tag: str) -> str:
        return self.xml_tree.find(tag).text

    def get_id_name(self, tag: str, tree: etree.ElementTree | None | etree.Element = None) -> IDName:
        tree = self.xml_tree.find(tag) if tree is None else tree.find(tag)
        return IDName(ID=tree.find("id").text, name=str(tree.find("str").text))


class ItemParser(Parser):
    class_name = "Item"

    def handle_one_condition(self, condition: etree.Element) -> Condition | None:
        def str_or_none(s):
            return s if s != "None" else None

        res = Condition(Category=condition.find("Category").text, kindTrack=str_or_none(condition.find("kindTrack").text), kindCredit=str_or_none(condition.find("kindCredit").text), kindTotal=str_or_none(condition.find("kindTotal").text),
                        partnerId=self.get_id_name("partnerId", condition), titleId=self.get_id_name("titleId", condition), plateId=self.get_id_name("plateId", condition), iconId=self.get_id_name("iconId", condition), frameId=self.get_id_name("frameId", condition),
                        charaId=self.get_id_name("charaId", condition), mapId=self.get_id_name("mapId", condition), musicId=self.get_id_name("musicId", condition), musicGroupId=self.get_id_name("musicGroupId", condition), musicGenreId=self.get_id_name("musicGenreId", condition),
                        hiSpeedTapTouchId=condition.find("hiSpeedTapTouchId").text,
                        hiSpeedSlideId=condition.find("hiSpeedSlideId").text, mirrorModeId=condition.find("mirrorModeId").text,
                        oldGradeId=condition.find("oldGradeId").text, gradeId=condition.find("gradeId").text, rankId=condition.find("rankId").text, satelliteId=condition.find("satelliteId").text, difficultyId=condition.find("difficultyId").text, todohukenId=condition.find("todohukenId").text,
                        param=condition.find("param").text, fcId=condition.find("fcId").text, syncId=condition.find("syncId").text, deluxeScoreId=condition.find("deluxeScoreId").text, moviebrightnessID=condition.find("moviebrightnessID").text,
                        matchingUserTitle=self.get_id_name("matchingUserTitle", condition),
                        allEquipTitles=[IDName(ID=title.find("id").text, name=str(title.find("str").text)) for title in condition.find('allEquipTitles')[0]], boolParam=condition.find("boolParam").text)
        return None if res.is_null() else res

    def handle_condition(self) -> Conditions:
        relConds = self.xml_tree.find('relConds')
        return Conditions(category=relConds.find("category").text, conditions=filter(None, [self.handle_one_condition(relConds[i]) for i in range(1, 6)]))

    def __call__(self) -> Item:
        return eval(self.class_name)(dataName=self.text('dataName'), normText=self.text('normText'),
                                     name=self.get_id_name('name'), netOpenName=self.get_id_name('netOpenName'), releaseTagName=self.get_id_name('releaseTagName'), genre=self.get_id_name('genre'), eventName=self.get_id_name('eventName'),
                                     relConds=self.handle_condition(), path=self.file_path)


class LoginBonusParser(Parser):
    def __call__(self) -> LoginBonus:
        return LoginBonus(dataName=self.text('dataName'), itemID=self.text('itemID'), BonusType=self.text('BonusType'), maxPoint=self.text('maxPoint'),
                          name=self.get_id_name('name'), PartnerId=self.get_id_name('PartnerId'), CharacterId=self.get_id_name('CharacterId'), MusicId=self.get_id_name('MusicId'), TitleId=self.get_id_name('TitleId'), PlateId=self.get_id_name('PlateId'), IconId=self.get_id_name('IconId'),
                          FrameId=self.get_id_name('FrameId'), TicketId=self.get_id_name('TicketId'), OpenEventId=self.get_id_name('OpenEventId'), netOpenName=self.get_id_name('netOpenName'), path=self.file_path)


class ChallengeParser(Parser):
    def __call__(self) -> Challenge:
        return Challenge(dataName=self.text('dataName'), name=self.get_id_name('name'), music=self.get_id_name('Music'), path=self.file_path)


class ClassParser(Parser):
    def __call__(self) -> Class:
        return Class(dataName=self.text('dataName'), name=self.get_id_name('name'), startPoint=self.text('startPoint'), classdownStartPoint=self.text('classdownStartPoint'), classupPoint=self.text('classupPoint'), winSameClass=self.text('winSameClass'), loseSameClass=self.text('loseSameClass'),
                     winUpperClass=self.text('winUpperClass'), loseUpperClass=self.text('loseUpperClass'), winLowerClass=self.text('winLowerClass'), loseLowerClass=self.text('loseLowerClass'), classBoss=self.get_id_name('classBoss'), npcBaseMusicByBoss=self.get_id_name('npcBaseMusicByBoss'),
                     path=self.file_path)


class EventParser(Parser):
    def __call__(self) -> Event:
        return Event(dataName=self.text('dataName'), name=self.get_id_name('name'), path=self.file_path)


class CharaParser(Parser):
    def __call__(self) -> Chara:
        return Chara(dataName=self.text('dataName'),
                     name=self.get_id_name('name'), color=self.get_id_name('color'), genre=self.get_id_name('genre'), netOpenName=self.get_id_name('netOpenName'), path=self.file_path)


class CharaGenreParser(Parser):
    def __call__(self) -> CharaGenre:
        return CharaGenre(dataName=self.text('dataName'), genreName=self.text('genreName'), FileName=self.text('FileName'), name=self.get_id_name('name'), path=self.file_path)


class CollectionGenreParser(Parser):
    def __call__(self) -> CollectionGenre:
        return CollectionGenre(dataName=self.text('dataName'), genreName=self.text('genreName'), FileName=self.text('FileName'), name=self.get_id_name('name'), path=self.file_path)


class CourseParser(Parser):
    def __call__(self) -> Course:
        return Course(dataName=self.text('dataName'), isRandom=self.text('isRandom'), lowerLevel=self.text('lowerLevel'), upperLevel=self.text('upperLevel'), life=self.text('life'), recover=self.text('recover'),
                      name=self.get_id_name('name'), baseDaniId=self.get_id_name('baseDaniId'), baseCourseId=self.get_id_name('baseCourseId'), eventId=self.get_id_name('eventId'), netOpenName=self.get_id_name('netOpenName'), conditionsUnlockCourse=self.get_id_name('conditionsUnlockCourse'),
                      courseMusicData=[MusicAndDifficulty(musicId=self.get_id_name('musicId', music), difficulty=music.find('difficulty').find('id').text) for music in self.xml_tree.find('courseMusicData')], path=self.file_path)


class TitleParser(ItemParser):
    def __call__(self) -> Title:
        return Title(dataName=self.text('dataName'), normText=self.text('normText'), rareType=self.text('rareType'), disable=self.text("disable"),
                     name=self.get_id_name('name'), netOpenName=self.get_id_name('netOpenName'), genre=self.get_id_name('genre'), eventName=self.get_id_name('eventName'), releaseTagName=self.get_id_name('releaseTagName'),
                     relConds=self.handle_condition(), path=self.file_path)


class TicketParser(Parser):
    def __call__(self) -> Ticket:
        return Ticket(dataName=self.text('dataName'), areaPercent=self.text('areaPercent'), charaMagnification=self.text('charaMagnification'), detail=self.text('detail'), filename=self.text('filename'),
                      name=self.get_id_name('name'), path=self.file_path)


class MusicParser(Parser):
    def get_notes_info(self, tree: etree.Element | None):
        musicLevelID = int(tree.find("musicLevelID").text)
        if musicLevelID == 0:
            return None

        level = tree.find('level').text
        levelDecimal = tree.find('levelDecimal').text
        levelID = str(musicLevelID) if musicLevelID <= 7 \
            else f"{int((musicLevelID + 7) / 2)}{'+' if musicLevelID % 2 == 0 else ''}"
        designer = self.get_id_name('notesDesigner', tree)

        def get_notes_detail(note_path: Path) -> NotesDetail:
            # with open(note_path, 'r', encoding='utf-8') as f:
            #     count = 0
            #     notes_dict = {}
            #     for i in f.readlines():
            #         if i == '\n':
            #             count += 1
            #             continue
            #         if count < 3 or count >= 4:
            #             continue
            #         tdata = i.strip().split("\t", 1)
            #         notes_dict[tdata[0]] = int(tdata[1])
            #     nd = NotesDetail(TTP=notes_dict.get('T_REC_TTP', 0), TAP=notes_dict['T_NUM_TAP'] - notes_dict.get('T_REC_TTP', 0), BRK=notes_dict['T_NUM_BRK'], HLD=notes_dict['T_NUM_HLD'], SLD=notes_dict['T_NUM_SLD'])
            #     return nd
            note_data = NoteParser()
            note_data.parse(note_path)
            nd = NotesDetail(TTP=note_data.touch_num(), TAP=note_data.tap_num(), BRK=note_data.break_num(), HLD=note_data.hold_num(), SLD=note_data.slide_num())
            return nd

        notes_path = self.file_path.parent / tree.find('file').find('path').text
        if not exists(notes_path):
            note_file_name = tree.find('file').find('path').text.split('.')[0]
            notes_detail = get_notes_detail(self.file_path.parent / f"{note_file_name}_L.ma2") + get_notes_detail(self.file_path.parent / f"{note_file_name}_R.ma2")
        else:
            notes_detail = get_notes_detail(notes_path)

        return NotesInfo(ds=f"{level}.{levelDecimal}", level=levelID, max_notes=tree.find('maxNotes').text, designer=designer, notes_detail=notes_detail)

    def __call__(self) -> Music:
        notesData = self.xml_tree.find("notesData")
        notes = {}
        for i in range(5):
            notes_info = self.get_notes_info(notesData[i])
            if notes_info is None:
                continue
            notes[i] = notes_info

        return Music(dataName=self.text('dataName'), sortName=self.text('sortName'), bpm=self.text("bpm"), version=self.text("version"), lockType=self.text("lockType"),
                     utageKanjiName=self.text("utageKanjiName"),
                     eventName={self.get_id_name("eventName"), self.get_id_name("eventName2"), self.get_id_name("subEventName")}, name=self.get_id_name("name"), netOpenName=self.get_id_name("netOpenName"), releaseTagName=self.get_id_name("releaseTagName"),
                     artistName=self.get_id_name("artistName"),
                     genreName=self.get_id_name("genreName"),
                     AddVersion=self.get_id_name("AddVersion"), notes=notes, path=self.file_path)


class MusicVersionParser(Parser):
    def __call__(self) -> MusicVersion:
        return MusicVersion(dataName=self.text('dataName'), genreName=self.text('genreName'), version=self.text('version'), FileName=self.text('FileName'), name=self.get_id_name('name'), path=self.file_path)


class MusicGroupParser(Parser):
    def __call__(self) -> MusicGroup:
        return MusicGroup(dataName=self.text('dataName'), MusicIds=[IDName(ID=music.find("id").text, name=str(music.find("str").text)) for music in self.xml_tree.find('MusicIds').find('list')], name=self.get_id_name('name'), path=self.file_path)


class MapBonusMusicParser(Parser):
    def __call__(self) -> MapBonusMusic:
        music_ids = []
        for music in self.xml_tree.find('MusicIds').find('list'):
            music_ids.append(IDName(ID=music.find("id").text, name=str(music.find("str").text)))
        return MapBonusMusic(dataName=self.text('dataName'), MusicIds=music_ids, name=self.get_id_name('name'), path=self.file_path)


class MapParser(Parser):
    def __call__(self) -> Map:
        treasure_dict = {}
        for treasure in self.xml_tree.find('TreasureExDatas'):
            treasure_dict[int(treasure.find('Distance').text)] = self.get_id_name('TreasureId', treasure)
        return Map(dataName=self.text('dataName'), IsCollabo=self.text('IsCollabo'), IsInfinity=self.text('IsInfinity'),
                   name=self.get_id_name('name'), IslandId=self.get_id_name('IslandId'), ColorId=self.get_id_name('ColorId'), BonusMusicId=self.get_id_name('BonusMusicId'), OpenEventId=self.get_id_name('OpenEventId'), netOpenName=self.get_id_name('netOpenName'), TreasureExDatas=treasure_dict,
                   path=self.file_path)


class MapTreasureParser(Parser):
    def __call__(self) -> MapTreasure:
        return MapTreasure(dataName=self.text('dataName'), itemID=self.text('itemID'), TreasureType=self.text('TreasureType'),
                           name=self.get_id_name('name'), CharacterId=self.get_id_name('CharacterId'), MusicId=self.get_id_name('MusicId'), NamePlate=self.get_id_name('NamePlate'), Frame=self.get_id_name('Frame'), Title=self.get_id_name('Title'), Icon=self.get_id_name('Icon'),
                           Challenge=self.get_id_name('Challenge'), path=self.file_path)


class MapColorParser(Parser):
    def __call__(self) -> MapColor:
        return MapColor(dataName=self.text('dataName'), ColorGroupId=self.get_id_name('ColorGroupId'), name=self.get_id_name('name'), path=self.file_path)


class PartnerParser(Parser):
    def __call__(self) -> Partner:
        return Partner(dataName=self.text('dataName'), normText=self.text('normText'),
                       name=self.get_id_name('name'), netOpenName=self.get_id_name('netOpenName'), genre=self.get_id_name('genre'), eventName=self.get_id_name('eventName'), releaseTagName=self.get_id_name('releaseTagName'), naviChara=self.get_id_name('naviChara'), path=self.file_path)


class FrameParser(ItemParser):
    class_name = "Frame"


class IconParser(ItemParser):
    class_name = "Icon"


class PlateParser(ItemParser):
    class_name = "Plate"


def extract_texture2d(dir_name: str | Path, out_path: str | Path = current_path / "out"):
    current_out_path = out_path / dir_name
    current_out_path.mkdir(exist_ok=True)

    for part in listdir(base_path):
        part_ab_path = base_path / part / "AssetBundleImages" / dir_name
        if not part_ab_path.exists():
            continue
        for ab_file in listdir(part_ab_path):
            ab_path = part_ab_path / ab_file
            if ab_path.suffix != ".ab":
                continue

            env = UnityPy.load(str(ab_path))
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    dest = current_out_path / f"{data.name[3:]}.png"
                    data.image.save(dest)


def extract_map_texture2d(out_path: str | Path = current_path / "out"):
    current_out_path = out_path / "map"
    current_out_path.mkdir(exist_ok=True)

    file_name_dict = {
        "ui_chara_star.ab": "c_star",
        "ui_chara_lframe.ab": "clv_frame",
        "ui_chara_frame.ab": "ccl_frame",
        "ui_chara_rframe.ab": "csl_frame",
        "ui_chara_rbase.ab": "csl_frame_base",
        "ui_eventbanner.ab": "event",
        "ui_islandcomp.ab": "map"
    }

    for part in listdir(base_path):
        part_ab_path = base_path / part / "AssetBundleImages" / "map" / "sprite" / "bg"
        if not part_ab_path.exists():
            continue
        for map_dir_name in listdir(part_ab_path):
            for ab_path in listdir(part_ab_path / map_dir_name):
                if ab_path not in file_name_dict.keys():
                    continue
                env = UnityPy.load(str(part_ab_path / map_dir_name / ab_path))
                for obj in env.objects:
                    if obj.type.name == "Texture2D":
                        data = obj.read()
                        dest = current_out_path / f"{file_name_dict[ab_path]}_{map_dir_name}.png"
                        data.image.save(dest)


def extract_all_texture2d(input_path=base_path, out_path: str | Path = current_path / "out"):
    global base_path
    if input_path != base_path:
        base_path = input_path
    out_path.mkdir(exist_ok=True)
    ab_resources = ["chara", "frame", "icon", "jacket", "nameplate", "partner"]
    for ab in ab_resources:
        extract_texture2d(ab, out_path)
        print(f"extract {ab} texture2d done")
    extract_map_texture2d(out_path)
    print(f"extract map texture2d done")


def handle_assests(name: str):
    print(f"handling {name} xml...")
    res_dict = {}
    path_list = get_assests_path(name, name.capitalize() + ".xml")
    for one in path_list:
        current = eval(f'{name[0].upper() + name[1:]}Parser(one)')()
        one_id = current.name.ID
        if res_dict.__contains__(one_id):
            res_dict[one_id].append(current)
        else:
            res_dict[one_id] = [current]
    return res_dict


def export_dict(data: dict[int, list[BaseItem]]):
    def export_one_item(item: BaseItem):
        return f"{item.__class__.__name__}(**{item.model_dump(exclude={'path'})})"

    res_dict = {}
    for one in [i[-1] for i in data.values()]:
        res_dict[one.name.ID] = one

    class_name = list(res_dict.values())[0].__class__.__name__

    res_str = f"{class_name}_dict = " + '{\n'
    for k, v in res_dict.items():
        res_str += f"\t{k}: {export_one_item(v)},\n"
    res_str += '}\n\n\n'

    return res_str


def export_pydantic_type(name: str):
    template_str = """
class _TemplatePydanticAnnotation:
\t@classmethod
\tdef __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
\t\tdef validate_from_int(value: int) -> Icon | int:
\t\t\treturn other_db.get_dict('Template_dict').get(value, value)\n
\t\tfrom_int_schema = core_schema.chain_schema(
\t\t\t[
\t\t\t\tcore_schema.int_schema(),
\t\t\t\tcore_schema.no_info_plain_validator_function(validate_from_int),
\t\t\t]
\t\t)\n
\t\treturn core_schema.json_or_python_schema(
\t\t\tjson_schema=from_int_schema,
\t\t\tpython_schema=core_schema.union_schema(
\t\t\t\t[
\t\t\t\t\tcore_schema.is_instance_schema(Template),
\t\t\t\t\tfrom_int_schema,
\t\t\t\t]
\t\t\t),
\t\t\tserialization=core_schema.plain_serializer_function_ser_schema(
\t\t\t\tlambda instance: instance if isinstance(instance, int) else instance.name.ID
\t\t\t),
\t\t)\n
\t@classmethod
\tdef __get_pydantic_json_schema__(
\t\t\tcls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
\t) -> JsonSchemaValue:
\t\treturn handler(core_schema.int_schema())\n\n
PydanticTemplate = Annotated[int | Template, _TemplatePydanticAnnotation]\n\n"""
    return template_str.replace("Template", name[0].upper() + name[1:])


def export_types(out_path="db_types.py"):
    with open(out_path, "w", encoding='utf-8') as f:
        f.write("# -*- auto-generated -*-\n")
        f.write("""from typing import Any, Annotated\n
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema\n
from .dmr import *\n
other_db = DBManager()\n\n""")
        resource_str_list = ["challenge", "chara", "charaGenre", "class", "collectionGenre", "course", "event", "frame", "icon", "loginBonus", "map", "mapBonusMusic", "mapColor", "mapTreasure", "music", "musicGroup", "musicVersion", "title", "ticket", "plate", "partner"]
        res = ""
        for i in resource_str_list:
            res += export_pydantic_type(i[0].upper() + i[1:])
        res = res.replace("\t", "    ")
        f.write(res[:-1])
        f.write("""__all__ = [
    'PydanticChallenge',
    'PydanticChara',
    'PydanticCharaGenre',
    'PydanticClass',
    'PydanticCollectionGenre',
    'PydanticCourse',
    'PydanticEvent',
    'PydanticFrame',
    'PydanticIcon',
    'PydanticLoginBonus',
    'PydanticMap',
    'PydanticMapBonusMusic',
    'PydanticMapColor',
    'PydanticMapTreasure',
    'PydanticMusic',
    'PydanticMusicGroup',
    'PydanticMusicVersion',
    'PydanticTitle',
    'PydanticTicket',
    'PydanticPlate',
    'PydanticPartner',
]""")


def export_dict_all(input_path=base_path, out_path="db.py"):
    global base_path
    if input_path != base_path:
        base_path = input_path
    with open(out_path, "w", encoding='utf-8') as f:
        f.write("# -*- auto-generated -*-\n")
        f.write("from mailoxy.dmr import *\n\n\n")
        resource_str_list = ["challenge", "chara", "charaGenre", "class", "collectionGenre", "course", "event", "frame", "icon", "loginBonus", "map", "mapBonusMusic", "mapColor", "mapTreasure", "music", "musicGroup", "musicVersion", "title", "ticket", "plate", "partner"]
        for i in resource_str_list:
            f.write(export_dict(handle_assests(i)))


if __name__ == '__main__':
    t = NoteParser()
    t.parse(r"C:\Users\30533\project\mai3script\maiResource\SDGB\A000\music\music011228\011228_04.ma2")
    print()
