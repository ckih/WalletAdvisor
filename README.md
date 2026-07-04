# Autonomous Financial Adviser (AFA) - Phase 1 MVP

A conversational, AI-driven financial planning platform for retail investors.

## Architecture Overview

- **Backend:** FastAPI (Python) - REST API, JWT Auth, AES-256 Encryption.
- **Frontend:** Next.js (TypeScript) - Tailwind CSS, Shadcn/UI.
- **AI:** Anthropic Claude (via API) for conversational advice; Rules-based Risk Scorer (PyTorch compatible).
- **Database:** PostgreSQL (Data), Redis (Cache/Session).
- **Events:** Apache Kafka (Internal events like goal creation).
- **Deployment:** Docker Compose (Local) and Kubernetes (Production).

## Setup Instructions

### Local Development (Docker Compose)

1. **Prerequisites:** Docker and Docker Compose installed.
2. **Environment Variables:** Create a `.env` file in the root or set in `docker-compose.yml`:
   - `ANTHROPIC_API_KEY`: Your Anthropic API Key.
   - `SECRET_KEY`: Random string for JWT.
   - `ENCRYPTION_KEY`: AES-256 key (generated if not provided).
3. **Run:**
   ```bash
   docker compose up -d
   ```
4. **Seed Data:**
   ```bash
   # In the backend container or local venv
   python scripts/seed_data.py
   ```
5. **Access:**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

### Kubernetes Deployment

1. Manifests are located in `infra/k8s/`.
2. Apply them to your cluster:
   ```bash
   kubectl apply -f infra/k8s/
   ```
3. *Note:* You will need to configure Ingress and StorageClasses based on your cloud provider (GKE/EKS/etc.).

## Features Implemented

1. **Onboarding & Risk Profiler:** Rules-based engine with explainability.
2. **Goal Planner:** Roadmap generation and "what-if" scenarios.
3. **AI Chat Adviser:** Context-aware chat with Claude, including audit logging.
4. **Dashboard:** Visual summary of net worth, goals, and risk profile.

## Limitations & Deferred Features (Phase 1)

- No live bank integrations (Mock data used).
- No real market data or live trading.
- Risk Scorer is rules-based (Phase 2 will use a trained ML model).
- Kubernetes manifests are cloud-agnostic; require provider-specific ingress tuning.

## Security

- JWT-based Auth.
- Bcrypt password hashing.
- AES-256 encryption for sensitive fields (income, debts, etc.) at rest.
- Audit logs capture every AI recommendation.
