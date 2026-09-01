# 📋 StreetSmart SOP QA System — Master Handoff Document

> **Quick Copy/Paste Note**: If you start a brand new Antigravity session on a clean computer, simply copy the **Prompt for Antigravity** below and paste it directly into the chat!

---

## ⚡ 1. Instant Start Prompt for Antigravity at Home

```text
Hi Antigravity! I'm Carlo Ferrara from StreetSmart Insurance. We are continuing development on our automated Quality Assurance (QA) Auditing System.

Please clone and inspect our repository:
https://github.com/carlo504/streetsmart-sop-qa.git

Key System Components:
1. Engine: 100-Point scoring engine (engine/qa_evaluator.rb & engine/run_department_audits.rb) codifying SOP 1: New Business and SOP 2: Policy Change Request with non-negotiable instant failure gates.
2. Data Sources: Integrates RingCentral telephony (response SLA, talk time, warm transfers), Magellan sentiment intelligence (empathy scores, talk-to-listen ratios, CENT objection handling), and EZLynx AMS (account IDs, policy numbers, task memos, download matching).
3. Employee Roster: 85 employees categorized by Producers (Sales) vs CSRs/Technicians/AMs (Servicing).
4. Verified Test Accounts: 9 verified EZLynx accounts across Personal Lines, Commercial Lines, and Trucking & Transportation.
5. Interactive Web Dashboard: Located at dashboard/index.html.

Let's review where we left off in HANDOFF_DOC.md and continue building!
```

---

## 🔗 2. GitHub Repository Information

* **Repository URL**: [`https://github.com/carlo504/streetsmart-sop-qa`](https://github.com/carlo504/streetsmart-sop-qa)
* **Clone URL (HTTPS)**: `https://github.com/carlo504/streetsmart-sop-qa.git`
* **Clone Command**:
  ```bash
  git clone https://github.com/carlo504/streetsmart-sop-qa.git
  cd streetsmart-sop-qa
  ```

---

## 🏢 3. Verified EZLynx Account & Team Assignment Matrix

| Department | EZLynx Acct # | Client / Insured Name | Primary Carrier | Audited Rep & Role | Key Scenario Evaluated |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Personal Lines** | `#93686872` | **Nicole Scrivanich & Jason Santos** | Plymouth Rock & Selective | **Jazmin Molina** (Producer) / Ana Flores (CSR) | Flawless 3-market quote & phone presentation (Pass 100%) |
| **Personal Lines** | `#174421544` | **Martha Parra** | Progressive Insurance | **Amber Voigt** (Producer) | Emailed quote before phone presentation (Critical Fail 47%) |
| **Personal Lines** | `#58768907` | **Dean & Danielle Lacorte** | Chubb Group & Markel | **Ana Flores** (CSR) / **Carlo Ferrara** (Producer) | High-Net-Worth vehicle addition & $5M Umbrella cross-check (Pass 100%) |
| **Commercial Lines** | `#209289444` | **Bobby Os Affordable Auto Body & Super Mario Towing** | Atlantic Casualty & Progressive | **Carlo Ferrara** (Producer) / Andrea Illanes (CSR) | Garage & towing multi-option presentation & binding (Pass 100%) |
| **Commercial Lines** | `#68223048` | **Accutemp Heating & Cooling LLC** | Selective Insurance Company | **Andrea Illanes** (CSR) / Taylor Cimei | Additional insured endorsement & fast COI issuance (Pass 100%) |
| **Commercial Lines** | `#53693496` | **3 Sons Gutter LLC** | Utica First Insurance Company | **Jackie Arriola** (CSR) / **Taylor Cimei** (Producer) | Bound unpaid agency-bill endorsement without payment (Critical Fail 91%) |
| **Trucking & Trans.** | `#34962586` | **Kevin Kosza Trucking LLC** | Progressive Commercial & Liberty | **Ricardo Aguilar** (Producer / CSR) | Fleet binding, cargo limits, Form E filing (Pass 100%) |
| **Trucking & Trans.** | `#220890322` | **STRAIGHT TO THE SOURCE LLC** | Progressive & Diesel Insurance | **Ricardo Aguilar** (CSR / Tech) | Added Freightliner Cascadia + CDL driver + 2FA SMS cab cards (Pass 93%) |
| **Trucking & Trans.** | `#209619419` | **US EAGLE TRANSPORTATION LLC** | GEICO Marine Insurance Company | **Diana Cabrera** (CSR) / **Ricardo Aguilar** (Producer) | Premature confirmation before carrier Form E download (Critical Fail 67%) |

---

## 👥 4. Key Agency Staff Roster (Producers vs. CSRs)

* **Personal Lines**:
  * Producers (Sales): **Carlo Ferrara**, **Jazmin Molina**, **Amber Voigt**
  * CSRs / Account Managers (Servicing): **Ana Flores**, **Daniela Aguilar**, **Mitchell Dean Slagle**, **Ashley Huntley** (Dept Manager)
* **Commercial Lines**:
  * Producers (Sales): **Carlo Ferrara**, **Taylor Cimei**
  * CSRs / Account Managers (Servicing): **Andrea Nicole Illanes**, **Jackie Arriola**, **Lenin Perdomo**, **Sandy Santana** (Dept Manager), **Angie Valladarez**, **Eimy Ramos**
* **Trucking & Transportation**:
  * Producers & Servicing Specialists: **Ricardo Aguilar**, **Carlo Ferrara**
  * CSRs / Technicians: **Diana Cabrera**, **Jose Cabrera**, **Gabriela Chutin** (Dept Manager)

---

## 🚦 5. Codified Non-Negotiable QA Rules (Instant Failure Gates)

### SOP 1: New Business
1. **`NN_NB_01`**: **Never email a quote before presenting it directly on the phone or screen share.** (Critical Fail).
2. **`NN_NB_02`**: **Do not request a declarations page at intake.** Build rapport, capture basic details, and warm-transfer. (Major Flag).
3. **`NN_NB_03`**: **Follow payment rules: EFT required before binding.** (Critical Fail).

### SOP 2: Policy Change Request
1. **`NN_PC_01`**: **Never close or confirm a change request without verified carrier download or official endorsement docs.** (Critical Fail).
2. **`NN_PC_02`**: **Never bind an agency-bill endorsement before required payment or finance confirmation is received.** (Critical Fail).
3. **`NN_PC_03`**: **Never omit EZLynx change request task, notes, or signed change forms.** (Major Flag).

---

## 🚀 6. Execution Commands

* **Launch Interactive Web Dashboard**:
  ```bash
  open dashboard/index.html
  ```
* **Run Automated 9-Case Department Audit Suite**:
  ```bash
  ruby engine/run_department_audits.rb
  ```
* **Run Live Telephony & Sentiment Batch Auditor**:
  ```bash
  ruby engine/live_batch_auditor.rb
  ```
* **Sync Changes to GitHub via Built-in Git Connector or Terminal**:
  ```bash
  git add . && git commit -m "Update QA features" && git push
  ```

---

## 🗺️ 7. Priority Next Steps to Build

1. **Daily Manager Scorecard Alerts**: Build an automated script/webhook to email or Slack daily audit summaries to Ashley Huntley, Sandy Santana, and Gabriela Chutin.
2. **Automated Live Ingestion**: Connect scheduled webhooks to continuously pull RingCentral call recordings and Magellan sentiment transcripts into `data/live_ringcentral_magellan_batch.json`.
3. **Add Remaining Agency SOPs**:
   * **SOP 3: Certificates of Insurance (COI) & Additional Insured Endorsements**
   * **SOP 4: Policy Renewal Review & Remarketing**
   * **SOP 5: Claims Intake & Carrier Reporting**
