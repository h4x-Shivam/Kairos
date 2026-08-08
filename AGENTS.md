# AGENTS.md — Project Engineering Rules & Architecture Governance
# Project: "When to Sell" Engine (Kairos Quant)
**Document Status:** Active Behavioral & Coding Standards  
**Scope:** Universal to all AI agents, engineers, and contributors working in this repository.

---

## 1. Core Project Rules & Behavioral Directives

1. **Never change architecture without asking.**
   - All system boundaries, mathematical scoring band thresholds, 2D Precedence Grids, database schemas, and API contracts defined in [PRD.md](file:///d:/Kairos/PRD.md), [TRD.md](file:///d:/Kairos/TRD.md), [UI_UX.md](file:///d:/Kairos/UI_UX.md), [APP_FLOW.md](file:///d:/Kairos/APP_FLOW.md), [BACKEND_SCHEMA.md](file:///d:/Kairos/BACKEND_SCHEMA.md), and [API.md](file:///d:/Kairos/API.md) are immutable unless explicitly approved by the User.
   - Any proposed architectural refactoring must be presented in an Implementation Plan before execution.

2. **Use TypeScript only.**
   - All frontend and full-stack client code must be strictly written in TypeScript (`.ts` / `.tsx`).
   - JavaScript (`.js` / `.jsx`) is strictly prohibited except for root configuration files (e.g. `postcss.config.js` or `tailwind.config.ts`).

3. **Never use `any`.**
   - Explicit typing is mandatory across all functions, components, API responses, and hooks.
   - Use `unknown` with runtime type narrowing / Zod schemas, or generic parameters (`<T>`) when dealing with dynamic or uncertain payloads.

4. **Follow Clean Architecture.**
   - Maintain strict separation of concerns across layers:
     - **Domain Layer:** Pure quant entities, math calculation formulas, and business rule state machines (framework-agnostic).
     - **Application / Use Case Layer:** Orchestrators, workflow handlers, and Server Actions.
     - **Infrastructure Layer:** Database repositories (SQLAlchemy/TimescaleDB), Redis adapters, external API clients (Yahoo Finance, NSE feed), and Razorpay SDK.
     - **Presentation Layer:** React/Next.js components, UI hooks, and terminal rendering views.

5. **Write reusable components.**
   - Build modular, composable, and single-responsibility components in `src/components/ui/` and `src/components/terminal/`.
   - Avoid monolithic page components; decompose layouts into granular presentation units (e.g., `TypographicVerdict`, `ChandelierChart`, `DiagnosticLedgerRow`, `TrimSimulator`).

6. **Keep files under 300 lines.**
   - No single source file (`.ts`, `.tsx`, `.py`, `.css`) should exceed 300 lines of code.
   - If a file approaches 300 lines, proactively decompose helper functions, sub-components, types, or utility modules into adjacent files.

7. **Always create tests.**
   - Unit tests are mandatory for all quant calculations (Wilder ATR, Chandelier Ratchet, 2D Precedence Grid weights, Kelly formula, tax math).
   - Component integration tests (Playwright / Vitest / React Testing Library) are mandatory for critical interactive flows (search autocomplete, mode switching, trim simulation).
   - Backend tests must use `pytest` with 100% coverage on math engine edge cases.

8. **Never expose API keys.**
   - All secret keys (`RAZORPAY_KEY_SECRET`, `JWT_SECRET`, database passwords, Redis URLs) must be loaded exclusively via environment variables (`.env.local` / backend config).
   - Never hardcode secrets in source code, commit history, or client-side bundles (`NEXT_PUBLIC_` is restricted strictly to public keys like `NEXT_PUBLIC_RAZORPAY_KEY_ID`).

9. **Use Tailwind CSS only.**
   - All styling must use Tailwind CSS utility classes aligned with the design tokens defined in [UI_UX.md](file:///d:/Kairos/UI_UX.md).
   - Avoid ad-hoc inline styles (`style={{...}}`) or detached CSS modules unless required for 3rd-party canvas integrations (e.g., TradingView Lightweight Charts).

10. **Always explain major changes.**
    - Provide a concise rationale before and after making non-trivial modifications, detailing how the changes align with the master specification and why specific implementation choices were made.

11. **Run lint before finishing.**
    - Always execute type-checking (`tsc --noEmit` / `mypy`) and linting (`npm run lint` / `ruff check .` / `flake8`) to verify zero errors before completing a task turn.

12. **Use Server Actions where possible.**
    - Leverage Next.js 15 Server Actions (`"use server"`) for form submissions, user preferences, watchlist updates, and authenticated server-side mutations to minimize unnecessary client-side boilerplate.

13. **Follow the existing folder structure.**
    - Respect established repository conventions and directory hierarchies for both `kairos-web` (Next.js) and `kairos-engine` (FastAPI).

---

## 2. Standard Workspace Directory Structure

```
d:/Kairos/
├── PRD.md                  # Product Requirements Document
├── TRD.md                  # Technical Requirements Document
├── UI_UX.md                # UI/UX Design Specification & Terminal Architecture
├── APP_FLOW.md             # Application Flow & User Journey Architecture
├── BACKEND_SCHEMA.md       # Database DDL, TimescaleDB, Redis & Pydantic Contracts
├── API.md                  # RESTful & WebSocket API Contracts
├── AGENTS.md               # Project Rules & Engineering Standards (This file)
│
├── kairos-web/             # Next.js 15 (React 19) Frontend Application
│   ├── src/
│   │   ├── app/            # App Router (Pages, Layouts, Server Actions)
│   │   │   ├── (marketing)/# Landing Hero & Proof Ledgers
│   │   │   ├── diagnostic/ # Terminal Dashboard & Staged Loading Stream
│   │   │   ├── api/        # Next.js Edge / BFF Proxy Routes
│   │   │   └── actions/    # Server Actions (Watchlist, Preferences)
│   │   ├── components/     # Clean Architecture Component Hierarchy
│   │   │   ├── ui/         # Base UI Elements (Buttons, Inputs, Modals)
│   │   │   ├── terminal/   # Terminal-Specific Elements (Ledger, Verdict, Proof)
│   │   │   └── charts/     # TradingView Chandelier Canvas Components
│   │   ├── hooks/          # Custom React Hooks (useStockSearch, useHorizonMode)
│   │   ├── lib/            # Utilities, API Client, Formatters, Constants
│   │   └── types/          # Strict TypeScript Type Definitions & Interfaces
│   ├── tailwind.config.ts  # Tailwind Design Tokens (Colors, Typography, Borders)
│   └── package.json
│
└── kairos-engine/          # FastAPI & Python Quant Math Backend
    ├── app/
    │   ├── api/            # API Route Handlers (v1 Routers)
    │   ├── core/           # Config, Redis Pool, Database Session, Security
    │   ├── engine/         # Pure Quant Math & Conflict Resolution State Machine
    │   ├── models/         # SQLAlchemy 2.0 ORM Models & TimescaleDB Hypertables
    │   ├── schemas/        # Pydantic v2 Serialization Contracts
    │   └── services/       # Upstream Market Data Ingestion & FinBERT Worker
    ├── tests/              # Pytest Math & API Integration Test Suite
    ├── alembic/            # Database Migrations
    └── requirements.txt
```

---

## 3. Code Quality & Formatting Checklist

Before submitting code or declaring a feature complete, verify:
- [ ] TypeScript: `tsc --noEmit` returns **0 errors**.
- [ ] ESLint: `npm run lint` returns **0 warnings / 0 errors**.
- [ ] Python: `ruff check .` / `mypy` returns **clean status**.
- [ ] File Length: All modified/created files are **under 300 lines**.
- [ ] Accessibility & Contrast: Colors strictly adhere to WCAG 2.1 AA tokens (`--text-disclaimer` $\ge 7.5:1$, `--bg-obsidian` `#07090E`).
- [ ] Zero `any` types present in TypeScript codebase.
- [ ] All tests pass: `pytest` and `npm test`.

---
*Maintained under Kairos Quant Engineering Standards.*
