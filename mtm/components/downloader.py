import json
import os
from .meta_crawler import MetaCrawler
from .exceptions import DownloadError
from ..utils.string_fmt import fmt_dirname
import youtube_dl
from ..config import DEFAULT_AUDIO_FMT

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
cache_dir = os.environ.get("cache_dir", "tests")


class Downloader:
    def __init__(self):
        pass

    def download(self, url, cache_path):
        meta_crawler = MetaCrawler()
        meta = meta_crawler.get_meta(url)
        title = fmt_dirname(meta["title"])
        unique_id = meta["id"]
        download_dir = "%s/%s-%s" % (cache_path, title, unique_id)
        print("download_dir:", download_dir)
        ydl_opts = {
            "proxy": "socks5://127.0.0.1:17720",
            # "logger": MyLogger(),
            "progress_hooks": [my_hook],
            "quiet": False,
            "no_warnings": True,
            # "format": "bestaudio/best",
            "writethumbnail": True,
            "outtmpl": download_dir + "/" + "%(id)s.%(ext)s",
            "writeinfojson": True,
            "format": DEFAULT_AUDIO_FMT
            # "postprocessors": [
            #     {
            #         "key": "FFmpegExtractAudio",
            #         "preferredcodec": DEFAULT_AUDIO_FMT,
            #         "preferredquality": "192",
            #     }
            # ],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ret = ydl.download([url])
            if ret:
                raise DownloadError()
            else:
                return download_dir
