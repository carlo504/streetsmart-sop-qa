# STREETSMART INSURANCE QA SYSTEM — COMPLETE PROJECT HANDOFF DOCUMENT

**Document Version:** 2.0  
**Date:** September 1, 2026  
**Author / System:** StreetSmart AI QA Engineering  
**Project:** Autonomous Standard Operating Procedure (SOP) QA Evaluation Engine & Dashboard  
**Status:** Production-Ready & Tested Across All Departments  

---

## 1. Executive Summary & Project Purpose

The **StreetSmart SOP QA System** is an automated quality assurance evaluation engine and interactive management dashboard designed to audit, score, and provide actionable coaching for agency workflows across three core Standard Operating Procedures:
1. **SOP 1: New Business** (Lead Qualification, 2-3 Market Quoting, CENT Phone Presentation, EFT Binding, SalesCenter).
2. **SOP 2: Policy Change Requests** (Authority Verification, Category Question Guides, EZLynx Processing, 48h Follow-up, Carrier Download Match).
3. **SOP 3: Certificate of Insurance (COI) Requests** (Written Request Intake, Red Flag Screening, Progressive LOB Breakouts, Dedicated Folders, **Mandatory 7-Day Carlo Escalation Rule**).

The system audits multi-source operational data (RingCentral telephony, Magellan sentiment/empathy analysis, EZLynx management system entries, carrier portal logs, and conversation transcripts), enforces agency **Non-Negotiables** with zero-tolerance critical failures, scores submissions out of **100 points**, and outputs role-specific coaching plans.

> [!IMPORTANT]
> **Data Sanitization & Privacy Standard:** All datasets, test cases, JSON files, Ruby evaluation scripts, and UI dashboards use **100% synthetic, anonymized demo accounts** (e.g., `Alex & Sarah Morgan`, `Metro Auto Body & Towing LLC`, `Apex Hauling & Logistics LLC`, `Horizon Freightways LLC`, `Pinnacle Mechanical Contractors LLC`). Zero real agency customer PII exists in this codebase.

---

## 2. Directory & Repository Structure

```
/Users/carloferrara/.gemini/antigravity/scratch/
├── data/
│   ├── sop1_new_business_rubric.json       # 100-pt rubric & checkpoints for SOP 1
│   ├── sop2_policy_change_rubric.json      # 100-pt rubric & checkpoints for SOP 2
│   ├── sop3_coi_rubric.json                # 100-pt rubric & checkpoints for SOP 3
│   ├── department_test_cases.json          # 12 synthetic benchmark test cases (PL, CL, TRK)
│   └── test_cases/                         # Standalone test case JSON files
│       ├── nb_tc_01_flawless_producer_sal.json
│       ├── nb_tc_02_critical_failure_emai.json
│       ├── nb_tc_03_major_flag_csr_reques.json
│       ├── pc_tc_01_flawless_csr_add_driv.json
│       ├── pc_tc_02_critical_failure_addr.json
│       ├── pc_tc_03_critical_failure_unpa.json
│       ├── coi_tc_01_flawless_commercial_general_con.json
│       ├── coi_tc_02_critical_failure_unsupported_pr.json
│       ├── coi_tc_03_compliant_trucking_uiia_intermo.json
│       └── coi_tc_04_critical_failure_9_day_pending_.json
├── engine/
│   ├── qa_evaluator.rb                     # Core Ruby evaluation engine
│   └── run_department_audits.rb            # Department benchmark suite runner & summary matrix
├── dashboard/
│   ├── index.html                          # Interactive QA & Coaching Dashboard (UI)
│   └── cases_data.json                     # Synthetic test cases payload for UI
└── HANDOFF_DOCUMENT.md                     # Markdown handoff documentation (this document)
```

---

## 3. Standard Operating Procedures & Rubric Specifications

### SOP 1: New Business
- **Objective:** Manage incoming personal, commercial, and trucking leads, prepare multi-market quotes within SLA, present quotes live via phone using the CENT objection handling framework, and secure EFT payment prior to binding.
- **SLA:** 5-minute lead response; 2-hour quote preparation; 24-hour client delivery.
- **Non-Negotiables:**
  - `NN_NB_01` (CRITICAL_FAIL): *Never email a quote before presenting it directly on the phone or screen.*
  - `NN_NB_02` (MAJOR_FLAG): *Do not request a declarations page at intake.*
  - `NN_NB_03` (CRITICAL_FAIL): *Never bind or mark Won without EFT monthly or annual authorization.*
- **Scoring Categories (100 pts):**
  1. Intake & Lead Qualification (20 pts)
  2. Quoting & Multi-Market Tracking (20 pts)
  3. Quote Presentation & CENT Objections (25 pts)
  4. Closing, Won Policy & Subjectivity Documentation (20 pts)
  5. Follow-Up Cadence & System Standards (15 pts)

---

### SOP 2: Policy Change Requests
- **Objective:** Process mid-term policy change requests for Personal Lines, Commercial Lines, and Trucking across driver, vehicle, address, and coverage additions with strict verification and follow-up.
- **SLA:** Same-day portal entry; 48-hour follow-up cadence until carrier download verification.
- **Non-Negotiables:**
  - `NN_PC_01` (CRITICAL_FAIL): *Never close or confirm a change request without verified carrier download or official endorsement documents.*
  - `NN_PC_02` (CRITICAL_FAIL): *Never bind an agency-bill endorsement before required payment or finance confirmation is received.*
  - `NN_PC_03` (MAJOR_FLAG): *Never omit EZLynx change request task, notes, signed form, or required coverage selection form.*
- **Scoring Categories (100 pts):**
  1. Client Verification & Core Intake Questions (25 pts)
  2. Question Guide Adherence — Branch Specific (25 pts)
  3. EZLynx Processing & Billing Standards (20 pts)
  4. Task Follow-Up & Carrier Verification (20 pts)
  5. Final Confirmation & Documentation (10 pts)

---

### SOP 3: Certificate of Insurance (COI) Requests
- **Objective:** Issue certificates of insurance with verified carrier coverage, correct holder legal names, attached endorsements (AI, WOS, Completed Operations CG 2010/2037), Progressive LOB breakout, and digital delivery via Client Center.
- **SLA:** `<1 hour` from receipt of written request.
- **Non-Negotiables:**
  - `NN_COI_01` (CRITICAL_FAIL): *Never issue unsupported proof without verified active policy status, required endorsements, or unresolved red flags.*
  - `NN_COI_02` (CRITICAL_FAIL): *Never issue reinstatement proof relying solely on finance company notice without carrier or MGA written confirmation.*
  - `NN_COI_03` (CRITICAL_FAIL): *Never issue proof on uncompleted or unapproved policy changes without EZLynx entry or AM sign-off.*
  - `NN_COI_04` (CRITICAL_FAIL): *Bypassing mandatory Carlo escalation when a certificate request remains pending over 7 calendar days.*
  - `NN_COI_05` (MAJOR_FLAG): *Never accept oral-only certificate requests without obtaining written instructions.*
  - `NN_COI_06` (MAJOR_FLAG): *Never create duplicate certificate holders in EZLynx database.*
- **Scoring Categories (100 pts):**
  1. Intake & Written Verification (20 pts)
  2. Coverage & Red Flag Screening (25 pts)
  3. Master Certificate Preparation (20 pts)
  4. Digital Delivery & Client Center (20 pts)
  5. Tracking & Carlo Escalation Rules (15 pts)

---

## 4. Benchmark Department Audit Results Matrix

All 12 synthetic department scenarios were audited and validated with `run_department_audits.rb`:

| Department | Test ID | Fictitious Insured Profile | Audited Employee | Score | Grade | Status | Root Cause / Key Rule |
|---|---|---|---|:---:|:---:|:---:|---|
| **Personal Lines** | `PL_TC_01` | Alex & Sarah Morgan | Jazmin Molina | 100/100 | A+ | **PASS** | Flawless Producer sales presentation & EFT binding |
| **Personal Lines** | `PL_TC_02` | David & Lisa Miller | Amber Voigt | 41/100 | F | **CRITICAL_FAIL** | `NN_NB_01`: Producer emailed quote before phone presentation |
| **Personal Lines** | `PL_TC_03` | Michael & Elena Vance | Ana Flores | 100/100 | A+ | **PASS** | HNW vehicle addition with umbrella cross-check |
| **Personal Lines** | `PL_TC_04` | Jonathan & Karen Hayes | Ana Flores | 100/100 | A+ | **PASS** | High-value condo master COI with ACORD 101 |
| **Commercial Lines** | `CL_TC_01` | Metro Auto Body & Towing LLC | Carlo Ferrara | 100/100 | A+ | **PASS** | Commercial garagekeepers & towing multi-market quote |
| **Commercial Lines** | `CL_TC_02` | Summit Climate Systems LLC | Andrea Illanes | 100/100 | A+ | **PASS** | Certificate endorsement with blanket AI & primary wording |
| **Commercial Lines** | `CL_TC_03` | Tri-County Roofing & Gutter LLC | Jackie Arriola | 88/100 | F | **CRITICAL_FAIL** | `NN_PC_02`: Bound unpaid $1,800 agency bill endorsement |
| **Commercial Lines** | `CL_TC_04` | Pinnacle Mechanical Contractors | Andrea Illanes | 100/100 | A+ | **PASS** | GC certificate with CG 2010/2037 completed ops |
| **Trucking & Trans** | `TRK_TC_01` | Horizon Freightways LLC | Ricardo Aguilar | 100/100 | A+ | **PASS** | Fleet multi-market binding & Form E filing auth |
| **Trucking & Trans** | `TRK_TC_02` | Apex Hauling & Logistics LLC | Ricardo Aguilar | 100/100 | A+ | **PASS** | CDL driver MVR verification & Cascadia tractor add |
| **Trucking & Trans** | `TRK_TC_03` | Eagle Express Intermodal LLC | Diana Cabrera | 66/100 | F | **CRITICAL_FAIL** | `NN_PC_01`: Premature confirmation on DOT Form E filing |
| **Trucking & Trans** | `TRK_TC_04` | Vanguard Freight Transport LLC | Diana Cabrera | 39/100 | F | **CRITICAL_FAIL** | `NN_COI_04`: 9-day pending COI without Carlo escalation |

---

## 5. How to Run Audits & Launch Dashboard

### 1. Run Complete Department Audits (CLI)
```bash
cd /Users/carloferrara/.gemini/antigravity/scratch
ruby engine/run_department_audits.rb
```

### 2. Run Single Test Case / Custom JSON Audit
```bash
ruby -I engine -e '
  require "qa_evaluator"
  require "json"
  evaluator = StreetSmartQAEvaluator.new
  test_case = JSON.parse(File.read("data/test_cases/coi_tc_01_flawless_commercial_general_con.json"))
  result = evaluator.evaluate(test_case)
  puts "Result: #{result[:score]}/#{result[:max_score]} (#{result[:grade]}) - Status: #{result[:status]}"
'
```

### 3. Launch Interactive Web Dashboard
Open [`dashboard/index.html`](file:///Users/carloferrara/.gemini/antigravity/scratch/dashboard/index.html) in any modern web browser:
- Switch between **Personal Lines**, **Commercial Lines**, and **Trucking & Transportation** tabs.
- Select **SOP 1**, **SOP 2**, or **SOP 3**.
- Click any synthetic test scenario pill to immediately view real-time category score progress bars, non-negotiable alert banners, and customized remediation action items.

---

## 6. How to Upload / Save this Document to Google Drive

To save this Handoff Document directly to your Google Drive:
1. **Option A (Google Docs Copy/Paste)**:
   - Open [Google Docs](https://docs.google.com).
   - Create a new document titled **"StreetSmart SOP QA System — Complete Project Handoff"**.
   - Copy the text of this handoff document or open the HTML file [`HANDOFF_DOCUMENT.html`](file:///Users/carloferrara/.gemini/antigravity/scratch/HANDOFF_DOCUMENT.html) and paste it into Google Docs.
2. **Option B (Direct File Upload)**:
   - In Google Drive, click **New > File upload**.
   - Select `/Users/carloferrara/.gemini/antigravity/scratch/HANDOFF_DOCUMENT.md` or [`HANDOFF_DOCUMENT.html`](file:///Users/carloferrara/.gemini/antigravity/scratch/HANDOFF_DOCUMENT.html).
   - Right-click the uploaded file in Google Drive and select **Open with > Google Docs** to convert it into a collaborative Google Doc.

---

## 7. Future Roadmap & Recommendations

1. **Direct Webhook Integrations**:
   - Connect RingCentral Webhooks to automatically stream call duration, response times, and caller ID verification into the evaluator.
   - Connect Magellan API to parse post-call sentiment and empathy scores automatically.
   - Connect EZLynx Integration Center / Open API to ingest daily discussion threads, folder structures, and tasks.
2. **Automated Weekly Manager Scorecards**:
   - Schedule a weekly cron job to run `run_department_audits.rb` and email consolidated scorecards to department leads (Personal Lines, Commercial Lines, Trucking).
3. **Real-time Alerting for Carlo Escalation Rule**:
   - Set up an automated Slack/email alert to Carlo Ferrara whenever a certificate request in EZLynx reaches Day 7 without resolution.
