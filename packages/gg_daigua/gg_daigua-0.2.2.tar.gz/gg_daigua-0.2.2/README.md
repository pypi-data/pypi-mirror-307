## 自用的工具箱


### 使用

`gg --help`

```shell

Usage: gg [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                           │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.    │
│ --help                        Show this message and exit.                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ my          自用工作流，1.下载最清晰的youtube视频，2.提取srt文件，3.合并字幕与视频，并清除多余文件，只留带字幕的… │
│ srt         自动生成视频的字幕srt文件                                                                             │
│ srt-merge   合并srt字幕和视频文件                                                                                 │
│ youtube     下载youtube视频                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```



### 打包上传

安装依赖

`poetry install`

构建包

`opetry build`

配置pypi token（配置过可跳过）

`poetry config pypi-token.pypi <your-api-token>`

上传

`poetry publish`


### 版本更新

```shell

poetry version patch   # 增加补丁版本，0.1.0 -> 0.1.1
poetry version minor   # 增加次版本，0.1.0 -> 0.2.0
poetry version major   # 增加主版本，0.1.0 -> 1.0.0
poetry version <新版本号>  # 直接设置为特定版本号

```