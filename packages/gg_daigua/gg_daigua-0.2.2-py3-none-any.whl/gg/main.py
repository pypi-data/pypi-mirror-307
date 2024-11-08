from typing import List, Optional
import typer
from gg.start_init import start_init
from gg.utils.common import ColorPrinter, Downloader, sanitize_filename
from pathlib import Path
from rich.console import Console
from rich.table import Table



console = Console()

app = typer.Typer()


def validate_file_path(filepath: Path):
    if filepath is None:
        return filepath
    if not filepath.exists(): # 路径是否存在
        raise typer.BadParameter("文件不存在！")
    if not filepath.is_file():  # 是否是文件而不是文件夹
        raise typer.BadParameter("只支持文件类型！")
    return filepath



@app.command(help="自动生成视频的字幕srt文件")
def srt(
    filepath: Path = typer.Argument(..., callback=validate_file_path, help="视频文件路径"), 
    merge:bool = typer.Option(default=False, help="将字幕合并到视频中"),
    y:bool=typer.Option(default=False, help="是否忽略所有已存在的文件，默认为false"),
):
    new_file_path = filepath.with_suffix(".srt")
    if not y and new_file_path.exists():
        typer.secho(f"已存在文件：{new_file_path}", fg=typer.colors.YELLOW)
        confirm =  typer.confirm("是否继续生成？")
        if not confirm:
            raise typer.Abort()

    from gg.utils.srt import generate_srt
    generate_srt(filepath, new_file_path)
    if merge:
        srt_merge(filepath, new_file_path)
    return new_file_path


@app.command(help="合并srt字幕和视频文件")
def srt_merge(
    video_path: Path = typer.Argument(..., callback=validate_file_path, help="视频文件路径"),
    srt_path: Path = typer.Argument(..., callback=validate_file_path, help="srt文件路径"),
    y:bool=typer.Option(default=False, help="是否忽略所有已存在的文件，默认为false")
    ):
    from gg.utils.srt import merge_srt_with_mp4
    new_video_path = video_path.parent / f"{video_path.stem}【带字幕】{video_path.suffix}"
    merge_srt_with_mp4(video_path, srt_path, new_video_path, y)
    return new_video_path



@app.command(help="下载youtube视频")
def youtube(
    url: str, dest:Path=None, auto_srt:bool=False, 
            max_video:bool=typer.Option(default=False, help="自动下载最大（一般最清晰）的视频"),
            y:bool=typer.Option(default=False, help="是否忽略所有已存在的文件，默认为false")
            ):
    # 1.获取视频信息
    from gg.utils.youtube import YouTubeUtils
    ok, video_info = YouTubeUtils.get_video_info(url)
    if ok != 0:
        return typer.secho(f"获取视频信息错误：{video_info}", fg=typer.colors.RED)
    
    # 2.展示视频信息
    video_title = video_info["video_title"]
    ColorPrinter.print(f"{video_title}")
    table = Table("序号","类型", "直链下载", "大小")
    item_list = video_info["item_list"]
    for i, v in enumerate(item_list):
        no = i+ 1 
        can_download = v.get("can_download")
        data_size = v.get("data_size")
        data_name = v.get("data_name")
        
        table.add_row(
            f"{no}",
            data_name,
            "是" if can_download else "否",
            data_size,
            )

    console.print(table)

    # 3.输入序号选择下载
    if max_video:
        dn = len(item_list)
    else:
        dn = int(typer.prompt("输入序号开始下载"))
    item = item_list[dn-1]
    # ColorPrinter.print(item)

    # 检测文件是否已经存在
    video_title = sanitize_filename(video_title)
    dest = dest or Path(f"{video_title}.{item['data_type']}")
    if not y and dest.exists():
        typer.secho(f"已存在文件：{dest}", fg=typer.colors.YELLOW)
        confirm =  typer.confirm("是否继续生成？")
        if not confirm:
            raise typer.Abort()

    status = ret = None
    total = 200
    pre_percent = 0
    with typer.progressbar(label="获取下载链接：", length=total) as progress:
        for status, ret in YouTubeUtils.download(item):
            # ColorPrinter.print_yellow(f"下载状态: {status} {ret}")
            if status == 0:
                progress.update(total)
            elif status == 1:
                percent = float(ret["percent"][:-1].strip())
                percent_type = ret.get("type")
                if percent_type in ["converting", "merging"]:
                    percent += 100
                # ColorPrinter.print(f"{percent_type =}, {percent = }")
                progress.update(percent - pre_percent)
                pre_percent = percent
            elif status == 2:
                typer.Abort("系统繁忙")
            else:
                typer.Abort("未知错误")
    
    # 4.下载保存
    Downloader.download(ret, dest=dest)
    ColorPrinter.print(f"下载完成：{dest}")

    # 5.生成srt文件
    if auto_srt:
        ColorPrinter.print("开始生成字幕文件...")
        srt(dest)
    
    return dest


@app.command(help="自用工作流，1.下载最清晰的youtube视频，2.提取srt文件，3.合并字幕与视频，并清除多余文件，只留带字幕的新视频")
def my(urls: Optional[List[str]]  = typer.Argument(None ,help="可以接收多个url")):
    urls = urls or []
    for url in urls:
        ColorPrinter.print_green(f"开始任务：{url}")

        # 下载视频
        video_path = youtube(url=url, max_video=True, y=True)
        # 生成srt
        srt_path = srt(video_path, merge=False, y=True)
        # 合并视频和字幕
        srt_merge(video_path, srt_path, y=True)

        ColorPrinter.print("清理文件...")
        video_path.unlink()
        srt_path.unlink()
        ColorPrinter.print_green(f"结束任务：{url}")


if __name__ == "__main__":
    # https://www.youtube.com/watch?v=HS2okxA1TQ0&t=1s
    start_init()
    app()