import pytest

from gtooth.core import LinkState
from protocol.gtooth_packet import GToothPacket


def test_packet_round_trip_and_compact_size() -> None:
    packet = GToothPacket(
        sequence=17,
        node_id=513,
        timestamp_ms=1_234_567,
        state=LinkState(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    )
    encoded = packet.to_bytes()
    decoded = GToothPacket.from_bytes(encoded)
    assert len(encoded) == 18
    assert decoded.sequence == packet.sequence
    assert decoded.node_id == packet.node_id
    assert decoded.timestamp_ms == packet.timestamp_ms
    assert decoded.state.as_tuple() == pytest.approx(packet.state.as_tuple(), abs=1 / 255)


@pytest.mark.parametrize(
    "update",
    [
        {"sequence": -1},
        {"node_id": 65536},
        {"timestamp_ms": 2**32},
    ],
)
def test_packet_fields_are_range_checked(update: dict[str, int]) -> None:
    fields = {
        "sequence": 0,
        "node_id": 1,
        "timestamp_ms": 100,
        "state": LinkState(0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
    }
    fields.update(update)
    with pytest.raises(ValueError):
        GToothPacket(**fields)


@pytest.mark.parametrize(
    "payload",
    [
        b"",
        b"NO" + bytes(16),
        b"GT" + bytes([2, 0]) + bytes(14),
        b"GT" + bytes([1, 1]) + bytes(14),
    ],
)
def test_packet_parser_rejects_invalid_records(payload: bytes) -> None:
    with pytest.raises(ValueError):
        GToothPacket.from_bytes(payload)
