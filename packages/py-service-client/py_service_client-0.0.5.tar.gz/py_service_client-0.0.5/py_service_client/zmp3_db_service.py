
import sys

sys.path.append("py_service_client/thrift_gen")

from typing import List
from py_service_client.thrift_gen.zmp3_db_service import ZMP3DBServiceRead
from py_service_client.thrift_gen.zmp3_common.ttypes import TAuthInfo
from py_service_client.thrift_gen.zmp3_core import ttypes
from py_service_client.common.base_client import BaseClient
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

host = config["ZMP3DBServiceReadClient"]["host"]
port = config["ZMP3DBServiceReadClient"]["port"]
timeout = config["ZMP3DBServiceReadClient"]["timeout"]

    
class ZMP3DBServiceReadClient(BaseClient[ZMP3DBServiceRead.Client]): 
    def __init__(self):
        super().__init__(ZMP3DBServiceRead, host, port, int(timeout))

    # /*--------------------------------MEDIA-------------------------------*/
    def getMedia(self, id: int) -> ttypes.TMediaResult:
        return self.client.getMedia(TAuthInfo(), id)
    

    def getListMedia(self, ids: List[int]) -> ttypes.TMediaListResult:
        return self.client.getListMedia(TAuthInfo(), ids)
    

    def getMapMedia(self, ids: List[int]) -> ttypes.TMediaMapResult:
        return self.client.getMapMedia(TAuthInfo(), ids)
    
    # /*--------------------------------PLAYLIST-------------------------------*/
    def getPlaylist(self, id: int) -> ttypes.TPlaylistResult:
        return self.client.getPlaylist(TAuthInfo(), id)
    

    def getListPlaylist(self, ids: List[int]) -> ttypes.TPlaylistListResult:
        return self.client.getListPlaylist(TAuthInfo(), ids)
    

    def getMapPlaylist(self, ids: List[int]) -> ttypes.TPlaylistMapResult:
        return self.client.getMapPlaylist(TAuthInfo(), ids)
    
    # /*--------------------------------ARTIST-------------------------------*/
    def getArtist(self, id: int) -> ttypes.TArtistResult:
        return self.client.getArtist(TAuthInfo(), id)
    

    def getListArtist(self, ids: List[int]) -> ttypes.TArtistListResult:
        return self.client.getListArtist(TAuthInfo(), ids)
    

    def getMapArtist(self, ids: List[int]) -> ttypes.TArtistMapResult:
        return self.client.getMapArtist(TAuthInfo(), ids)
    
    # /*--------------------------------GENRE-------------------------------*/
    def getGenre(self, id: int) -> ttypes.TGenreResult:
        return self.client.getGenre(TAuthInfo(), id)
    

    def getListGenre(self, ids: List[int])-> ttypes.TGenreListResult:
        return self.client.getListGenre(TAuthInfo(), ids)
    

    def getMapGenre(self, ids: List[int]) -> ttypes.TGenreMapResult:
        return self.client.getMapGenre(TAuthInfo(), ids)

    # /*--------------------------------LYRIC-------------------------------*/
    def getLyric(self, id: int) -> ttypes.TLyricResult:
        return self.client.getLyric(TAuthInfo(), id)
    

    def getListLyric(self, ids: List[int])-> ttypes.TLyricListResult:
        return self.client.getListLyric(TAuthInfo(), ids)
    
    def getMapLyric(self, ids: List[int]) -> ttypes.TLyricMapResult:
        return self.client.getMapLyric(TAuthInfo(), ids)

    # /*--------------------------------USER-------------------------------*/

    def getPlaylistUser(self, id: int) -> ttypes.TPlaylistUserResult:
        return self.client.getPlaylistUser(TAuthInfo(), id)
    
    def getListPlaylistUser(self, ids: List[int]) ->  ttypes.TPlaylistUserListResult:
        return self.client.getListPlaylistUser(TAuthInfo(), ids)
    
    def getMapPlaylistUser(self, ids: List[int]) -> ttypes.TPlaylistUserMapResult:
        return self.client.getMapPlaylistUser(TAuthInfo(), ids)
    
    # /*--------------------------------KV-------------------------------*/
    def getMediaKV(self, id: int) -> ttypes.TMediaResult:
        return self.client.getMediaKV(TAuthInfo(), id)
    