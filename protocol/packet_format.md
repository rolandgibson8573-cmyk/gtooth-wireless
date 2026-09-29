# Proposed Packet Metadata Format

**Status: proposed, version 1.** This is a compact metadata record for experimentation, not a complete packet protocol. It carries no user payload, provides no encryption/authentication, and is not a claim of a fixed overhead for any radio frame.

## Version-1 layout

All multibyte integers use network byte order (big-endian). The record is exactly 18 bytes:

| Offset | Size | Type | Field | Meaning |
| ---: | ---: | --- | --- | --- |
| 0 | 2 | bytes | Magic | ASCII `GT` |
| 2 | 1 | uint8 | Version | `1` |
| 3 | 1 | uint8 | Flags | Reserved; must be zero in v1 |
| 4 | 2 | uint16 | Sequence | Sender packet sequence, wraps modulo \(2^{16}\) |
| 6 | 2 | uint16 | Node ID | Sender-assigned identifier; uniqueness is deployment-managed |
| 8 | 4 | uint32 | Timestamp ms | Sender monotonic milliseconds modulo \(2^{32}\) |
| 12 | 6 | uint8[6] | State | Quantized scalars in the LinkState order below |

Scalar order: link quality, freshness, stability, path quality, gateway contribution, resource score. Each normalized \(v\in[0,1]\) is encoded as the nearest integer to \(255v\); decoding maps byte \(q\) to \(q/255\). The conversion is lossy, with a maximum ideal quantization error of \(1/(2\cdot255)\), before floating representation.

Timestamp age is meaningful only under a defined sender/receiver clock basis. A monotonic sender timestamp alone is not comparable across unsynchronized devices. If modular subtraction is used, the age must be unambiguous and less than \(2^{31}\) milliseconds; deployments must define wrap, reset, and reboot handling. Sequence numbers likewise wrap; they are metadata, not guaranteed replay protection.

## Compatibility and evolution

Reject unknown versions rather than misinterpreting fields. V1 readers reject nonzero reserved flags. Any incompatible layout change requires a new version and a documented migration/negotiation policy. A transport must safely distinguish metadata from application payload. Do not append fields to v1 and assume old readers will skip them.

The record's 18-byte application-level size excludes lower-layer headers, framing, checksum, retransmission, padding, and security overhead. Measure actual airtime/overhead in the target transport before making efficiency claims. Implementations may omit this proposal entirely if overhead or compatibility requirements make it unsuitable.

## Python helper

`protocol/gtooth_packet.py` supplies a dependency-free `GToothPacket` dataclass with range validation and exact-length round-trip serialization for this proposal.
