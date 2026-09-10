#!/usr/bin/env python3
"""
ACORD 125, 126, 140 PDF Generator for Emio 'Sonny' Abagnale
Generates a clean, professional, multi-page ACORD application PDF.
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
    # Top banner background
    c.set_fill_color(0.08, 0.22, 0.45) # Professional Navy #143872
    c.rect(36, 730, 540, 36, fill=True, stroke=False)
    
    # Title
    c.text(46, 744, title, font="F2", size=12, rgb=(1, 1, 1))
    c.text(475, 744, f"PAGE {page_num} OF 3", font="F2", size=9, rgb=(0.85, 0.9, 1))

    # Sub-banner info
    c.set_fill_color(0.94, 0.96, 0.99)
    c.set_stroke_color(0.8, 0.85, 0.92)
    c.set_line_width(0.75)
    c.rect(36, 696, 540, 30, fill=True, stroke=True)

    c.text(46, 712, "AGENCY: Streetsmart Insurance (Freehold, NJ)  |  PRODUCER: Carlo Ferrara", font="F2", size=8.5, rgb=(0.1, 0.1, 0.1))
    c.text(46, 701, "INSURED: Emio 'Sonny' Abagnale  |  EZLYNX # 221774967  |  EFF DATE: 10/01/2026", font="F1", size=8.5, rgb=(0.3, 0.3, 0.3))

    # Footer
    c.line(36, 32, 576, 32, stroke_rgb=(0.8, 0.8, 0.8), width=0.5)
    c.text(36, 22, "CONFIDENTIAL  -  Streetsmart Insurance  -  Commercial Lines Application Package", font="F1", size=7.5, rgb=(0.5, 0.5, 0.5))
    c.text(470, 22, "EZLynx / Tarmika Export", font="F1", size=7.5, rgb=(0.5, 0.5, 0.5))


def build_page_1():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 125 -- COMMERCIAL INSURANCE APPLICATION", "Applicant & Premises Information", 1)

    y = 675
    # Section Header: Applicant Info
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "FIRST NAMED INSURED & CONTACT INFORMATION", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 100, 540, 100, fill=False, stroke=True)

    rows = [
        ("First Named Insured:", "Emio 'Sonny' Abagnale"),
        ("Legal Entity Type:", "Individual / Sole Proprietor (DOB: 12/20/1932)"),
        ("Mailing Address:", "20 Lawrence Way, Cedar Grove, NJ 07009-1335 (Essex County)"),
        ("Contact & Inspection:", "Emio Abagnale  |  Phone: (201) 310-4433  |  Email: sonnycars@yahoo.com"),
        ("SIC & NAICS Code:", "SIC: 6512 (Nonresidential Building Operators)  |  NAICS: 531120 (Lessors)"),
        ("Years in Business:", "Established 01/01/1980 (46 Years Active Ownership)"),
        ("Nature of Business:", "Lessor's Risk Only (LRO) -- Multi-tenant automotive commercial property"),
    ]

    curr_y = y - 12
    for label, val in rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    y -= 118
    # Section Header: Premises Information
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "PREMISES INFORMATION -- 11-33 ROOSEVELT AVE, BELLEVILLE, NJ 07109", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 130, 540, 130, fill=False, stroke=True)

    prem_rows = [
        ("Location Address:", "11-33 Roosevelt Ave, Belleville, NJ 07109 (Essex County)"),
        ("Protection Class & Hydrant:", "Protection Class: 03  |  Distance to Hydrant: 1,000 ft  |  Fire Station: 1-2 mi"),
        ("Premises #1 / Lot 11:", "Paved Commercial Parking & Staging Lot (12,000 SF) -- Class 67512"),
        ("Premises #1 / Building 1:", "13-15 Roosevelt Ave | 10,000 SF | Auto Body & Collision Repair Shop"),
        ("Premises #1 / Building 2:", "17-33 Roosevelt Ave | 14,500 SF | Multi-Tenant (Wholesale Parts & Heavy Truck)"),
        ("Suite Breakdown (Bldg 2):", "Suite 17-21: Wholesale Auto Parts  |  Suite 27-33: Heavy Commercial Truck Repair"),
        ("Occupancy Status:", "100% Tenant-Occupied (Lessor's Risk Only) -- No owner-operated businesses"),
        ("Lease Controls:", "Written commercial leases in place; mandatory $1,000,000 GL COIs naming Landlord as AI"),
    ]

    curr_y = y - 12
    for label, val in prem_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 14

    y -= 148
    # Section Header: Prior Carrier & Loss History
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "PRIOR CARRIER INFORMATION & 5-YEAR LOSS HISTORY", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 85, 540, 85, fill=False, stroke=True)

    loss_rows = [
        ("Prior Carrier:", "State Farm Fire & Casualty Company"),
        ("Prior Policy Number:", "98-BA-1234-1  (Commercial Package Policy)"),
        ("Expiring Annual Premium:", "$12,000.00 / year"),
        ("5-Year Loss History:", "ZERO CLAIMS / LOSS-FREE (0 Claims / 5 Years)"),
        ("Loss Run Status:", "Hard-copy State Farm loss runs on file verifying 0 losses / $0 paid"),
        ("Reason for Marketing:", "Exploring comprehensive multi-carrier middle market terms and higher TIV coverage"),
    ]

    curr_y = y - 12
    for label, val in loss_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 12

    return c


def build_page_2():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 126 -- COMMERCIAL GENERAL LIABILITY SECTION", "General Liability & Exposure Schedule", 2)

    y = 675
    # Section Header: CGL Limits
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "LIMITS OF LIABILITY (OCCURRENCE BASIS)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 90, 540, 90, fill=False, stroke=True)

    limits_rows = [
        ("General Aggregate Limit:", "$2,000,000.00"),
        ("Products / Completed Operations Aggregate:", "$2,000,000.00"),
        ("Each Occurrence Limit:", "$1,000,000.00"),
        ("Personal & Advertising Injury:", "$1,000,000.00"),
        ("Damage to Rented Premises (Each Occ):", "$100,000.00"),
        ("Medical Expense Limit (Any One Person):", "$5,000.00"),
    ]

    curr_y = y - 12
    for label, val in limits_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(260, curr_y, val, font="F1", size=8.5, rgb=(0.05, 0.05, 0.05))
        curr_y -= 13

    y -= 108
    # Section Header: Schedule of Hazards
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "SCHEDULE OF HAZARDS & CLASSIFICATIONS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 120, 540, 120, fill=False, stroke=True)

    c.text(42, y - 14, "Loc 1, Bldg 1 (13-15 Roosevelt Ave):", font="F2", size=8.5, rgb=(0.1, 0.2, 0.4))
    c.text(42, y - 26, "  - Class 61226: Buildings or Premises - Lessor's Risk Only (Auto Body / Repair Shop)", font="F1", size=8)
    c.text(42, y - 38, "  - Exposure Basis: Area | Exposure: 10,000 Sq. Ft.", font="F1", size=8)

    c.text(42, y - 56, "Loc 1, Bldg 2 (17-33 Roosevelt Ave):", font="F2", size=8.5, rgb=(0.1, 0.2, 0.4))
    c.text(42, y - 68, "  - Class 61226 / 61217: Buildings or Premises - LRO (Wholesale Auto Parts & Heavy Truck Repair)", font="F1", size=8)
    c.text(42, y - 80, "  - Exposure Basis: Area | Exposure: 14,500 Sq. Ft.", font="F1", size=8)

    c.text(42, y - 98, "Loc 1, Lot 11 (11 Roosevelt Ave):", font="F2", size=8.5, rgb=(0.1, 0.2, 0.4))
    c.text(42, y - 110, "  - Class 67512: Parking Lots - Open / Non-Attendant (Vehicle Staging & Parking)", font="F1", size=8)

    y -= 138
    # Section Header: Risk Controls & Questionnaire
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "UNDERWRITING QUESTIONNAIRE & RISK CONTROLS", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 110, 540, 110, fill=False, stroke=True)

    c.text(42, y - 14, "[x] Formal Written Leases with Indemnification & Hold Harmless in favor of Landlord.", font="F1", size=8)
    c.text(42, y - 28, "[x] Mandatory Certificates of Insurance (COIs) required annually from all tenants.", font="F1", size=8)
    c.text(42, y - 42, "[x] Minimum $1,000,000 GL carried by all tenants; Landlord named as Additional Insured.", font="F1", size=8)
    c.text(42, y - 56, "[x] No uncorrected fire, building code, or life safety violations on premises.", font="F1", size=8)
    c.text(42, y - 70, "[x] Spray booth in Building 1 has automatic suppression system & semi-annual servicing.", font="F1", size=8)
    c.text(42, y - 84, "[x] Heavy truck repair in Building 2 has dedicated welding bay with safety screens.", font="F1", size=8)
    c.text(42, y - 98, "[x] No hazardous waste dumping, past environmental claims, or uninsured exposures.", font="F1", size=8)

    return c


def build_page_3():
    c = PDFCanvas()
    draw_common_header(c, "ACORD 140 -- COMMERCIAL PROPERTY SECTION", "Building Schedules, Valuations & Protections", 3)

    y = 675
    # Section Header: Building 1
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "BUILDING #1: 13-15 ROOSEVELT AVE (AUTO BODY & COLLISION REPAIR)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.set_stroke_color(0.8, 0.8, 0.8)
    c.set_line_width(0.5)
    c.rect(36, y - 140, 540, 140, fill=False, stroke=True)

    b1_rows = [
        ("Subject of Insurance:", "Building: $3,500,000.00 | Valuation: Replacement Cost (RC)"),
        ("Coinsurance & Deductible:", "80% Coinsurance | Causes of Loss: Special Form | Deductible: $2,500.00"),
        ("Construction Type:", "Joisted Masonry (ISO Code 2) | Stories: 2 | Basements: 1 | Area: 10,000 SF"),
        ("Year Built & Updates:", "Year Built: 1950 | 100% Full 4-Point Updates completed in 2018"),
        ("  - Roof Type & Update:", "Flat / EPDM Rubber Membrane (Full tear-off / new roof installed 2018)"),
        ("  - Wiring & Electrical:", "100% updated in 2018 (Commercial circuit breakers, conduit wiring)"),
        ("  - Plumbing & Heating:", "100% updated in 2018 (Commercial gas-fired unit heaters, modern copper/PEX)"),
        ("Protective Safeguards:", "Local Gong / Fire Alarm | Semi-annual dry-chem spray booth suppression (NFPA 33)"),
        ("Occupant Description:", "Automotive repair, body work, and spray painting (Single tenant auto body)"),
    ]

    curr_y = y - 12
    for label, val in b1_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 13

    y -= 158
    # Section Header: Building 2
    c.set_fill_color(0.15, 0.28, 0.48)
    c.rect(36, y, 540, 16, fill=True, stroke=False)
    c.text(42, y + 4, "BUILDING #2: 17-33 ROOSEVELT AVE (WHOLESALE PARTS & HEAVY TRUCK REPAIR)", font="F2", size=8.5, rgb=(1, 1, 1))

    y -= 16
    c.rect(36, y - 140, 540, 140, fill=False, stroke=True)

    b2_rows = [
        ("Subject of Insurance:", "Building: $3,500,000.00 | Valuation: Replacement Cost (RC)"),
        ("Coinsurance & Deductible:", "80% Coinsurance | Causes of Loss: Special Form | Deductible: $2,500.00"),
        ("Construction Type:", "Joisted Masonry (ISO Code 2) | Stories: 1 | Basements: 0 | Area: 14,500 SF"),
        ("Year Built & Updates:", "Year Built: 1950 | 100% Full 4-Point Updates completed in 2018"),
        ("  - Roof Type & Update:", "Flat / EPDM Rubber Membrane (Full tear-off / new roof installed 2018)"),
        ("  - Wiring & Electrical:", "100% updated in 2018 (Commercial circuit breakers, industrial power)"),
        ("  - Plumbing & Heating:", "100% updated in 2018 (Commercial gas unit heaters, updated plumbing)"),
        ("Protective Safeguards:", "Local Gong / Fire Alarm | Dedicated welding screens | Flammable fluid cabinets"),
        ("Occupant Breakdown:", "Suite 17-21: Wholesale Auto Parts | Suite 27-33: Heavy Commercial Truck Repair"),
    ]

    curr_y = y - 12
    for label, val in b2_rows:
        c.text(42, curr_y, label, font="F2", size=8, rgb=(0.2, 0.2, 0.2))
        c.text(180, curr_y, val, font="F1", size=8, rgb=(0.05, 0.05, 0.05))
        curr_y -= 13

    # Total Insurable Value box
    y -= 155
    c.set_fill_color(0.9, 0.94, 0.98)
    c.set_stroke_color(0.08, 0.22, 0.45)
    c.set_line_width(1)
    c.rect(36, y, 540, 30, fill=True, stroke=True)
    c.text(46, y + 18, "TOTAL PORTFOLIO INSURABLE VALUE (TIV): $7,000,000 PROPERTY + $1M/$2M/$2M CGL", font="F2", size=9.5, rgb=(0.08, 0.22, 0.45))
    c.text(46, y + 6, "Valuations aligned with Marshall & Swift / CoreLogic 360Value commercial cost estimators.", font="F1", size=8, rgb=(0.2, 0.3, 0.4))

    return c


def main():
    doc = SimplePDFDocument()
    doc.add_page(build_page_1())
    doc.add_page(build_page_2())
    doc.add_page(build_page_3())

    pdf_bytes = doc.render()
    output_path = "/Users/carloferrara/.gemini/antigravity/scratch/ACORD_125_126_140_Abagnale.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    print(f"Successfully generated ACORD package: {output_path} ({len(pdf_bytes)} bytes)")

if __name__ == "__main__":
    main()
