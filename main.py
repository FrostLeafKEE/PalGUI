"""幻兽帕鲁（Palworld）开服管理 GUI 工具 —— 入口文件。

用法：
    python main.py

依赖：
    pip install -r requirements.txt
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QStyleFactory

from app.main_window import MainWindow


def main():
    # 启用高 DPI 支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("PalworldServerManager")
    app.setApplicationDisplayName("幻兽帕鲁开服管理工具")
    app.setOrganizationName("PalGUI")

    # 使用 Fusion 风格作为基底（跨平台一致性）
    app.setStyle(QStyleFactory.create("Fusion"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
