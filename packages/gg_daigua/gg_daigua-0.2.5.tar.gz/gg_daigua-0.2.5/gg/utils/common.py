import json
import re
import shutil
from pathlib import Path

import imageio
import requests
import typer
from tqdm import tqdm


def sure_path_exists(a_p: Path):
    if not a_p.exists():
        a_p.mkdir(parents=True, exist_ok=True)


def sure_file_exists(a_p: Path):
    if not a_p.exists():
        a_p.touch(exist_ok=True)


# 其它目录
ffmpeg_bin_path = Path(imageio.plugins.ffmpeg.get_exe())

# 本地目录相关
# 家目录：~/.gg_daigua
home_path = Path.home() / ".gg_daigua"

home_bins_path = home_path / "bins"
sure_path_exists(home_bins_path)

config_json_path = home_path / "config.json"
sure_file_exists(config_json_path)

model_path = home_path / "resources"
sure_path_exists(model_path)

ffmpeg_log_file_path = home_path / "ffmpeg_log.txt"

tmp_file_path = home_path / "tmp/tmp.file"
sure_path_exists(tmp_file_path)

# 项目目录相关
project_path = Path(__file__).parent.parent
resource_path = project_path.joinpath("resources")

resource_youtube_js_path = resource_path.joinpath("js/youtube.js")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def delete_folder(folder_path):
    """
    删除指定路径的文件夹，包括其中的所有文件和子文件夹

    Args:
      folder_path: 要删除的文件夹路径
    """

    path = Path(folder_path)
    if path.exists() and path.is_dir():
        shutil.rmtree(path)


def get_path_str(p: Path):
    return str(p.resolve())


def get_filename_from_content_disposition(headers):
    """从 Content-Disposition 头中提取文件名"""
    content_disposition = headers.get('Content-Disposition')
    if content_disposition:
        filename_parts = [part for part in content_disposition.split(';') if 'filename=' in part]
        if filename_parts:
            filename = filename_parts[0].split('=')[1].strip('\"')
            return filename
    return None


def sanitize_filename(filename):
    # 定义一个正则表达式，匹配不合法字符
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # 进一步去除多余的空格
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized


class ColorPrinter:

    @staticmethod
    def print_green(text):
        typer.secho(f"{text}", bg=typer.colors.GREEN)

    @staticmethod
    def print_yellow(text):
        typer.secho(f"{text}", bg=typer.colors.YELLOW)

    @staticmethod
    def print_red(text):
        typer.secho(f"{text}", bg=typer.colors.RED)

    @staticmethod
    def print(text, bg=None):
        typer.secho(f"{text}", bg=bg)


class Downloader:
    req_headers = {"user-agent": UA}

    @classmethod
    def get_file_size(cls, url):
        with requests.get(url, stream=True, headers=cls.req_headers) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            return total_size  # 字节

    @classmethod
    def download(cls, url, dest: Path = None, check_exists=False):

        with requests.get(url, stream=True, headers=cls.req_headers) as response:
            response.raise_for_status()  # 检查是否请求成功
            if dest is None:
                filename = get_filename_from_content_disposition(response.headers)
                dest = Path(filename)
            if dest.exists() and check_exists:
                return dest
            total_size = int(response.headers.get('content-length', 0))
            dest.parent.mkdir(parents=True, exist_ok=True)
            chunk_size = 1024  # 每次读取的字节数
            with open(dest, "wb") as file, tqdm(
                    total=total_size, unit='B', unit_scale=True, unit_divisor=1024,
                    desc="文件下载中", ascii=True
            ) as progress:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
                    progress.update(len(chunk))
            return dest


class ConfigJson:

    @classmethod
    def _load(cls):
        content = config_json_path.read_text(encoding="utf-8")
        return json.loads(content) if content else {}

    @classmethod
    def get(cls, key):
        return cls._load().get(key)

    @classmethod
    def set(cls, key, value):
        x = cls._load()
        x[key] = value
        config_json_path.write_text(json.dumps(x), encoding="utf-8")


if __name__ == "__main__":
    ConfigJson.set("a", 1000)
    print(ConfigJson.get("a"))
