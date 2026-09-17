# Future Work

## ASM v0.3

### Attack Surface Graph

Visualize relationships between:

- Internet
- Routes
- Authentication
- Services
- Databases

### Service Mapping

Map:

Route
↓
Service
↓
Database

relationships.

---

## ASM v1.0

### Attack Path Generator

Generate:

Source
↓
Sink
↓
Potential Security Path

Examples:

req.body.url
↓
axios.get()

Potential SSRF Candidate

---

## ASM v2.0

### Reachability Analysis

Determine:

Can attacker-controlled data reach:

- exec()
- sql query
- file write
- outbound requests

---

## ASM v3.0

### Security Hypothesis Engine

Generate:

- SSRF hypotheses
- IDOR hypotheses
- SQLi hypotheses
- Authz hypotheses