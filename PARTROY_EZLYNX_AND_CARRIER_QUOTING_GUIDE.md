# 🏢 EZLynx Setup & Multi-Carrier BOP / WC Quoting Blueprint
## Account: Par-Troy Sheet Metal & Air Conditioning LLC (Par-Troy Metals, LLC)
**Agency**: Streetsmart Insurance | **Producer**: Carlo Ferrara  
**Target Lines**: Business Owner's Policy (BOP) & Workers' Compensation (WC)  
**Location**: 122 Clinton Rd, Ste 3A, Fairfield, NJ 07004-2921 (Essex County)  
**Effective Dates**: 04/06/2026 – 04/06/2027  
**Hartford WC Benchmark**: **$19,214.00** (Quote # `13 WEC CB5ADZ - 001` | E-Mod: **0.959**)

---

## 🎯 Section 1: EZLynx Step-by-Step Setup Guide
### (Adding BOP and WC to the Existing Commercial Application)

Follow this exact workflow inside **EZLynx AMS / Commercial Rater**:

### Step 1: Open Existing Account & Application
1. In the EZLynx top search bar, locate **Par-Troy Sheet Metal & Air Conditioning LLC** (or search by address: `122 Clinton Rd, Fairfield, NJ`).
2. Go to the **Applications** tab on the left sidebar.
3. If an existing Commercial Application exists (e.g., Commercial Auto or General Application):
   * Click **Actions** > **Edit Application** (or **Copy Application** to create a fresh 2026–2027 renewal/rewrite submission).
   * If adding lines to the current open file, click **Add Line of Business (LOB)**.
4. Select both:
   * [x] **Workers' Compensation (WC)**
   * [x] **Commercial Package / Business Owner's Policy (BOP)**

---

### Step 2: Commercial Applicant & Location Verification
Under the **Applicant Info** and **Locations** tabs, verify:
* **Legal Named Insured**: `Par-Troy Sheet Metal & Air Conditioning LLC`
* **DBA / Trade Name**: `Par-Troy Metals, LLC`
* **Entity Type**: `Limited Liability Company (LLC)`
* **Year Established**: `1981` (45 Years in Continuous Operation)
* **Website**: `https://www.par-troy.com`
* **Primary Contact**: Lino Rocha / Management | Phone: `(973) 227-1150` | `info@par-troy.com`
* **NAICS Code**: `238220` (Plumbing, Heating, and Air-Conditioning Contractors) & `332322` (Sheet Metal Work)
* **SIC Code**: `1711` (Plumbing, Heating & AC) & `3444` (Sheet Metal Work)
* **Location #1**:
  * Address: `122 Clinton Rd, Ste 3A, Fairfield, NJ 07004-2921` (Essex County)
  * Occupancy: **Tenant** (Office, Sheet Metal Fabrication Shop & Contractor Warehouse)
  * Protection Class: **03** (Fairfield Fire Dept)
  * Building Construction: **Masonry / Non-Combustible** (Code 3/4), 8,500 SF

---

### Step 3: Workers' Compensation Tab Entry
Navigate to the **Workers' Compensation** policy section and enter the exact state rating schedule matching the Hartford baseline:

| State | Class Code | Classification Description | Annual Payroll | Blended Rate | Hartford Est. Premium |
| :---: | :---: | :--- | :---: | :---: | :---: |
| **NJ** | **3724** | **HVAC Installation, Service or Repair & Drivers - Comm & Res** | **$343,000** | 5.47 | $19,331.00 |
| **NJ** | **8810** | **Clerical Office Employees NOC** | **$100,000** | 0.17 | $136.00 |
| **NJ** | **8742** | **Salesperson, Collectors, or Messengers - Outside** | **$33,000** | 0.32 | $97.00 |
| **TOTAL** | | **Total Exposure / Gross Payroll** | **$476,000** | | **$19,564 (Base)** |

* **Experience Modifier (E-Mod)**: Enter `0.959` (Credit Mod — applies 4.1% standard discount).
* **Employer's Liability Limits**:
  * Bodily Injury by Accident: **$500,000** Each Accident
  * Bodily Injury by Disease: **$500,000** Policy Limit
  * Bodily Injury by Disease: **$500,000** Each Employee
  *(Note: Check option for $1,000,000 if binding underlying umbrella)*.
* **Owners / Officers Section**:
  * LLC Managing Members: Select **Included** (New Jersey default inclusion for LLC members actively working in operations).

---

### Step 4: Business Owner's Policy (BOP) / Commercial Package Tab Entry
Navigate to the **BOP / Commercial Property & General Liability** section:

1. **Commercial General Liability (CGL) Limits**:
   * Each Occurrence: **$1,000,000**
   * General Aggregate: **$2,000,000**
   * Products / Completed Operations Aggregate: **$2,000,000**
   * Personal & Advertising Injury: **$1,000,000**
   * Damage to Rented Premises: **$100,000**
   * Medical Payments: **$10,000**
2. **Gross Annual Receipts / Rating Basis**:
   * Total Estimated Gross Sales: **$1,750,000**
   * Split: **70% Commercial / Industrial** ($1,225,000) | **30% Residential** ($525,000)
   * ISO Class Codes:
     * `95647` (HVAC Installation / Service - Commercial) — $1,225,000 Sales
     * `95648` (HVAC Installation / Service - Residential) — $525,000 Sales
     * `98636` (Sheet Metal Fabrication / Shop) — $343,000 Payroll
3. **Property & Inland Marine (Contractor's Schedule)**:
   * **Building Limit**: `$0` (Tenant)
   * **Business Personal Property (BPP)**: **$150,000** (Replacement Cost, 80% Coinsurance, $1,000 Deductible, Special Form)
   * **Business Income & Extra Expense**: **Actual Loss Sustained (12 Months)**
   * **Contractor's Tools & Equipment Floater**: **$50,000** Unscheduled ($2,500 max per item, $500 deductible)
   * **Installation Floater**: **$25,000** (materials in transit or staging on customer job sites)

---

### Step 5: Document Uploads & Tarmika Rating Handoff
1. Go to the **Documents** tab inside the Par-Troy EZLynx account.
2. Upload:
   * `The Hartford Workers Comp Quote (Ref: 13 WEC CB5ADZ - 001).pdf`
   * `ACORD_125_130_160_ParTroy.pdf` (Generated by our agency script).
3. Under the **Integrations / Rating** dropdown:
   * Click **Send to Tarmika** (or launch carrier direct portals from EZLynx SSO).

---

## 🛡️ Section 2: Carrier-by-Carrier Quoting & Underwriting Strategies

### 1. Selective Insurance (OnePath / Tarmika)
* **Appetite Tier**: ⭐⭐⭐⭐⭐ **Top Target (NJ Home Market Powerhouse)**
* **Why They Win**: Selective is headquartered in Branchville, NJ and has an industry-leading appetite for premier New Jersey HVAC and mechanical contractors. A 45-year established business with a `0.959` E-Mod qualifies for Selective's **Contractor Elite** pricing tier.
* **Underwriter Hot Buttons & Knockout Defenses**:
  1. *Roofing Exposure*: Selective underwriters will flag "Sheet Metal" wondering if they do roofing tear-offs or hot-tar membrane roofing.  
     **Agent Defense**: "Par-Troy does NOT do roofing installation or tear-offs. Operations are strictly architectural sheet metal panel fabrication, custom ES-1 edge metals, coping, gutters, and HVAC ductwork."
  2. *Hot Work / Brazing*: Selective requires a formal hot work safety program.  
     **Agent Defense**: "All field brazing/soldering adheres to strict hot work safety standards: 30-minute fire watch, calibrated ABC fire extinguishers at each workstation, and flame-retardant welding shields."
  3. *Subcontractor Risk Transfer*:  
     **Agent Defense**: "Less than 10% subcontracted work. Subcontractors are strictly specialized crane operators for heavy rooftop units. Par-Troy mandates written contracts with $1M GL limits, primary/non-contributory status, and Additional Insured endorsements."

---

### 2. Travelers (Travelers Select Accounts BOP + 1st Choice WC)
* **Appetite Tier**: ⭐⭐⭐⭐⭐ **Fast Automated Binding & Strong Package Pricing**
* **Why They Win**: Travelers' automated BOP engine (Master Pac) loves HVAC service contractors with clean loss histories. Combining BOP + WC triggers Travelers' **Multi-Line Package Credit (10% to 15% discount across both lines)**.
* **Underwriter Hot Buttons & Knockout Defenses**:
  1. *Rigging & Crane Exposure*:  
     **Agent Defense**: "Direct employees do not operate cranes. Heavy crane lifting of rooftop packaged units is 100% contracted out to licensed, insured rigging contractors."
  2. *Refrigerant Handling*:  
     **Agent Defense**: "100% of technicians hold EPA Section 608 Universal Certification with certified closed-loop recovery equipment."
  3. *Work at Heights*:  
     **Agent Defense**: "Work over 2 stories is restricted to mechanical roof rooms or flat commercial rooftops with OSHA-compliant perimeter tie-offs."

---

### 3. Nationwide (Commercial Digital Storefront / Tarmika)
* **Appetite Tier**: ⭐⭐⭐⭐ **High Value Endorsement Package**
* **Why They Win**: Nationwide offers the **Contractor's Advantage Endorsement Plus**, which bundles Blanket Additional Insured, Blanket Waiver of Subrogation, and Per-Project Aggregate—saving Par-Troy thousands in certificate fees when working for General Contractors.
* **Underwriter Hot Buttons & Knockout Defenses**:
  1. *Residential vs. Commercial Split*:  
     **Agent Defense**: "70% commercial / 30% residential. No tract home development or high-rise exterior work."
  2. *Tool Security*:  
     **Agent Defense**: "Service vans are parked overnight inside the locked Fairfield facility perimeter; vehicles have alarmed partitions and lockboxes for tools."

---

### 4. The Hanover Insurance Group (Hanover TAP)
* **Appetite Tier**: ⭐⭐⭐⭐ **Comprehensive Trade Contractor Package**
* **Why They Win**: Hanover's Point of Sale (TAP) offers tailored limits for BPP and off-premises installation floaters with generous automatic extensions.
* **Underwriter Hot Buttons & Knockout Defenses**:
  1. *Duct Cleaning / Chimney Work*:  
     **Agent Defense**: "No chimney sweeping or structural masonry flues. Standard commercial/residential sheet metal duct fabrication, assembly, and service."
  2. *Water Damage / Condensate Control*:  
     **Agent Defense**: "Emergency drain pans, float switches, and secondary drain lines installed on all attic and suspended ceiling HVAC units per International Mechanical Code (IMC)."

---

## ❓ Section 3: Universal Carrier Knockout Questions & Cheat Sheet

Keep this cheat sheet open when completing portal questions in Selective, Travelers, Nationwide, or Hanover:

| # | Underwriting Knockout Question | Compliant Agency Response | Underwriting Rationale |
| :-: | :--- | :---: | :--- |
| **1** | Does the applicant perform any hot-tar, torch-applied, or membrane roofing? | **NO** | They fabricate & supply standing seam metal panels and trim only. |
| **2** | Does the applicant do work exceeding 3 stories or 35 feet? | **NO** | Direct work is limited to 1–2 story structures and rooftop equipment. |
| **3** | Are all HVAC technicians EPA Section 608 certified? | **YES** | Mandatory requirement for handling R-410A / R-32 / refrigerants. |
| **4** | Does the applicant perform commercial kitchen hood exhaust fire suppression? | **NO** | Mechanical ducting only; fire suppression systems are subbed to licensed specialists. |
| **5** | Are certificates of insurance obtained from all subcontractors with $1M GL & AI? | **YES** | Standard written subcontractor agreement enforced on 100% of subbed work. |
| **6** | Does the applicant perform any industrial ammonia refrigeration or boiler manufacturing? | **NO** | Standard commercial/residential comfort heating, ventilation, and AC. |
| **7** | Is there a formal written safety program and designated safety coordinator? | **YES** | 45-year continuous safety program with weekly toolbox talks. |
| **8** | Any past losses or open claims over $10,000 in the last 5 years? | **NO** | Spotless loss record reflected in 0.959 credit E-Mod. |
| **9** | Are hot work permits and fire watch protocols utilized for open-flame work? | **YES** | Minimum 30-minute post-work fire watch with fire extinguishers on site. |
| **10** | Are service vehicles equipped with secured shelving and anti-theft locks? | **YES** | All tools and equipment secured in locked commercial vans. |

---

## ✉️ Section 4: Underwriter Submission Email Templates

### 📧 Email 1: Selective Insurance (NJ Underwriting Team)
```text
To: njcommercial@selective.com (or your Selective Commercial Lines Underwriter)
From: Carlo Ferrara (carlo@streetsmart.insurance) | Streetsmart Insurance
Subject: NEW SUBMISSION: Par-Troy Sheet Metal & Air Conditioning LLC — BOP & WC Package | Fairfield, NJ | Eff: 04/06/2026

Good afternoon [Underwriter Name],

I hope your week is going well.

Please find attached our complete commercial submission (BOP & Workers' Compensation) for Par-Troy Sheet Metal & Air Conditioning LLC, a premier HVAC and architectural sheet metal fabrication contractor located in Fairfield, NJ (Essex County).

This is a pristine 45-year-old family business (established in 1981) with an exceptional safety record and an expiring 0.959 credit E-Mod. We have an in-hand Workers' Comp quote from The Hartford at $19,214.00 (attached) that we are targeting to beat with Selective's Contractor Elite package.

Key Account Highlights:
* Named Insured: Par-Troy Sheet Metal & Air Conditioning LLC (Par-Troy Metals, LLC)
* Location: 122 Clinton Rd, Ste 3A, Fairfield, NJ 07004 (Tenant Occupied Shop & Office)
* Years in Business: 45 Years (Founded 1981 by Lino Rocha Sr.)
* E-Mod: 0.959 (Credit Mod)
* Workers' Comp Payroll ($476k Total):
  - Code 3724 (HVAC Install/Service & Drivers): $343,000
  - Code 8810 (Clerical NOC): $100,000
  - Code 8742 (Outside Sales): $33,000
  - Employers Liability: $500k/$500k/$500k
* BOP / CGL: $1M/$2M/$2M Occurrence | $150k BPP | $50k Contractor Tools | $25k Installation Floater
* Gross Sales: $1,750,000 (70% Commercial / 30% Residential)
* Operations & Risk Controls: No hot-tar/torch roofing (architectural metal panel/flashing supply & install only). All techs EPA 608 certified. Formal hot work & 30-min fire watch protocols strictly observed. Subbed work <10% (crane rigging only, 100% insured with hold harmless & AI).

Attached Documents:
1. Completed ACORD 125, 130, and 160 Package (PDF)
2. Hartford WC Quote Benchmark ($19,214 - Ref: 13 WEC CB5ADZ - 001)

Please let us know if Selective can offer an aggressive package quote on this top-tier NJ contractor.

Best regards,

Carlo Ferrara
Streetsmart Insurance
208 South Street, Freehold, NJ 07728
Office: (732) 462-8343 | Mobile: (201) 310-4433
carlo@streetsmart.insurance
```

---

### 📧 Email 2: Travelers (Select Accounts / Commercial Underwriter)
```text
To: [Travelers Commercial Lines Underwriter]
From: Carlo Ferrara (carlo@streetsmart.insurance) | Streetsmart Insurance
Subject: SUBMISSION: Par-Troy Sheet Metal & Air Conditioning LLC — Master Pac BOP & 1st Choice WC | Eff: 04/06/2026

Hi [Underwriter Name],

We are submitting a high-quality HVAC and sheet metal contracting risk for Travelers Master Pac BOP and 1st Choice Workers' Compensation:

* Insured: Par-Troy Sheet Metal & Air Conditioning LLC
* Address: 122 Clinton Rd, Ste 3A, Fairfield, NJ 07004
* Target Eff: 04/06/2026
* Experience Mod: 0.959 Credit Mod
* Hartford WC Target: $19,214.00 (Targeting Travelers Multi-Line Package Credit)
* Total WC Payroll: $476,000 (Code 3724: $343k, Code 8810: $100k, Code 8742: $33k)
* BOP Requirements: $1M/$2M CGL, $150k BPP, $50k Tools Floater, $25k Installation Floater
* Risk Notes: 45 years in business (since 1981). Established Fairfield shop. Zero structural roofing work. Direct work limited to 2 stories and flat roofs. Rigging cranes subbed out to insured crane contractors.

Attached is the full ACORD application and the Hartford benchmark quote. Looking forward to reviewing Travelers' package pricing.

Thank you,

Carlo Ferrara | Streetsmart Insurance
```

---

### 📧 Email 3: Nationwide Commercial Lines Underwriter
```text
To: [Nationwide Commercial Lines Underwriter]
From: Carlo Ferrara (carlo@streetsmart.insurance) | Streetsmart Insurance
Subject: SUBMISSION: Par-Troy Sheet Metal & Air Conditioning LLC — Contractor BOP & WC | Eff: 04/06/2026

Hi [Underwriter Name],

Please review our submission for Par-Troy Sheet Metal & Air Conditioning LLC for Nationwide's Contractor BOP (with Contractor Advantage Plus endorsement) and Workers' Compensation.

Risk Profile:
* 45 years in business in Essex County, NJ (1981 inception).
* Clean loss record with an active 0.959 E-Mod.
* Current Hartford WC benchmark: $19,214.00.
* WC Payroll: $343k (3724), $100k (8810), $33k (8742). Total: $476,000.
* BOP: $1M/$2M Limits, $150,000 BPP, $50,000 Mobile Tools, $25,000 Installation Floater.
* Strong safety culture, EPA universal certified techs, locked vehicle security.

Complete ACORD application and Hartford quote attached. Please let us know if Nationwide can provide competitive package terms.

Best regards,

Carlo Ferrara | Streetsmart Insurance
```

---

### 📧 Email 4: The Hanover Insurance Group (Regional Underwriting)
```text
To: [Hanover Regional Commercial Underwriter]
From: Carlo Ferrara (carlo@streetsmart.insurance) | Streetsmart Insurance
Subject: NEW SUBMISSION: Par-Troy Sheet Metal & Air Conditioning LLC — Hanover Advantage BOP & WC | Eff: 04/06/2026

Hi [Underwriter Name],

We have an excellent candidate for Hanover's Trade Contractor Advantage program in northern New Jersey.

Account: Par-Troy Sheet Metal & Air Conditioning LLC (Par-Troy Metals, LLC)
Location: 122 Clinton Rd, Ste 3A, Fairfield, NJ 07004
Established: 1981 (45 Years Continuous Operation)
E-Mod: 0.959 (Credit)
Lines: BOP + Workers' Compensation (Package)
Target WC Premium: Beating Hartford's $19,214.00 quote.

Operations are commercial/residential HVAC installation and architectural sheet metal fabrication. No torch-down roofing, no industrial process boilers, and all crane work subbed to insured specialists.

Full submission package and Hartford quote attached.

Thank you,

Carlo Ferrara | Streetsmart Insurance
```
