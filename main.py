from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ir-sim-secret-key-2024")

GLOSSARY = [
    {"term": "GDPR", "full": "General Data Protection Regulation", "definition": "EU regulation governing personal data processing. Requires breach notification to supervisory authorities within 72 hours and to affected individuals 'without undue delay' when rights are at high risk."},
    {"term": "CCPA", "full": "California Consumer Privacy Act", "definition": "California state law giving residents rights over their personal data. Businesses must notify consumers of breaches involving unencrypted personal information."},
    {"term": "HIPAA", "full": "Health Insurance Portability and Accountability Act", "definition": "US federal law protecting health information. Requires covered entities to notify individuals within 60 days of discovering a breach of unsecured protected health information (PHI)."},
    {"term": "DPA", "full": "Data Protection Authority", "definition": "A national or regional regulator responsible for enforcing data protection law (e.g., the ICO in the UK, the CNIL in France). Under GDPR, breaches must be reported to the relevant DPA within 72 hours."},
    {"term": "PII", "full": "Personally Identifiable Information", "definition": "Any data that could identify a specific individual — names, addresses, email addresses, Social Security numbers, etc. Exposure of PII typically triggers breach notification obligations."},
    {"term": "PHI", "full": "Protected Health Information", "definition": "Any individually identifiable health information held or transmitted by a HIPAA-covered entity. Breach of PHI triggers HIPAA notification requirements."},
    {"term": "IR", "full": "Incident Response", "definition": "The structured approach an organization takes to address and manage the aftermath of a security breach or cyberattack. The NIST framework defines six phases: Preparation, Identification, Containment, Eradication, Recovery, and Lessons Learned."},
    {"term": "DLP", "full": "Data Loss Prevention", "definition": "Technology and policies that detect and prevent unauthorized transfer of sensitive data outside an organization. Commonly used to detect insider threats and accidental data leaks."},
    {"term": "NIST", "full": "National Institute of Standards and Technology", "definition": "US federal agency that publishes the widely used NIST Cybersecurity Framework (CSF) and Special Publication 800-61, which provides guidelines for computer security incident handling."},
    {"term": "Ransomware", "full": "Ransomware", "definition": "Malicious software that encrypts a victim's files and demands payment (usually cryptocurrency) for the decryption key. Paying the ransom is discouraged by law enforcement and may be illegal in some jurisdictions."},
    {"term": "Chain of Custody", "full": "Chain of Custody", "definition": "The chronological documentation showing who has had possession of digital evidence. Maintaining an unbroken chain of custody is essential for evidence to be admissible in legal proceedings."},
    {"term": "Trade Secret", "full": "Trade Secret", "definition": "Confidential business information that provides a competitive advantage — formulas, practices, processes, designs, or compilations. Protected under the US Defend Trade Secrets Act (DTSA) and state laws. Theft can carry civil and criminal liability."},
]

FRAMEWORKS = {
    1: [
        {"name": "NIST SP 800-61 Rev. 2", "description": "Computer Security Incident Handling Guide", "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf"},
        {"name": "GDPR Article 33 & 34", "description": "Personal data breach notification obligations", "url": "https://gdpr-info.eu/art-33-gdpr/"},
        {"name": "ENISA Breach Notification Guidelines", "description": "Practical guidelines for breach notifications under GDPR", "url": "https://www.enisa.europa.eu/publications/recommendations-for-a-methodology-of-the-assessment-of-severity-of-personal-data-breaches"},
    ],
    2: [
        {"name": "CISA Ransomware Guide", "description": "CISA & FBI guidance on ransomware response", "url": "https://www.cisa.gov/stopransomware/ransomware-guide"},
        {"name": "NIST SP 800-61 Rev. 2", "description": "Computer Security Incident Handling Guide", "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf"},
        {"name": "OFAC Ransomware Advisory", "description": "US Treasury guidance on sanctions risks of ransomware payments", "url": "https://ofac.treasury.gov/media/912981/download?inline"},
    ],
    3: [
        {"name": "NIST SP 800-53 (Personnel Security)", "description": "Security controls for insider threat programs", "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final"},
        {"name": "DTSA Overview", "description": "Defend Trade Secrets Act — federal civil remedy for trade secret theft", "url": "https://www.govinfo.gov/content/pkg/PLAW-114publ153/pdf/PLAW-114publ153.pdf"},
        {"name": "CISA Insider Threat Mitigation", "description": "CISA guidance on insider threat detection and response", "url": "https://www.cisa.gov/insider-threat-mitigation"},
    ],
}

SCENARIOS = [
    {
        "id": 1,
        "title": "Data Breach: Customer PII Exposed",
        "description": "Your company's database containing customer personal information (names, emails, addresses) has been accessed without authorization. An employee reports seeing strange login activity on the admin panel.",
        "category": "Data Breach",
        "difficulty": "Beginner",
        "step_order": ["s1", "s2", "s3", "s3b", "s4"],
        "main_steps": ["s1", "s2", "s3", "s4"],
        "steps": {
            "s1": {
                "id": "s1",
                "label": "Decision Point 1",
                "prompt": "You receive an alert that customer data may have been exposed. What is your FIRST action?",
                "hint": "Think about what you need to know before taking any external action. Who should be in the room when you make these decisions?",
                "time_limit": 90,
                "options": [
                    {"id": "a", "text": "Immediately notify all customers via email", "score": 1, "feedback": "Notifying customers is important, but first you need to confirm the breach and contain it. Acting without verified information can cause panic and may not be legally required yet.", "next_step": "s2"},
                    {"id": "b", "text": "Activate the incident response team and begin assessment", "score": 3, "feedback": "Correct! Activating your IR team to assess the situation is the right first step. You need to understand the scope before taking further action.", "next_step": "s2"},
                    {"id": "c", "text": "Shut down all company systems immediately", "score": 2, "feedback": "While containing the breach is important, shutting down ALL systems could cause unnecessary business disruption. A targeted response is more appropriate.", "next_step": "s2"},
                    {"id": "d", "text": "Call the press to get ahead of the story", "score": 0, "feedback": "This would be premature and could expose the company to legal liability before the breach is even confirmed or contained.", "next_step": "s2"},
                ],
                "best_answer": "b",
            },
            "s2": {
                "id": "s2",
                "label": "Decision Point 2",
                "prompt": "The IR team confirms unauthorized access occurred. Approximately 5,000 customer records were accessed. What should you do next?",
                "hint": "Forensics and legal proceedings both depend heavily on what is available after the fact. What gets lost if you act too fast?",
                "time_limit": 90,
                "options": [
                    {"id": "a", "text": "Document findings and preserve evidence (logs, access records)", "score": 3, "feedback": "Excellent! Preserving evidence is critical for legal proceedings, regulatory compliance, and understanding how the breach occurred.", "next_step": "s3"},
                    {"id": "b", "text": "Delete the compromised database to prevent further exposure", "score": 0, "feedback": "Never delete evidence! This could violate data retention laws and eliminate information needed for the investigation and legal proceedings.", "next_step": "s3"},
                    {"id": "c", "text": "Change all employee passwords immediately", "score": 2, "feedback": "Password changes may be necessary, but documenting the incident and preserving evidence should happen first to avoid losing forensic data.", "next_step": "s3"},
                    {"id": "d", "text": "Wait 30 days before taking action to avoid legal complications", "score": 0, "feedback": "Waiting is dangerous. Many jurisdictions require breach notification within 72 hours (GDPR). Delay significantly increases legal liability.", "next_step": "s3"},
                ],
                "best_answer": "a",
            },
            "s3": {
                "id": "s3",
                "label": "Decision Point 3",
                "prompt": "You have documented the breach. Who must be notified and in what timeframe? (Assume GDPR applies)",
                "hint": "GDPR has two separate notification obligations — one to regulators, one to individuals. What triggers each?",
                "time_limit": 90,
                "options": [
                    {"id": "a", "text": "Only internal leadership — keep it confidential to avoid reputational damage", "score": 0, "feedback": "Concealing a breach violates GDPR and many other privacy laws. This approach increases legal liability dramatically.", "next_step": "s3b"},
                    {"id": "b", "text": "Notify the relevant Data Protection Authority within 72 hours, and affected individuals if high risk", "score": 3, "feedback": "Correct! GDPR Article 33 requires notification to the supervisory authority within 72 hours. Article 34 requires notifying affected individuals when the breach poses high risk to their rights.", "next_step": "s4"},
                    {"id": "c", "text": "Notify customers within 1 year as required by law", "score": 0, "feedback": "Incorrect. GDPR requires DPA notification within 72 hours, not 1 year. This timeline would result in significant regulatory fines.", "next_step": "s3b"},
                    {"id": "d", "text": "Post a notice on your website and consider the obligation fulfilled", "score": 1, "feedback": "A website notice alone does not fulfill GDPR notification requirements. You must directly notify the DPA and potentially affected individuals.", "next_step": "s3b"},
                ],
                "best_answer": "b",
            },
            "s3b": {
                "id": "s3b",
                "label": "Consequence",
                "is_branch": True,
                "branch_context": "Three days have passed. The Data Protection Authority has discovered the breach through a third party and has launched an investigation. Your organization is now facing a formal inquiry for failing to notify within 72 hours.",
                "prompt": "The DPA is now formally investigating your late notification. What is your best course of action?",
                "hint": "In regulatory investigations, cooperation and transparency typically yield better outcomes than resistance.",
                "time_limit": 75,
                "options": [
                    {"id": "a", "text": "Engage legal counsel, fully cooperate with the DPA, and document all remediation steps taken", "score": 3, "feedback": "Correct. Full cooperation, legal representation, and clear documentation of remediation efforts are the best response to a regulatory investigation. Demonstrating good faith can reduce penalties.", "next_step": "s4"},
                    {"id": "b", "text": "Deny the breach occurred and challenge the DPA's authority", "score": 0, "feedback": "Denying a confirmed breach and challenging regulatory authority will dramatically worsen the outcome. GDPR fines can reach €20 million or 4% of global annual turnover.", "next_step": "s4"},
                    {"id": "c", "text": "Notify all customers immediately and hope this satisfies the DPA", "score": 1, "feedback": "Late customer notification is better than none, but it doesn't resolve the failure to notify the DPA on time. Legal counsel and formal cooperation with the investigation are still essential.", "next_step": "s4"},
                    {"id": "d", "text": "Offer a financial settlement directly to the DPA", "score": 0, "feedback": "DPAs cannot accept informal settlements — they impose fines through formal regulatory processes. Attempting this could be seen as an attempt to improperly influence a regulator.", "next_step": "s4"},
                ],
                "best_answer": "a",
            },
            "s4": {
                "id": "s4",
                "label": "Decision Point 4",
                "prompt": "After containing the breach and meeting your notification obligations, what is the final phase of incident response?",
                "hint": "The goal isn't just to recover — it's to make sure this doesn't happen again. What does a mature IR program do at this stage?",
                "time_limit": 75,
                "options": [
                    {"id": "a", "text": "Resume normal operations and move on as quickly as possible", "score": 1, "feedback": "Resuming operations is necessary, but without a proper post-incident review, you risk the same breach happening again.", "next_step": None},
                    {"id": "b", "text": "Conduct a post-incident review, update policies, and implement preventive measures", "score": 3, "feedback": "Excellent! The recovery phase includes a thorough post-incident analysis, updating incident response plans, improving security controls, and training staff to prevent recurrence.", "next_step": None},
                    {"id": "c", "text": "Fire the IT team responsible for the breach", "score": 0, "feedback": "Punitive measures alone don't improve security. Focus on systemic improvements, root cause analysis, and process changes rather than blame.", "next_step": None},
                    {"id": "d", "text": "Hire a PR firm to manage the story and nothing else", "score": 0, "feedback": "PR management alone is insufficient. You need technical remediation, policy updates, and regulatory compliance steps.", "next_step": None},
                ],
                "best_answer": "b",
            },
        },
    },
    {
        "id": 2,
        "title": "Ransomware Attack on Corporate Network",
        "description": "Monday morning, employees arrive to find their files encrypted with a ransom note demanding cryptocurrency payment. Several critical systems are affected including HR and Finance.",
        "category": "Ransomware",
        "difficulty": "Intermediate",
        "step_order": ["s1", "s1b", "s2", "s3"],
        "main_steps": ["s1", "s2", "s3"],
        "steps": {
            "s1": {
                "id": "s1",
                "label": "Decision Point 1",
                "prompt": "Employees report they cannot access their files and see ransom notes on their screens. What is your immediate priority?",
                "hint": "Ransomware spreads through connected networks. What single action stops it from reaching more machines?",
                "time_limit": 75,
                "options": [
                    {"id": "a", "text": "Pay the ransom immediately to restore operations", "score": 0, "feedback": "Paying the ransom is strongly discouraged by law enforcement. It funds criminal activity, doesn't guarantee file recovery, and may be illegal if the attackers are sanctioned entities.", "next_step": "s1b"},
                    {"id": "b", "text": "Isolate affected systems from the network to prevent spread", "score": 3, "feedback": "Correct! Network isolation is the critical first step. Disconnect affected machines immediately — unplug network cables or disable Wi-Fi — to prevent ransomware from spreading to other systems.", "next_step": "s2"},
                    {"id": "c", "text": "Restart all computers to clear the ransomware", "score": 0, "feedback": "Restarting infected systems can trigger additional encryption or destroy forensic evidence needed for investigation. Isolation, not restart, is the correct response.", "next_step": "s2"},
                    {"id": "d", "text": "Send an all-company email warning about the attack", "score": 1, "feedback": "Communication is important but containment must come first. An uncontrolled email might also cause employees to take actions that spread the malware further.", "next_step": "s2"},
                ],
                "best_answer": "b",
            },
            "s1b": {
                "id": "s1b",
                "label": "Consequence",
                "is_branch": True,
                "branch_context": "You paid $200,000 in Bitcoin. The attackers provided a partial decryption key — only 40% of files were restored. They are now demanding a second payment. Meanwhile, the ransomware continued spreading while you negotiated, and three more business units are now encrypted.",
                "prompt": "The situation has escalated. You've paid once but files are still encrypted. What do you do now?",
                "hint": "Paying once didn't work. What should have been done first before any payment decision was made?",
                "time_limit": 75,
                "options": [
                    {"id": "a", "text": "Pay the second ransom — you've already committed to this approach", "score": 0, "feedback": "Each payment further funds criminals and signals you will keep paying. There is no guarantee a second payment works either. You must stop and engage proper IR resources.", "next_step": "s2"},
                    {"id": "b", "text": "Stop all payments, isolate remaining systems, engage a forensic IR firm and legal counsel", "score": 3, "feedback": "Correct. Cut losses, contain spread, and bring in expert help. Legal counsel is essential to assess ransom payment legality (OFAC sanctions compliance) and regulatory obligations.", "next_step": "s2"},
                    {"id": "c", "text": "Negotiate directly with the attackers for a better price", "score": 0, "feedback": "Direct negotiation without expert ransomware negotiators and legal guidance is extremely risky. It extends the time your systems remain compromised and may violate OFAC sanctions rules.", "next_step": "s2"},
                    {"id": "d", "text": "Go public with the attack to pressure the attackers into giving you the key", "score": 0, "feedback": "Public disclosure without legal guidance, before containment, and without notifying regulators first creates significant legal and reputational risk. Attackers may also escalate by publishing your stolen data.", "next_step": "s2"},
                ],
                "best_answer": "b",
            },
            "s2": {
                "id": "s2",
                "label": "Decision Point 2",
                "prompt": "Systems are isolated. Finance and HR data was present on the affected systems. What legal obligations must you assess?",
                "hint": "Encryption alone doesn't necessarily mean data was copied or exfiltrated. But can you prove it wasn't? What laws apply to HR and financial data?",
                "time_limit": 90,
                "options": [
                    {"id": "a", "text": "Ransomware attacks are IT issues only — no legal obligations apply", "score": 0, "feedback": "Incorrect. If personal data was accessed or exfiltrated, breach notification laws (GDPR, CCPA, HIPAA, etc.) apply regardless of how the breach occurred.", "next_step": "s3"},
                    {"id": "b", "text": "Assess whether personal data was exfiltrated; notify regulators as required by applicable law", "score": 3, "feedback": "Correct. You must determine whether personal data was accessed or stolen — not just encrypted. If so, data protection laws require timely notification to authorities and potentially affected individuals.", "next_step": "s3"},
                    {"id": "c", "text": "Only notify authorities if you decide to pay the ransom", "score": 0, "feedback": "Notification obligations are triggered by data exposure, not by whether you pay the ransom. These are entirely separate legal questions.", "next_step": "s3"},
                    {"id": "d", "text": "Wait until systems are fully restored before assessing legal obligations", "score": 1, "feedback": "Waiting for full restoration could cause you to miss critical notification deadlines. Legal assessment must run concurrently with technical remediation.", "next_step": "s3"},
                ],
                "best_answer": "b",
            },
            "s3": {
                "id": "s3",
                "label": "Decision Point 3",
                "prompt": "Forensics confirms no data was exfiltrated — only encrypted. You have verified clean backups from 48 hours ago. What is the safest restoration approach?",
                "hint": "The ransomware is still on the infected machines. What must happen before you restore any data?",
                "time_limit": 90,
                "options": [
                    {"id": "a", "text": "Restore from backup immediately on the same infected systems", "score": 0, "feedback": "Restoring onto infected systems risks immediate re-infection. The ransomware — and any backdoors it installed — must be fully removed before restoration.", "next_step": None},
                    {"id": "b", "text": "Wipe and rebuild affected systems, then restore from verified clean backups", "score": 3, "feedback": "Correct. Fully wipe and rebuild infected systems, then restore from clean pre-infection backups. This eliminates any remaining malware, persistence mechanisms, or backdoors.", "next_step": None},
                    {"id": "c", "text": "Run antivirus and restore if the scan comes back clean", "score": 1, "feedback": "Antivirus scans may miss advanced ransomware variants or hidden backdoors. A full wipe and rebuild is the more reliable approach for serious ransomware incidents.", "next_step": None},
                    {"id": "d", "text": "Accept the 48-hour data loss and build new systems without restoring anything", "score": 1, "feedback": "While building clean systems is correct, abandoning clean backups unnecessarily is not ideal. Restore as much as possible from your verified clean backups.", "next_step": None},
                ],
                "best_answer": "b",
            },
        },
    },
    {
        "id": 3,
        "title": "Insider Threat: Employee Data Exfiltration",
        "description": "Your DLP system flags that a departing employee has uploaded a large volume of proprietary documents to a personal cloud storage account in their final week of employment.",
        "category": "Insider Threat",
        "difficulty": "Beginner",
        "step_order": ["s1", "s2", "s2b", "s3"],
        "main_steps": ["s1", "s2", "s3"],
        "steps": {
            "s1": {
                "id": "s1",
                "label": "Decision Point 1",
                "prompt": "Your DLP system alerts you to the suspicious upload activity. The employee is still in their notice period. How do you proceed?",
                "hint": "You need to stop the leak AND preserve evidence. Which action does both without tipping the person off?",
                "time_limit": 75,
                "options": [
                    {"id": "a", "text": "Immediately confront the employee and demand they delete the files", "score": 0, "feedback": "Confronting without investigation can tip off the individual and result in evidence destruction. It could also create legal issues if the activity has an innocent explanation.", "next_step": "s2"},
                    {"id": "b", "text": "Disable the employee's access and escalate to Legal and HR for a proper investigation", "score": 3, "feedback": "Correct! Revoking access prevents further exfiltration while escalating to Legal and HR ensures the investigation is conducted properly and evidence is preserved for potential legal action.", "next_step": "s2"},
                    {"id": "c", "text": "Do nothing until the employee leaves, then assess the damage", "score": 0, "feedback": "Waiting allows continued exfiltration. The employee may take even more data before their last day. Immediate containment is necessary.", "next_step": "s2"},
                    {"id": "d", "text": "Send a company-wide warning about data theft policies", "score": 1, "feedback": "General awareness is valuable but doesn't address the immediate incident. It may also signal to the employee that they have been detected, prompting data destruction.", "next_step": "s2"},
                ],
                "best_answer": "b",
            },
            "s2": {
                "id": "s2",
                "label": "Decision Point 2",
                "prompt": "Legal and HR are involved. To investigate, your team wants to review the employee's work emails and device activity logs. What must you consider?",
                "hint": "Security investigations don't suspend privacy rights. What legal basis do you need to monitor employee communications?",
                "time_limit": 90,
                "options": [
                    {"id": "a", "text": "Review everything — security incidents override all privacy considerations", "score": 0, "feedback": "Privacy laws do not suspend during security incidents. Accessing communications without proper legal basis can render evidence inadmissible and expose the company to privacy law violations.", "next_step": "s2b"},
                    {"id": "b", "text": "Review only work device and system logs; consult Legal on the legal basis for accessing communications", "score": 3, "feedback": "Correct. System and access logs are typically within scope under acceptable use policies. Accessing personal or work communications requires proper legal basis — consult employment law counsel before proceeding.", "next_step": "s3"},
                    {"id": "c", "text": "Only financial data is legally sensitive — proceed freely with everything else", "score": 0, "feedback": "Employee communications and personal data are protected regardless of content. GDPR, employment law, and wiretapping statutes can all apply to how employer monitoring is conducted.", "next_step": "s2b"},
                    {"id": "d", "text": "Share all raw investigation findings with the full HR team immediately", "score": 1, "feedback": "Investigation findings should be shared on a strict need-to-know basis. Broad distribution can compromise the investigation, expose confidential data, and create legal liability.", "next_step": "s2b"},
                ],
                "best_answer": "b",
            },
            "s2b": {
                "id": "s2b",
                "label": "Consequence",
                "is_branch": True,
                "branch_context": "Your team accessed the employee's personal email account without proper legal authorization. The employee's attorney is now threatening a lawsuit for unlawful interception of communications. The evidence gathered may be inadmissible, and the company faces a counter-claim that could complicate any trade secret case.",
                "prompt": "Your investigation has been legally compromised. What is the best path forward?",
                "hint": "When an investigation goes wrong legally, the priority is to limit further damage and get proper guidance.",
                "time_limit": 75,
                "options": [
                    {"id": "a", "text": "Continue using the improperly obtained evidence — it still shows wrongdoing", "score": 0, "feedback": "Using improperly obtained evidence can expose the company to further legal liability and may result in the evidence being excluded in court. It also weakens any trade secret case you might bring.", "next_step": "s3"},
                    {"id": "b", "text": "Immediately engage legal counsel, preserve lawfully obtained evidence, and assess exposure from the improper access", "score": 3, "feedback": "Correct. Stop using compromised evidence, get proper legal guidance on your exposure, and rebuild the investigation using only lawfully obtained materials. Transparency with counsel is critical.", "next_step": "s3"},
                    {"id": "c", "text": "Delete all evidence to prevent the employee from using it against the company", "score": 0, "feedback": "Destroying evidence when litigation is reasonably anticipated is spoliation — a serious legal violation that can result in court sanctions, adverse inferences, and criminal liability.", "next_step": "s3"},
                    {"id": "d", "text": "Settle immediately with the employee to make all issues go away", "score": 1, "feedback": "While settlement is sometimes appropriate, doing so immediately without legal advice — and while trade secrets remain exposed — may not serve the company's best interests. Consult counsel first.", "next_step": "s3"},
                ],
                "best_answer": "b",
            },
            "s3": {
                "id": "s3",
                "label": "Decision Point 3",
                "prompt": "The investigation confirms intentional data theft. The employee took proprietary source code and client lists. What is the appropriate legal response?",
                "hint": "Trade secret theft has both civil and criminal dimensions. Which law protects trade secrets at the federal level in the US?",
                "time_limit": 90,
                "options": [
                    {"id": "a", "text": "Resolve it quietly with a stronger NDA and move on", "score": 1, "feedback": "While NDAs can have a role, quiet resolution may not adequately protect the company's IP or address all legal obligations. The stolen data is already out, and civil or criminal action may be necessary to prevent further harm.", "next_step": None},
                    {"id": "b", "text": "Work with Legal to pursue civil remedies under the DTSA and potentially refer to law enforcement for criminal prosecution", "score": 3, "feedback": "Correct. Trade secret theft may be pursued as both a civil matter (Defend Trade Secrets Act, state law) and a criminal matter (Economic Espionage Act). Law enforcement referral, injunctive relief, and damages are all available remedies.", "next_step": None},
                    {"id": "c", "text": "Fire the employee (if not already done) and take no further action", "score": 1, "feedback": "Termination is appropriate but insufficient. The stolen trade secrets remain in circulation. Legal remedies — including injunctions to prevent further use — are necessary to protect the company.", "next_step": None},
                    {"id": "d", "text": "Publicly name and shame the individual on company social media", "score": 0, "feedback": "This creates significant legal risk including defamation claims, undermines legal proceedings, and can violate court-ordered confidentiality. All public communications must go through Legal counsel.", "next_step": None},
                ],
                "best_answer": "b",
            },
        },
    },
]


def get_all_steps_list(scenario):
    return [scenario["steps"][sid] for sid in scenario["step_order"]]


@app.route("/")
def index():
    return render_template("index.html", scenarios=SCENARIOS)


@app.route("/scenario/<int:scenario_id>")
def scenario(scenario_id):
    scen = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scen:
        return "Scenario not found", 404
    steps_list = get_all_steps_list(scen)
    frameworks = FRAMEWORKS.get(scenario_id, [])
    return render_template("scenario.html", scenario=scen, steps_list=steps_list, frameworks=frameworks, glossary=GLOSSARY)


@app.route("/api/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    scenario_id = data.get("scenario_id")
    step_id = data.get("step_id")
    answer_id = data.get("answer_id")

    scen = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scen:
        return jsonify({"error": "Scenario not found"}), 404

    step = scen["steps"].get(step_id)
    if not step:
        return jsonify({"error": "Step not found"}), 404

    option = next((o for o in step["options"] if o["id"] == answer_id), None)
    if not option:
        return jsonify({"error": "Option not found"}), 404

    is_best = answer_id == step["best_answer"]
    next_step_id = option.get("next_step")

    if next_step_id:
        next_step = scen["steps"].get(next_step_id, {})
        next_is_branch = next_step.get("is_branch", False)
        next_branch_context = next_step.get("branch_context", "")
    else:
        next_is_branch = False
        next_branch_context = ""

    return jsonify({
        "score": option["score"],
        "max_score": 3,
        "feedback": option["feedback"],
        "is_best": is_best,
        "best_answer": step["best_answer"],
        "next_step_id": next_step_id,
        "next_is_branch": next_is_branch,
        "next_branch_context": next_branch_context,
    })


@app.route("/about")
def about():
    return render_template("about.html", glossary=GLOSSARY)


@app.route("/glossary")
def glossary():
    return render_template("glossary.html", glossary=GLOSSARY)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
