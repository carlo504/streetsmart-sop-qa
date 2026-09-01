# StreetSmart Standard Operating Procedures (SOP) QA System

This Quality Assurance (QA) auditing system provides automated, objective evaluation for **CSRs** and **Producers** across two core StreetSmart SOPs:
1. **SOP 1: New Business** (Intake, Quoting, Presentations, Objection Handling, Won Stage Documentation)
2. **SOP 2: Policy Change Request** (Client Verification, Core & Branch Question Guides, Direct/Agency Billing, 48h Carrier Follow-Up, Confirmation Standards)

---

## 🚀 Key Features

* **Multi-Source Ingestion & Signal Analysis**:
  * **RingCentral**: Evaluates inbound call pickup speed (<5-min SLA), talk time, warm-transfer logs, and phone quote presentation completion.
  * **Magellan Sentiment Intelligence**: Analyzes talk-to-listen ratio, empathy scores, customer sentiment trends (Positive / Neutral / Negative), and detects **CENT** objection-handling cues.
  * **EZLynx & Carrier Portals**: Audits SalesCenter pipeline stages, task memos, discussion titles, document uploads, and carrier download match verification.
* **Instant Non-Negotiable Gate Detection**:
  * Flagging critical violations immediately (e.g., emailing quotes before phone presentation, requesting decs page at intake, binding unpaid agency-bill endorsements, confirming changes before carrier download).
* **Dual Execution Modes**:
  1. **CLI Terminal Runner (Ruby)**: Automated batch tester for backend or CI evaluations (`ruby engine/qa_evaluator.rb`).
  2. **Interactive Generative UI Dashboard (HTML/JS)**: Clean local dashboard (`dashboard/index.html`) with preloaded benchmark scenarios, custom input auditing, real-time score gauges, and personalized coaching plans.

---

## 📊 Scorecard & Rubric Breakdown

### SOP 1: New Business (100 Points Total)
1. **Intake & Lead Qualification (20 pts)**: 5-min response SLA, LOB/X-date capture, no dec page at intake, warm transfer / priority `!` task.
2. **Quoting & Multi-Market Tracking (20 pts)**: 2h entry / 24h quote SLA, multiple markets quoted, 2–3 coverage options, designated folder saving.
3. **Quote Presentation & CENT Objections (25 pts)**: Phone presentation BEFORE email, 3 distinct carrier benefits, direct closing ask, CENT objection handling.
4. **Closing, Won & Documentation (20 pts)**: EFT payment method, $100 agency fee on manual policies, Sales Center Won status & premium recorded, document uploads.
5. **Follow-Up & System Standards (15 pts)**: 2-day follow-up cadence (up to 14 days), Sales Center stage alignment, EZLynx naming & labels.

### SOP 2: Policy Change Request (100 Points Total)
1. **Client Verification & Core Intake (25 pts)**: Caller authority, effective date & loss screening, umbrella & cross-policy impact, turnaround expectation.
2. **Question Guide Adherence (25 pts)**: Address (household residents, territory rates), Add/Remove Driver (DOB, DL#, student discounts), Add/Remove Vehicle (VIN, lienholder, rideshare/Turo check), Legal/Entity documentation.
3. **EZLynx Processing & Billing Standards (20 pts)**: Multi-policy entry, carrier portal submission, agency-bill payment & accounting checklist, AM escalation.
4. **Follow-Up & Carrier Verification (20 pts)**: `Reassign to CSR for follow up` task kept open, 48-hour follow-up cadence, carrier download matched against request.
5. **Final Confirmation & Documentation (10 pts)**: EZLynx folder & label standards, Client Center document delivery, `Policy Change Processed` closeout note.

---

## 📂 File Structure

```
/Users/carloferrara/.gemini/antigravity/scratch/
├── data/
│   ├── sop1_new_business_rubric.json        # Structured JSON rubric for New Business
│   ├── sop2_policy_change_rubric.json       # Structured JSON rubric for Policy Changes
│   └── test_cases/                          # Benchmark scenarios
│       ├── nb_case_01_compliant_producer.json
│       ├── nb_case_02_quote_emailed_first_fail.json
│       ├── nb_case_03_csr_intake_decs_fail.json
│       ├── pc_case_01_flawless_add_driver_vehicle.json
│       ├── pc_case_02_address_change_missed_drivers.json
│       └── pc_case_03_agency_bill_unpaid_bind_fail.json
├── engine/
│   └── qa_evaluator.rb                      # Core CLI scoring engine and evaluator
├── dashboard/
│   └── index.html                           # Standalone Generative UI QA Dashboard
└── README.md
```

---

## 🛠️ How to Run & Test

### 1. Run the Terminal Benchmark Suite
```bash
ruby engine/qa_evaluator.rb
```

### 2. Launch the Interactive Dashboard
Open `dashboard/index.html` in any web browser:
```bash
open dashboard/index.html
```
* Use the top dropdown to switch between **New Business** and **Policy Change Request**.
* Click on any of the **Benchmark Pills** to instantly load test data and observe the live QA scorecard, score ring, non-negotiable alerts, and coaching notes.
* Paste your own team's RingCentral metrics, Magellan sentiment, EZLynx notes, or call transcripts to audit live interactions on the fly!
