"""全局主题样式表 —— 现代暗色主题（高级版）。

色彩体系：
  - 主背景: #0f1117       深邃黑
  - 次级背景: #181a24     微亮
  - 卡片面板: #1e2030     面板色
  - 卡片悬浮: #252840     微亮
  - 输入框: #161825
  - 边框: #2e3148
  - 边框亮色: #3d4060
  - 文字主色: #e2e4f0
  - 文字次级: #8b8fa8
  - 文字三级: #5c6080
  - 强调色: #7c9aff       冰蓝
  - 强调色悬浮: #6889f0
  - 强调色暗: #4c6ad8
  - 成功: #4ade80
  - 警告: #fbbf24
  - 危险: #f87171
  - 渐变起点: #6366f1     靛蓝
  - 渐变终点: #8b5cf6     紫罗兰
"""

FUSION_QSS = """
/* ============================================================
   整体框架
   ============================================================ */
QMainWindow {
    background-color: #0f1117;
}
QWidget#centralWidget {
    background-color: #0f1117;
}
QWidget {
    background-color: transparent;
    color: #e2e4f0;
    font-family: "Microsoft YaHei", "Segoe UI", "Noto Sans SC", "PingFang SC", sans-serif;
    font-size: 13px;
}
QWidget:disabled {
    color: #4a4e68;
}

/* ============================================================
   标签页（Tab）—— 磨砂玻璃风格
   ============================================================ */
QTabWidget::pane {
    border: none;
    background-color: #0f1117;
    top: -1px;
}
QTabBar {
    background-color: #13151f;
    border-bottom: 1px solid #2e3148;
}
QTabBar::tab {
    background-color: transparent;
    color: #6b6f8a;
    padding: 14px 32px;
    margin: 0;
    margin-bottom: -1px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    border-bottom: 3px solid transparent;
}
QTabBar::tab:selected {
    color: #7c9aff;
    border-bottom: 3px solid #7c9aff;
    background-color: transparent;
}
QTabBar::tab:hover:!selected {
    color: #a5a8c0;
    border-bottom: 3px solid #3d4060;
}

/* ============================================================
   分组框（GroupBox）—— 卡片风格
   ============================================================ */
QGroupBox {
    background-color: #181a24;
    border: 1px solid #2e3148;
    border-radius: 12px;
    margin-top: 20px;
    padding: 28px 20px 16px 20px;
    font-weight: 600;
    font-size: 14px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 12px;
    color: #a5a8c0;
    background-color: #181a24;
    border: none;
    border-radius: 4px;
    top: 0px;
    left: 14px;
    font-size: 13px;
}

/* ============================================================
   按钮 —— 通用
   ============================================================ */
QPushButton {
    background-color: #252840;
    color: #e2e4f0;
    border: none;
    border-radius: 8px;
    padding: 9px 20px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #303458;
}
QPushButton:pressed {
    background-color: #1e2038;
}
QPushButton:disabled {
    background-color: #1a1c2a;
    color: #4a4e68;
}

/* ============================================================
   文本框 / 输入框
   ============================================================ */
QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QPlainTextEdit {
    background-color: #161825;
    color: #e2e4f0;
    border: 1px solid #2e3148;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: #4c6ad8;
    selection-color: #ffffff;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
    border: 1px solid #7c9aff;
}
QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled {
    background-color: #13151f;
    color: #4a4e68;
}
QLineEdit[readOnly="true"] {
    background-color: #161825;
    color: #a5a8c0;
}

QTextEdit, QPlainTextEdit {
    background-color: #0c0e16;
    border: 1px solid #2e3148;
    border-radius: 10px;
    padding: 12px 14px;
    color: #e2e4f0;
}

/* ============================================================
   下拉框（ComboBox）
   ============================================================ */
QComboBox {
    background-color: #161825;
    color: #e2e4f0;
    border: 1px solid #2e3148;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    min-height: 24px;
}
QComboBox:focus, QComboBox:hover {
    border: 1px solid #7c9aff;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #2e3148;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}
QComboBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6b6f8a;
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #1e2030;
    color: #e2e4f0;
    border: 1px solid #2e3148;
    border-radius: 8px;
    padding: 6px;
    selection-background-color: #252840;
    selection-color: #7c9aff;
    outline: none;
}
QComboBox:disabled {
    background-color: #13151f;
    color: #4a4e68;
}

/* ============================================================
   复选框（CheckBox）
   ============================================================ */
QCheckBox {
    spacing: 10px;
    font-size: 13px;
    color: #e2e4f0;
}
QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 5px;
    border: 2px solid #3d4060;
    background-color: #161825;
}
QCheckBox::indicator:checked {
    background-color: #7c9aff;
    border: 2px solid #7c9aff;
}
QCheckBox::indicator:checked:hover {
    background-color: #6889f0;
    border: 2px solid #6889f0;
}
QCheckBox::indicator:hover {
    border: 2px solid #7c9aff;
}
QCheckBox::indicator:disabled {
    background-color: #13151f;
    border: 2px solid #2e3148;
}

/* ============================================================
   滑块（QSlider）
   ============================================================ */
QSlider::groove:horizontal {
    height: 6px;
    background-color: #252840;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background-color: #7c9aff;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
    border: 2px solid #6889f0;
}
QSlider::handle:horizontal:hover {
    background-color: #6889f0;
    border: 2px solid #7c9aff;
}
QSlider::sub-page:horizontal {
    background-color: #7c9aff;
    border-radius: 3px;
}
QSlider::add-page:horizontal {
    background-color: #252840;
    border-radius: 3px;
}
QSlider:disabled {
    opacity: 0.5;
}

/* ============================================================
   滚动条 —— 超细风格
   ============================================================ */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    border: none;
    border-radius: 4px;
    margin: 4px 0;
}
QScrollBar::handle:vertical {
    background-color: #2e3148;
    min-height: 30px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background-color: #4a4e68;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
    background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    border: none;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background-color: #2e3148;
    min-width: 30px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #4a4e68;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
    background: none;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

/* ============================================================
   数值控件（SpinBox 的上下箭头）
   ============================================================ */
QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #2e3148;
    border-bottom: 1px solid #2e3148;
    border-top-right-radius: 8px;
    background-color: #1e2030;
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 24px;
    border-left: 1px solid #2e3148;
    border-bottom-right-radius: 8px;
    background-color: #1e2030;
}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    width: 8px;
    height: 8px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid #6b6f8a;
}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    width: 8px;
    height: 8px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #6b6f8a;
}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #252840;
}

/* ============================================================
   提示框（ToolTip）
   ============================================================ */
QToolTip {
    background-color: #1e2030;
    color: #e2e4f0;
    border: 1px solid #7c9aff;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
}

/* ============================================================
   消息框（QMessageBox）
   ============================================================ */
QMessageBox {
    background-color: #181a24;
}
QMessageBox QLabel {
    color: #e2e4f0;
    font-size: 13px;
}

/* ============================================================
   嵌套分组框
   ============================================================ */
QGroupBox QGroupBox {
    background-color: #13151f;
    border: 1px solid #252840;
    border-radius: 8px;
    margin-top: 16px;
    padding: 22px 14px 12px 14px;
}
QGroupBox QGroupBox::title {
    background-color: #13151f;
    top: 0px;
    left: 10px;
}

/* ============================================================
   ScrollArea 内部
   ============================================================ */
QScrollArea {
    border: none;
    background: transparent;
}

/* ============================================================
   标签页内容区域
   ============================================================ */
QWidget#tabContent {
    background-color: #0f1117;
}

/* ============================================================
   状态栏
   ============================================================ */
QStatusBar {
    background-color: #13151f;
    border-top: 1px solid #2e3148;
    color: #6b6f8a;
    font-size: 12px;
    padding: 2px 8px;
}
QStatusBar::item {
    border: none;
}
QStatusBar QLabel {
    color: #6b6f8a;
    font-size: 12px;
    padding: 0 4px;
}

/* ============================================================
   标签（QLabel）
   ============================================================ */
QLabel {
    background-color: transparent;
}

/* ============================================================
   框架（QFrame）
   ============================================================ */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #2e3148;
}
"""

CONSOLE_QSS = """
QTextEdit {
    background-color: #0a0c14;
    color: #c8ccd8;
    border: 1px solid #2e3148;
    border-radius: 10px;
    padding: 14px 16px;
    font-family: "Cascadia Code", "JetBrains Mono", "Fira Code", "Consolas", monospace;
    font-size: 13px;
    selection-background-color: #4c6ad8;
    selection-color: #ffffff;
}
"""

STATUS_ONLINE_QSS = """
QLabel {
    color: #4ade80;
    font-size: 14px;
    font-weight: bold;
    padding-left: 8px;
}
"""

STATUS_OFFLINE_QSS = """
QLabel {
    color: #6b6f8a;
    font-size: 14px;
    font-weight: bold;
    padding-left: 8px;
}
"""

STATUS_ERROR_QSS = """
QLabel {
    color: #f87171;
    font-size: 14px;
    font-weight: bold;
    padding-left: 8px;
}
"""

BTN_START_QSS = """
QPushButton {
    background-color: #166534;
    color: #4ade80;
    border: 1px solid #22c55e;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 700;
    padding: 12px 32px;
}
QPushButton:hover {
    background-color: #15803d;
    color: #86efac;
    border: 1px solid #4ade80;
}
QPushButton:pressed {
    background-color: #14532d;
}
QPushButton:disabled {
    background-color: #1a1c2a;
    color: #4a4e68;
    border: 1px solid #2e3148;
}
"""

BTN_STOP_QSS = """
QPushButton {
    background-color: #7f1d1d;
    color: #f87171;
    border: 1px solid #ef4444;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 700;
    padding: 12px 32px;
}
QPushButton:hover {
    background-color: #991b1b;
    color: #fca5a5;
    border: 1px solid #f87171;
}
QPushButton:pressed {
    background-color: #450a0a;
}
QPushButton:disabled {
    background-color: #1a1c2a;
    color: #4a4e68;
    border: 1px solid #2e3148;
}
"""

BTN_STARTING_QSS = """
QPushButton {
    background-color: #78350f;
    color: #fbbf24;
    border: 1px solid #f59e0b;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 700;
    padding: 12px 32px;
}
QPushButton:disabled {
    background-color: #78350f;
    color: #d97706;
    border: 1px solid #b45309;
}
"""

BTN_STOPPING_QSS = """
QPushButton {
    background-color: #78350f;
    color: #fbbf24;
    border: 1px solid #f59e0b;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 700;
    padding: 12px 32px;
}
QPushButton:disabled {
    background-color: #78350f;
    color: #d97706;
    border: 1px solid #b45309;
}
"""

BTN_UPDATE_QSS = """
QPushButton {
    background-color: #312e81;
    color: #a5b4fc;
    border: 1px solid #6366f1;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    padding: 10px 28px;
}
QPushButton:hover {
    background-color: #3730a3;
    color: #c7d2fe;
    border: 1px solid #818cf8;
}
QPushButton:pressed {
    background-color: #1e1b4b;
}
QPushButton:disabled {
    background-color: #1a1c2a;
    color: #4a4e68;
    border: 1px solid #2e3148;
}
"""

BTN_UPDATING_QSS = """
QPushButton {
    background-color: #312e81;
    color: #a5b4fc;
    border: 1px solid #6366f1;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    padding: 10px 28px;
}
QPushButton:disabled {
    background-color: #312e81;
    color: #6366f1;
    border: 1px solid #4338ca;
}
"""

BTN_SECONDARY_QSS = """
QPushButton {
    background-color: #1e2030;
    color: #a5a8c0;
    border: 1px solid #2e3148;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #252840;
    border: 1px solid #3d4060;
    color: #e2e4f0;
}
QPushButton:pressed {
    background-color: #161825;
}
QPushButton:disabled {
    background-color: #13151f;
    color: #4a4e68;
    border: 1px solid #2e3148;
}
"""

BTN_SAVE_QSS = """
QPushButton {
    background-color: #312e81;
    color: #a5b4fc;
    border: 1px solid #6366f1;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 700;
    padding: 12px 36px;
}
QPushButton:hover {
    background-color: #3730a3;
    color: #c7d2fe;
    border: 1px solid #818cf8;
}
QPushButton:pressed {
    background-color: #1e1b4b;
}
QPushButton:disabled {
    background-color: #1a1c2a;
    color: #4a4e68;
    border: 1px solid #2e3148;
}
"""

PATH_DISPLAY_QSS = """
QLineEdit {
    background-color: #13151f;
    color: #a5a8c0;
    border: 1px solid #2e3148;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    font-family: "Cascadia Code", "Consolas", monospace;
}
"""

PATH_FOUND_QSS = """
QLineEdit {
    background-color: #13151f;
    color: #4ade80;
    border: 1px solid #166534;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    font-family: "Cascadia Code", "Consolas", monospace;
}
"""

PATH_ERROR_QSS = """
QLineEdit {
    background-color: #13151f;
    color: #f87171;
    border: 1px solid #7f1d1d;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    font-family: "Cascadia Code", "Consolas", monospace;
}
"""
