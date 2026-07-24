"""简单的 RCON 客户端，用于连接 Palworld 服务器获取玩家列表等信息。

Palworld 使用 Source RCON 协议。
"""

import socket
import struct
from typing import Optional


class RconError(Exception):
    pass


class RconClient:
    def __init__(self, host: str, port: int, password: str, timeout: float = 5.0):
        self._host = host
        self._port = port
        self._password = password
        self._timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._request_id = 1

    def connect(self) -> None:
        if self._sock:
            return
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(self._timeout)
        try:
            self._sock.connect((self._host, self._port))
        except (ConnectionRefusedError, OSError) as e:
            self._sock.close()
            self._sock = None
            raise RconError(f"无法连接到 RCON {self._host}:{self._port} - {e}")

        self._send_packet(3, self._password.encode("utf-8"))
        response = self._recv_packet()
        if response is None or response[1] == -1:
            self.disconnect()
            raise RconError("RCON 认证失败，请检查密码")

    def disconnect(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def send_command(self, command: str) -> str:
        if not self._sock:
            self.connect()
        self._send_packet(2, command.encode("utf-8"))
        response = self._recv_packet()
        if response is None:
            raise RconError("RCON 无响应")
        if response[1] == -1:
            raise RconError("RCON 命令执行失败")
        return response[2].decode("utf-8", errors="replace")

    def _send_packet(self, packet_type: int, payload: bytes) -> None:
        if not self._sock:
            raise RconError("未连接到 RCON 服务器")
        request_id = self._request_id
        self._request_id += 1
        packet = struct.pack("<ii", request_id, packet_type) + payload + b"\x00\x00"
        length = struct.pack("<i", len(packet))
        self._sock.sendall(length + packet)

    def _recv_packet(self) -> Optional[tuple]:
        if not self._sock:
            return None
        try:
            length_data = self._recv_exact(4)
            if not length_data:
                return None
            length = struct.unpack("<i", length_data)[0]
            packet_data = self._recv_exact(length)
            if not packet_data:
                return None
            request_id, packet_type = struct.unpack("<ii", packet_data[:8])
            payload = packet_data[8:-2]
            return (request_id, packet_type, payload)
        except socket.timeout:
            return None
        except Exception:
            return None

    def _recv_exact(self, n: int) -> Optional[bytes]:
        data = b""
        while len(data) < n:
            try:
                chunk = self._sock.recv(n - len(data))
                if not chunk:
                    return None
                data += chunk
            except socket.timeout:
                return None
        return data
