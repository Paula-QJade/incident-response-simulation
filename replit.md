# Incident Response Simulator

A beginner-friendly incident response simulation tool for legal & policy professionals.

## Overview

This is an interactive web application that guides users through realistic cybersecurity incident response scenarios. It's designed specifically for legal counsel, compliance officers, and policy professionals who need to understand incident response from a legal and regulatory perspective.

## Tech Stack

- **Language**: Python 3.11
- **Framework**: Flask
- **Server (dev)**: Flask built-in dev server on port 5000
- **Server (prod)**: Gunicorn
- **Frontend**: Vanilla HTML/CSS/JavaScript with Jinja2 templates

## Project Structure

```
main.py              # Flask application with all routes and scenario data
templates/
  base.html          # Base layout template
  index.html         # Home page with scenario cards
  scenario.html      # Interactive scenario page
  about.html         # About page with IR lifecycle info
static/
  css/style.css      # All styles
```

## Features

- 3 interactive scenarios: Data Breach, Ransomware, Insider Threat
- Decision-point based gameplay with 0–3 point scoring
- Immediate feedback explaining why each choice is correct or incorrect
- Progress tracking and final results summary
- Responsive design

## Running the App

The app starts automatically via the "Start application" workflow:
```bash
python main.py
```

Runs on `0.0.0.0:5000`.

## Deployment

Configured for autoscale deployment using Gunicorn:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
```
