# Incident Response Simulator

A beginner-friendly incident response simulation tool for legal & policy professionals.

## Overview

Interactive web application guiding users through realistic cybersecurity incident response scenarios. Designed for legal counsel, compliance officers, and policy professionals who need to understand IR from a legal and regulatory perspective.

## Tech Stack

- **Language**: Python 3.11
- **Framework**: Flask
- **Server (dev)**: Flask built-in dev server on port 5000
- **Server (prod)**: Gunicorn
- **Frontend**: Vanilla HTML/CSS/JavaScript with Jinja2 templates

## Project Structure

```
main.py              # Flask app — routes, scenario data, glossary, framework links
templates/
  base.html          # Base layout (navbar, footer)
  index.html         # Home page with scenario cards
  scenario.html      # Interactive scenario page (all gameplay features)
  about.html         # About page with IR lifecycle info
  glossary.html      # Standalone glossary page
static/
  css/style.css      # All styles
```

## Features

### Scenarios (3 total)
- **Data Breach: Customer PII Exposed** (Beginner, 4 decision points)
- **Ransomware Attack on Corporate Network** (Intermediate, 3 decision points)
- **Insider Threat: Employee Data Exfiltration** (Beginner, 3 decision points)

### Gameplay
- **Branching decisions** — critical wrong choices trigger consequence steps before continuing
- **Countdown timer** — 75–90s per step; turns red at 15s; auto-reveals best answer on timeout
- **Hint system** — reveal a contextual hint at a -1 point penalty
- **0–3 point scoring** per step; branch steps scored separately

### Learning Tools
- **Glossary panel** — slide-in sidebar during gameplay with 12 key legal/regulatory terms
- **Glossary page** — standalone `/glossary` route with full term definitions
- **Framework links** — per-scenario reading list (NIST, CISA, GDPR, DTSA, OFAC) shown after completion
- **Answer summary** — full decision review on the results page

## Running the App

```bash
python main.py
```

Runs on `0.0.0.0:5000`.

## Deployment

Configured for autoscale deployment using Gunicorn:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
```
