# Attack Surface Mapper

Attack Surface Mapper (ASM) is an application understanding engine designed to help security agents understand a codebase before vulnerability discovery begins.

## Current Features

✅ Framework Detection

✅ Route Discovery

✅ Authentication Discovery

✅ External Service Discovery

✅ Attack Surface Report Generation

## Architecture

Repository

    ↓
Framework Detection

    ↓
Route Discovery

    ↓
Authentication Discovery

    ↓
Service Discovery

    ↓
Attack Surface Report

## Roadmap

Phase 1
- Framework Detection
- Route Discovery
- Auth Discovery
- Service Discovery

Phase 2
- Attack Path Generation

Phase 3
- Reachability Analysis

Phase 4
- Security Hypothesis Generation

## Example

python asm.py ./example/test-app

Output:

Framework: Express

Routes Found: 34

Admin Routes: 4

External Services:
- Stripe
- Redis
