"""幻兽帕鲁服务端进程管理。

使用 QProcess 实现异步、非阻塞的服务端启动与关闭。
提供信号机制让 UI 层响应进程状态变化。
"""

import os
from pathlib import Path

from PyQt6.QtCore import QObject, QProcess, pyqtSignal, pyqtSlot


# PalServer 可执行文件名候选列表
_PALSERVER_CANDIDATES = [
    "PalServer.exe",
    "PalServer-Win64-Test-Cmd.exe",
    "PalServer-Win64-Shipping-Cmd.exe",
    "PalServer.sh",          # Linux
]


class ServerProcess(QObject):
    """管理幻兽帕鲁服务端子进程的生命周期。

    信号：
        started: 服务器成功启动
        stopped(int): 服务器已停止，参数为退出码
        output_received(str): 服务器标准输出
        error_occurred(str): 发生错误
        state_changed(bool): 运行状态改变（True=运行中）
    """

    started = pyqtSignal()
    stopped = pyqtSignal(int)       # exit_code
    output_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    state_changed = pyqtSignal(bool)  # is_running

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._process: QProcess | None = None
        self._running = False

    # ---- 公开属性 ----

    def is_running(self) -> bool:
        """返回服务端是否正在运行"""
        return self._running

    # ---- 启动 ----

    def start(self, server_dir: str) -> None:
        """启动服务端。

        Args:
            server_dir: 服务器根目录（包含 PalServer.exe 的目录）
        """
        if self._running:
            self.error_occurred.emit("服务端已在运行中")
            return

        # 查找可执行文件
        executable = _find_executable(server_dir)
        if not executable:
            self.error_occurred.emit(
                f"在目录中未找到 PalServer 可执行文件:\n{server_dir}\n\n"
                "请确认已通过 SteamCMD 正确安装了 Palworld Dedicated Server。"
            )
            return

        # 创建 QProcess
        self._process = QProcess(self)
        self._process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self._process.setWorkingDirectory(server_dir)

        # 连接信号
        self._process.started.connect(self._on_started)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self._process.readyReadStandardOutput.connect(self._on_ready_read)

        # 启动（可添加额外参数如 -port=8211）
        self._process.start(executable, [])

    # ---- 停止 ----

    def stop(self) -> None:
        """优雅地停止服务端。

        策略：
        1. 先发送 terminate()（相当于 WM_CLOSE / SIGTERM）
        2. 等待 5 秒
        3. 如果仍未退出，发送 kill()
        4. 再等待 2 秒
        5. 如果仍未退出，强制终止
        """
        if not self._running or self._process is None:
            return

        # 优雅终止
        self._process.terminate()

        # 5 秒后检查，如果没退出则强杀
        if not self._process.waitForFinished(5000):
            self._process.kill()
            if not self._process.waitForFinished(2000):
                # 极端情况：强制关闭
                self._process.close()
                self._on_stopped(-1)

    # ---- 内部槽函数 ----

    @pyqtSlot()
    def _on_started(self):
        self._running = True
        self.state_changed.emit(True)
        self.started.emit()

    @pyqtSlot(int, QProcess.ExitStatus)
    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus):
        self._running = False
        self.state_changed.emit(False)
        self.stopped.emit(exit_code)
        self._cleanup()

    @pyqtSlot(QProcess.ProcessError)
    def _on_error(self, error: QProcess.ProcessError):
        error_msgs = {
            QProcess.ProcessError.FailedToStart: "无法启动服务端进程（可执行文件缺失或权限不足）",
            QProcess.ProcessError.Crashed: "服务端进程崩溃",
            QProcess.ProcessError.Timedout: "服务端进程操作超时",
            QProcess.ProcessError.WriteError: "向服务端进程写入失败",
            QProcess.ProcessError.ReadError: "从服务端进程读取失败",
            QProcess.ProcessError.UnknownError: "服务端进程发生未知错误",
        }
        msg = error_msgs.get(error, f"未知错误代码: {error}")
        self.error_occurred.emit(msg)
        self._running = False
        self.state_changed.emit(False)
        self._cleanup()

    @pyqtSlot()
    def _on_ready_read(self):
        if self._process is None:
            return
        data = self._process.readAllStandardOutput()
        try:
            text = bytes(data).decode("utf-8", errors="replace")
        except Exception:
            text = str(data)
        if text.strip():
            self.output_received.emit(text)

    def _on_stopped(self, exit_code: int):
        self._running = False
        self.state_changed.emit(False)
        self.stopped.emit(exit_code)
        self._cleanup()

    def _cleanup(self):
        if self._process is not None:
            try:
                self._process.close()
            except Exception:
                pass
            self._process = None


def _find_executable(server_dir: str) -> str | None:
    """在服务器目录中查找 PalServer 可执行文件"""
    server_path = Path(server_dir)
    if not server_path.is_dir():
        return None

    for candidate in _PALSERVER_CANDIDATES:
        exe_path = server_path / candidate
        if exe_path.is_file():
            return str(exe_path)

    # 在子目录中也搜索一下（某些安装方式可能把 exe 放在 bin 子目录）
    for candidate in _PALSERVER_CANDIDATES:
        for found in server_path.rglob(candidate):
            if found.is_file():
                return str(found)

    return None


def find_server_executable(server_dir: str) -> str | None:
    """公开的辅助函数：在给定目录中查找 PalServer 可执行文件"""
    return _find_executable(server_dir)
