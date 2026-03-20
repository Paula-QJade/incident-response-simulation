# incident-response-simulation
Incident Response Simulator
A CyberJuris training tool by Paula Queen

A beginner-friendly, interactive web application that guides legal and policy professionals through realistic cybersecurity incident response scenarios. Users practice making decisions under pressure and receive immediate expert feedback on each choice.

What It Does
The simulator presents real-world incident types — data breaches, ransomware attacks, insider threats — as step-by-step decision exercises. Each scenario branches based on your choices, with consequences for critical mistakes, just like a real incident.

Key Features
Branching decisions — critical wrong choices lead to consequence steps that show what actually happens, before continuing
Countdown timer — each decision has a time limit to simulate incident pressure; runs out, the best answer is revealed
Hint system — request a contextual clue at a -1 point penalty
Immediate feedback — every answer includes a detailed explanation of why it is correct, partial, or wrong
Answer summary — full review of all your decisions at the end of each scenario
Framework links — authoritative reading (NIST, CISA, GDPR, DTSA, OFAC) linked on the results page
Legal & IR Glossary — 12 key terms (GDPR, HIPAA, CCPA, DPA, PII, DTSA, and more) accessible at any time during a scenario or via the dedicated Glossary page

Scenarios
Title	Category	Difficulty	Decision Points
Data Breach: Customer PII Exposed	Data Breach	Beginner	4
Ransomware Attack on Corporate Network	Ransomware	Intermediate	3
Insider Threat: Employee Data Exfiltration	Insider Threat	Beginner	3
Scoring
Each decision is scored 0–3:

Score	Meaning
3	Best practice response
2	Acceptable but not optimal
1	Partially correct or incomplete
0	Incorrect or harmful action
Aim for 80% or higher to demonstrate strong incident response competency. Using a hint deducts 1 point from that step's score.

Who It's For
In-house legal counsel handling data privacy and security matters
Compliance officers and privacy professionals
Policy professionals working on cybersecurity regulation
Anyone new to incident response who wants a practical, low-stakes introduction
Tech Stack
Python 3.11 with Flask
Gunicorn for production serving
Vanilla HTML / CSS / JavaScript with Jinja2 templates
No database required — all scenario data is defined in main.py
Running Locally
pip install flask gunicorn
python main.py
The app runs on http://0.0.0.0:5000.

For production:

gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
Project Structure
main.py                  # Flask app, routes, scenario data, glossary, framework links
templates/
  base.html              # Base layout (navbar, footer)
  index.html             # Home page with scenario cards
  scenario.html          # Interactive scenario page
  about.html             # About page with creator info and IR lifecycle
  glossary.html          # Standalone glossary page
static/
  css/style.css          # All styles
README.md
IR Lifecycle
Scenarios follow the standard NIST Incident Response lifecycle:
Preparation — policies and plans in place before incidents occur
Identification — detecting and confirming an incident
Containment — limiting scope and impact
Eradication — removing the threat and root cause
Recovery — restoring systems to normal operation
Lessons Learned — post-incident review to improve future response

Creator
Paula Queen — CyberJuris
Built to make cybersecurity incident response concepts accessible and actionable for legal and policy professionals.
