"""服务器配置可视化编辑器标签页。

功能：
- 根据 config_schema 动态生成分组的表单控件
- 从 PalWorldSettings.ini 读取当前配置值填充 UI
- 支持将所有修改写回配置文件（OptionSettings 格式）
- 绝对不修改 DefaultPalWorldSettings.ini
"""

import os
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.config_manager import read_config, write_config, ConfigError, DEFAULT_CONFIG_FILENAME
from app.config_schema import (
    CONFIG_SCHEMA,
    ConfigItem,
    ConfigType,
    get_defaults,
    get_groups,
)
from app.theme import BTN_SAVE_QSS, BTN_SECONDARY_QSS


class SettingsTab(QWidget):
    """设置编辑器标签页"""

    settings_saved = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._server_path: str = ""
        self._widgets: dict[str, QWidget] = {}
        self._values: dict[str, Any] = {}

        self._setup_ui()

    @property
    def server_path(self) -> str:
        return self._server_path

    @server_path.setter
    def server_path(self, path: str):
        self._server_path = path
        self._load_config()

    def load_config(self):
        self._load_config()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 20, 24, 20)

        info_row = QHBoxLayout()

        self._lbl_path = QLabel("服务器路径未设置")
        self._lbl_path.setStyleSheet("color: #6b6f8a; font-size: 12px; padding-left: 4px;")
        info_row.addWidget(self._lbl_path)

        info_row.addStretch()

        self._btn_reload = QPushButton("  重新加载")
        self._btn_reload.setToolTip("重新从配置文件读取当前设置")
        self._btn_reload.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_reload.setStyleSheet(BTN_SECONDARY_QSS)
        self._btn_reload.clicked.connect(self._load_config)
        self._btn_reload.setEnabled(False)
        info_row.addWidget(self._btn_reload)

        layout.addLayout(info_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._form_container = QWidget()
        self._form_layout = QVBoxLayout(self._form_container)
        self._form_layout.setSpacing(16)
        self._form_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self._form_container)
        layout.addWidget(scroll, 1)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()

        self._btn_save = QPushButton("  保存配置")
        self._btn_save.setMinimumHeight(48)
        self._btn_save.setMinimumWidth(200)
        self._btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_save.setStyleSheet(BTN_SAVE_QSS)
        self._btn_save.clicked.connect(self._on_save)
        self._btn_save.setEnabled(False)
        bottom_row.addWidget(self._btn_save)

        bottom_row.addStretch()
        layout.addLayout(bottom_row)

    def _load_config(self):
        self._widgets.clear()
        while self._form_layout.count():
            child = self._form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self._server_path:
            self._lbl_path.setText("服务器路径未设置 —— 请先在「服务器控制」标签页中设置路径")
            self._btn_save.setEnabled(False)
            self._btn_reload.setEnabled(False)
            return

        config_file = self._get_config_path()
        self._lbl_path.setText(f"配置文件: {config_file}")
        self._btn_reload.setEnabled(True)

        if os.path.basename(config_file).lower() == DEFAULT_CONFIG_FILENAME.lower():
            placeholder = QLabel(
                "  这是默认示例配置文件，更改它不会反映到服务器上！\n\n"
                "请前往「服务器控制」标签页设置正确的服务器路径。\n"
                "配置文件应位于: Pal/Saved/Config/WindowsServer/PalWorldSettings.ini"
            )
            placeholder.setStyleSheet("color: #fbbf24; font-size: 14px; padding: 24px;")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setWordWrap(True)
            self._form_layout.addWidget(placeholder)
            self._btn_save.setEnabled(False)
            return

        try:
            self._values = read_config(config_file)
        except ConfigError as e:
            self._show_error(str(e))
            return

        file_exists = os.path.exists(config_file)
        if not file_exists:
            notice = QLabel(
                "  配置文件尚不存在。\n"
                "系统将显示所有默认值。点击「保存配置」即可创建配置文件。"
            )
            notice.setStyleSheet("color: #7c9aff; font-size: 13px; padding: 8px;")
            notice.setWordWrap(True)
            self._form_layout.addWidget(notice)

        self._btn_save.setEnabled(True)

        for group_name in get_groups():
            group_items = [item for item in CONFIG_SCHEMA if item.group == group_name]
            if not group_items:
                continue

            group_box = QGroupBox(f"  {group_name}")
            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(10)

            for item in group_items:
                row = self._create_widget_row(item)
                group_layout.addLayout(row)

            self._form_layout.addWidget(group_box)

        self._form_layout.addStretch()

    def _create_widget_row(self, item: ConfigItem) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(14)

        label = QLabel(item.label_cn)
        label.setMinimumWidth(180)
        label.setMaximumWidth(220)
        label.setToolTip(item.description)
        label.setStyleSheet("font-size: 13px; font-weight: normal; color: #a5a8c0;")
        row.addWidget(label)

        value = self._values.get(item.key, item.default)
        widget = self._create_control(item, value)
        self._widgets[item.key] = widget
        row.addWidget(widget, 1)

        if item.config_type in (ConfigType.FLOAT, ConfigType.INT):
            val_label = QLabel()
            val_label.setMinimumWidth(60)
            val_label.setStyleSheet("color: #6b6f8a; font-size: 12px;")
            setattr(widget, "_val_label", val_label)
            self._connect_value_display(widget, val_label, item)
            row.addWidget(val_label)

            widget._item = item

        return row

    def _create_control(self, item: ConfigItem, value: Any) -> QWidget:
        if item.config_type == ConfigType.BOOL:
            cb = QCheckBox()
            cb.setChecked(bool(value))
            cb.setToolTip(item.description)
            return cb

        elif item.config_type == ConfigType.FLOAT:
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)

            spin = QDoubleSpinBox()
            spin.setDecimals(item.decimals)

            if item.min_val is not None:
                spin.setMinimum(item.min_val)
            else:
                spin.setMinimum(0.0)
            if item.max_val is not None:
                spin.setMaximum(item.max_val)
            else:
                spin.setMaximum(1000000.0)

            spin.setValue(float(value))
            spin.setSingleStep(item.step)
            spin.setToolTip(item.description)

            layout.addWidget(spin)

            if item.min_val is not None and item.max_val is not None and item.max_val <= 1000:
                slider = QSlider(Qt.Orientation.Horizontal)
                slider_min = int(item.min_val / item.step) if item.step > 0 else int(item.min_val)
                slider_max = int(item.max_val / item.step) if item.step > 0 else int(item.max_val)
                slider.setMinimum(slider_min)
                slider.setMaximum(slider_max)

                slider_val = int(float(value) / item.step)
                slider.setValue(slider_val)

                def make_float_slider_to_spin(s=spin, step=item.step, sl=slider):
                    def _sync(v):
                        s.blockSignals(True)
                        s.setValue(v * step)
                        s.blockSignals(False)
                    return _sync

                def make_float_spin_to_slider(sl=slider, step=item.step, sp=spin):
                    def _sync(v):
                        sl.blockSignals(True)
                        sl.setValue(int(v / step))
                        sl.blockSignals(False)
                    return _sync

                slider.valueChanged.connect(make_float_slider_to_spin())
                spin.valueChanged.connect(make_float_spin_to_slider())

                layout.addWidget(slider)

            return container

        elif item.config_type == ConfigType.INT:
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)

            spin = QSpinBox()
            if item.min_val is not None:
                spin.setMinimum(int(item.min_val))
            else:
                spin.setMinimum(0)
            if item.max_val is not None:
                spin.setMaximum(int(item.max_val))
            else:
                spin.setMaximum(999999)

            spin.setValue(int(value))
            spin.setSingleStep(int(item.step))
            spin.setToolTip(item.description)

            layout.addWidget(spin)

            if item.min_val is not None and item.max_val is not None and item.max_val <= 5000:
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setMinimum(int(item.min_val))
                slider.setMaximum(int(item.max_val))
                slider.setValue(int(value))

                def make_int_slider_to_spin(s=spin, sl=slider):
                    def _sync(v):
                        s.blockSignals(True)
                        s.setValue(v)
                        s.blockSignals(False)
                    return _sync

                def make_int_spin_to_slider(sl=slider, sp=spin):
                    def _sync(v):
                        sl.blockSignals(True)
                        sl.setValue(v)
                        sl.blockSignals(False)
                    return _sync

                slider.valueChanged.connect(make_int_slider_to_spin())
                spin.valueChanged.connect(make_int_spin_to_slider())
                layout.addWidget(slider)

            return container

        elif item.config_type == ConfigType.ENUM:
            combo = QComboBox()
            if item.options:
                combo.addItems(item.options)
            idx = combo.findText(str(value))
            if idx >= 0:
                combo.setCurrentIndex(idx)
            combo.setToolTip(item.description)
            return combo

        elif item.config_type == ConfigType.STRING:
            entry = QLineEdit()
            entry.setText(str(value) if value else "")
            entry.setToolTip(item.description)
            if item.password:
                entry.setEchoMode(QLineEdit.EchoMode.Password)
            return entry

        return QLineEdit()

    def _connect_value_display(
        self, container: QWidget, label: QLabel, item: ConfigItem
    ):
        spin = None
        if isinstance(container, QWidget):
            for child in container.findChildren((QSpinBox, QDoubleSpinBox)):
                spin = child
                break

        if spin is None:
            return

        def update_label(v):
            if item.config_type == ConfigType.FLOAT and item.decimals:
                label.setText(f"{float(v):.{item.decimals}f}")
            else:
                label.setText(str(v))

        spin.valueChanged.connect(update_label)
        update_label(spin.value())

    @pyqtSlot()
    def _on_save(self):
        if not self._server_path:
            QMessageBox.warning(self, "路径未设置", "请先在「服务器控制」标签页设置服务器路径。")
            return

        values: dict[str, Any] = {}
        for item in CONFIG_SCHEMA:
            widget = self._widgets.get(item.key)
            if widget is None:
                values[item.key] = item.default
                continue

            try:
                values[item.key] = self._get_widget_value(widget, item)
            except Exception as e:
                QMessageBox.critical(self, "数据收集错误", f"配置项 {item.key}: {e}")
                return

        config_file = self._get_config_path()
        try:
            write_config(config_file, values)
            self.settings_saved.emit(config_file)
            QMessageBox.information(
                self, "保存成功",
                f"配置已成功保存到：\n{config_file}\n\n"
                "请重启服务端以使更改生效。"
            )
        except ConfigError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"保存配置时出错：{e}")

    def _get_widget_value(self, widget: QWidget, item: ConfigItem) -> Any:
        if item.config_type == ConfigType.BOOL:
            if isinstance(widget, QCheckBox):
                return widget.isChecked()
            return widget.isChecked() if hasattr(widget, 'isChecked') else False

        elif item.config_type == ConfigType.FLOAT:
            for child in widget.findChildren(QDoubleSpinBox):
                return child.value()
            return float(widget.value()) if hasattr(widget, 'value') else item.default

        elif item.config_type == ConfigType.INT:
            for child in widget.findChildren(QSpinBox):
                return child.value()
            return int(widget.value()) if hasattr(widget, 'value') else item.default

        elif item.config_type == ConfigType.ENUM:
            if isinstance(widget, QComboBox):
                return widget.currentText()
            return widget.currentText() if hasattr(widget, 'currentText') else item.default

        elif item.config_type == ConfigType.STRING:
            if isinstance(widget, QLineEdit):
                return widget.text()
            return widget.text() if hasattr(widget, 'text') else item.default

        return item.default

    def _get_config_path(self) -> str:
        return os.path.join(
            self._server_path,
            "Pal", "Saved", "Config", "WindowsServer",
            "PalWorldSettings.ini"
        )

    def _show_error(self, msg: str):
        QMessageBox.critical(self, "错误", msg)
