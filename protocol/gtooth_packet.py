"""Dependency-free serializer for the proposed version-1 packet metadata."""

from __future__ import annotations

from dataclasses import dataclass
import struct

from gtooth.core import LinkState

_FORMAT = struct.Struct("!2sBBHHI6B")
_MAGIC = b"GT"
_VERSION = 1


@dataclass(frozen=True)
class GToothPacket:
    """Versioned metadata record; it does not contain or secure user payloads."""

    sequence: int
    node_id: int
    timestamp_ms: int
    state: LinkState

    def __post_init__(self) -> None:
        for value, name, maximum in (
            (self.sequence, "sequence", 0xFFFF),
            (self.node_id, "node_id", 0xFFFF),
            (self.timestamp_ms, "timestamp_ms", 0xFFFFFFFF),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
                raise ValueError(f"{name} must be an integer in [0, {maximum}]")
        if not isinstance(self.state, LinkState):
            raise ValueError("state must be a LinkState")

    def to_bytes(self) -> bytes:
        """Serialize in network (big-endian) byte order."""
        quantized = tuple(round(value * 255) for value in self.state.as_tuple())
        return _FORMAT.pack(
            _MAGIC,
            _VERSION,
            0,
            self.sequence,
            self.node_id,
            self.timestamp_ms,
            *quantized,
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> GToothPacket:
        """Parse exactly one supported metadata record."""
        if not isinstance(data, bytes) or len(data) != _FORMAT.size:
            raise ValueError(f"packet metadata must be exactly {_FORMAT.size} bytes")
        magic, version, flags, sequence, node_id, timestamp_ms, *values = _FORMAT.unpack(data)
        if magic != _MAGIC:
            raise ValueError("invalid packet magic")
        if version != _VERSION:
            raise ValueError(f"unsupported packet version: {version}")
        if flags != 0:
            raise ValueError("version 1 reserved flags must be zero")
        state = LinkState(*(value / 255.0 for value in values))
        return cls(sequence, node_id, timestamp_ms, state)
