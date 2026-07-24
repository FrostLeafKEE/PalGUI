import os
import re
from typing import Any

from app.config_schema import CONFIG_SCHEMA, ConfigType, get_defaults, get_item

DEFAULT_CONFIG_FILENAME = "DefaultPalWorldSettings.ini"


class ConfigError(Exception):
    pass


def _format_value(key: str, value: Any, item_type: ConfigType) -> str:
    if value is None:
        value = ""

    if item_type == ConfigType.BOOL:
        return "True" if value else "False"
    elif item_type == ConfigType.INT:
        return str(int(value))
    elif item_type == ConfigType.FLOAT:
        return f"{float(value):.6f}"
    elif item_type == ConfigType.ENUM:
        return str(value)
    elif item_type == ConfigType.STRING:
        s = str(value)
        s = s.replace('"', '\\"')
        return f'"{s}"'
    return str(value)


def _parse_value(key: str, raw: str, item_type: ConfigType) -> Any:
    raw = raw.strip()

    if item_type == ConfigType.BOOL:
        return raw.lower() == "true"
    elif item_type == ConfigType.INT:
        try:
            return int(raw)
        except ValueError:
            return 0
    elif item_type == ConfigType.FLOAT:
        try:
            return float(raw)
        except ValueError:
            return 0.0
    elif item_type == ConfigType.STRING:
        if raw.startswith('"') and raw.endswith('"'):
            return raw[1:-1]
        return raw
    elif item_type == ConfigType.ENUM:
        return raw
    return raw


def _extract_kv_pairs(content: str) -> dict[str, str]:
    raw_pairs: dict[str, str] = {}

    tokens = _split_kv(content)
    for token in tokens:
        token = token.strip()
        if not token or token.startswith(";"):
            continue
        idx = token.find("=")
        if idx == -1:
            continue
        key = token[:idx].strip()
        val = token[idx + 1:].strip()
        if key:
            raw_pairs[key] = val

    return raw_pairs


def _split_kv(text: str) -> list[str]:
    parts = []
    current = []
    depth = 0
    in_string = False
    for ch in text:
        if ch == '"':
            in_string = not in_string
            current.append(ch)
        elif ch == '(' and not in_string:
            depth += 1
            current.append(ch)
        elif ch == ')' and not in_string:
            depth -= 1
            current.append(ch)
        elif ch == ',' and depth == 0 and not in_string:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        remaining = "".join(current).strip()
        if remaining:
            parts.append(remaining)
    return parts


def read_config(filepath: str) -> dict[str, Any]:
    if os.path.basename(filepath).lower() == DEFAULT_CONFIG_FILENAME.lower():
        raise ConfigError(
            f"禁止读取默认示例配置文件 {DEFAULT_CONFIG_FILENAME}！\n"
            "该文件的更改不会反映到服务器上。\n"
            "请确保选择的路径指向 Pal/Saved/Config/WindowsServer/PalWorldSettings.ini"
        )

    defaults = get_defaults()

    if not os.path.exists(filepath):
        return defaults

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "OptionSettings=("
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return defaults

    pos = start_idx + len(start_marker)
    block_content = content[pos:]
    depth = 0
    end_idx = -1
    for i, ch in enumerate(block_content):
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth == 0:
                end_idx = i
                break
            depth -= 1

    if end_idx == -1:
        return defaults

    block = block_content[:end_idx]

    raw_pairs = _extract_kv_pairs(block)

    values = dict(defaults)
    for key, raw_val in raw_pairs.items():
        item = get_item(key)
        if item:
            values[key] = _parse_value(key, raw_val, item.config_type)
        else:
            values[key] = raw_val.strip('"')

    return values


def write_config(filepath: str, values: dict[str, Any]) -> None:
    if os.path.basename(filepath).lower() == DEFAULT_CONFIG_FILENAME.lower():
        raise ConfigError(
            f"禁止修改默认示例配置文件 {DEFAULT_CONFIG_FILENAME}！\n"
            "该文件的更改不会反映到服务器上。\n"
            "请确保选择的路径指向 Pal/Saved/Config/WindowsServer/PalWorldSettings.ini"
        )

    header_lines: list[str] = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing = f.read()
        header_marker = "[/Script/Pal.PalGameWorldSettings]"
        if header_marker in existing:
            header_lines = existing[:existing.index(header_marker)].rstrip().split("\n")
        else:
            opt_marker = "OptionSettings=("
            if opt_marker in existing:
                header_lines = existing[:existing.index(opt_marker)].rstrip().split("\n")

    lines: list[str] = []

    if not header_lines or all(l.strip().startswith(";") or not l.strip() for l in header_lines):
        if header_lines:
            lines.extend(header_lines)
        else:
            lines.append("; 幻兽帕鲁服务器配置文件")
            lines.append("; 由 PalGUI 开服管理工具自动生成")
            lines.append("")

    lines.append("[/Script/Pal.PalGameWorldSettings]")

    kv_pairs: list[str] = []
    for item in CONFIG_SCHEMA:
        value = values.get(item.key, item.default)
        formatted = _format_value(item.key, value, item.config_type)
        kv_pairs.append(f"{item.key}={formatted}")

    lines.append(f"OptionSettings=({','.join(kv_pairs)})")
    lines.append("")

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\r\n".join(lines))
