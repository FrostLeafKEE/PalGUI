"""服务器控制标签页。

提供：
- 服务器路径管理（自动寻找 + 手动浏览）
- 服务器启停 Toggle 按钮与状态指示
- SteamCMD 更新服务器（login anonymous + app_update）
- 服务端输出实时控制台
"""

import os
import shutil
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QProcess
from PyQt6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.server_process import ServerProcess, find_server_executable
from app.theme import (
    BTN_START_QSS,
    BTN_STOP_QSS,
    BTN_STARTING_QSS,
    BTN_STOPPING_QSS,
    BTN_UPDATE_QSS,
    BTN_UPDATING_QSS,
    BTN_SECONDARY_QSS,
    CONSOLE_QSS,
    PATH_DISPLAY_QSS,
    PATH_FOUND_QSS,
    PATH_ERROR_QSS,
    STATUS_ONLINE_QSS,
    STATUS_OFFLINE_QSS,
)

_COMMON_STEAM_PATHS = [
    r"C:\steamcmd\steamapps\common\PalServer",
    r"C:\Program Files (x86)\Steam\steamapps\common\PalServer",
    r"C:\Steam\steamapps\common\PalServer",
    r"D:\steamcmd\steamapps\common\PalServer",
    r"D:\Steam\steamapps\common\PalServer",
    r"E:\steamcmd\steamapps\common\PalServer",
    r"E:\Steam\steamapps\common\PalServer",
]

_COMMON_STEAMCMD_PATHS = [
    r"C:\steamcmd\steamcmd.exe",
    r"D:\steamcmd\steamcmd.exe",
    r"E:\steamcmd\steamcmd.exe",
    r"C:\Steam\steamcmd\steamcmd.exe",
]

_PALSERVER_APP_ID = "2394010"


class ServerTab(QWidget):
    """服务器控制标签页"""

    path_changed = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._server_process = ServerProcess(self)
        self._update_process: QProcess | None = None
        self._server_path: str = ""
        self._steamcmd_path: str = ""
        self._updating = False

        self._setup_ui()
        self._connect_signals()

    @property
    def server_path(self) -> str:
        return self._server_path

    @server_path.setter
    def server_path(self, path: str):
        self._server_path = path
        self._path_display.setText(path)
        self._detect_steamcmd()
        self.path_changed.emit(path)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 20, 24, 20)

        # ========== 服务器路径管理 ==========
        path_group = QGroupBox("  服务器路径")
        path_layout = QVBoxLayout(path_group)
        path_layout.setSpacing(10)

        path_row = QHBoxLayout()
        path_row.setSpacing(10)

        self._path_display = QLineEdit()
        self._path_display.setReadOnly(True)
        self._path_display.setPlaceholderText("  尚未设置服务器路径...")
        self._path_display.setStyleSheet(PATH_DISPLAY_QSS)

        self._btn_auto_find = QPushButton("  自动寻找")
        self._btn_auto_find.setToolTip("在常见 SteamCMD 默认路径中搜索服务端")
        self._btn_auto_find.setMinimumWidth(110)
        self._btn_auto_find.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_auto_find.setStyleSheet(BTN_SECONDARY_QSS)

        self._btn_browse = QPushButton("  手动选择")
        self._btn_browse.setToolTip("打开文件夹选择对话框选择服务端目录")
        self._btn_browse.setMinimumWidth(110)
        self._btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_browse.setStyleSheet(BTN_SECONDARY_QSS)

        path_row.addWidget(self._path_display, 1)
        path_row.addWidget(self._btn_auto_find)
        path_row.addWidget(self._btn_browse)
        path_layout.addLayout(path_row)

        self._lbl_exe_status = QLabel("")
        self._lbl_exe_status.setStyleSheet("color: #6b6f8a; font-size: 12px; padding-left: 4px;")
        path_layout.addWidget(self._lbl_exe_status)

        layout.addWidget(path_group)

        # ========== 服务器控制 ==========
        control_group = QGroupBox("  服务器控制")
        control_layout = QVBoxLayout(control_group)
        control_layout.setSpacing(12)

        control_row = QHBoxLayout()
        control_row.setSpacing(16)

        self._btn_toggle = QPushButton("  启动服务器")
        self._btn_toggle.setMinimumHeight(50)
        self._btn_toggle.setMinimumWidth(200)
        self._btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_toggle.setStyleSheet(BTN_START_QSS)
        self._btn_toggle.setEnabled(False)

        self._lbl_status = QLabel("●  未运行")
        self._lbl_status.setStyleSheet(STATUS_OFFLINE_QSS)

        control_row.addWidget(self._btn_toggle)
        control_row.addWidget(self._lbl_status)
        control_row.addStretch()
        control_layout.addLayout(control_row)

        layout.addWidget(control_group)

        # ========== 服务器更新（SteamCMD） ==========
        update_group = QGroupBox("  服务器更新 (SteamCMD)")
        update_layout = QVBoxLayout(update_group)
        update_layout.setSpacing(12)

        steamcmd_row = QHBoxLayout()
        steamcmd_row.setSpacing(10)

        self._steamcmd_display = QLineEdit()
        self._steamcmd_display.setReadOnly(True)
        self._steamcmd_display.setPlaceholderText("  设置服务器路径后将自动检测 steamcmd.exe...")
        self._steamcmd_display.setStyleSheet(PATH_DISPLAY_QSS)

        self._btn_steamcmd_browse = QPushButton("  手动定位")
        self._btn_steamcmd_browse.setToolTip("手动选择 steamcmd.exe 的位置")
        self._btn_steamcmd_browse.setMinimumWidth(110)
        self._btn_steamcmd_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_steamcmd_browse.setStyleSheet(BTN_SECONDARY_QSS)

        steamcmd_row.addWidget(self._steamcmd_display, 1)
        steamcmd_row.addWidget(self._btn_steamcmd_browse)
        update_layout.addLayout(steamcmd_row)

        update_btn_row = QHBoxLayout()
        update_btn_row.setSpacing(16)

        self._btn_update = QPushButton("  更新服务器")
        self._btn_update.setMinimumHeight(44)
        self._btn_update.setMinimumWidth(180)
        self._btn_update.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_update.setStyleSheet(BTN_UPDATE_QSS)
        self._btn_update.setToolTip(
            "通过 SteamCMD 更新幻兽帕鲁服务端\n"
            "（依次执行 login anonymous -> app_update 2394010 validate -> quit）"
        )
        self._btn_update.setEnabled(False)

        self._lbl_update_status = QLabel("")
        self._lbl_update_status.setStyleSheet(
            "font-size: 13px; color: #6b6f8a; padding-left: 8px;"
        )

        update_btn_row.addWidget(self._btn_update)
        update_btn_row.addWidget(self._lbl_update_status)
        update_btn_row.addStretch()
        update_layout.addLayout(update_btn_row)

        layout.addWidget(update_group)

        # ========== 输出控制台 ==========
        console_group = QGroupBox("  输出日志")
        console_layout = QVBoxLayout(console_group)
        console_layout.setSpacing(8)

        self._console = QTextEdit()
        self._console.setReadOnly(True)
        self._console.setStyleSheet(CONSOLE_QSS)
        self._console.setPlaceholderText("服务器和更新日志将显示在这里...")

        clear_row = QHBoxLayout()
        clear_row.addStretch()
        btn_clear = QPushButton("  清除日志")
        btn_clear.setFixedWidth(100)
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet(BTN_SECONDARY_QSS)
        btn_clear.clicked.connect(self._console.clear)
        clear_row.addWidget(btn_clear)

        console_layout.addWidget(self._console)
        console_layout.addLayout(clear_row)
        layout.addWidget(console_group, 1)

    def _connect_signals(self):
        self._btn_auto_find.clicked.connect(self._on_auto_find)
        self._btn_browse.clicked.connect(self._on_browse)
        self._btn_toggle.clicked.connect(self._on_toggle)
        self._btn_steamcmd_browse.clicked.connect(self._on_browse_steamcmd)
        self._btn_update.clicked.connect(self._on_update_server)

        self._server_process.started.connect(self._on_server_started)
        self._server_process.stopped.connect(self._on_server_stopped)
        self._server_process.output_received.connect(self._on_server_output)
        self._server_process.error_occurred.connect(self._on_server_error)

    @pyqtSlot()
    def _on_auto_find(self):
        found = None
        for p in _COMMON_STEAM_PATHS:
            exe = find_server_executable(p)
            if exe:
                found = Path(p)
                break

        if not found:
            import string
            for drive in string.ascii_uppercase:
                root = f"{drive}:\\"
                if not os.path.exists(root):
                    continue
                steam_path = os.path.join(root, "steamcmd", "steamapps", "common", "PalServer")
                exe = find_server_executable(steam_path)
                if exe:
                    found = Path(steam_path)
                    break

        if found and found.is_dir():
            self.server_path = str(found)
            self._check_executable()
            QMessageBox.information(
                self, "自动寻找完成",
                f"已在以下位置找到服务端：\n{found}"
            )
        else:
            QMessageBox.warning(
                self, "未找到",
                "未能自动找到 PalServer 服务端。\n\n"
                "请确保已通过 SteamCMD 安装 Palworld Dedicated Server，\n"
                "或使用「手动选择」按钮指定服务端目录。\n\n"
                "常见安装路径：\n"
                "  C:\\steamcmd\\steamapps\\common\\PalServer"
            )

    @pyqtSlot()
    def _on_browse(self):
        start_dir = self._server_path if self._server_path else "C:\\"
        folder = QFileDialog.getExistingDirectory(
            self, "选择幻兽帕鲁服务端根目录", start_dir
        )
        if folder:
            self.server_path = folder
            self._check_executable()

    @pyqtSlot()
    def _on_toggle(self):
        if self._server_process.is_running():
            self._server_process.stop()
            self._btn_toggle.setEnabled(False)
            self._btn_toggle.setText("  正在关闭...")
            self._btn_toggle.setStyleSheet(BTN_STOPPING_QSS)
        else:
            self._start_server()

    def _start_server(self):
        if not self._server_path:
            QMessageBox.warning(self, "路径未设置", "请先设置服务端目录路径。")
            return

        exe = find_server_executable(self._server_path)
        if not exe:
            QMessageBox.critical(
                self, "找不到可执行文件",
                f"在指定路径中未找到 PalServer 可执行文件：\n{self._server_path}\n\n"
                "请确认已正确安装 Palworld Dedicated Server。"
            )
            return

        self._console.clear()
        self._append_console("正在启动服务端...\n")
        self._append_console(f"目录: {self._server_path}\n")
        self._append_console(f"可执行文件: {exe}\n")
        self._append_console("-" * 50 + "\n")

        self._btn_toggle.setEnabled(False)
        self._btn_toggle.setText("  正在启动...")
        self._btn_toggle.setStyleSheet(BTN_STARTING_QSS)

        self._server_process.start(self._server_path)

    @pyqtSlot()
    def _on_server_started(self):
        self._btn_toggle.setEnabled(True)
        self._btn_toggle.setText("  关闭服务器")
        self._btn_toggle.setStyleSheet(BTN_STOP_QSS)
        self._lbl_status.setText("●  运行中")
        self._lbl_status.setStyleSheet(STATUS_ONLINE_QSS)
        self._append_console("服务端已启动！\n")

    @pyqtSlot(int)
    def _on_server_stopped(self, exit_code: int):
        self._btn_toggle.setEnabled(True)
        self._btn_toggle.setText("  启动服务器")
        self._btn_toggle.setStyleSheet(BTN_START_QSS)
        self._lbl_status.setText("●  未运行")
        self._lbl_status.setStyleSheet(STATUS_OFFLINE_QSS)
        self._append_console(f"\n服务端已停止（退出码: {exit_code}）\n")
        self._check_executable()

    @pyqtSlot(str)
    def _on_server_output(self, text: str):
        self._append_console(text)

    @pyqtSlot(str)
    def _on_server_error(self, msg: str):
        self._append_console(f"[错误] {msg}\n")
        self._btn_toggle.setEnabled(True)
        self._btn_toggle.setText("  启动服务器")
        self._btn_toggle.setStyleSheet(BTN_START_QSS)
        self._lbl_status.setText("●  未运行")
        self._lbl_status.setStyleSheet(STATUS_OFFLINE_QSS)

    @pyqtSlot()
    def _on_browse_steamcmd(self):
        start_dir = os.path.dirname(self._steamcmd_path) if self._steamcmd_path else "C:\\"
        chosen, _ = QFileDialog.getOpenFileName(
            self, "选择 steamcmd.exe", start_dir,
            "steamcmd.exe (steamcmd.exe);;所有可执行文件 (*.exe)"
        )
        if chosen and os.path.isfile(chosen):
            self._steamcmd_path = chosen
            self._steamcmd_display.setText(chosen)
            self._steamcmd_display.setStyleSheet(PATH_FOUND_QSS)
            self._btn_update.setEnabled(True)

    @pyqtSlot()
    def _on_update_server(self):
        if self._server_process.is_running():
            reply = QMessageBox.question(
                self, "服务端正在运行",
                "检测到服务端正在运行。\n\n"
                "更新过程中建议先关闭服务端。\n"
                "是否先关闭服务端再继续更新？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._server_process.stop()
                self._append_console("正在关闭服务端以准备更新...\n")
                QMessageBox.information(
                    self, "请稍候",
                    "服务端正在关闭，请在控制台确认服务端已停止后，再点击一次「更新服务器」按钮。"
                )
                return

        if not self._steamcmd_path or not os.path.isfile(self._steamcmd_path):
            QMessageBox.warning(
                self, "找不到 steamcmd.exe",
                "未找到 steamcmd.exe。\n\n"
                "请确认：\n"
                "1. 已正确安装 SteamCMD\n"
                "2. 使用「手动定位」按钮指定 steamcmd.exe 的路径\n\n"
                "SteamCMD 下载地址：https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
            )
            return

        if self._updating:
            QMessageBox.warning(self, "更新进行中", "服务器更新已在运行中，请等待完成。")
            return

        self._updating = True
        self._btn_update.setEnabled(False)
        self._btn_update.setText("  正在更新...")
        self._btn_update.setStyleSheet(BTN_UPDATING_QSS)
        self._lbl_update_status.setText("SteamCMD 运行中...")
        self._lbl_update_status.setStyleSheet("font-size: 13px; color: #fbbf24; padding-left: 8px;")

        self._append_console("\n" + "=" * 60 + "\n")
        self._append_console("  SteamCMD 服务器更新\n")
        self._append_console("=" * 60 + "\n")
        self._append_console(f"steamcmd: {self._steamcmd_path}\n")
        self._append_console(f"app_id: {_PALSERVER_APP_ID}\n")
        self._append_console(f"install_dir: {self._get_install_dir()}\n")
        self._append_console("-" * 60 + "\n")

        args = [
            "+login", "anonymous",
            "+app_update", _PALSERVER_APP_ID, "validate",
            "+quit",
        ]

        install_dir = self._get_install_dir()
        if install_dir:
            args.insert(4, install_dir)
            args.insert(4, "+force_install_dir")

        self._append_console("执行命令:\n")
        self._append_console(f"  steamcmd.exe {' '.join(args)}\n")
        self._append_console("-" * 60 + "\n")

        self._update_process = QProcess(self)
        self._update_process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self._update_process.setWorkingDirectory(os.path.dirname(self._steamcmd_path))

        self._update_process.finished.connect(self._on_update_finished)
        self._update_process.errorOccurred.connect(self._on_update_error)
        self._update_process.readyReadStandardOutput.connect(self._on_update_output)

        self._update_process.start(self._steamcmd_path, args)

    @pyqtSlot(int, QProcess.ExitStatus)
    def _on_update_finished(self, exit_code: int, exit_status: QProcess.ExitStatus):
        self._updating = False
        self._btn_update.setEnabled(True)
        self._btn_update.setText("  更新服务器")
        self._btn_update.setStyleSheet(BTN_UPDATE_QSS)

        if exit_code == 0:
            self._lbl_update_status.setText("  更新完成")
            self._lbl_update_status.setStyleSheet("font-size: 13px; color: #4ade80; padding-left: 8px;")
            self._append_console("\n" + "=" * 60 + "\n")
            self._append_console("  服务器更新成功！\n")
            self._append_console("=" * 60 + "\n\n")
            if self._server_path:
                self._check_executable()
        else:
            self._lbl_update_status.setText(f"  更新失败（退出码: {exit_code}）")
            self._lbl_update_status.setStyleSheet("font-size: 13px; color: #f87171; padding-left: 8px;")
            self._append_console(f"\n  更新失败（退出码: {exit_code}）\n\n")

        self._cleanup_update_process()

    @pyqtSlot(QProcess.ProcessError)
    def _on_update_error(self, error: QProcess.ProcessError):
        self._updating = False
        error_msgs = {
            QProcess.ProcessError.FailedToStart: "无法启动 steamcmd.exe（文件缺失或权限不足）",
            QProcess.ProcessError.Crashed: "SteamCMD 进程崩溃",
            QProcess.ProcessError.Timedout: "SteamCMD 操作超时",
            QProcess.ProcessError.WriteError: "向 SteamCMD 写入失败",
            QProcess.ProcessError.ReadError: "从 SteamCMD 读取失败",
            QProcess.ProcessError.UnknownError: "SteamCMD 未知错误",
        }
        msg = error_msgs.get(error, f"未知错误代码: {error}")
        self._lbl_update_status.setText(f"  {msg}")
        self._lbl_update_status.setStyleSheet("font-size: 13px; color: #f87171; padding-left: 8px;")
        self._append_console(f"\n[SteamCMD 错误] {msg}\n")

        self._btn_update.setEnabled(True)
        self._btn_update.setText("  更新服务器")
        self._btn_update.setStyleSheet(BTN_UPDATE_QSS)
        self._cleanup_update_process()

    @pyqtSlot()
    def _on_update_output(self):
        if self._update_process is None:
            return
        data = self._update_process.readAllStandardOutput()
        try:
            text = bytes(data).decode("utf-8", errors="replace")
        except Exception:
            text = str(data)
        if text.strip():
            self._append_console(text)

    def _detect_steamcmd(self):
        if not self._server_path:
            return

        parent = Path(self._server_path)
        for _ in range(5):
            parent = parent.parent
            candidate = parent / "steamcmd.exe"
            if candidate.is_file():
                self._steamcmd_path = str(candidate)
                self._steamcmd_display.setText(self._steamcmd_path)
                self._steamcmd_display.setStyleSheet(PATH_FOUND_QSS)
                self._btn_update.setEnabled(True)
                return

        for p in _COMMON_STEAMCMD_PATHS:
            if os.path.isfile(p):
                self._steamcmd_path = p
                self._steamcmd_display.setText(p)
                self._steamcmd_display.setStyleSheet(PATH_FOUND_QSS)
                self._btn_update.setEnabled(True)
                return

        try:
            result = shutil.which("steamcmd")
            if result:
                self._steamcmd_path = result
                self._steamcmd_display.setText(result)
                self._steamcmd_display.setStyleSheet(PATH_FOUND_QSS)
                self._btn_update.setEnabled(True)
                return
        except Exception:
            pass

        self._steamcmd_path = ""
        self._steamcmd_display.setText("  未检测到 steamcmd.exe，请手动定位")
        self._steamcmd_display.setStyleSheet(PATH_ERROR_QSS)
        self._btn_update.setEnabled(False)

    def _get_install_dir(self) -> str:
        if not self._server_path:
            return ""
        pal_server = Path(self._server_path)
        common_dir = pal_server.parent
        steamapps_dir = common_dir.parent
        if steamapps_dir.name.lower() == "steamapps":
            return str(steamapps_dir.parent)
        return str(pal_server)

    def _check_executable(self):
        if not self._server_path:
            self._btn_toggle.setEnabled(False)
            self._lbl_exe_status.setText("")
            return

        exe = find_server_executable(self._server_path)
        if exe:
            self._lbl_exe_status.setText(f"  已找到可执行文件: {Path(exe).name}")
            self._lbl_exe_status.setStyleSheet("color: #4ade80; font-size: 12px; padding-left: 4px;")
            self._btn_toggle.setEnabled(True)
        else:
            self._lbl_exe_status.setText("  未找到 PalServer 可执行文件")
            self._lbl_exe_status.setStyleSheet("color: #f87171; font-size: 12px; padding-left: 4px;")
            self._btn_toggle.setEnabled(False)

    def _append_console(self, text: str):
        self._console.moveCursor(self._console.textCursor().MoveOperation.End)
        self._console.insertPlainText(text)
        scrollbar = self._console.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())

    def _cleanup_update_process(self):
        if self._update_process is not None:
            try:
                self._update_process.close()
            except Exception:
                pass
            self._update_process = None
