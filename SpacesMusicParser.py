import requests
import json

from typing import List
from enum import Enum

from logger import logger

class SpacesFileType(Enum):
  FILE = 5
  FILEDIR = 1
  MUSIC = 6
  MUSICDIR = 2
  PICDIR = 3
  PICTURE = 7
  VIDEO = 25
  VIDEODIR = 24

# Класс отдельного трека
class MusicTrack():

  def __init__(self, artist: str, name: str, downloadUrl: str, file_id: str, file_type: int,  duration: int, bitrate: int) -> None:
    self.artist: str = artist
    self.name: str = name
    self.downloadUrl: str = downloadUrl
    self.file_id: str = file_id
    self.duration: int = duration
    self.bitrate: int = bitrate
    self.spaces_file_type: SpacesFileType = SpacesFileType(file_type)


  def getFullName(self) -> str:
    return f"{self.artist} - {self.name}"

# Класс результатов поиска в музыке
class SearchResult():

  def __init__(self, query: str, moreUrl: str) -> None:
    self.query: str = query
    self.tracks: List[MusicTrack] = []
    self.moreUrl = moreUrl

# Класс результатов поиска в зоне обмена
class SharedZoneSearchResult(SearchResult):

  def __init__(self, query: str, moreUrl: str) -> None:
    super().__init__(query, moreUrl)

  def fill_tracks(self, tracks: list):
    for track in tracks:
      try:
        self.tracks.append(
            MusicTrack(
                artist=track['filename'],
                name='',
                file_id=track['nid'],
                file_type=int(track['type']),
                downloadUrl=track['download_url'],
                duration=0,
                bitrate=0
            )
        )
      except:
        logger.error("Не удалось добавить трек в список")

class SpacesMusicParser():
  # Метод ищет музыку по зоне обмена
  @staticmethod
  def shared_zone_search(query: str) -> SharedZoneSearchResult:
    url = 'https://spac1.net/ajax1633285714055/files/search/'

    h = {
      'X-Proxy': 'spaces'
    }

    p = {
      'word': query,
      'cfms': 'Найти',
      'Slist': 61, # указывает что поиск по музыке
      'Rli': 0
    }

    r = requests.post(url, params=p, headers=h).json()
    for hf in r['info']['form']['hidden']:
      if hf['name'] == 'stt':

        p['stt'] = hf['value']
        break
    print()
    r = requests.post(url, params=p, headers=h)

    data = r.json()
    result = SharedZoneSearchResult(
        query=data['info']['word'],
        moreUrl=''
    )
    if 'files_list' in data['info']:
      result.fill_tracks(data['info']['files_list'])

    return result