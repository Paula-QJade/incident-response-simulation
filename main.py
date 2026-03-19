from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ir-sim-secret-key-2024")

SCENARIOS = [
    {
        "id": 1,
        "title": "Data Breach: Customer PII Exposed",
        "description": "Your company's database containing customer personal information (names, emails, addresses) has been accessed without authorization. An employee reports seeing strange login activity on the admin panel.",
        "category": "Data Breach",
        "difficulty": "Beginner",
        "icon": "database",
        "steps": [
            {
                "id": 1,
                "prompt": "You receive an alert that customer data may have been exposed. What is your FIRST action?",
                "options": [
                    {"id": "a", "text": "Immediately notify all customers via email", "score": 1, "feedback": "Notifying customers is important, but first you need to confirm the breach and contain it. Acting without verified information can cause panic and may not be legally required yet."},
                    {"id": "b", "text": "Activate the incident response team and begin assessment", "score": 3, "feedback": "Correct! Activating your IR team to assess the situation is the right first step. You need to understand the scope before taking further action."},
                    {"id": "c", "text": "Shut down all company systems immediately", "score": 2, "feedback": "While containing the breach is important, shutting down ALL systems could cause unnecessary business disruption. A targeted response is more appropriate."},
                    {"id": "d", "text": "Call the press to get ahead of the story", "score": 0, "feedback": "This would be premature and could expose the company to legal liability before the breach is even confirmed or contained."}
                ],
                "best_answer": "b"
            },
            {
                "id": 2,
                "prompt": "The IR team confirms unauthorized access occurred. Approximately 5,000 customer records were accessed. What should you do next?",
                "options": [
                    {"id": "a", "text": "Document findings and preserve evidence (logs, access records)", "score": 3, "feedback": "Excellent! Preserving evidence is critical for legal proceedings, regulatory compliance, and understanding how the breach occurred."},
                    {"id": "b", "text": "Delete the compromised database to prevent further exposure", "score": 0, "feedback": "Never delete evidence! This could violate data retention laws and eliminate information needed for the investigation and legal proceedings."},
                    {"id": "c", "text": "Change all employee passwords immediately", "score": 2, "feedback": "Password changes may be necessary, but documenting the incident and preserving evidence should happen first to avoid losing forensic data."},
                    {"id": "d", "text": "Wait 30 days before taking action to avoid legal complications", "score": 0, "feedback": "Waiting is dangerous. Many jurisdictions require breach notification within 72 hours (GDPR) or 30 days. Delay increases liability significantly."}
                ],
                "best_answer": "a"
            },
            {
                "id": 3,
                "prompt": "You have documented the breach. Who must be notified and in what timeframe? (Assume GDPR applies)",
                "options": [
                    {"id": "a", "text": "Only internal leadership — keep it confidential to avoid reputational damage", "score": 0, "feedback": "Concealing a breach violates GDPR and many other privacy laws. This approach increases legal liability dramatically."},
                    {"id": "b", "text": "Notify the relevant Data Protection Authority within 72 hours, and affected individuals if high risk", "score": 3, "feedback": "Correct! GDPR Article 33 requires notification to the supervisory authority within 72 hours. Article 34 requires notifying affected individuals when the breach is high risk to their rights."},
                    {"id": "c", "text": "Notify customers within 1 year as required by law", "score": 0, "feedback": "Incorrect. GDPR requires DPA notification within 72 hours, not 1 year. This timeline would result in significant regulatory fines."},
                    {"id": "d", "text": "Post a notice on your website and consider the obligation fulfilled", "score": 1, "feedback": "A website notice alone does not fulfill GDPR notification requirements. You must directly notify the DPA and potentially affected individuals."}
                ],
                "best_answer": "b"
            },
            {
                "id": 4,
                "prompt": "After containing the breach and notifying authorities, what is the final phase of incident response?",
                "options": [
                    {"id": "a", "text": "Resume normal operations and move on as quickly as possible", "score": 1, "feedback": "Resuming operations is necessary, but without a proper post-incident review, you risk the same breach happening again."},
                    {"id": "b", "text": "Conduct a post-incident review, update policies, and implement preventive measures", "score": 3, "feedback": "Excellent! The recovery phase includes a thorough post-incident analysis, updating incident response plans, improving security controls, and training staff to prevent recurrence."},
                    {"id": "c", "text": "Fire the IT team responsible for the breach", "score": 0, "feedback": "Punitive measures alone don't improve security. Focus on systemic improvements, root cause analysis, and process changes rather than blame."},
                    {"id": "d", "text": "Hire a PR firm to manage the story and nothing else", "score": 0, "feedback": "PR management alone is insufficient. You need technical remediation, policy updates, and regulatory compliance steps."}
                ],
                "best_answer": "b"
            }
        ]
    },
    {
        "id": 2,
        "title": "Ransomware Attack on Corporate Network",
        "description": "Monday morning, employees arrive to find their files encrypted with a ransom note demanding cryptocurrency payment. Several critical systems are affected including HR and Finance.",
        "category": "Ransomware",
        "difficulty": "Intermediate",
        "icon": "lock",
        "steps": [
            {
                "id": 1,
                "prompt": "Employees report they cannot access their files and see ransom notes. What is your immediate priority?",
                "options": [
                    {"id": "a", "text": "Pay the ransom immediately to restore operations", "score": 0, "feedback": "Paying the ransom is strongly discouraged by law enforcement. It funds criminal activity, doesn't guarantee file recovery, and may be illegal if attackers are sanctioned entities."},
                    {"id": "b", "text": "Isolate affected systems from the network to prevent spread", "score": 3, "feedback": "Correct! Network isolation is the critical first step to contain ransomware. Disconnect affected machines from the network immediately to prevent the malware from spreading."},
                    {"id": "c", "text": "Restart all computers to clear the ransomware", "score": 0, "feedback": "Restarting infected systems can trigger additional encryption or destroy forensic evidence. Isolation, not restart, is the correct response."},
                    {"id": "d", "text": "Send an all-company email warning about the attack", "score": 1, "feedback": "Communication is important but containment must come first. An uncontrolled email might also cause employees to take actions that spread the malware further."}
                ],
                "best_answer": "b"
            },
            {
                "id": 2,
                "prompt": "Systems are isolated. Finance and HR data may be compromised. What legal obligations apply?",
                "options": [
                    {"id": "a", "text": "Ransomware attacks are only IT issues — no legal obligations apply", "score": 0, "feedback": "Incorrect. If personal data was accessed or exfiltrated, breach notification laws (GDPR, CCPA, HIPAA, etc.) apply regardless of how the breach occurred."},
                    {"id": "b", "text": "Assess whether personal data was exfiltrated; notify regulators if required by applicable law", "score": 3, "feedback": "Correct! You must determine if personal data was accessed or stolen (not just encrypted). If so, data protection laws require notification to authorities and potentially affected individuals."},
                    {"id": "c", "text": "Only notify authorities if you decide to pay the ransom", "score": 0, "feedback": "Notification obligations are triggered by data exposure, not by whether you pay the ransom. These are separate considerations."},
                    {"id": "d", "text": "Wait until systems are fully restored before assessing legal obligations", "score": 1, "feedback": "Waiting for full restoration could cause you to miss notification deadlines. Legal assessment should begin concurrently with technical remediation."}
                ],
                "best_answer": "b"
            },
            {
                "id": 3,
                "prompt": "You have good backups from 2 days ago. What is the safest restoration approach?",
                "options": [
                    {"id": "a", "text": "Restore from backup immediately on the same infected systems", "score": 0, "feedback": "Restoring onto infected systems risks re-infection. You must verify the ransomware and its persistence mechanisms are fully removed first."},
                    {"id": "b", "text": "Wipe and rebuild affected systems, then restore from verified clean backups", "score": 3, "feedback": "Correct! The safest approach is to fully wipe and rebuild infected systems from scratch, then restore data from clean, pre-infection backups. This eliminates any remaining malware or backdoors."},
                    {"id": "c", "text": "Run antivirus and restore if the scan comes back clean", "score": 1, "feedback": "Antivirus scans alone may miss advanced ransomware variants or backdoors. A full wipe and rebuild is the more reliable approach for serious ransomware incidents."},
                    {"id": "d", "text": "Accept the 2-day data loss and build new systems without restoring backups", "score": 1, "feedback": "While building clean systems is good, abandoning your backups unnecessarily is not ideal. Use your clean backups to recover as much data as possible."}
                ],
                "best_answer": "b"
            }
        ]
    },
    {
        "id": 3,
        "title": "Insider Threat: Employee Data Exfiltration",
        "description": "Your DLP system flags that a departing employee has uploaded a large volume of proprietary documents to a personal cloud storage account in their final week of employment.",
        "category": "Insider Threat",
        "difficulty": "Beginner",
        "icon": "user-secret",
        "steps": [
            {
                "id": 1,
                "prompt": "Your DLP system alerts you to the suspicious activity. How do you proceed?",
                "options": [
                    {"id": "a", "text": "Immediately confront the employee and demand they delete the files", "score": 0, "feedback": "Confronting without investigation can tip off the individual and result in evidence destruction. It could also create legal issues if the activity turns out to have an innocent explanation."},
                    {"id": "b", "text": "Disable the employee's access and escalate to Legal and HR for a proper investigation", "score": 3, "feedback": "Correct! Revoking access prevents further exfiltration while escalating to Legal and HR ensures the investigation is conducted properly and evidence is preserved for potential legal action."},
                    {"id": "c", "text": "Do nothing until the employee leaves, then assess the damage", "score": 0, "feedback": "Waiting allows continued exfiltration. The employee may take even more data before their last day. Immediate containment is necessary."},
                    {"id": "d", "text": "Send a company-wide warning about data theft policies", "score": 1, "feedback": "General awareness is valuable but doesn't address the immediate incident. Containment and proper investigation procedures should take priority."}
                ],
                "best_answer": "b"
            },
            {
                "id": 2,
                "prompt": "Legal is involved. What type of data must be treated with special care during this investigation?",
                "options": [
                    {"id": "a", "text": "Only financial data matters; personal data is not relevant", "score": 0, "feedback": "Personal data about employees, customers, or partners is highly sensitive and subject to privacy laws. Mishandling it during an investigation can create additional legal liability."},
                    {"id": "b", "text": "Any personal data about employees or third parties must be handled per privacy laws during the investigation", "score": 3, "feedback": "Correct! Privacy regulations like GDPR still apply during security investigations. You cannot simply access all employee data without proper legal basis and proportionality."},
                    {"id": "c", "text": "All restrictions are suspended during security incidents", "score": 0, "feedback": "Privacy laws do not suspend during incidents. Data protection obligations continue, and investigations must be conducted lawfully and proportionately."},
                    {"id": "d", "text": "Share all findings publicly to deter future incidents", "score": 0, "feedback": "Public disclosure of investigation details could violate employee privacy rights, undermine legal proceedings, and expose the company to liability."}
                ],
                "best_answer": "b"
            },
            {
                "id": 3,
                "prompt": "The investigation confirms intentional data theft. The employee took trade secrets. What is the appropriate response?",
                "options": [
                    {"id": "a", "text": "Resolve it quietly with a non-disclosure agreement and move on", "score": 1, "feedback": "While NDAs can have a role, quiet resolution may not adequately protect the company's intellectual property rights or address all legal obligations. Civil or criminal action may be warranted."},
                    {"id": "b", "text": "Work with Legal to pursue civil remedies and potentially refer to law enforcement for criminal trade secret theft", "score": 3, "feedback": "Correct! Trade secret theft may be a civil and/or criminal matter. Working with Legal to pursue appropriate remedies protects the company and deters future incidents. Document everything for potential litigation."},
                    {"id": "c", "text": "Fire the employee and take no further action", "score": 1, "feedback": "Termination may be appropriate but taking no further action leaves the stolen trade secrets in circulation and misses the opportunity for legal remedies and recovery."},
                    {"id": "d", "text": "Publicly name and shame the individual on social media", "score": 0, "feedback": "This approach creates significant legal risk (defamation claims) and undermines any ongoing legal proceedings. All communications should go through Legal counsel."}
                ],
                "best_answer": "b"
            }
        ]
    }
]


@app.route("/")
def index():
    return render_template("index.html", scenarios=SCENARIOS)


@app.route("/scenario/<int:scenario_id>")
def scenario(scenario_id):
    scen = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scen:
        return "Scenario not found", 404
    return render_template("scenario.html", scenario=scen)


@app.route("/api/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    scenario_id = data.get("scenario_id")
    step_id = data.get("step_id")
    answer_id = data.get("answer_id")

    scen = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scen:
        return jsonify({"error": "Scenario not found"}), 404

    step = next((s for s in scen["steps"] if s["id"] == step_id), None)
    if not step:
        return jsonify({"error": "Step not found"}), 404

    option = next((o for o in step["options"] if o["id"] == answer_id), None)
    if not option:
        return jsonify({"error": "Option not found"}), 404

    is_best = answer_id == step["best_answer"]

    return jsonify({
        "score": option["score"],
        "max_score": 3,
        "feedback": option["feedback"],
        "is_best": is_best,
        "best_answer": step["best_answer"]
    })


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
