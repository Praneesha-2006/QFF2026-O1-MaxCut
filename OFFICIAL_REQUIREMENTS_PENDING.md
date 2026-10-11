# Benchmark definitions and remaining assumptions

This study uses the five-node Processor A graph and all nine visible nodes of the Processor B graph illustrated in the supplied challenge guideline. The Processor B slide caption says seven qubits, so the reconstruction explicitly uses nine drawn nodes and records all assigned edge IDs in `TOPOLOGY_9Q_README.md`.

The supplied documents do not provide a separate machine-readable coupling map or device calibration data. Accordingly, native gates (`rz`, `sx`, `x`, `cx`), bidirectional CX, synthetic noise rates and fixed initial placement are documented participant modeling choices rather than official hardware calibrations.

The four graph JSON inputs are selected benchmark instances; no unique O1 graph input is specified in the supplied materials. The code is evaluated using Qiskit Aer simulation.

Still verify any later-issued repository naming/template instructions, submission portal requirements, deadline, and AI/LLM disclosure rules. The benchmark is an architecture-aware simulation rather than a claim of exact calibrated IBM hardware reproduction.
