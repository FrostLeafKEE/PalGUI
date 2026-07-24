# PalGUI

幻兽帕鲁（Palworld）开服管理工具，PyQt6 图形界面，暗色主题。

## 功能

### 服务器控制
- 启动/关闭 PalServer，实时控制台输出
- SteamCMD 一键更新服务端
- 存档备份（手动 + 自动定时备份）
- 右侧实时显示 CPU/内存/进程占用

### 玩家列表
- 通过 RCON 查看在线玩家
- 显示玩家名称、Player ID、Steam ID
- 支持自动刷新（5 秒间隔）

### 设置编辑器
- 可视化编辑 PalWorldSettings.ini
- 所有配置项分组展示，中文标注
- 支持滑块和数值输入

## 快速开始

### 直接运行

下载 Releases 里的 PalGUI.exe，双击即可。

### 从源码运行

```bash
pip install -r requirements.txt
python main.py
```

### 打包

```bash
pip install pyinstaller
pyinstaller PalGUI.spec
```

## 目录结构

```
PalGUI/
── main.py
├── app/
│   ├── main_window.py     # 主窗口
│   ├── server_tab.py      # 服务器控制 + 备份 + 资源监控
│   ├── player_tab.py      # 玩家在线列表
│   ├── settings_tab.py    # 设置编辑器
│   ├── rcon_client.py     # RCON 协议客户端
│   ├── server_process.py  # 进程管理
│   ├── config_manager.py  # 配置文件读写
│   ├── config_schema.py   # 配置项定义
│   └── theme.py           # 样式表
├── PalGUI.spec
└── requirements.txt
```

## 注意

- 需要先通过 SteamCMD 安装 Palworld Dedicated Server
- 设置页操作的是 `Pal/Saved/Config/WindowsServer/PalWorldSettings.ini`
- 修改配置后需重启服务端生效
- 玩家列表需要在设置中启用 RCON 并设置密码
