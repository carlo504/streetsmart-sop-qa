# 🚗 Bayshore Removal Service LLC — Commercial Auto Quoting & Rating Master Guide

## 📌 Account & Entity Overview
* **Legal Entity Name**: `BAYSHORE REMOVAL SERVICE LLC`
* **Entity Type**: Limited Liability Company (LLC)
* **FEIN**: `88-3502449`
* **Phone**: `(908) 675-7211`
* **Email**: `bayshoreremovalservice@gmail.com`
* **Primary Contact**: Rafael Rodrigues-Pereira
* **Mailing / Garaging Address**: `12 Lotus Court, Ocean Township, NJ 07712-7200` (Monmouth County, Rating Territory 116)
* **Business Start Date**: 01/01/2022 (4 Years in Continuous Business)
* **SIC Code**: `7261` (Funeral Service and Crematories)
* **NAICS Code**: `812210` (Funeral Homes and Funeral Services)
* **Operations**: First call removal & mortuary livery service. Transports deceased from hospitals, residences, and nursing facilities to funeral home preparation rooms and morgues.
  * Operating Radius: Local (0–50 miles)
  * Seasonality: Non-seasonal (year-round)
  * Staff: 10 full-time employees, 1 principal/owner, 1 licensed funeral director (no embalming operations on site).

---

## 🚘 Scheduled Vehicles (9 Total)
All garaged at `12 Lotus Court, Ocean Township, NJ 07712`:

| # | Year | Make / Model | VIN | Vehicle Classification | Class Code | Stated / Cost New |
| :- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 2015 | Kia Sedona LX | `KNDMB5C16F6055877` | Funeral Director - Hearse | `007922` | $25,900 |
| 2 | 2016 | Kia Sedona L | `KNDMA5C12G6173090` | Funeral Director - Hearse | `007922` | $26,400 |
| 3 | 2017 | Kia Sedona LX | `KNDMB5C10H6242633` | Funeral Director - Hearse | `007922` | $28,900 |
| 4 | 2016 | Kia Sedona L | `KNDMA5C1XG6106902` | Funeral Director - Hearse | `007922` | $26,400 |
| 5 | 2016 | Cadillac Escalade | `1GYS4DKJ4GR107496` | Limousine (Employee Operated) | `007911` | $72,970 |
| 6 | 2016 | Kia Sedona LX | `KNDMB5C12G6133816` | Funeral Director - Hearse | `007922` | $26,400 |
| 7 | 2019 | Kia Sedona L | `KNDMA5C14K6539138` | Funeral Director - Hearse | `007922` | $27,400 |
| 8 | 2017 | Kia Sedona L | `KNDMA5C1XH6282866` | Funeral Director - Hearse | `007922` | $28,900 |
| 9 | 2017 | Kia Sedona L | `KNDMA5C1XH6291678` | Funeral Director - Hearse | `007922` | $28,900 |

*Note: Replacement / Alternate VIN for Escalade: 2023 Cadillac Escalade (`1GYS4BKL1PR228458`).*

---

## 👨‍✈️ Scheduled Drivers (8 Total — All NJ Licensed)
All drivers confirmed with clean MVRs (0 moving violations, 0 at-fault accidents):

1. **Eduardo Assis** | DOB: `04/03/1978` | Gender: Male | NJ DL: `A80581926104782`
2. **Eduardo Machado** | DOB: `08/25/1981` | Gender: Male | NJ DL: `M00431920008812`
3. **Paulo Matos** | DOB: `06/17/1994` | Gender: Male | NJ DL: `F08806196806942`
4. **Fabio Braga** | DOB: `08/05/1990` | Gender: Male | NJ DL: `D67292580008906`
5. **Matheus Dayrell** | DOB: `11/21/1989` | Gender: Male | NJ DL: `D09725280011892`
6. **Gabriel Rodigues** | DOB: `06/06/1993` | Gender: Male | NJ DL: `R60942706806931`
7. **Janice Cruz** | DOB: `02/18/1984` | Gender: Female | NJ DL: `C76903857952842`
8. **Mario Machado** | DOB: `02/06/1981` | Gender: Male | NJ DL: `B72105196102812`

---

## 🛡️ Policy Coverages & Limits
* **Combined Single Limit (CSL) Liability**: `$1,000,000` (Symbol 7 — Specifically Described Autos)
* **Uninsured / Underinsured Motorist (UM/UIM)**: `$1,000,000 CSL` (Symbol 6 & 7)
* **Personal Injury Protection (PIP)**: Primary / Statutory (Symbol 5 & 7)
* **Physical Damage**: Not Wanted (No Comprehensive, No Collision)
* **Medical Payments / Extended Non-Owned**: Excluded as requested.

---

## 📜 Prior Carrier & Loss History
* **Prior Carrier**: Selective Insurance Company
* **Policy Number**: `S2290479`
* **Expiring Term**: `08/25/2025 – 08/25/2026`
* **Loss History**: 4 Full Policy Periods verified Loss-Free (0 claims, $0 incurred, $0 reserved across 2022–2026).

---

## 🏢 Carrier Quoting Portals Status & Learned Quirks

### 1. Merchants Mutual Insurance Portal
* **Quote Reference**: `CAPW326867`
* **Agency Code**: STREETSMART RISK MANAGERS INC (`84409`)
* **Underwriting Company**: Merchants Mutual Insurance Company
* **Status**: **Quoted & Rated**
* **Calculated Annual Premium**: **$14,686.00** (Valid until 10/08/2026)
* **Carrier Portal Quirk**:
  * Navigating across the final Underwriting Questions / Finish Application tab can trigger an internal session timeout (HTTP 500 or redirect to `secure.merchantsgroup.com/cgi-bin/lansaweb`). The quote remains safely saved under `CAPW326867` in recent quotes.

### 2. Plymouth Rock Assurance
* **Quote Reference**: `PACQ0002168096`
* **Status**: Saved in Quoting Portal
* **Insured Name**: Corrected from `Par-Troy LLC` to `Bayshore Removal Service LLC`.
* **All 9 Vehicles & 8 Drivers**: Keyed and saved.
* **Rating Engine Bug & Resolution**:
  * Plymouth Rock's XML backend enforces a strict **15-character length constraint** on the `PRIOR_CARR` schema tag. Entering `"Selective Insurance"` (19 characters) causes an unhandled schema overflow that triggers an automated underwriter referral hold. Truncating to `"Selective Ins"` or `"Selective"` circumvents the schema validation failure.

### 3. GEICO Gateway Commercial (`gateway.geico.com`)
* **Authentication Workflow**: Azure AD B2C Single Sign-On requires manual broker login followed by multi-factor authentication (SMS verification code to mobile phone).
* **Commercial Appetite Navigation**: In the GEICO Gateway dashboard, Commercial Auto appetite checks are located under **"B and C" (Business and Commercial)** -> **"Check Appetite"**.
* **Integration Status**: GEICO Commercial does not support direct agency comparative rating via Tarmika Bridge or EZLynx; policies must be evaluated through Gateway B&C or placed via Berkshire Hathaway GUARD.

### 4. Berkshire Hathaway GUARD (`gigezrate.guard.com`)
* **Agency Login**: Active under username `cferrara2`.
* **Fit**: Strong agency market for funeral livery and service vehicles within Berkshire Hathaway group.
