#!/usr/bin/env python3
"""
ACORD 125, 126, 140 PDF Generator
Generates a clean, professional, multi-page PDF document for insurance submission.
"""

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
        # Obj 1: Catalog
        objs.append("<< /Type /Catalog /Pages 2 0 R >>")
        # Obj 2: Pages
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
    # Top banner background
    c.set_fill_color(0.118, 0.227, 0.541) # Dark Blue #1e3a8a
    c.rect(36, 730, 540, 36, fill=True, stroke=False)
    
    # Title
    c.text(46, 744, title, font="F2", size=13, rgb=(1, 1, 1))
    c.text(460, 744, f"PAGE {page_num} OF 3", font="F2", size=9, rgb=(0.85, 0.9, 1))

    # Sub-banner info
    c.set_fill_color(0.94, 0.96, 0.99)
    c.set_stroke_color(0.8, 0.85, 0.92)
    c.set_line_width(0.75)
    c.rect(36, 696, 540, 30, fill=True, stroke=True)

    c.text(46, 712, "AGENCY: Streetsmart Insurance  |  PRODUCER: Angie Valladarez  |  CSR: Erika Palacios", font="F1", size=8.5, rgb=(0.1, 0.1, 0.1))
    c.text(46, 701, "EZLYNX SUBMISSION # 158937  |  APPLICATION # 200897142  |  DATE: 09/10/2026", font="F1", size=8.5, rgb=(0.3, 0.3, 0.3))

    # Footer
    c.line(36, 32, 576, 32, stroke_rgb=(0.8, 0.8, 0.8), width=0.5)
    c.text(36, 22, "CONFIDENTIAL  -  Streetsmart Insurance  -  Commercial Lines Application Package", font="F1", size=7.5, rgb=(0.5, 0.5, 0.5))
    c.text(495, 22, "EZLynx System Export", font="F1", size=7.5, rgb=(0.5, 0.5, 0.5))


def build_page_1():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 125 — COMMERCIAL INSURANCE APPLICATION", "Applicant & Premises Information", 1)

    y = 680
    # Section Header: Applicant Info
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "FIRST NAMED INSURED & CONTACT INFORMATION", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    # Table border
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)

    rows = [
        ("Legal Named Insured:", "Express Automotive Towing Inc, Express Towing Of Metuchen Inc"),
        ("Individual Named Insured (Loc 2):", "Michael Swartz  (Quote 201 Atlantic City Blvd under personal name per note)"),
        ("DBA / Trade Name:", "Express Auto Metuchen"),
        ("Mailing Address:", "2 PROSPECT ST, METUCHEN, NJ 08840-2279 (Middlesex County)"),
        ("Contact Person / Phone / Email:", "Michael Swartz  |  Work: (732) 494-4455  |  Cell: (732) 735-0119  |  xtowing@aol.com"),
        ("FEIN / Entity Type / Established:", "22-3390304  |  Entity: Corporation / Individual  |  Active client since 11/04/2022"),
        ("SIC / NAICS Codes:", "SIC: 7538 (General Automotive Repair)  |  NAICS: 811111 / 531120 (Lessors)"),
        ("Business Description / Operations:", "Auto mechanic performing towing for his own clients (5% towing, 95% general auto repair)."),
    ]

    curr_y = y - 12
    for label, val in rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(195, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        c.line(36, curr_y - 2, 576, curr_y - 2, stroke_rgb=(0.92, 0.92, 0.92), width=0.5)
        curr_y -= 13.5

    # Section Header: Policy Level Details
    y = 538
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "POLICY & TRANSACTION DETAILS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 48, 540, 48, fill=False, stroke=True)
    policy_rows = [
        ("Proposed Term / Quote Due:", "Effective: 09/24/2026  to  09/24/2027 (12 Months)  |  Quote Due Date: 09/17/2026"),
        ("Lines of Business Requested:", "Commercial General Liability (ACORD 126)  &  Commercial Property (ACORD 140) [BOP]"),
        ("Billing & Payment Plan:", "Direct Bill  |  Annual / Standard Carrier Installments  |  Audit: Annual"),
    ]
    curr_y = y - 12
    for label, val in policy_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(195, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        c.line(36, curr_y - 2, 576, curr_y - 2, stroke_rgb=(0.92, 0.92, 0.92), width=0.5)
        curr_y -= 15

    # Section Header: Premises Schedule
    y = 458
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "SCHEDULE OF PREMISES / LOCATIONS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 90, 540, 90, fill=False, stroke=True)
    # Header row
    c.set_fill_color(0.93, 0.94, 0.96)
    c.rect(36, y - 16, 540, 16, fill=True, stroke=False)
    c.text(42, y - 11, "Loc / Bldg", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(100, y - 11, "Address, City, State, Zip", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(280, y - 11, "Occupancy / Operations", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(490, y - 11, "Occupancy Type", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))

    # Row 1
    c.text(42, y - 32, "1 / 1", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(100, y - 32, "2 Prospect St, Metuchen, NJ 08840", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(280, y - 32, "Automotive mechanic repair shop & towing dispatch", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(490, y - 32, "Owner-Occupied", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.line(36, y - 44, 576, y - 44, stroke_rgb=(0.9, 0.9, 0.9), width=0.5)

    # Row 2
    c.text(42, y - 62, "2 / 1", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(100, y - 62, "201 Atlantic City Blvd, Beachwood, NJ 08722", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(280, y - 62, "Lessor's Risk Only (LRO) - Leased to restaurant with cooking", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(490, y - 62, "100% Leased", font="F1", size=8, rgb=(0.1, 0.1, 0.1))

    # Section Header: Prior Carrier & Loss History
    y = 336
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "PRIOR CARRIER INFORMATION & LOSS HISTORY (PAST 3 YEARS)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 80, 540, 80, fill=False, stroke=True)
    c.set_fill_color(0.93, 0.94, 0.96)
    c.rect(36, y - 16, 540, 16, fill=True, stroke=False)
    c.text(42, y - 11, "Coverage / Line", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(160, y - 11, "Carrier & Policy #", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(320, y - 11, "Term / Effective Dates", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(450, y - 11, "Premium / Status", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))

    # Row 1
    c.text(42, y - 30, "Commercial Package", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(160, y - 30, "Selective Insurance (# S 2531456)", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(320, y - 30, "01/24/2026 – 01/24/2027", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(450, y - 30, "$39,206.00 (Active/Reinstated)", font="F1", size=8, rgb=(0.05, 0.5, 0.2))
    c.line(36, y - 40, 576, y - 40, stroke_rgb=(0.9, 0.9, 0.9), width=0.5)

    # Row 2
    c.text(42, y - 52, "Workers Compensation", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(160, y - 52, "First Comp / Markel (# MWC0248189-01)", font="F2", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(320, y - 52, "01/24/2026 – 01/24/2027", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.text(450, y - 52, "$12,754.00 (Active Direct Bill)", font="F1", size=8, rgb=(0.1, 0.1, 0.1))
    c.line(36, y - 62, 576, y - 62, stroke_rgb=(0.9, 0.9, 0.9), width=0.5)

    c.text(42, y - 73, "Loss History Summary:", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(150, y - 73, "Application intake reported 'No' losses in 1-3 yrs; Selective records reflect 2 prior claims.", font="F1", size=7.5, rgb=(0.3, 0.3, 0.3))

    # Notes box
    y = 224
    c.set_fill_color(0.96, 0.97, 0.99)
    c.set_stroke_color(0.8, 0.85, 0.9)
    c.rect(36, y - 45, 540, 45, fill=True, stroke=True)
    c.text(44, y - 14, "SPECIAL UNDERWRITING INSTRUCTIONS (TASK NOTE BY CARLO FERRARA):", font="F2", size=8, rgb=(0.1, 0.2, 0.5))
    c.text(44, y - 28, "• 'quote this building under his personal name 201 Atlantic City BLVD Beechwood lessor risk with cooking'", font="F1", size=8, rgb=(0.2, 0.2, 0.2))
    c.text(44, y - 40, "• Property section completed under Michael Swartz; Cross-liability and Additional Insured ties to Express Automotive Towing.", font="F1", size=7.5, rgb=(0.3, 0.3, 0.3))

    return c


def build_page_2():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 126 — COMMERCIAL GENERAL LIABILITY SECTION", "Coverages, Limits & Schedule of Hazards", 2)

    y = 680
    # Section Header: Limits of Insurance
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "LIMITS OF LIABILITY (COMMERCIAL GENERAL LIABILITY)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 96, 540, 96, fill=False, stroke=True)

    limits = [
        ("Each Occurrence Limit:", "$1,000,000", "Damage to Premises Rented to You:", "$100,000"),
        ("General Aggregate Limit:", "$2,000,000", "Medical Expense Limit (Any 1 person):", "$5,000"),
        ("Products / Completed Operations Aggregate:", "$2,000,000", "Deductible (Bodily Injury & Property):", "$0 / $1,000"),
        ("Personal & Advertising Injury Limit:", "$1,000,000", "Coverage Basis:", "Commercial GL - Occurrence Basis"),
    ]

    curr_y = y - 15
    for l1, v1, l2, v2 in limits:
        c.text(44, curr_y, l1, font="F1", size=8.5, rgb=(0.25, 0.25, 0.25))
        c.text(180, curr_y, v1, font="F2", size=8.5, rgb=(0.05, 0.05, 0.05))
        c.text(320, curr_y, l2, font="F1", size=8.5, rgb=(0.25, 0.25, 0.25))
        c.text(475, curr_y, v2, font="F2", size=8.5, rgb=(0.05, 0.05, 0.05))
        c.line(36, curr_y - 4, 576, curr_y - 4, stroke_rgb=(0.92, 0.92, 0.92), width=0.5)
        curr_y -= 22

    # Section Header: Schedule of Hazards
    y = 550
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "SCHEDULE OF HAZARDS & CLASSIFICATIONS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)
    c.set_fill_color(0.93, 0.94, 0.96)
    c.rect(36, y - 16, 540, 16, fill=True, stroke=False)
    c.text(42, y - 11, "Loc", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(70, y - 11, "Bldg", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(105, y - 11, "Class Code", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(175, y - 11, "Classification Description", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(410, y - 11, "Premium Basis", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(495, y - 11, "Exposure", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))

    hazards = [
        ("1", "1", "91111", "Automobile Repair Shops (no sale of gas/oil)", "Gross Sales", "95% operations"),
        ("1", "1", "91120", "Automobile Towing Services (customer towing)", "Gross Receipts", "5% operations"),
        ("2", "1", "61212", "Buildings or Premises - Lessor's Risk (with cooking)", "Area (Sq Ft)", "100% Leased"),
    ]
    curr_y = y - 32
    for loc, bldg, code, desc, basis, exp in hazards:
        c.text(44, curr_y, loc, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(75, curr_y, bldg, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(110, curr_y, code, font="F2", size=8, rgb=(0.1, 0.2, 0.5))
        c.text(175, curr_y, desc, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(410, curr_y, basis, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(495, curr_y, exp, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.line(36, curr_y - 8, 576, curr_y - 8, stroke_rgb=(0.9, 0.9, 0.9), width=0.5)
        curr_y -= 26

    # Section Header: Underwriting & Exposure Questions
    y = 406
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "GENERAL LIABILITY UNDERWRITING QUESTIONS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 170, 540, 170, fill=False, stroke=True)

    questions = [
        ("1. Any work performed away from shop premises?", "YES", "Towing of client vehicles only (5% gross receipts). All repairs performed 100% on-premises."),
        ("2. Are subcontractors used in any operations?", "NO", "All mechanical repair work performed directly by in-house technicians."),
        ("3. Flammables, chemicals, or toxic materials stored?", "YES", "Motor oil, coolant, hydraulic fluids stored in approved containers; disposed via licensed recyclers."),
        ("4. Any products manufactured, sold, or repackaged?", "NO", "Pure service shop; replacement automotive parts installed during repairs only."),
        ("5. Any structural alterations, renovations, or demolition?", "NO", "Only routine facility maintenance performed."),
        ("6. Any policies cancelled, non-renewed, or declined (3 yrs)?", "NO", "Existing Selective package is active and reinstated."),
        ("7. Does commercial lease require tenant COI & liability?", "YES", "Restaurant lease requires minimum $1M/$2M GL coverage with Landlord named Additional Insured."),
    ]

    curr_y = y - 14
    for q, ans, exp in questions:
        c.text(42, curr_y, q, font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
        ans_color = (0, 0.5, 0.2) if ans == "NO" else (0.7, 0.3, 0)
        c.text(320, curr_y, f"[{ans}]", font="F2", size=7.5, rgb=ans_color)
        c.text(355, curr_y, exp, font="F1", size=7, rgb=(0.3, 0.3, 0.3))
        c.line(36, curr_y - 4, 576, curr_y - 4, stroke_rgb=(0.92, 0.92, 0.92), width=0.5)
        curr_y -= 22

    return c


def build_page_3():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 140 — COMMERCIAL PROPERTY SECTION", "Property Coverages, Safeguards & Quotes", 3)

    y = 680
    # Section Header: Subject Property
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "SUBJECT PROPERTY INFORMATION (LOCATION #2 / BUILDING #1)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 72, 540, 72, fill=False, stroke=True)

    prop_info = [
        ("Subject Property Address:", "201 Atlantic City BLVD, Beachwood, NJ 08722  (Ocean County)"),
        ("Occupancy / Tenant Use:", "Lessor's Risk Only (LRO) - Commercial restaurant tenant with active cooking exposure."),
        ("Named Insured for Property:", "Michael Swartz  (Building titled/quoted under individual name per Carlo Ferrara note)"),
        ("Construction & Protection:", "Masonry Non-Combustible / Joisted Masonry  |  Protection Class: Protected (Fire Hydrant)"),
    ]
    curr_y = y - 12
    for label, val in prop_info:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(195, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        c.line(36, curr_y - 2, 576, curr_y - 2, stroke_rgb=(0.92, 0.92, 0.92), width=0.5)
        curr_y -= 16

    # Section Header: Coverages, Limits & Valuation
    y = 574
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "PROPERTY COVERAGES, LIMITS & DEDUCTIBLES", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 120, 540, 120, fill=False, stroke=True)
    c.set_fill_color(0.93, 0.94, 0.96)
    c.rect(36, y - 16, 540, 16, fill=True, stroke=False)
    c.text(42, y - 11, "Subject of Insurance", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(160, y - 11, "Coverage Form", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(260, y - 11, "Valuation", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(350, y - 11, "Coinsurance", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(440, y - 11, "Deductible", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))

    prop_cov = [
        ("Building", "Special Form (incl. Theft)", "Replacement Cost (RC)", "80%", "$2,500 / $5,000"),
        ("Business Personal Property (Lessor)", "Special Form", "Replacement Cost (RC)", "80%", "$2,500"),
        ("Business Income & Extra Expense", "Special Form", "Actual Loss Sustained (ALS)", "12 Months", "72-Hour Waiting Period"),
        ("Equipment Breakdown", "Comprehensive Form", "Repair / Replace", "Included", "$2,500"),
        ("Outdoor Signs", "Special Form", "Replacement Cost", "Stated ($10,000)", "$1,000"),
    ]
    curr_y = y - 32
    for subj, form, val, coin, ded in prop_cov:
        c.text(42, curr_y, subj, font="F2", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(160, curr_y, form, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(260, curr_y, val, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(350, curr_y, coin, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.text(440, curr_y, ded, font="F1", size=8, rgb=(0.1, 0.1, 0.1))
        c.line(36, curr_y - 6, 576, curr_y - 6, stroke_rgb=(0.9, 0.9, 0.9), width=0.5)
        curr_y -= 20

    # Cooking & Protection safeguards
    y = 422
    c.set_fill_color(0.96, 0.97, 0.99)
    c.set_stroke_color(0.8, 0.85, 0.9)
    c.rect(36, y - 40, 540, 40, fill=True, stroke=True)
    c.text(44, y - 12, "COOKING & RESTAURANT TENANT SAFEGUARDS (UNDERWRITING REQUIREMENT):", font="F2", size=8, rgb=(0.1, 0.2, 0.5))
    c.text(44, y - 24, "• Commercial exhaust hood with UL-300 / Ansul R-102 wet chemical fire suppression system installed over cooking line.", font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(44, y - 34, "• Semi-annual maintenance service contract in force; grease filters cleaned bi-weekly; grease trap maintained per code.", font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))

    # Carrier Quote Comparison
    y = 368
    c.set_fill_color(0.2, 0.3, 0.45)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "CARRIER SUBMISSIONS & QUOTED PREMIUMS (EZLYNX SUBMISSION # 158937)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 18
    c.rect(36, y - 130, 540, 130, fill=False, stroke=True)
    c.set_fill_color(0.93, 0.94, 0.96)
    c.rect(36, y - 16, 540, 16, fill=True, stroke=False)
    c.text(42, y - 11, "Insurance Carrier", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(190, y - 11, "Line of Business", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(285, y - 11, "Status", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(370, y - 11, "Quoted Premium", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))
    c.text(475, y - 11, "Notes / Evaluation", font="F2", size=7.5, rgb=(0.2, 0.2, 0.2))

    carrier_quotes = [
        ("Franklin Mutual Group (FMG)", "Commercial Property", "Quoted", "$3,738.00", "Best property rate", (0.05, 0.5, 0.2)),
        ("Selective Insurance", "Commercial Property", "Quoted", "$3,952.00", "Incumbent package option", (0.1, 0.3, 0.7)),
        ("AmTrust Financial Services", "Commercial Property", "Quoted", "$4,606.00", "Doc ID 818320672 on file", (0.1, 0.3, 0.7)),
        ("Merchants Insurance Group", "Commercial Property", "Quoted", "$5,670.00", "Market option", (0.4, 0.4, 0.4)),
        ("Utica First Insurance", "Commercial Property", "Quoted", "$10,003.92", "Higher rate tier", (0.6, 0.4, 0.1)),
        ("Providence Mutual", "Commercial Property", "Quoted", "$13,509.00", "High tier", (0.6, 0.4, 0.1)),
        ("Nationwide Insurance", "Commercial Property", "Declined", "N/A", "Declined (cooking exposure)", (0.7, 0.1, 0.1)),
    ]

    curr_y = y - 30
    for carrier, lob, status, prem, note, color in carrier_quotes:
        c.text(42, curr_y, carrier, font="F2", size=7.5, rgb=(0.1, 0.1, 0.1))
        c.text(190, curr_y, lob, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
        c.text(285, curr_y, status, font="F2", size=7.5, rgb=color)
        c.text(370, curr_y, prem, font="F2", size=7.5, rgb=color)
        c.text(475, curr_y, note, font="F1", size=7, rgb=(0.3, 0.3, 0.3))
        c.line(36, curr_y - 4, 576, curr_y - 4, stroke_rgb=(0.92, 0.92, 0.92), width=0.5)
        curr_y -= 15

    # Producer signature block
    y = 205
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 48, 540, 48, fill=False, stroke=True)

    c.text(44, y - 14, "PRODUCER'S SIGNATURE: ________________________________________", font="F1", size=8, rgb=(0.2, 0.2, 0.2))
    c.text(420, y - 14, "DATE: 09/10/2026", font="F1", size=8, rgb=(0.2, 0.2, 0.2))
    c.text(44, y - 32, "APPLICANT'S SIGNATURE: ________________________________________", font="F1", size=8, rgb=(0.2, 0.2, 0.2))
    c.text(420, y - 32, "TITLE: President / Owner", font="F1", size=8, rgb=(0.2, 0.2, 0.2))

    return c


def main():
    doc = SimplePDFDocument()
    doc.add_page(build_page_1())
    doc.add_page(build_page_2())
    doc.add_page(build_page_3())

    pdf_bytes = doc.render()

    target_paths = [
        "/Users/carloferrara/.gemini/antigravity/scratch/ACORD_125_126_140_Official.pdf",
        "/Users/carloferrara/.gemini/antigravity/brain/61525e1d-e3aa-4f67-9ed8-fd789ac4b97f/ACORD_125_126_140_Official.pdf"
    ]

    for p in target_paths:
        with open(p, "wb") as f:
            f.write(pdf_bytes)
        print(f"Generated {p} ({len(pdf_bytes):,} bytes)")

if __name__ == "__main__":
    main()
