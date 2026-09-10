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
| **Commercial Lines** | `#221774967` | **Emio "Sonny" Abagnale** | Selective / Atlantic Casualty / State Farm Exp. | **Carlo Ferrara** (Producer) | Multi-tenant LRO commercial package submission ($7M TIV, 4 tenants) (Pass 100%) |
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

---

## 📁 8. Active Commercial Submission Case File: Emio "Sonny" Abagnale

* **EZLynx Account #**: `#221774967`
* **Applicant**: Emio "Sonny" Abagnale | Sole Proprietorship | DOB: 12/20/1932
* **Contact**: (201) 310-4433 | `sonnycars@yahoo.com` | 20 Lawrence Way, Cedar Grove, NJ 07009
* **Risk Location**: 11–33 Roosevelt Ave, Belleville, NJ 07109 (Essex County)
* **Operations**: 100% Lessor's Risk Only (LRO) — 4 Commercial Tenants:
  * **Lot 11**: Paved Commercial Parking & Staging Area (12,000 SF)
  * **Building 1 (13–15 Roosevelt Ave)**: Auto Body & Collision Repair Shop | 10,000 SF | Flat EPDM Membrane Roof | $3,500,000 Special Form RC ($2,500 Ded)
  * **Building 2 (17–33 Roosevelt Ave)**: Multi-Tenant Wholesale Parts & Heavy Truck Repair | 14,500 SF | Flat EPDM Membrane Roof | $3,500,000 Special Form RC ($2,500 Ded)
* **Commercial General Liability**: $1M / $2M / $2M | Class 61226 (LRO) & Class 67512 (Parking Lot)
* **Loss History & Prior Carrier**: 0 Losses in 5 Years | Prior Carrier: State Farm (~$12,000/yr)
* **Assigned Producer / CSR**: Carlo Ferrara


---

## 📁 9. Active Commercial Submission Case File: Par-Troy LLC

* **Applicant**: Par-Troy LLC | LLC Entity | FEIN: `22-3849102`
* **Contact**: (973) 887-1234 | `info@partroy.com` | 10 Leslie Court, Whippany, NJ 07981 (Morris County)
* **Operations**: Architectural Sheet Metal Fabrication & Rigging (Custom copper, zinc, aluminum exterior cladding, cornice restoration, standing seam roofing, and crane rigging).
* **Workers' Compensation**:
  * Payroll: $1,450,000 (Class Code `5538` Sheet Metal Work & Class `8810` Clerical)
  * Experience Mod: 0.88 (Favorable loss performance)
* **Commercial Auto**: 4 Scheduled Service & Rigging Trucks ($1M CSL Liability).
* **Official Application**: ACORD 125, ACORD 130 (Workers Comp), and ACORD 160 (Business Auto) compiled in `ACORD_125_130_160_ParTroy.pdf`.
* **Guide**: Full carrier strategy and underwriting guidelines documented in `PARTROY_EZLYNX_AND_CARRIER_QUOTING_GUIDE.md`.

---

## 📁 10. Active Commercial Submission Case File: Bayshore Removal Service LLC

* **Applicant**: Bayshore Removal Service LLC | LLC Entity | FEIN: `88-3502449`
* **Contact**: Rafael Rodrigues-Pereira | (908) 675-7211 | `bayshoreremovalservice@gmail.com` | 12 Lotus Court, Ocean Township, NJ 07712 (Monmouth County)
* **Operations**: First call removal & mortuary livery service (0–50 mile radius).
* **Vehicles (9 Total)**: 8 Hearses (Class `007922`, Kia Sedonas) and 1 Limousine (Class `007911`, Cadillac Escalade).
* **Drivers (8 Total)**: All scheduled with verified NJ driver licenses and clean MVRs.
* **Loss History**: 4 full policy periods verified Loss-Free (0 claims across 2022–2026, Prior carrier: Selective `S2290479`).
* **Merchants Mutual Insurance Portal (`CAPW326867`)**:
  * Successfully quoted and rated at **$14,686.00** annual premium ($1M CSL Liability, $1M UM/UIM, PIP).
* **Plymouth Rock Assurance (`PACQ0002168096`)**:
  * Named insured corrected from Par-Troy to `Bayshore Removal Service LLC`.
  * All 9 vehicles and 8 drivers entered and saved.
* **Guide**: Full VIN list, driver licenses, and portal breakdown documented in `BAYSHORE_REMOVAL_SERVICE_COMMERCIAL_AUTO_GUIDE.md`.

---

## 🛠️ 11. Carrier Quoting Portals & Engineering Learnings

1. **Merchants Mutual Insurance Group (`secure1.merchantsgroup.com`)**:
   * Agency Account: STREETSMART RISK MANAGERS INC (`84409`).
   * When navigating from the "Premium Summary" screen into subsequent tabs ("Underwriting Questions" / "Referrals"), the carrier's application gateway can trigger an internal session redirect back to the logon page (`secure.merchantsgroup.com`).
   * **Persistence**: Quotes persist in the database under their reference number (e.g. `CAPW326867`), retaining rated premiums, scheduled vehicles, and driver entries.
2. **Plymouth Rock Assurance Portal (`agentweb1.plymouthrock.com`)**:
   * **XML Schema Bug**: The rating submission schema enforces a strict 15-character length limit on the `<PRIOR_CARR>` element. Entering full legal carrier names such as `"Selective Insurance"` (19 chars) causes an unhandled schema exception that triggers an underwriter referral. Use abbreviations (e.g. `"Selective Ins"` or `"Selective"`) to pass schema validation.
3. **GEICO Gateway Commercial (`gateway.geico.com`)**:
   * Authentication requires Azure AD B2C Single Sign-On and multi-factor SMS code verification.
   * Commercial lines appetite checks reside under **"B and C" (Business and Commercial)** -> **"Check Appetite"**.
   * Not integrated into comparative raters (Tarmika / EZLynx) for independent agencies. Alternative agency access for Berkshire Hathaway commercial lines is available via **Berkshire Hathaway GUARD** (`gigezrate.guard.com`).
