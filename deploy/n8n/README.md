# Hosted n8n Deployment Starter

This folder packages n8n and the Python APMM pipeline into one container. It is intended for a protected Linux server behind HTTPS, not for exposing the local Windows editor directly to the internet.

## Prerequisites

- A Linux VPS or cloud VM with Docker Engine and Docker Compose v2
- A domain or subdomain such as `n8n.example.com`
- An HTTPS reverse proxy such as Caddy, Traefik, or Nginx
- Google OAuth credentials configured for the hosted n8n callback URL

## Start The Service

1. Copy `.env.example` to `.env`.
2. Replace `N8N_HOST` with the real domain.
3. Generate a long random `N8N_ENCRYPTION_KEY` and store it only in `.env` or a host secret manager.
4. Build and start the service:

```bash
docker compose --env-file .env up -d --build
docker compose ps
```

5. Configure the reverse proxy to send HTTPS traffic to `127.0.0.1:5678` and forward `X-Forwarded-For`, `X-Forwarded-Host`, and `X-Forwarded-Proto`.
6. Open the HTTPS URL, create the instance owner, and import `n8n/foundit_apmm_n8n_workflow_hosted.json`.
7. Recreate Google Drive and Gmail credentials. OAuth secrets are intentionally not stored in Git.
8. Test both routes, then publish the workflow.

## Important

- The n8n editor must remain authenticated.
- Do not commit `.env`, the n8n database, encryption keys, or OAuth secrets.
- The hosted workflow uses fixed paths inside the packaged container and imports as inactive for safe credential setup and testing.
- Code-node environment access is blocked, so workflow JavaScript cannot read the n8n encryption key or other container secrets.
- The built-in module allow-list is intended only for this trusted workflow; keep editor access authenticated and limited to authorized operators.
- This starter is statically validated in this repository. A live deployment still requires a server, domain, DNS, HTTPS, and OAuth configuration.
