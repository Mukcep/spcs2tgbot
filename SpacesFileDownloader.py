import requests
import shutil

from SpacesMusicParser import SpacesFileType


class SpacesFileDownloader():

  def __init__(self, file_id: str, file_type: SpacesFileType) -> None:
    self.file_id = file_id
    self.local_file_name = None
    self.is_downloaded = False
    self.error = None
    self.file_name = None
    self.file_type: SpacesFileType = file_type
    self.downloadUrl = None

  def download(self, fake = False) -> bool:
    if self.file_type == SpacesFileType.MUSIC:
      url = f"https://spac1.net/music/view/{self.file_id}/"
    elif self.file_type == SpacesFileType.FILE:
      url = f"https://spac1.net/files/view/{self.file_id}/"
    else:
      self.error = 'Неизвестный тип файла'
      return False

    file_page_json = requests.get(url, headers={'X-Proxy': 'spaces'})
    file_page_json = file_page_json.json()

    if self.file_type == SpacesFileType.MUSIC:
      # Уведомление что контент 18+, но ссылка там все равно есть
      if 'adult_check_UI' in file_page_json['info']:
        downloadUrl = file_page_json['info']['adult_check_UI']['blurredPreview']['downloadLinkSSL']
        fileName = file_page_json['info']['adult_check_UI']['blurredPreview']['filename']
      else:
        downloadUrl = file_page_json['info']['file_widget']['downloadBox']['downloadLink']['url']
        fileName = file_page_json['info']['file_widget']['filename']
    elif self.file_type == SpacesFileType.FILE:
      downloadUrl = file_page_json['info']['file_widget']['downloadBox']['downloadURL']
      fileName = file_page_json['info']['file_widget']['filename']
    
    self.file_name = fileName
    self.downloadUrl = downloadUrl
    if fake:
      return False

    r = requests.get(downloadUrl, stream=True)
    if r.status_code == 200:
      try:
        with open(f'music_{self.file_id}.mp3', 'wb') as f:
          r.raw.decode_content = True
          shutil.copyfileobj(r.raw, f)
          self.local_file_name = f"music_{self.file_id}.mp3"
          self.is_downloaded = True
      except Exception as ex:
        self.error = str(ex)
        return False
      return True
    else:
      return False
