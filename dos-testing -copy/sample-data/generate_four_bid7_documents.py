"""
Generator script for the Four Mandatory Bid Documents for Bid #7
Tender GEM/2026/B/1003 | Bidder: Delta Manufacturing Pvt Ltd (ID 24) | Bid ID: 7

Mandatory documents required by Tender 3:
1. PAN Certificate (Income Tax Department / NSDL) -> bid_7_pan_certificate.pdf
2. GST Registration Certificate (Form GST REG-06) -> bid_7_gst_certificate.pdf
3. OEM Manufacturer Authorization Certificate -> bid_7_oem_authorization.pdf
4. BIS Quality Mark Licence (CM/L-1000004) -> bid_7_bis_certificate.pdf
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas

# Palette
C_NAVY = colors.HexColor("#0B2545")
C_STEEL = colors.HexColor("#134074")
C_GOLD = colors.HexColor("#8D6E16")
C_EMERALD = colors.HexColor("#0F766E")
C_DARK = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#64748B")
C_BG_LIGHT = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_ACCENT_BG = colors.HexColor("#EFF6FF")
C_WHITE = colors.HexColor("#FFFFFF")
C_GREEN_BG = colors.HexColor("#ECFDF5")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setStrokeColor(C_STEEL)
        self.setLineWidth(1.5)
        self.line(36, 806, 559, 806)
        
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.8)
        self.line(36, 42, 559, 42)

        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(C_NAVY)
        self.drawString(36, 812, "GOVERNMENT OF INDIA / STATUTORY COMPLIANCE DOSSIER")
        self.setFont("Helvetica", 7)
        self.setFillColor(C_MUTED)
        self.drawRightString(559, 812, "Tender: GEM/2026/B/1003 | Bid ID: 7")

        self.setFont("Helvetica", 7)
        self.drawString(36, 32, "Verified against National Procurement Registry Database | Bidder: Delta Manufacturing Pvt Ltd")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 32, page_text)
        self.restoreState()


def get_styles():
    ss = getSampleStyleSheet()
    title = ParagraphStyle("DocTitle", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=C_NAVY, alignment=1)
    subtitle = ParagraphStyle("DocSubTitle", parent=ss["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=C_STEEL, alignment=1)
    h2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=C_NAVY, spaceBefore=4, spaceAfter=2)
    body = ParagraphStyle("Body", parent=ss["Normal"], fontName="Helvetica", fontSize=8, leading=11, textColor=C_DARK)
    bold = ParagraphStyle("Bold", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=C_DARK)
    code = ParagraphStyle("Code", parent=ss["Normal"], fontName="Courier-Bold", fontSize=8.5, leading=11, textColor=C_NAVY)
    alert = ParagraphStyle("Alert", parent=ss["Normal"], fontName="Helvetica", fontSize=7.5, leading=10, textColor=C_DARK)
    return {"title": title, "subtitle": subtitle, "h2": h2, "body": body, "bold": bold, "code": code, "alert": alert}


# ==============================================================================
# 1. PAN CERTIFICATE & INCOME TAX ALLOTMENT RECORD
# ==============================================================================
def generate_pan_pdf(out_path):
    doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=48)
    st = get_styles()
    story = []

    # Title & Header
    story.append(Paragraph("INCOME TAX DEPARTMENT &bull; GOVT. OF INDIA", st["subtitle"]))
    story.append(Paragraph("PERMANENT ACCOUNT NUMBER (PAN) ALLOTMENT CERTIFICATE", st["title"]))
    story.append(Paragraph("Issued under Section 139A of the Income-tax Act, 1961 | Directorate of Income Tax (Systems)", st["subtitle"]))
    story.append(Spacer(1, 8))

    # Procurement Reference Banner
    ref_data = [
        [
            Paragraph("<b>Target Tender ID:</b> GEM/2026/B/1003", st["body"]),
            Paragraph("<b>Bid Reference:</b> BID-CPCL-0007 (Bid ID: 7)", st["body"]),
            Paragraph("<b>Procuring Entity:</b> BPCL Kochi", st["body"]),
        ]
    ]
    ref_table = Table(ref_data, colWidths=[180, 180, 163])
    ref_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_ACCENT_BG),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 10))

    # Core PAN Card Box
    story.append(Paragraph("Core Permanent Account Number Record", st["h2"]))
    pan_box_data = [
        [
            Paragraph("<b>PERMANENT ACCOUNT NUMBER (PAN)</b>", st["bold"]),
            Paragraph("DEFGH1004I", st["code"]),
            Paragraph("<b>PAN ALLOTMENT DATE</b>", st["bold"]),
            Paragraph("22/04/2017", st["body"]),
        ],
        [
            Paragraph("<b>LEGAL NAME</b>", st["bold"]),
            Paragraph("<b>Delta Manufacturing Pvt Ltd</b>", st["body"]),
            Paragraph("<b>PAN STATUS</b>", st["bold"]),
            Paragraph("<font color='#0F766E'><b>ACTIVE / OPERATIVE</b></font>", st["body"]),
        ],
        [
            Paragraph("<b>PAN CATEGORY / TYPE</b>", st["bold"]),
            Paragraph("COMPANY (Private Limited)", st["body"]),
            Paragraph("<b>VERIFICATION METHOD</b>", st["bold"]),
            Paragraph("Income Tax API / NSDL Database", st["body"]),
        ],
        [
            Paragraph("<b>REGISTERED ENTITY NAME</b>", st["bold"]),
            Paragraph("Delta Manufacturing Private Limited", st["body"]),
            Paragraph("<b>JURISDICTION WARD</b>", st["bold"]),
            Paragraph("WARD 14(3), CHENNAI", st["body"]),
        ],
        [
            Paragraph("<b>REGISTERED OFFICE ADDRESS</b>", st["bold"]),
            Paragraph("404, Ambattur Industrial Estate, Chennai, Tamil Nadu - 600058", st["body"]),
            Paragraph("<b>STATE CODE</b>", st["bold"]),
            Paragraph("Tamil Nadu (State Code: 33)", st["body"]),
        ],
    ]
    pan_table = Table(pan_box_data, colWidths=[140, 160, 110, 113])
    pan_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, C_NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (1, 0), (1, 0), C_ACCENT_BG),
    ]))
    story.append(pan_table)
    story.append(Spacer(1, 10))

    # Income Tax Return & Compliance History
    story.append(Paragraph("Income Tax Compliance & ITR Filing Track Record", st["h2"]))
    itr_data = [
        ["Assessment Year", "ITR Acknowledgement No.", "Filing Date", "Filing Status", "Tax Compliance"],
        ["AY 2023-24", "456789012345678", "28/10/2023", "FILED & VERIFIED", "COMPLIANT (Nil Demand)"],
        ["AY 2022-23", "345678901234567", "30/10/2022", "FILED & VERIFIED", "COMPLIANT (Nil Demand)"],
        ["AY 2021-22", "234567890123456", "25/11/2021", "FILED & VERIFIED", "COMPLIANT (Nil Demand)"],
    ]
    itr_table = Table(itr_data, colWidths=[80, 130, 80, 115, 118])
    itr_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_BG_LIGHT]),
    ]))
    story.append(itr_table)
    story.append(Spacer(1, 10))

    # Statutory Certificate & Legal Undertaking
    story.append(Paragraph("Statutory Validation Undertaking", st["h2"]))
    decl_p = Paragraph(
        "This e-PAN certificate confirms that Permanent Account Number <b>DEFGH1004I</b> has been duly allotted "
        "to <b>Delta Manufacturing Pvt Ltd</b> in accordance with Section 139A of the Income-tax Act, 1961. "
        "The record is active, verified with the National Tax Base, and all statutory filings are up to date with zero "
        "outstanding judicial tax demands. This document constitutes primary proof of financial identity for GeM Tender <b>GEM/2026/B/1003</b>.",
        st["alert"],
    )
    story.append(decl_p)
    story.append(Spacer(1, 12))

    # Signature Block
    sig_data = [
        [
            Paragraph("<b>Digitally Verified By:</b><br/>Directorate General of Income Tax (Systems)<br/>CBDT, New Delhi, Govt. of India<br/>UID: ITD-PAN-VERIF-DEFGH1004I", st["alert"]),
            Paragraph("<b>Authorized Signatory for Bidder:</b><br/>Delta Manufacturing Pvt Ltd<br/>Name: K. Sundaram, Managing Director<br/>DIN: 08849201 | Date: 01/03/2026", st["alert"]),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[260, 263])
    sig_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(sig_table)

    doc.build(story, canvasmaker=NumberedCanvas)


# ==============================================================================
# 2. GST REGISTRATION CERTIFICATE (FORM GST REG-06)
# ==============================================================================
def generate_gst_pdf(out_path):
    doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=48)
    st = get_styles()
    story = []

    story.append(Paragraph("GOVERNMENT OF INDIA &bull; GOODS AND SERVICES TAX", st["subtitle"]))
    story.append(Paragraph("FORM GST REG-06 &bull; REGISTRATION CERTIFICATE", st["title"]))
    story.append(Paragraph("Issued under Section 25 of the Central Goods and Services Tax Act, 2017 & Tamil Nadu GST Act", st["subtitle"]))
    story.append(Spacer(1, 8))

    # Reference Banner
    ref_data = [
        [
            Paragraph("<b>GeM Tender:</b> GEM/2026/B/1003", st["body"]),
            Paragraph("<b>Bid Submission:</b> BID-CPCL-0007 (Bid #7)", st["body"]),
            Paragraph("<b>Authority:</b> Bharat Petroleum Corp. Ltd", st["body"]),
        ]
    ]
    ref_table = Table(ref_data, colWidths=[180, 180, 163])
    ref_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_ACCENT_BG),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 10))

    # Core GSTIN Data
    story.append(Paragraph("Registration Details & Statutory Classification", st["h2"]))
    gst_data = [
        [
            Paragraph("<b>GSTIN</b>", st["bold"]),
            Paragraph("36DEFGH1004I1ZC", st["code"]),
            Paragraph("<b>REGISTRATION STATUS</b>", st["bold"]),
            Paragraph("<font color='#0F766E'><b>ACTIVE</b></font>", st["body"]),
        ],
        [
            Paragraph("<b>LEGAL NAME</b>", st["bold"]),
            Paragraph("<b>Delta Manufacturing Pvt Ltd</b>", st["body"]),
            Paragraph("<b>TRADE NAME</b>", st["bold"]),
            Paragraph("Delta Manufacturing Private Limited", st["body"]),
        ],
        [
            Paragraph("<b>CONSTITUTION OF BUSINESS</b>", st["bold"]),
            Paragraph("Private Limited Company", st["body"]),
            Paragraph("<b>TAXPAYER TYPE</b>", st["bold"]),
            Paragraph("<b>Regular</b>", st["body"]),
        ],
        [
            Paragraph("<b>DATE OF LIABILITY</b>", st["bold"]),
            Paragraph("22/04/2017", st["body"]),
            Paragraph("<b>PERIOD OF VALIDITY</b>", st["bold"]),
            Paragraph("From 22/04/2017 to Regular / Continuing", st["body"]),
        ],
        [
            Paragraph("<b>PRINCIPAL PLACE OF BUSINESS</b>", st["bold"]),
            Paragraph("404, Ambattur Industrial Estate, Chennai, Tamil Nadu - 600058", st["body"]),
            Paragraph("<b>STATE JURISDICTION</b>", st["bold"]),
            Paragraph("Tamil Nadu &bull; Range III, Chennai", st["body"]),
        ],
        [
            Paragraph("<b>PAN LINKED TO GSTIN</b>", st["bold"]),
            Paragraph("DEFGH1004I (Verified Active)", st["body"]),
            Paragraph("<b>CENTRE JURISDICTION</b>", st["bold"]),
            Paragraph("Chennai North Commissionerate", st["body"]),
        ],
    ]
    gst_table = Table(gst_data, colWidths=[140, 160, 110, 113])
    gst_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, C_NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (1, 0), (1, 0), C_ACCENT_BG),
    ]))
    story.append(gst_table)
    story.append(Spacer(1, 10))

    # Annexure A - Manufacturing & Operating Units
    story.append(Paragraph("Annexure A: Certified Manufacturing Units & Supply Locations", st["h2"]))
    ann_data = [
        ["Unit / Factory Code", "Address & Facility", "Operations / Line of Activity", "Compliance Status"],
        ["UNIT-01 (HQ)", "404, Ambattur Industrial Estate, Chennai, TN - 600058", "Heavy Gas Compression & Pumps Assembly", "ACTIVE"],
        ["UNIT-02 (Forging)", "Plot 18B, SIDCO Industrial Estate, Ambattur, Chennai", "High Pressure Impellers & Casing Foundry", "ACTIVE"],
        ["UNIT-03 (Testing)", "Refinery Equip. Test Bay 4, Ambattur, Chennai", "Hydrostatic & API 617 Performance Test Facility", "ACTIVE"],
    ]
    ann_table = Table(ann_data, colWidths=[85, 175, 185, 78])
    ann_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_BG_LIGHT]),
    ]))
    story.append(ann_table)
    story.append(Spacer(1, 10))

    # GSTR Filing Compliance Status
    story.append(Paragraph("Monthly Statutory GST Return Filing Compliance (GSTR-1 & GSTR-3B)", st["h2"]))
    filing_data = [
        ["Tax Period", "Return Type", "ARN Number", "Date of Filing", "Filing Status"],
        ["January 2026", "GSTR-3B", "AA330126049281X", "20/02/2026", "FILED - ON TIME"],
        ["December 2025", "GSTR-3B", "AA331225091823M", "19/01/2026", "FILED - ON TIME"],
        ["November 2025", "GSTR-3B", "AA331125018274Q", "18/12/2025", "FILED - ON TIME"],
    ]
    filing_table = Table(filing_data, colWidths=[90, 80, 140, 100, 113])
    filing_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_STEEL),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_BG_LIGHT]),
    ]))
    story.append(filing_table)
    story.append(Spacer(1, 10))

    # Signatory Block
    sig_data = [
        [
            Paragraph("<b>Approved By GST Authority:</b><br/>Commercial Taxes Department, Government of Tamil Nadu<br/>Assistant Commissioner of GST, Chennai North<br/>Digital Verification Stamp: GSTN-TN-36DEFGH1004I1ZC", st["alert"]),
            Paragraph("<b>Authorized Signatory for Bidder:</b><br/>Delta Manufacturing Pvt Ltd<br/>Name: K. Sundaram, Managing Director<br/>Date: 01/03/2026 | Place: Chennai", st["alert"]),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[260, 263])
    sig_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(sig_table)

    doc.build(story, canvasmaker=NumberedCanvas)


# ==============================================================================
# 3. OEM AUTHORIZATION & TECHNICAL WARRANTY UNDERTAKING
# ==============================================================================
def generate_oem_pdf(out_path):
    doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=48)
    st = get_styles()
    story = []

    story.append(Paragraph("DELTA MANUFACTURING PVT LTD &bull; HEAVY ENGINEERING DIVISION", st["subtitle"]))
    story.append(Paragraph("ORIGINAL EQUIPMENT MANUFACTURER (OEM) AUTHORIZATION CERTIFICATE", st["title"]))
    story.append(Paragraph("Original Equipment Manufacturer Authorization Form | Statutory Undertaking | Form OEM-AUTH-2026", st["subtitle"]))
    story.append(Spacer(1, 8))

    # Reference Header
    ref_data = [
        [
            Paragraph("<b>Tender Ref:</b> GEM/2026/B/1003", st["body"]),
            Paragraph("<b>Tender Title:</b> Procurement of Refinery Gas Compressors", st["body"]),
            Paragraph("<b>Procuring Entity:</b> BPCL Kochi", st["body"]),
        ]
    ]
    ref_table = Table(ref_data, colWidths=[160, 220, 143])
    ref_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_ACCENT_BG),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 10))

    # Core OEM Certification Matrix
    story.append(Paragraph("OEM Manufacturer Authorization Details & Parameters", st["h2"]))
    oem_data = [
        [
            Paragraph("<b>OEM AUTHORIZATION NUMBER</b>", st["bold"]),
            Paragraph("DM-OEM-AUTH-2026-1004", st["code"]),
            Paragraph("<b>AUTHORIZATION STATUS</b>", st["bold"]),
            Paragraph("<font color='#0F766E'><b>ACTIVE / VALID</b></font>", st["body"]),
        ],
        [
            Paragraph("<b>OEM / MANUFACTURER NAME</b>", st["bold"]),
            Paragraph("<b>Delta Manufacturing Pvt Ltd</b>", st["body"]),
            Paragraph("<b>AUTHORIZED BIDDER</b>", st["bold"]),
            Paragraph("Delta Manufacturing Pvt Ltd (Self-OEM)", st["body"]),
        ],
        [
            Paragraph("<b>AUTHORIZATION DATE</b>", st["bold"]),
            Paragraph("15/02/2026", st["body"]),
            Paragraph("<b>VALID UNTIL</b>", st["bold"]),
            Paragraph("14/02/2028 (24 Months Operative)", st["body"]),
        ],
        [
            Paragraph("<b>PRODUCT CATEGORY</b>", st["bold"]),
            Paragraph("Heavy Machinery & Gas Compressors", st["body"]),
            Paragraph("<b>BID REFERENCE</b>", st["bold"]),
            Paragraph("BID-CPCL-0007 (Bid ID: 7)", st["body"]),
        ],
        [
            Paragraph("<b>APPLICABLE STANDARDS</b>", st["bold"]),
            Paragraph("API 617 (Centrifugal), API 610, IS 2825", st["body"]),
            Paragraph("<b>MANUFACTURING PLANT</b>", st["bold"]),
            Paragraph("Ambattur Industrial Estate, Chennai", st["body"]),
        ],
        [
            Paragraph("<b>MANUFACTURER PAN / CIN</b>", st["bold"]),
            Paragraph("PAN: DEFGH1004I | CIN: U00004IN2020PTC000004", st["body"]),
            Paragraph("<b>OEM STATUS IN REGISTRY</b>", st["bold"]),
            Paragraph("<b>VERIFIED OEM (is_oem = True)</b>", st["body"]),
        ],
    ]
    oem_table = Table(oem_data, colWidths=[140, 160, 110, 113])
    oem_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, C_NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (1, 0), (1, 0), C_ACCENT_BG),
    ]))
    story.append(oem_table)
    story.append(Spacer(1, 10))

    # OEM Mandatory Technical Undertaking
    story.append(Paragraph("Mandatory OEM Warranty & Technical Undertaking", st["h2"]))
    decl_clauses = [
        Paragraph("1. <b>Bona Fide Manufacturer Certification:</b> We hereby certify that Delta Manufacturing Pvt Ltd is the genuine Original Equipment Manufacturer (OEM) of the offered Centrifugal Refinery Process Gas Compressors and Heavy Process Pumps with dedicated manufacturing lines at Ambattur, Chennai.", st["body"]),
        Paragraph("2. <b>Direct OEM Warranty:</b> We provide a comprehensive 24-month OEM on-site warranty from the date of commissioning at BPCL Kochi Refinery, covering full replacement of mechanical seals, bearings, impellers, and auxiliary subsystems.", st["body"]),
        Paragraph("3. <b>Life-Cycle Spares & Service Guarantee:</b> We unequivocally guarantee the availability of original OEM replacement components, overhaul services, and specialized rotor assembly engineering support for a minimum period of 10 years.", st["body"]),
        Paragraph("4. <b>API 617 Technical Adherence:</b> The supplied machinery is engineered with horizontally split heavy alloy casings, 17-4PH precipitation-hardened stainless steel impellers, dry gas seals with nitrogen barrier purging, and integrated automated anti-surge control protection valves.", st["body"]),
    ]
    for clause in decl_clauses:
        story.append(clause)
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 6))

    # Technical Specifications Comparison
    story.append(Paragraph("Technical Parameters & Manufacturing Specifications", st["h2"]))
    tech_data = [
        ["Parameter", "Tender Requirement", "OEM Manufacturer Certified Specification", "Conformity"],
        ["Design Standard", "API 617 / API 610", "API 617 8th Edition & API 610 Centrifugal Heavy Duty", "COMPLIES"],
        ["Casing Test Pressure", "Minimum 1.5x MAWP", "Hydrostatically tested to 1.8x MAWP (85.0 bar)", "COMPLIES"],
        ["Surge Control", "Automated Anti-Surge Loop", "Dual-redundant high-speed PLC automated surge loop (<80ms)", "COMPLIES"],
        ["Rotor Balancing", "ISO 1940 Grade G1.0", "Precision dynamic balanced to Grade G0.67", "COMPLIES"],
    ]
    tech_table = Table(tech_data, colWidths=[95, 125, 230, 73])
    tech_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_BG_LIGHT]),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 10))

    # Signature Block
    sig_data = [
        [
            Paragraph("<b>Factory & Quality Assurance Head:</b><br/>Delta Manufacturing Pvt Ltd<br/>Ambattur Heavy Works Division, Chennai<br/>R. Venkataraman, VP Technical & Quality<br/>Stamp: CERTIFIED OEM PRODUCTION PLANT", st["alert"]),
            Paragraph("<b>Executive OEM Signatory:</b><br/>Delta Manufacturing Pvt Ltd<br/>K. Sundaram, Managing Director<br/>Date: 15/02/2026 | Place: Chennai<br/>Reference: DM-OEM-AUTH-2026-1004", st["alert"]),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[260, 263])
    sig_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(sig_table)

    doc.build(story, canvasmaker=NumberedCanvas)


# ==============================================================================
# 4. BIS QUALITY MARK LICENCE (CM/L-1000004 & IS 2825)
# ==============================================================================
def generate_bis_pdf(out_path):
    doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=48)
    st = get_styles()
    story = []

    story.append(Paragraph("BUREAU OF INDIAN STANDARDS &bull; भारतीय मानक ब्यूरो", st["subtitle"]))
    story.append(Paragraph("LICENCE FOR THE USE OF STANDARD MARK (ISI / BIS)", st["title"]))
    story.append(Paragraph("Granted under the Bureau of Indian Standards Act, 2016 & Conformity Assessment Regulations", st["subtitle"]))
    story.append(Spacer(1, 8))

    # Reference Header
    ref_data = [
        [
            Paragraph("<b>Tender Mandate:</b> GEM/2026/B/1003", st["body"]),
            Paragraph("<b>Bid Reference:</b> BID-CPCL-0007 (Bid #7)", st["body"]),
            Paragraph("<b>Procuring Entity:</b> BPCL Kochi", st["body"]),
        ]
    ]
    ref_table = Table(ref_data, colWidths=[180, 180, 163])
    ref_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_ACCENT_BG),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 10))

    # Core BIS Licence Details
    story.append(Paragraph("Standard Mark Licence Record (National Conformity Database)", st["h2"]))
    bis_data = [
        [
            Paragraph("<b>LICENCE NUMBER (CM/L)</b>", st["bold"]),
            Paragraph("CM/L-1000004", st["code"]),
            Paragraph("<b>LICENCE STATUS</b>", st["bold"]),
            Paragraph("<font color='#0F766E'><b>OPERATIVE</b></font>", st["body"]),
        ],
        [
            Paragraph("<b>LICENSEE / MANUFACTURER</b>", st["bold"]),
            Paragraph("<b>Delta Manufacturing Pvt Ltd</b>", st["body"]),
            Paragraph("<b>LEGAL NAME IN REGISTRY</b>", st["bold"]),
            Paragraph("Delta Manufacturing Pvt Ltd", st["body"]),
        ],
        [
            Paragraph("<b>INDIAN STANDARD NUMBER</b>", st["bold"]),
            Paragraph("<b>IS 2825</b>", st["bold"]),
            Paragraph("<b>PRODUCT NAME</b>", st["bold"]),
            Paragraph("Gas Compression Systems", st["body"]),
        ],
        [
            Paragraph("<b>DATE OF GRANT / ISSUE</b>", st["bold"]),
            Paragraph("12/07/2015", st["body"]),
            Paragraph("<b>VALID UNTIL</b>", st["bold"]),
            Paragraph("31/12/2030 (Operative Long-Term)", st["body"]),
        ],
        [
            Paragraph("<b>CERTIFIED FACTORY ADDRESS</b>", st["bold"]),
            Paragraph("Ambattur Industrial Estate Chennai, Tamil Nadu", st["body"]),
            Paragraph("<b>OPERATING STATE</b>", st["bold"]),
            Paragraph("Tamil Nadu", st["body"]),
        ],
        [
            Paragraph("<b>SUPERVISING BRANCH</b>", st["bold"]),
            Paragraph("Chennai Branch Office (CNBO), SRO", st["body"]),
            Paragraph("<b>SCHEME OF TESTING</b>", st["bold"]),
            Paragraph("SIT-2825 (100% Factory Tested)", st["body"]),
        ],
    ]
    bis_table = Table(bis_data, colWidths=[140, 160, 110, 113])
    bis_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, C_NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (1, 0), (1, 0), C_ACCENT_BG),
    ]))
    story.append(bis_table)
    story.append(Spacer(1, 10))

    # Scope of Certification & Technical Standard Endorsement
    story.append(Paragraph("Scope of Endorsement & Product Classification", st["h2"]))
    scope_data = [
        ["Standard Code", "Standard Description", "Endorsed Manufacturing Scope", "Testing Scheme"],
        ["IS 2825:1969", "Code for Unfired Pressure Vessels", "Refinery Process Gas Compressor Casings, Intercoolers & Pulsation Dampeners", "Hydrostatic 1.5x, Radiographic RT-1"],
        ["IS/ISO 9001:2015", "Quality Management Systems", "Design, Manufacture, Assembly and Testing of Centrifugal Compressors", "Audit Surveillance Passed"],
        ["API 617 / 610", "Refinery Rotating Equipment", "Axial / Centrifugal Compressors for Petroleum & Gas Industries", "Shop Test & Factory Performance Run"],
    ]
    scope_table = Table(scope_data, colWidths=[80, 120, 223, 100])
    scope_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_BG_LIGHT]),
    ]))
    story.append(scope_table)
    story.append(Spacer(1, 10))

    # Quality Audit & Inspection History
    story.append(Paragraph("Quality Surveillance & Periodic Factory Inspection Log", st["h2"]))
    insp_data = [
        ["Surveillance Date", "Auditing Officer / Branch", "Sample Testing Result", "Licence Status"],
        ["14/11/2025", "CNBO / Scientist-D (Mechanical)", "PASSED (Compressor Casing Burst & NDT Conformity)", "ENDORSED OPERATIVE"],
        ["18/11/2024", "CNBO / Scientist-D (Metallurgy)", "PASSED (Material Grade IS 2825 Class 1)", "ENDORSED OPERATIVE"],
        ["22/10/2023", "CNBO / Quality Assessment Team", "PASSED (Performance & Pressure Vessel Safety)", "ENDORSED OPERATIVE"],
    ]
    insp_table = Table(insp_data, colWidths=[85, 140, 208, 90])
    insp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_STEEL),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_BG_LIGHT]),
    ]))
    story.append(insp_table)
    story.append(Spacer(1, 10))

    # Signatory Block
    sig_data = [
        [
            Paragraph("<b>Issued by Competent BIS Authority:</b><br/>Bureau of Indian Standards (BIS)<br/>Southern Regional Office, CIT Campus, Chennai<br/>Scientist-F & Head, CNBO<br/>Digital Certificate UID: BIS-SRO-CML1000004", st["alert"]),
            Paragraph("<b>Licensee Acceptance & Endorsement:</b><br/>Delta Manufacturing Pvt Ltd<br/>K. Sundaram, Managing Director<br/>Date: 01/03/2026 | Factory: Ambattur, Chennai<br/>Tender Submission: GEM/2026/B/1003", st["alert"]),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[260, 263])
    sig_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.8, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(sig_table)

    doc.build(story, canvasmaker=NumberedCanvas)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_data_dir = base_dir
    frontend_pub_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "frontend", "public", "sample-documents"))
    storage_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "storage", "documents"))

    os.makedirs(sample_data_dir, exist_ok=True)
    os.makedirs(frontend_pub_dir, exist_ok=True)
    os.makedirs(storage_dir, exist_ok=True)

    docs = [
        ("bid_7_pan_certificate.pdf", generate_pan_pdf),
        ("bid_7_gst_certificate.pdf", generate_gst_pdf),
        ("bid_7_oem_authorization.pdf", generate_oem_pdf),
        ("bid_7_bis_certificate.pdf", generate_bis_pdf),
    ]

    for filename, gen_fn in docs:
        out_sample = os.path.join(sample_data_dir, filename)
        gen_fn(out_sample)
        print(f"Generated: {out_sample} ({os.path.getsize(out_sample)} bytes)")

        # Copy to frontend public
        out_frontend = os.path.join(frontend_pub_dir, filename)
        with open(out_sample, "rb") as f_src, open(out_frontend, "wb") as f_dst:
            f_dst.write(f_src.read())
        print(f"Copied to frontend public: {out_frontend}")

    print("\nAll 4 mandatory documents generated successfully!")


if __name__ == "__main__":
    main()
