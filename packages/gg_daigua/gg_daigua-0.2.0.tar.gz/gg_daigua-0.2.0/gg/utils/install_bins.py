import platform
import tarfile
import zipfile
from pathlib import Path
from gg.utils.common import Downloader, ColorPrinter, delete_folder, ConfigJson, get_path_str

# FFmpeg 下载链接
FFMPEG_URLS = {
    "windows": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.1-latest-win64-lgpl-7.1.zip",
    "mac": "https://ffmpeg.org/releases/ffmpeg-5.1.2.tar.bz2",
    "linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"
}

# 获取平台类型并返回对应平台的 FFmpeg 下载 URL
def get_ffmpeg_url():
    system = platform.system().lower()
    
    if system == 'windows':
        return FFMPEG_URLS["windows"]
    elif system == 'darwin':  # macOS
        return FFMPEG_URLS["mac"]
    elif system == 'linux':  # Ubuntu
        return FFMPEG_URLS["linux"]
    else:
        raise Exception("Unsupported platform")

# 下载 FFmpeg 文件并显示下载进度
def download_ffmpeg(target_dir: Path, rename="ffmpeg"):
    final_path = target_dir / rename
    if final_path.exists():
        delete_folder(final_path)

    final_bin_path = final_path / "bin/ffmpeg"

    url = get_ffmpeg_url()
    ColorPrinter.print_green("开始下载ffmpeg...")
    zip_path = Downloader.download(url)
        
    print("下载完成，开始解压...")
    
    if zip_path.suffix.endswith((".zip")):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 获取解压后的文件夹名称
            fold_name = zip_ref.namelist()[0]
            zip_ref.extractall(target_dir)  # 解压到指定文件夹
            extracted_folder = target_dir / fold_name
            print(f"解压完成，文件夹名称：{extracted_folder}")
            
            # 重命名解压出的文件夹
            extracted_folder.rename(final_path)
            print(f"文件夹已重命名为：{final_path}")

    # 根据文件类型解压
    elif zip_path.suffix.endswith(".tar.xz") or zip_path.suffix.endswith(".tar.bz2"):
        with tarfile.open(zip_path, "r:xz") as tar:
            # 获取解压后的文件夹名称
            members = tar.getnames()
            fold_name = members[0].split('/')[0]  # 获取第一个文件夹名
            tar.extractall(path=target_dir)  # 解压到指定文件夹
            extracted_folder = target_dir / fold_name
            print(f"解压完成，文件夹名称：{extracted_folder}")
            
            # 重命名解压出的文件夹
            extracted_folder.rename(final_path)
            print(f"文件夹已重命名为：{final_path}")
    else:
        raise Exception(f"出错：{zip_path}")

    zip_path.unlink()
    return final_bin_path

# 安装 FFmpeg 方法
def install_ffmpeg(target_dir: Path):
    plat = platform.system().lower()

    if x:= ConfigJson.get(f"{plat}:ffmpeg"):
        return x

    target_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_path = download_ffmpeg(target_dir)
    # 如果是在 Windows 下，需要调整为 .exe 文件
    if plat == 'windows':
        ffmpeg_path = ffmpeg_path.with_suffix('.exe')
    
    ConfigJson.set(f"{plat}:ffmpeg",  get_path_str(ffmpeg_path))
    return ffmpeg_path


# 示例：调用方法来下载并安装 FFmpeg
if __name__ == "__main__":
    # 设定下载目录
    target_dir = Path.home() / ".gg_daigua/bins"
    ffmpeg_path = install_ffmpeg(target_dir)
    print(f"FFmpeg 可执行文件路径: {ffmpeg_path}")
