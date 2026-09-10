#!/usr/bin/env python3
"""
ACORD 125, 130, 160 PDF Generator for Par-Troy Sheet Metal & Air Conditioning LLC
Generates a clean, professional, multi-page ACORD application PDF ready for carrier submission.
"""
import sys

def escape(s):
    if not isinstance(s, str):
        s = str(s)
    s = s.replace('\u2014', '--').replace('\u2013', '-').replace('\u2022', '*')
    s = s.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

class PDFCanvas:
    def __init__(self):
        self.cmd = []

    def set_stroke_color(self, r, g, b):
        self.cmd.append(f"{r:.3f} {g:.3f} {b:.3f} RG")

    def set_fill_color(self, r, g, b):
        self.cmd.append(f"{r:.3f} {g:.3f} {b:.3f} rg")

    def set_line_width(self, w):
        self.cmd.append(f"{w:.2f} w")

    def rect(self, x, y, w, h, fill=False, stroke=True):
        self.cmd.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")
        if fill and stroke:
            self.cmd.append("B")
        elif fill:
            self.cmd.append("f")
        else:
            self.cmd.append("S")

    def text(self, x, y, string, font="F1", size=10, rgb=(0, 0, 0)):
        self.set_fill_color(*rgb)
        self.cmd.append(f"BT /{font} {size} Tf {x:.2f} {y:.2f} Td ({escape(string)}) Tj ET")

    def line(self, x1, y1, x2, y2, stroke_rgb=(0.8, 0.8, 0.8), width=1):
        self.set_stroke_color(*stroke_rgb)
        self.set_line_width(width)
        self.cmd.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def get_stream(self):
        return "\n".join(self.cmd)


class SimplePDFDocument:
    def __init__(self):
        self.pages = []

    def add_page(self, canvas):
        self.pages.append(canvas.get_stream())

    def render(self):
        num_pages = len(self.pages)
        objs = []
        objs.append("<< /Type /Catalog /Pages 2 0 R >>")
        page_refs = [f"{3 + i*2} 0 R" for i in range(num_pages)]
        objs.append(f"<< /Type /Pages /Kids [{ ' '.join(page_refs) }] /Count {num_pages} >>")

        font_helv_id = 3 + num_pages * 2
        font_bold_id = 4 + num_pages * 2

        for i, stream_content in enumerate(self.pages):
            content_id = 3 + i * 2 + 1
            objs.append(
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_helv_id} 0 R /F2 {font_bold_id} 0 R >> >> "
                f"/Contents {content_id} 0 R >>"
            )
            raw_bytes = stream_content.encode("latin1")
            objs.append(f"<< /Length {len(raw_bytes)} >>\nstream\n{stream_content}\nendstream")

        objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

        out = bytearray(b"%PDF-1.4\n")
        xref = [0]
        for i, obj_str in enumerate(objs):
            pos = len(out)
            xref.append(pos)
            out.extend(f"{i+1} 0 obj\n{obj_str}\nendobj\n".encode("latin1"))

        startxref = len(out)
        out.extend(f"xref\n0 {len(xref)}\n0000000000 65535 f \n".encode("latin1"))
        for offset in xref[1:]:
            out.extend(f"{offset:010d} 00000 n \n".encode("latin1"))
        out.extend(f"trailer\n<< /Size {len(xref)} /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode("latin1"))
        return bytes(out)


def draw_common_header(c, title, subtitle, page_num):
    # Top banner background - Dark Navy
    c.set_fill_color(0.08, 0.22, 0.45) # Professional Navy #143872
    c.rect(36, 730, 540, 36, fill=True, stroke=False)
    
    # Title
    c.text(46, 744, title, font="F2", size=11, rgb=(1, 1, 1))
    c.text(475, 744, f"PAGE {page_num} OF 3", font="F2", size=9, rgb=(0.85, 0.9, 1))

    # Sub-banner info
    c.set_fill_color(0.94, 0.96, 0.99)
    c.set_stroke_color(0.8, 0.85, 0.92)
    c.set_line_width(0.75)
    c.rect(36, 696, 540, 30, fill=True, stroke=True)

    c.text(46, 712, "AGENCY: Streetsmart Insurance (Freehold, NJ)  |  PRODUCER: Carlo Ferrara", font="F2", size=8.5, rgb=(0.1, 0.1, 0.1))
    c.text(46, 701, "INSURED: Par-Troy Sheet Metal & Air Conditioning LLC  |  EFF: 04/06/2026 - 04/06/2027", font="F1", size=8.5, rgb=(0.3, 0.3, 0.3))

    # Footer
    c.line(36, 32, 576, 32, stroke_rgb=(0.8, 0.8, 0.8), width=0.5)
    c.text(36, 22, "CONFIDENTIAL  -  Streetsmart Insurance  -  Commercial Lines Application Package", font="F1", size=7.5, rgb=(0.5, 0.5, 0.5))
    c.text(450, 22, "EZLynx / Multi-Carrier Submission", font="F1", size=7.5, rgb=(0.5, 0.5, 0.5))


def build_page_1():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 125 -- COMMERCIAL INSURANCE APPLICATION", "Applicant, Premises & Operations", 1)

    y = 675
    # Section Header: Applicant Info
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "FIRST NAMED INSURED & CONTACT INFORMATION", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)

    rows = [
        ("First Named Insured:", "Par-Troy Sheet Metal & Air Conditioning LLC"),
        ("DBA / Trade Name:", "Par-Troy Metals, LLC"),
        ("Legal Entity Type:", "Limited Liability Company (LLC)  |  Established: 1981 (45 Years)"),
        ("Mailing Address:", "122 Clinton Rd, Ste 3A, Fairfield, NJ 07004-2921 (Essex County)"),
        ("Primary Contact:", "Lino Rocha / Management  |  Phone: (973) 227-1150  |  info@par-troy.com"),
        ("Company Website:", "https://www.par-troy.com"),
        ("SIC & NAICS Codes:", "SIC: 1711 (Plumbing, Heating, A/C), 3444  |  NAICS: 238220, 332322"),
        ("Nature of Business:", "Architectural sheet metal fabrication, supply & HVAC ductwork/installation"),
    ]

    curr_y = y - 12
    for label, val in rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    y -= 128
    # Section Header: Premises Information
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "PREMISES INFORMATION -- LOCATION #1 (OPERATING HEADQUARTERS & SHOP)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)

    prem_rows = [
        ("Location Address:", "122 Clinton Rd, Ste 3A, Fairfield, NJ 07004-2921 (Essex County)"),
        ("Protection Class:", "Protection Class 03 (Fairfield Fire Dept)  |  Hydrant: <500 ft"),
        ("Occupancy / Interest:", "Tenant Occupied -- Office, Sheet Metal Shop, Machinery & Staging Warehouse"),
        ("Building Construction:", "Masonry / Non-Combustible (ISO Code 3/4)  |  8,500 Sq. Ft. Area"),
        ("Machinery / Equipment:", "CNC Press Brakes, Waterjet/Plasma Precision Cutting, Shearing & Forming Benches"),
        ("Flammable Storage:", "Approved OSHA/NFPA double-walled safety cabinets for solvents and oils"),
        ("Fire Safeguards:", "Central station monitored fire & burglary alarm; calibrated ABC fire extinguishers"),
        ("Hours of Operation:", "Monday - Friday, 7:00 AM - 4:00 PM (No late-night high-hazard shifts)"),
    ]

    curr_y = y - 12
    for label, val in prem_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    y -= 128
    # Section Header: Operations & Underwriting Controls
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "OPERATIONAL CONTROLS & UNDERWRITING SAFENETS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)

    ctrl_rows = [
        ("Roofing Work Exclusion:", "NO hot-tar, torch-down, or membrane roofing. Standing seam panels & trim only."),
        ("Refrigerant Compliance:", "100% of HVAC technicians hold active EPA Section 608 Universal Certifications."),
        ("Hot Work / Brazing:", "Formal hot work permit protocol, spark shields & mandatory 30-min fire watch."),
        ("Subcontractor Transfer:", "<10% subbed (crane rigging only). Mandatory $1M GL COI with AI & Hold Harmless."),
        ("Height Restrictions:", "Direct employee work limited to 1-2 stories & flat rooftops with OSHA tie-offs."),
        ("Fleet & Tool Security:", "Service vehicles locked overnight inside Fairfield facility with secured compartments."),
        ("Loss History:", "Clean 5-year claims record; active 0.959 credit Experience Modifier."),
        ("Target Carriers:", "Selective (Top Regional), Travelers (Automated BOP/WC), Nationwide, The Hanover."),
    ]

    curr_y = y - 12
    for label, val in ctrl_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    return c


def build_page_2():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 130 -- WORKERS COMPENSATION APPLICATION", "Rating Schedule, Payrolls & Benchmark", 2)

    y = 675
    # Section Header: Policy Terms & Employer Liability Limits
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "EMPLOYER'S LIABILITY LIMITS & POLICY TERMS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 75, 540, 75, fill=False, stroke=True)

    limits_rows = [
        ("Policy Proposed Term:", "April 6, 2026 to April 6, 2027 (12 Months)"),
        ("Bodily Injury By Accident:", "$500,000.00  Each Accident  (Option for $1,000,000 Umbrella Underlying)"),
        ("Bodily Injury By Disease:", "$500,000.00  Policy Limit"),
        ("Bodily Injury By Disease:", "$500,000.00  Each Employee"),
        ("Owners / Officers Status:", "New Jersey LLC Managing Members: INCLUDED per state statute"),
    ]

    curr_y = y - 12
    for label, val in limits_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(200, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    y -= 90
    # Section Header: NJ Rating Schedule Table
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "NEW JERSEY WORKERS COMPENSATION RATING SCHEDULE & PAYROLL BREAKDOWN", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 125, 540, 125, fill=False, stroke=True)

    # Table Header
    c.set_fill_color(0.92, 0.94, 0.97)
    c.rect(36, y - 18, 540, 18, fill=True, stroke=True)
    c.text(42, y - 13, "CODE", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(80, y - 13, "CLASSIFICATION DESCRIPTION", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(320, y - 13, "PAYROLL (EXPOSURE)", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(440, y - 13, "BLENDED RATE", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(515, y - 13, "CLASS PREM", font="F2", size=8, rgb=(0.1, 0.1, 0.1))

    table_data = [
        ("3724", "HVAC INSTALLATION, SERVICE & DRIVERS - COMM/RES", "$343,000", "5.47", "$19,331.00"),
        ("8810", "CLERICAL OFFICE EMPLOYEES NOC", "$100,000", "0.17", "$136.00"),
        ("8742", "SALESPERSON, COLLECTORS, OR MESSENGERS - OUTSIDE", "$33,000", "0.32", "$97.00"),
    ]

    ty = y - 32
    for code, desc, pay, rate, prem in table_data:
        c.text(42, ty, code, font="F2", size=8, rgb=(0.1, 0.2, 0.4))
        c.text(80, ty, desc, font="F1", size=7.5, rgb=(0.1, 0.1, 0.1))
        c.text(330, ty, pay, font="F2", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(455, ty, rate, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(515, ty, prem, font="F2", size=8, rgb=(0.1, 0.1, 0.1))
        c.line(36, ty - 4, 576, ty - 4, stroke_rgb=(0.9, 0.9, 0.9), width=0.5)
        ty -= 16

    # Total exposure row
    c.set_fill_color(0.96, 0.98, 1.0)
    c.rect(36, ty - 2, 540, 16, fill=True, stroke=False)
    c.text(80, ty + 2, "TOTAL STATE PAYROLL EXPOSURE & BASE CLASS PREMIUM:", font="F2", size=8, rgb=(0.08, 0.22, 0.45))
    c.text(330, ty + 2, "$476,000.00", font="F2", size=8.5, rgb=(0.08, 0.22, 0.45))
    c.text(515, ty + 2, "$19,564.00", font="F2", size=8.5, rgb=(0.08, 0.22, 0.45))

    y -= 142
    # Section Header: Premium Adjustments & Benchmark Target
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "RATING FACTORS, SURCHARGES & HARTFORD BENCHMARK COMPARISON", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)

    adj_rows = [
        ("Total Estimated Class Premium:", "$19,564.00"),
        ("Employer Liability Increased Limits (0.011):", "+ $215.00"),
        ("Experience Rating Modifier (0.959 CREDIT):", "- $811.00  (Credit Mod applied to standard premium)"),
        ("Total Estimated Standard Premium:", "$18,968.00"),
        ("Catastrophe & Terrorism (TRIPRA):", "+ $191.00  ($48 Catastrophe + $143 Terrorism)"),
        ("Expense Constant & Premium Discount:", "- $656.00  ($160 Constant - $816 NJ Premium Discount)"),
        ("NJ 2nd Injury Fund Surcharge (3.75%):", "+ $711.00"),
        ("TOTAL ESTIMATED ANNUAL WC PREMIUM:", "$19,214.00  (Target to beat across Selective, Travelers, Nationwide, Hanover)"),
    ]

    curr_y = y - 12
    for label, val in adj_rows:
        if "TOTAL ESTIMATED ANNUAL" in label:
            c.text(42, curr_y, label, font="F2", size=8.5, rgb=(0.7, 0.1, 0.1))
            c.text(260, curr_y, val, font="F2", size=8.5, rgb=(0.7, 0.1, 0.1))
        else:
            c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
            c.text(260, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    return c


def build_page_3():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 160 -- BUSINESSOWNERS POLICY / PACKAGE SECTION", "General Liability, Property & Inland Marine", 3)

    y = 675
    # Section Header: CGL Limits
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "COMMERCIAL GENERAL LIABILITY (CGL) LIMITS -- OCCURRENCE FORM", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 85, 540, 85, fill=False, stroke=True)

    cgl_rows = [
        ("Each Occurrence Limit:", "$1,000,000.00"),
        ("General Aggregate Limit:", "$2,000,000.00"),
        ("Products / Completed Operations Aggregate:", "$2,000,000.00"),
        ("Personal & Advertising Injury Limit:", "$1,000,000.00"),
        ("Damage to Rented Premises (Any One Premise):", "$100,000.00"),
        ("Medical Expense Limit (Any One Person):", "$10,000.00"),
    ]

    curr_y = y - 12
    for label, val in cgl_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(280, curr_y, val, font="F1", size=8.5, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    y -= 100
    # Section Header: CGL Rating Basis & ISO Classes
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "CGL CLASSIFICATION CODES & EXPOSURE DISTRIBUTION", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 90, 540, 90, fill=False, stroke=True)

    c.text(42, y - 12, "Total Estimated Gross Annual Sales: $1,750,000.00 (Split: 70% Commercial / 30% Residential)", font="F2", size=8.5, rgb=(0.08, 0.22, 0.45))
    
    gl_codes = [
        ("ISO Code 95647:", "Heating / AC Systems - Installation, Servicing or Repair (Commercial)", "Gross Sales: $1,225,000"),
        ("ISO Code 95648:", "Heating / AC Systems - Installation, Servicing or Repair (Residential)", "Gross Sales: $525,000"),
        ("ISO Code 98636:", "Sheet Metal Work - Shop & Fabrication / Supply", "Gross Payroll: $343,000"),
    ]

    gy = y - 28
    for code, desc, exp in gl_codes:
        c.text(42, gy, code, font="F2", size=8, rgb=(0.1, 0.2, 0.4))
        c.text(140, gy, desc, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(440, gy, exp, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        gy -= 18

    y -= 105
    # Section Header: Property & Inland Marine
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "BUSINESS PERSONAL PROPERTY & INLAND MARINE CONTRACTOR FLOATER", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)

    prop_rows = [
        ("Building Coverage (122 Clinton Rd):", "$0.00 (Tenant Occupied -- No Building Coverage Requested)"),
        ("Business Personal Property (BPP):", "$150,000.00  |  Replacement Cost  |  80% Coinsurance  |  $1,000 Ded"),
        ("BPP Property Description:", "Shop machinery, CNC brakes, waterjet/plasma cutters, sheet metal & stock"),
        ("Business Income & Extra Expense:", "Actual Loss Sustained (12 Months Coverage Extended)"),
        ("Contractor's Tools & Equipment Floater:", "$50,000.00 Total  |  $2,500 Any One Item  |  $5,000 Employee Tools"),
        ("Installation Floater Limit:", "$25,000.00 (Materials in transit and awaiting installation at job site)"),
        ("Causes of Loss Form:", "Special Causes of Loss Form (including Theft & Water Damage)"),
        ("Blanket Contractor Endorsements:", "Requesting Blanket Additional Insured & Blanket Waiver of Subrogation"),
    ]

    curr_y = y - 12
    for label, val in prop_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(220, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    return c


def main():
    doc = SimplePDFDocument()
    doc.add_page(build_page_1())
    doc.add_page(build_page_2())
    doc.add_page(build_page_3())

    pdf_bytes = doc.render()
    output_filename = "ACORD_125_130_160_ParTroy.pdf"
    with open(output_filename, "wb") as f:
        f.write(pdf_bytes)

    print(f"Successfully generated {output_filename} ({len(pdf_bytes)} bytes, 3 pages)")

if __name__ == "__main__":
    main()
