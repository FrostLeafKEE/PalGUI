"""玩家在线列表标签页。

通过 RCON 连接服务器获取在线玩家信息。
"""

from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.rcon_client import RconClient, RconError
from app.theme import (
    BTN_SECONDARY_QSS,
    BTN_PRIMARY_QSS,
    PLAYER_TABLE_QSS,
    RESOURCE_CARD_QSS,
)


class PlayerTab(QWidget):
    """玩家在线列表标签页"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._rcon: RconClient | None = None
        self._auto_refresh = False

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 20, 24, 20)

        # RCON 连接设置
        rcon_group = QGroupBox("  RCON 连接设置")
        rcon_layout = QVBoxLayout(rcon_group)
        rcon_layout.setSpacing(10)

        row1 = QHBoxLayout()
        row1.setSpacing(10)

        self._host_input = QLineEdit()
        self._host_input.setPlaceholderText("  服务器 IP（默认 127.0.0.1）")
        self._host_input.setText("127.0.0.1")
        self._host_input.setStyleSheet("QLineEdit { background-color: #13151f; color: #e2e4f0; border: 1px solid #2e3148; border-radius: 8px; padding: 8px 14px; font-size: 13px; }")

        self._port_input = QLineEdit()
        self._port_input.setPlaceholderText("  RCON 端口（默认 25575）")
        self._port_input.setText("25575")
        self._port_input.setFixedWidth(140)
        self._port_input.setStyleSheet("QLineEdit { background-color: #13151f; color: #e2e4f0; border: 1px solid #2e3148; border-radius: 8px; padding: 8px 14px; font-size: 13px; }")

        row1.addWidget(self._host_input, 1)
        row1.addWidget(self._port_input)
        rcon_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(10)

        self._password_input = QLineEdit()
        self._password_input.setPlaceholderText("  RCON 密码（在设置编辑器中配置）")
        self._password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_input.setStyleSheet("QLineEdit { background-color: #13151f; color: #e2e4f0; border: 1px solid #2e3148; border-radius: 8px; padding: 8px 14px; font-size: 13px; }")

        self._btn_connect = QPushButton("  连接")
        self._btn_connect.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_connect.setStyleSheet(BTN_PRIMARY_QSS)
        self._btn_connect.clicked.connect(self._on_connect)

        row2.addWidget(self._password_input, 1)
        row2.addWidget(self._btn_connect)
        rcon_layout.addLayout(row2)

        self._rcon_status = QLabel("  未连接")
        self._rcon_status.setStyleSheet("color: #6b6f8a; font-size: 12px; padding-left: 4px;")
        rcon_layout.addWidget(self._rcon_status)

        layout.addWidget(rcon_group)

        # 玩家列表
        player_group = QGroupBox("  在线玩家")
        player_layout = QVBoxLayout(player_group)
        player_layout.setSpacing(10)

        toolbar = QHBoxLayout()

        self._btn_refresh = QPushButton("  刷新列表")
        self._btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_refresh.setStyleSheet(BTN_SECONDARY_QSS)
        self._btn_refresh.clicked.connect(self._refresh_players)
        self._btn_refresh.setEnabled(False)

        self._auto_refresh_cb = QCheckBox("  自动刷新（5秒）")
        self._auto_refresh_cb.setStyleSheet("QCheckBox { color: #a5a8c0; font-size: 13px; }")
        self._auto_refresh_cb.stateChanged.connect(self._on_auto_refresh_changed)

        toolbar.addWidget(self._btn_refresh)
        toolbar.addWidget(self._auto_refresh_cb)
        toolbar.addStretch()

        self._player_count_label = QLabel("在线：0 人")
        self._player_count_label.setStyleSheet("color: #7c9aff; font-size: 13px; font-weight: 600;")
        toolbar.addWidget(self._player_count_label)

        player_layout.addLayout(toolbar)

        self._player_table = QTableWidget()
        self._player_table.setColumnCount(4)
        self._player_table.setHorizontalHeaderLabels(["玩家名称", "Player ID", "Steam ID", "在线时长"])
        self._player_table.setStyleSheet(PLAYER_TABLE_QSS)
        self._player_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._player_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._player_table.setAlternatingRowColors(True)
        header = self._player_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self._player_table.verticalHeader().setVisible(False)

        player_layout.addWidget(self._player_table)
        layout.addWidget(player_group, 1)

        # 自动刷新定时器
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_players)

    def _on_connect(self):
        host = self._host_input.text().strip() or "127.0.0.1"
        try:
            port = int(self._port_input.text().strip() or "25575")
        except ValueError:
            self._rcon_status.setText("  端口格式错误")
            self._rcon_status.setStyleSheet("color: #f87171; font-size: 12px; padding-left: 4px;")
            return

        password = self._password_input.text()
        if not password:
            self._rcon_status.setText("  请输入 RCON 密码")
            self._rcon_status.setStyleSheet("color: #f87171; font-size: 12px; padding-left: 4px;")
            return

        if self._rcon:
            self._rcon.disconnect()
            self._rcon = None

        try:
            self._rcon = RconClient(host, port, password)
            self._rcon.connect()
            self._rcon_status.setText("  已连接")
            self._rcon_status.setStyleSheet("color: #4ade80; font-size: 12px; padding-left: 4px;")
            self._btn_refresh.setEnabled(True)
            self._btn_connect.setText("  断开")
            self._btn_connect.setStyleSheet(BTN_SECONDARY_QSS)
            self._btn_connect.clicked.disconnect()
            self._btn_connect.clicked.connect(self._on_disconnect)
            self._refresh_players()
        except RconError as e:
            self._rcon_status.setText(f"  连接失败：{e}")
            self._rcon_status.setStyleSheet("color: #f87171; font-size: 12px; padding-left: 4px;")
            self._rcon = None

    def _on_disconnect(self):
        if self._rcon:
            self._rcon.disconnect()
            self._rcon = None
        self._auto_refresh_cb.setChecked(False)
        self._rcon_status.setText("  未连接")
        self._rcon_status.setStyleSheet("color: #6b6f8a; font-size: 12px; padding-left: 4px;")
        self._btn_refresh.setEnabled(False)
        self._btn_connect.setText("  连接")
        self._btn_connect.setStyleSheet(BTN_PRIMARY_QSS)
        self._btn_connect.clicked.disconnect()
        self._btn_connect.clicked.connect(self._on_connect)
        self._player_table.setRowCount(0)
        self._player_count_label.setText("在线：0 人")

    @pyqtSlot()
    def _refresh_players(self):
        if not self._rcon:
            return
        try:
            response = self._rcon.send_command("ShowPlayers")
            self._parse_player_list(response)
        except RconError as e:
            self._rcon_status.setText(f"  查询失败：{e}")
            self._rcon_status.setStyleSheet("color: #f87171; font-size: 12px; padding-left: 4px;")

    def _parse_player_list(self, response: str):
        lines = response.strip().split("\n")
        self._player_table.setRowCount(0)

        if not lines or lines[0].strip() == "":
            self._player_count_label.setText("在线：0 人")
            return

        # 第一行是表头：name,playerid,steamid
        # 后续行是数据
        for i, line in enumerate(lines[1:], start=0):
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 3:
                continue
            name = parts[0].strip()
            player_id = parts[1].strip()
            steam_id = parts[2].strip()

            row = self._player_table.rowCount()
            self._player_table.insertRow(row)
            self._player_table.setItem(row, 0, QTableWidgetItem(name))
            self._player_table.setItem(row, 1, QTableWidgetItem(player_id))
            self._player_table.setItem(row, 2, QTableWidgetItem(steam_id))
            self._player_table.setItem(row, 3, QTableWidgetItem("--"))

        count = self._player_table.rowCount()
        self._player_count_label.setText(f"在线：{count} 人")

    def _on_auto_refresh_changed(self, state):
        self._auto_refresh = state == Qt.CheckState.Checked.value
        if self._auto_refresh:
            self._refresh_timer.start(5000)
        else:
            self._refresh_timer.stop()

    def set_rcon_defaults(self, host: str, port: str, password: str):
        """从设置页面同步 RCON 默认值"""
        if host and not self._host_input.text().strip():
            self._host_input.setText(host)
        if port and not self._port_input.text().strip():
            self._port_input.setText(port)
        if password and not self._password_input.text():
            self._password_input.setText(password)
