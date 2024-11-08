import time

import execjs
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout

from gg.utils.common import resource_youtube_js_path, Downloader

youtube_js_ctx = execjs.compile(resource_youtube_js_path.read_text(encoding="utf-8"))


def murmur_hash64(a_str):
    return youtube_js_ctx.call("murmurHash64", a_str)


fake_document = """
var document = {
    getElementById: function(id) {
        var x = {
        
            getElementsByTagName: function(name){
                return [];
            }
        };
        return x;
    }
}
"""


class YouTubeUtils:

    @classmethod
    def fill_n(cls, soup: BeautifulSoup, url: str):
        script = soup.find_all("script")[-1]
        script = fake_document + script.text
        js_ctx = execjs.compile(script)
        return js_ctx.call("fillN", url)

    @classmethod
    def _parse_video_info(cls, text):

        ret = {}
        soup = BeautifulSoup(text, "html.parser")

        # 视频标题：
        video_title = soup.find("span", id="video_title")
        if video_title:
            video_title = video_title.text

        ret["video_title"] = video_title

        table_content = soup.find("div", id="myTabContent")
        if not table_content:
            return -1, "未找到内容"

        item_list = []
        all_tds = table_content.find_all(class_="btn-success")
        for td in all_tds:
            tr_class = td.parent.parent.get("class", [])
            if "noaudio" in tr_class:
                continue

            name = td.name
            can_download = name == "a"
            onclick = td.get("onclick", "")
            href = td.get("href", "")
            if can_download:
                href = cls.fill_n(soup, td.get("href"))
            else:
                if "download" not in onclick:
                    continue
                onclick = eval(onclick[8:])

            data_size = td.find_parent().find_previous_sibling().text.strip()
            data_name = td.find_parent().find_previous_sibling().find_previous_sibling().text.strip()
            data_type = td.get("data-ftype")

            item_list.append({
                "data_type": data_type,
                "data_size": data_size,
                "data_name": data_name,
                "can_download": can_download,
                "href": href,
                "onclick": onclick,
                "byte_size": float(onclick[4] if onclick else Downloader.get_file_size(href))
            })
        item_list = sorted(item_list, key=lambda x: x["byte_size"])
        # print(item_list)
        ret["item_list"] = item_list
        return 0, ret

    @classmethod
    def get_video_info(cls, video_url):
        mhash = murmur_hash64(video_url)
        url = f"https://yt1d.com/mates/en/analyze/ajax?retry=undefined&platform=youtube&mhash={mhash}"

        resp = requests.post(url, data={"url": video_url, "ajax": 1, "lang": "zh-tw"})
        text = resp.json()["result"]
        return cls._parse_video_info(text)

    @classmethod
    def download(cls, video_info: dict, query_type=1):
        """
        0-下载完毕
        1-进行中
        2-系统繁忙
        3-错误

        query_type: 1.下载 2.查询下载状态
        """
        can_download = video_info.get("can_download")
        if can_download:
            yield 0, video_info["href"]
            return

        onclick = video_info["onclick"]
        url, title, vid, ext, totalSize, note, format = onclick

        headers = {
            "x-note": note
        }
        data = {
            "platform": "youtube",
            "url": url,
            "title": title,
            "id": vid,
            "ext": ext,
            "note": note,
            "format": format,
        }
        durl = f"https://yt1d.com/mates/en/convert?id={vid}" if query_type == 1 else f"https://yt1d.com/mates/en/convert/status?id={vid}"
        try:
            ret = requests.post(durl, data=data, headers=headers, timeout=4).json()
            status = ret.get("status")
            if status == "success":  # 有结果
                yield 0, ret["downloadUrlX"]
                return
            elif status == "convert_ready":  # 转换成功
                time.sleep(1)
                yield from cls.download(video_info)
            elif status == "busy":  # 系统繁忙
                yield 2, "系统繁忙，稍后重试"
                return
            elif status == "processing":  # 处理中
                yield 1, ret  # {"status":"processing","percent":" 32.3%","type":"downloading"}
                yield from cls.download(video_info, query_type=2)
            else:  # 系统错误
                yield 3, ret

        except ReadTimeout:
            # 继续查询
            yield from cls.download(video_info, query_type=2)


if __name__ == '__main__':
    print(YouTubeUtils.get_video_info("https://www.youtube.com/watch?v=RDJWHNwwI-M"))
