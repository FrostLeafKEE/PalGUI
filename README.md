# PalGUI

幻兽帕鲁（Palworld）开服管理工具，基于 PyQt6 的图形界面。

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6%2B-green)

## 功能

- **服务器控制**：一键启动/关闭 PalServer 进程，实时查看控制台输出
- **SteamCMD 更新**：自动检测 steamcmd，一键更新服务端
- **设置编辑器**：可视化编辑 PalWorldSettings.ini，所有配置项按分组展示，带中文标注

## 截图

（待补充）

## 快速开始

### 直接运行

下载 Releases 里的 PalGUI.exe，双击运行即可。

### 从源码运行

```bash
pip install -r requirements.txt
python main.py
```

### 打包 exe

```bash
pip install pyinstaller
pyinstaller PalGUI.spec
```

## 目录结构

```
PalGUI/
├── main.py              # 入口
├── app/
│   ├── __init__.py
│   ├── main_window.py   # 主窗口
│   ├── server_tab.py    # 服务器控制页
│   ├── settings_tab.py  # 设置编辑器页
│   ├── server_process.py # 进程管理
│   ├── config_manager.py # 配置文件读写
│   ├── config_schema.py  # 配置项定义
│   └── theme.py         # 暗色主题样式
├── PalGUI.spec          # PyInstaller 打包配置
└── requirements.txt
```

## 注意事项

- 需要先通过 SteamCMD 安装 Palworld Dedicated Server
- 设置页面操作的是 `Pal/Saved/Config/WindowsServer/PalWorldSettings.ini`
- 修改配置后需重启服务端生效
