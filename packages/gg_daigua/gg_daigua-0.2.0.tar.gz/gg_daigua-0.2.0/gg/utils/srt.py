import whisper
import moviepy.editor as mp
from moviepy.config import change_settings
from pathlib import Path
from gg.utils.common import model_path, get_path_str, resource_tmp_file, ColorPrinter, ffmpeg_bin_path
from gg.ext_packages.better_ffmpeg_progress import FfmpegProcess

change_settings({"FFMPEG_BINARY": ffmpeg_bin_path})


def generate_srt(vfile: Path, ofile: Path):
    vfilepath = get_path_str(vfile)
    ofilepath = get_path_str(ofile)

    # 加载 Whisper 模型
    base_pt_path = model_path/"base.pt"
    if base_pt_path.exists():
        model = whisper.load_model(base_pt_path)  # 可以选择 "small", "medium", "large" 作为模型大小
    else:
        ColorPrinter.print("下载模型...")
        model = whisper.load_model("base", download_root=get_path_str(model_path))

    # 提取音频
    video = mp.VideoFileClip(vfilepath)
    tmp_file = resource_tmp_file.with_suffix(".wav")
    try:
        audio_file = get_path_str(tmp_file)
        video.audio.write_audiofile(audio_file)

        # 使用 Whisper 生成字幕
        result = model.transcribe(audio_file, verbose=False)
    except Exception as e:
        ColorPrinter.print_red(e)
        return
    finally:
        try:
            tmp_file.unlink()
            video.close()
        except:
            pass

    # 将结果写入 SRT 文件
    with open(ofilepath, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result['segments']):
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            f.write(f"{i + 1}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{text}\n\n")
    ColorPrinter.print(f"生成字幕文件：{ofilepath}")


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"



def merge_srt_with_mp4(video_path:Path, srt_path:Path, output_path:Path, y):

    command = [
        f"{ffmpeg_bin_path}",
        "-i", str(video_path),
        "-i", str(srt_path),
        "-c:s", "mov_text",
        "-c:v", "copy",
        "-c:a", "copy",
        str(output_path)
    ]
    if y:
        command.insert(1, "-y")
    process = FfmpegProcess(command)
    process.run(progress_bar_description="合并中：", 
                log_file="ffmpeg.log",
                # progress_handler=progress_handler
                )
    ColorPrinter.print(f"生成带字幕视频: {output_path}")

 
   
