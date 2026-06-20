# two-site.md — Seam S2: Hangzhou ↔ Kunshan

> The highest-leverage seam. Two sites connected ONLY through the interface contract.
> **End-to-end process flow (with the full diagram):** see `dev-flow.md` — phases, parallel lines, gates W1/W2/W19.

## Geography
- **Hangzhou** — front-end (React/Lottie/ECharts) + back-end (state-machine/WebSocket/FastAPI) + **Mock service**.
- **Kunshan** — hardware-abstraction gateway (CAN FD ↔ MQTT) + hardware (9 mechanisms, sensors, 4 screens) + **IO table/protocol**.
- They meet only at the **interface contract** (amber layer). Hangzhou builds against Mock; Kunshan against real hardware.

## Architecture intent
Interface-driven, Mock-first, parallel development. Hangzhou starts ~4–6 weeks early against Mock; at W19+ real hardware just plugs into MQTT with **zero front/back-end code change** — *if* the contract was right.

## Three gates (PMO must watch)
| Gate | Week | Meaning |
|------|------|---------|
| **G1 — Mock start** | W1 | Hangzhou starts without waiting for hardware |
| **G2 — Contract freeze** | ~W2–3 | Three-party written sign-off. **The命门.** Changes after require both-site notice |
| **G3 — Real-hardware integration** | W22–26 | Real data into MQTT; "zero code change" = success |

## The four contracts to freeze at G2
1. **WebSocket message format** — health data fields, types, units. (back-end → front-end)
2. **Scene-trigger API** — S1–S4 triggers, reset, status. (back-end → embedded)
3. **IO table** — every signal name/type/address/range/CAN FD ID. (embedded → front+back)
4. **CAN FD protocol** — 9 mechanisms' command IDs, frame format, timing. (embedded → back-end)

## Three cross-site risks
1. **Contract drift** — one side changes, other doesn't know → change control (F2), both-site sign-off.
2. **Mock ≠ real hardware** — sync IO-table updates to Hangzhou's Mock; push for an early integration before W22.
3. **Geographic gap** — all cross-site Q&A written, traceable, visible to both (Bitable + Wiki), never lost in one site's chat.

## Maps to risks
R03 (multi-screen sync stability), R10 (voice in noise), and others with cross-site exposure.
