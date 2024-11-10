from typing import List

import httpx
from pydantic import BaseModel

from mailoxy.dmr import DifficultyEnum
from mailoxy.errors import DivingFishError


class DivingFishMusicDetail(BaseModel):
    achievements: float
    ds: float
    dxScore: int
    fc: str
    fs: str
    level: str
    level_index: DifficultyEnum
    level_label: str
    ra: int
    rate: str
    song_id: int
    title: str
    type: str


class DivingFishBMR(BaseModel):
    dx: List[DivingFishMusicDetail]
    sd: List[DivingFishMusicDetail]


class DivingFishMusicRecord(BaseModel):
    additional_rating: int
    nickname: str
    plate: str
    rating: int
    charts: DivingFishBMR


class DivingFishApi:
    _base_df_url = 'https://www.diving-fish.com/api/maimaidxprober/'

    def __init__(self, develop_token: str = None):
        self.token = develop_token

    def _get(self, url: str, headers: dict = None, **params) -> dict | list:
        res = httpx.get(self._base_df_url + url, headers=headers, params=params)
        data = res.json()
        if res.status_code == 200:
            return data
        elif res.status_code == 400 or res.status_code == 403:
            raise DivingFishError(message=data['message'])

    def _post(self, url: str, data: dict | list = None, headers: dict = None, ) -> dict:
        res = httpx.post(self._base_df_url + url, headers=headers, json=data)
        data = res.json()
        if res.status_code == 200:
            return data
        elif res.status_code == 400 or res.status_code == 403:
            raise DivingFishError(message=data['message'])

    def alive_check(self) -> bool:
        return self._get('alive_check')["message"] == "ok"

    @staticmethod
    def get_import_header(import_token: str):
        return {'Import-Token': import_token}

    def get_developer_header(self):
        return {'Developer-Token': self.token}

    def dev_player_records(self, qq: int) -> DivingFishMusicRecord:
        return DivingFishMusicRecord(**self._get('dev/player/records', self.get_developer_header(), qq=qq))

    def dev_player_record(self, qq: int, song_id: list[int]) -> DivingFishMusicRecord:
        data = {'qq': qq, 'song_id': song_id}
        return DivingFishMusicRecord(**self._post('dev/player/record', data=data, headers=self.get_developer_header()))

    def player_record(self, itoken: str):
        return DivingFishMusicRecord(**self._get('player/records', headers=self.get_import_header(itoken)))

    def query_player(self, qq: int, b50: bool = True) -> DivingFishMusicRecord:
        data = {'qq': qq}
        if b50:
            data['b50'] = 1
        return DivingFishMusicRecord(**self._post('query/player', data=data))

    def rating_ranking(self) -> list[dict]:
        """
        - example response:
        [{
        "username": "user1",
        "ra": 11111
        }]
        """
        return self._get('rating/ranking')

    def player_update_records(self, itoken: str, records: list[DivingFishMusicDetail]):
        data = [r.model_dump() for r in records]
        return self._post('player/update_records', headers=self.get_import_header(itoken), data=data)


__all__ = ['DivingFishApi', 'DivingFishMusicDetail', 'DivingFishBMR', 'DivingFishMusicRecord']
