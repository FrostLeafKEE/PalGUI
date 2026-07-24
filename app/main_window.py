"""主窗口 —— 整合所有子模块。

包含 QTabWidget 的三个标签页：
- 服务器控制（启停 + 路径管理 + SteamCMD 更新 + 存档备份）
- 玩家列表（RCON 在线玩家查询）
- 设置编辑器（PalWorldSettings.ini 可视化编辑）

标签页共享服务器路径状态。
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QTabWidget,
)

from app.server_tab import ServerTab
from app.settings_tab import SettingsTab
from app.player_tab import PlayerTab
from app.theme import FUSION_QSS


class MainWindow(QMainWindow):
    """幻兽帕鲁开服管理工具主窗口"""

    WINDOW_TITLE = "幻兽帕鲁（Palworld）开服管理工具"
    MIN_WIDTH = 1000
    MIN_HEIGHT = 600

    def __init__(self):
        super().__init__()

        self._server_path: str = ""

        self._setup_window()
        self._setup_tabs()
        self._setup_statusbar()

    def _setup_window(self):
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.resize(1200, 800)

        screen = self.screen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        self.setStyleSheet(FUSION_QSS)

    def _setup_tabs(self):
        self._tabs = QTabWidget()
        self._tabs.setObjectName("mainTabs")

        self._server_tab = ServerTab()
        self._tabs.addTab(self._server_tab, "  服务器控制")
        self._server_tab.path_changed.connect(self._on_path_changed)

        self._player_tab = PlayerTab()
        self._tabs.addTab(self._player_tab, "  玩家列表")

        self._settings_tab = SettingsTab()
        self._tabs.addTab(self._settings_tab, "  设置编辑器")

        self._tabs.currentChanged.connect(self._on_tab_changed)

        self.setCentralWidget(self._tabs)

    def _setup_statusbar(self):
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
        self._statusbar.showMessage("就绪 - 请设置服务器路径")

    @pyqtSlot(str)
    def _on_path_changed(self, path: str):
        self._server_path = path
        self._settings_tab.server_path = path
        if path:
            self._statusbar.showMessage(f"服务器路径：{path}")
        else:
            self._statusbar.showMessage("就绪 - 请设置服务器路径")

    @pyqtSlot(int)
    def _on_tab_changed(self, index: int):
        if self._tabs.widget(index) is self._settings_tab:
            if self._settings_tab.server_path != self._server_path:
                self._settings_tab.server_path = self._server_path
            else:
                self._settings_tab.load_config()
        elif self._tabs.widget(index) is self._player_tab:
            # 从设置中同步 RCON 默认值
            if self._server_path:
                config_file = self._settings_tab._get_config_path()
                try:
                    from app.config_manager import read_config
                    values = read_config(config_file)
                    host = values.get("PublicIP", "127.0.0.1") or "127.0.0.1"
                    port = str(values.get("RCONPort", 25575))
                    password = values.get("AdminPassword", "")
                    self._player_tab.set_rcon_defaults(host, port, password)
                except Exception:
                    pass
