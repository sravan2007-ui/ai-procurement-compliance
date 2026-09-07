import os
import sys
import shutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

OUTPUT_DIR = os.path.abspath("docs-and-testing/sample-data")
FRONTEND_PUBLIC_DIR = os.path.abspath("frontend/public/sample-documents")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRONTEND_PUBLIC_DIR, exist_ok=True)

PDF_PATH = os.path.join(OUTPUT_DIR, "bid_1_end_to_end_compliance_test.pdf")
PUBLIC_PDF_PATH = os.path.join(FRONTEND_PUBLIC_DIR, "bid_1_end_to_end_compliance_test.pdf")

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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Running Top Header on pages > 1
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, 808, 555, 808)
            self.drawString(40, 812, "GOVERNMENT e-PROCUREMENT (GeM) • BID SUBMISSION & COMPLIANCE DOSSIER")
            self.drawRightString(555, 812, "BID REF: BID-CPCL-0001 | TENDER: GEM/2026/B/1001")

        # Running Bottom Footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 42, 555, 42)
        self.drawString(40, 30, "ABC Technologies Pvt Ltd • Authoritative Bid Submission Dossier • Self-Certified Document")
        self.drawRightString(555, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#0F172A") # slate-900
    accent_blue = colors.HexColor("#1E3A8A")   # blue-900
    text_dark = colors.HexColor("#1E293B")     # slate-800
    text_muted = colors.HexColor("#64748B")    # slate-500
    border_color = colors.HexColor("#CBD5E1")  # slate-300
    bg_light = colors.HexColor("#F8FAFC")      # slate-50
    bg_header = colors.HexColor("#F1F5F9")     # slate-100

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=accent_blue,
        alignment=1
    )

    meta_bar_style = ParagraphStyle(
        'MetaBar',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#065F46"),
        alignment=1
    )

    sec_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=accent_blue,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=text_dark
    )

    table_label = ParagraphStyle(
        'TableLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=text_dark
    )

    table_val = ParagraphStyle(
        'TableValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=text_dark
    )

    table_val_mono = ParagraphStyle(
        'TableValueMono',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.5,
        leading=10,
        textColor=accent_blue
    )

    story = []

    # =========================================================================
    # PAGE 1: HEADER, METADATA, SECTION 1, SECTION 2, SECTION 3
    # =========================================================================
    banner_data = [
        [
            Paragraph("<b>GOVERNMENT OF INDIA • MINISTRY OF PETROLEUM & NATURAL GAS</b><br/>"
                      "<font size=6.5 color='#64748B'>GOVERNMENT e-PROCUREMENT (GeM) COMPLIANCE VERIFICATION PLATFORM</font>", 
                      ParagraphStyle('BannerL', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=primary_color)),
            Paragraph("<b>OFFICIAL BID SUBMISSION</b><br/>"
                      "<font size=6.5 color='#047857'>CONFIDENTIAL / BID DOSSIER</font>",
                      ParagraphStyle('BannerR', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=accent_blue, alignment=2))
        ]
    ]
    t_banner = Table(banner_data, colWidths=[355, 160])
    t_banner.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 1, accent_blue)
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 6))

    story.append(Paragraph("BID SUBMISSION AND COMPLIANCE EVIDENCE DOCUMENT", title_style))
    story.append(Paragraph("TECHNICAL, STATUTORY & COMMERCIAL QUALIFICATION DOCKET", subtitle_style))
    story.append(Spacer(1, 5))

    meta_box = [
        [
            Paragraph("<b>DOCUMENT TYPE:</b> Bid Submission / Compliance Evidence", meta_bar_style),
            Paragraph("<b>BID ID:</b> 1", meta_bar_style),
            Paragraph("<b>TENDER ID:</b> 1", meta_bar_style),
            Paragraph("<b>BIDDER ID:</b> 21", meta_bar_style),
            Paragraph("<b>VERSION:</b> 1.0", meta_bar_style)
        ]
    ]
    t_meta = Table(meta_box, colWidths=[165, 75, 85, 95, 95])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ECFDF5")),
        ('BORDER', (0,0), (-1,-1), 0.5, colors.HexColor("#A7F3D0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # SECTION 1: TENDER DETAILS
    story.append(Paragraph("SECTION 1: TENDER & INVITATION DETAILS", sec_heading))
    sec1_data = [
        [Paragraph("Tender Reference Number", table_label), Paragraph("GEM/2026/B/1001", table_val_mono),
         Paragraph("Tender Database ID", table_label), Paragraph("1", table_val)],
        [Paragraph("Tender Title", table_label), Paragraph("Supply and Installation of High-Pressure Industrial Valves", table_val),
         Paragraph("Procurement Category", table_label), Paragraph("Goods (Oil and Gas)", table_val)],
        [Paragraph("Procuring Organization", table_label), Paragraph("Oil and Natural Gas Corporation (ONGC)", table_val),
         Paragraph("Department", table_label), Paragraph("Drilling and Production", table_val)],
        [Paragraph("Site / Delivery Location", table_label), Paragraph("Mumbai Maharashtra", table_val),
         Paragraph("Submission Deadline", table_label), Paragraph("31-12-2026 18:00:00 IST", table_val)],
        [Paragraph("Estimated Tender Value", table_label), Paragraph("INR 25,000,000.00 (INR 2.50 Cr)", table_val_mono),
         Paragraph("Scope Summary", table_label), Paragraph("Procurement & commissioning of API-grade high pressure valves for offshore platforms", table_val)],
        [Paragraph("Statutory Criteria Thresholds", table_label), Paragraph("Min Turnover: INR 50,000,000 | Min Experience: 5 Years | OEM Status: REQUIRED", table_val),
         Paragraph("Mandatory Documents Required", table_label), Paragraph("PAN, GST, BIS_CERTIFICATE, AUDITED_BALANCE_SHEET", table_val)],
    ]
    t1 = Table(sec1_data, colWidths=[125, 140, 115, 135])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    # SECTION 2: BID DETAILS
    story.append(Paragraph("SECTION 2: COMMERCIAL BID PROPOSAL & SUBMISSION", sec_heading))
    sec2_data = [
        [Paragraph("Bid Dossier Number", table_label), Paragraph("BID-CPCL-0001 (Database ID: 1)", table_val_mono),
         Paragraph("Bidder Reference ID", table_label), Paragraph("21", table_val)],
        [Paragraph("Submitted Quoted Amount", table_label), Paragraph("INR 24,200,000.00 (INR 2.42 Cr)", table_val_mono),
         Paragraph("Budget Variance", table_label), Paragraph("96.8% of Estimated Budget (Competitive)", table_val)],
        [Paragraph("Submission Date & Time", table_label), Paragraph("06-09-2026 11:34:13 IST", table_val),
         Paragraph("Workflow Status", table_label), Paragraph("SUBMITTED", table_val_mono)],
        [Paragraph("Technical Description Scope", table_label), 
         Paragraph("Turnkey supply of high-pressure API 6D pipeline ball and gate valves with forged steel bodies.", table_val),
         Paragraph("Responsiveness", table_label), Paragraph("Fully Responsive to GeM NIT GEM/2026/B/1001", table_val)],
    ]
    t2 = Table(sec2_data, colWidths=[125, 140, 115, 135])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    # SECTION 3: BIDDER CORPORATE IDENTIFICATION
    story.append(Paragraph("SECTION 3: BIDDER CORPORATE IDENTIFICATION", sec_heading))
    sec3_data = [
        [Paragraph("Company Legal Name", table_label), Paragraph("ABC Technologies Pvt Ltd", table_val_mono),
         Paragraph("Operating Trade Name", table_label), Paragraph("ABC Technologies Pvt Ltd", table_val)],
        [Paragraph("Constitution / Business Type", table_label), Paragraph("Private Limited (Non-govt company)", table_val),
         Paragraph("Date of Incorporation", table_label), Paragraph("15-01-2010 (RoC-Mumbai)", table_val)],
        [Paragraph("Principal Registered Address", table_label), Paragraph("Mumbai Maharashtra, India", table_val),
         Paragraph("State of Domicile", table_label), Paragraph("Maharashtra (State Code: 27/29)", table_val)],
        [Paragraph("Designated Contact Person", table_label), Paragraph("Contact Person 1", table_val),
         Paragraph("Official Contact Email", table_label), Paragraph("bidder1@example.com", table_val)],
        [Paragraph("Official Contact Phone", table_label), Paragraph("+91 9000000001", table_val),
         Paragraph("Industry Sector & Category", table_label), Paragraph("Oil and Gas • Industrial Pumps and Pipeline Equipment", table_val)],
    ]
    t3 = Table(sec3_data, colWidths=[125, 140, 115, 135])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t3)

    # Clean Break to Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SECTION 4, SECTION 5, SECTION 6, SECTION 7
    # =========================================================================
    story.append(Paragraph("SECTION 4: STATUTORY REGISTRATION IDENTIFIERS", sec_heading))
    sec4_data = [
        [Paragraph("Statutory Authority", table_label), Paragraph("Registration Number", table_label), 
         Paragraph("Registration Date", table_label), Paragraph("Verification State", table_label)],
        [Paragraph("Permanent Account Number (PAN)", table_val), Paragraph("ABCDE1001F", table_val_mono), 
         Paragraph("10-01-2018 (Issued: COMPANY)", table_val), Paragraph("ACTIVE / OPERATIVE", table_val_mono)],
        [Paragraph("GST Identification Number (GSTIN)", table_val), Paragraph("29ABCDE1001F1Z7", table_val_mono), 
         Paragraph("10-01-2018 (Regular Taxpayer)", table_val), Paragraph("ACTIVE / REGULAR", table_val_mono)],
        [Paragraph("Corporate Identity Number (CIN)", table_val), Paragraph("U00001IN2020PTC000001", table_val_mono), 
         Paragraph("15-01-2010 (RoC-Mumbai)", table_val), Paragraph("ACTIVE / COMPLIANT", table_val_mono)],
        [Paragraph("MSME Udyam Registration", table_val), Paragraph("UDYAM-IN-12-0000001", table_val_mono), 
         Paragraph("02-07-2020 (Enterprise: MEDIUM)", table_val), Paragraph("ACTIVE / VERIFIED", table_val_mono)],
        [Paragraph("EPFO Establishment Code", table_val), Paragraph("EPFO-MH-10001", table_val_mono), 
         Paragraph("15-01-2010 (120 Employees)", table_val), Paragraph("COMPLIANT (Month: 2026-08)", table_val_mono)],
        [Paragraph("ESIC Establishment Number", table_val), Paragraph("31000000010001001", table_val_mono), 
         Paragraph("15-01-2010 (110 Employees)", table_val), Paragraph("COMPLIANT (Branch: Mumbai)", table_val_mono)],
    ]
    t4 = Table(sec4_data, colWidths=[150, 140, 115, 110])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_header),
        ('BACKGROUND', (0,1), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t4)
    story.append(Spacer(1, 8))

    # SECTION 5: FINANCIAL & EXPERIENCE
    story.append(Paragraph("SECTION 5: FINANCIAL CAPACITY & EXPERIENCE CREDENTIALS", sec_heading))
    sec5_data = [
        [Paragraph("Annual Certified Turnover", table_label), Paragraph("INR 180,000,000.00 (INR 18.00 Cr)", table_val_mono),
         Paragraph("Tender Min Requirement", table_label), Paragraph("INR 50,000,000.00 (MET: 360%)", table_val)],
        [Paragraph("Authorized Share Capital", table_label), Paragraph("INR 50,000,000.00 (INR 5.00 Cr)", table_val),
         Paragraph("Paid-up Share Capital", table_label), Paragraph("INR 25,000,000.00 (INR 2.50 Cr)", table_val)],
        [Paragraph("Cumulative Experience in Sector", table_label), Paragraph("16 Years (Since 2010)", table_val_mono),
         Paragraph("Tender Min Experience", table_label), Paragraph("5 Years (MET: Satisfied)", table_val)],
        [Paragraph("Income Tax Return (ITR) Ack No.", table_label), Paragraph("123456789012345", table_val_mono),
         Paragraph("Assessment Year Filed", table_label), Paragraph("AY 2023-24 (Filing Date: 15-07-2023)", table_val)],
        [Paragraph("Certified Total Income (ITR)", table_label), Paragraph("INR 1,500,000.00 (Status: FILED)", table_val),
         Paragraph("Audit Standard", table_label), Paragraph("Audited by Chartered Accountants", table_val)],
    ]
    t5 = Table(sec5_data, colWidths=[130, 135, 115, 135])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t5)
    story.append(Spacer(1, 8))

    # SECTION 6: TECHNICAL / PRODUCT SPECIFICATIONS
    story.append(Paragraph("SECTION 6: TECHNICAL SPECIFICATION & PRODUCT ELIGIBILITY", sec_heading))
    sec6_data = [
        [Paragraph("Product Name & Specification", table_label), 
         Paragraph("Industrial Pumps and Pipeline Equipment • API 6D Pipeline Ball and Gate Valves", table_val)],
        [Paragraph("Design & Construction Standard", table_label), 
         Paragraph("Forged steel body, high-pressure rating (ASME Class 150 to 2500), NACE MR0175 compliant", table_val)],
        [Paragraph("Applicable Indian Standard (BIS)", table_label), 
         Paragraph("IS 1520 (High-Pressure Pipeline Service Specification)", table_val_mono)],
        [Paragraph("Target Operational Domain", table_label), 
         Paragraph("Offshore crude oil production, pipeline transportation, and refinery manifold systems", table_val)],
        [Paragraph("Factory Location & In-House Testing", table_label), 
         Paragraph("Plot 12 MIDC Mumbai, Maharashtra, India (Hydrostatic test facility up to 10,000 PSI in-house)", table_val)],
    ]
    t6 = Table(sec6_data, colWidths=[150, 365])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t6)
    story.append(Spacer(1, 8))

    # SECTION 7: OEM DECLARATION
    story.append(Paragraph("SECTION 7: ORIGINAL EQUIPMENT MANUFACTURER (OEM) DECLARATION", sec_heading))
    oem_text = (
        "We, <b>ABC Technologies Pvt Ltd</b>, hereby solemnly declare and certify that we are the "
        "<b>Original Equipment Manufacturer (OEM)</b> of the quoted industrial valves and pipeline equipment. "
        "The manufacturing, machining, assembly, welding, and pressure testing are carried out in our fully owned "
        "manufacturing facility situated at <b>Plot 12 MIDC Mumbai, Maharashtra</b>. "
        "We satisfy the mandatory OEM qualification requirement stipulated in Tender GEM/2026/B/1001. "
        "We possess all necessary engineering drawings, type-test certificates, and manufacturing machinery required "
        "to execute this contract without third-party authorization."
    )
    story.append(Paragraph(oem_text, body_style))

    # Clean Break to Page 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SECTION 8, SECTION 9, SECTION 10, SECTION 11, SECTION 12
    # =========================================================================
    story.append(Paragraph("SECTION 8: QUALITY MARKS & STATUTORY CERTIFICATION DOCKET", sec_heading))
    sec8_data = [
        [Paragraph("Certification / Quality Standard", table_label), Paragraph("Registration / Licence No.", table_label), 
         Paragraph("Validity Period", table_label), Paragraph("Operative Status", table_label)],
        [Paragraph("Bureau of Indian Standards (BIS Mark)", table_val), Paragraph("CM/L-1000001 (Standard: IS 1520)", table_val_mono), 
         Paragraph("15-01-2010 to 31-12-2030", table_val), Paragraph("OPERATIVE / VALID", table_val_mono)],
        [Paragraph("Quality Management System (ISO)", table_val), Paragraph("ISO 9001:2015 (QMS-IND-2020-001)", table_val_mono), 
         Paragraph("Valid through 31-12-2028", table_val), Paragraph("CERTIFIED", table_val_mono)],
        [Paragraph("NSIC Single Point Registration", table_val), Paragraph("NSIC-MH-10001 (Category: SMALL)", table_val_mono), 
         Paragraph("15-01-2010 to 31-12-2030", table_val), Paragraph("ACTIVE (Limit: 1.50 Cr)", table_val_mono)],
        [Paragraph("DPIIT Startup Recognition", table_val), Paragraph("DIPP10001 (Oil & Gas Sector)", table_val_mono), 
         Paragraph("20-01-2016 to 31-12-2030", table_val), Paragraph("ACTIVE / ELIGIBLE", table_val_mono)],
    ]
    t8 = Table(sec8_data, colWidths=[150, 140, 115, 110])
    t8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_header),
        ('BACKGROUND', (0,1), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t8)
    story.append(Spacer(1, 8))

    # SECTION 9: LOCAL CONTENT (MAKE IN INDIA)
    story.append(Paragraph("SECTION 9: LOCAL CONTENT (MAKE IN INDIA) DECLARATION", sec_heading))
    local_content_text = (
        "In accordance with the Public Procurement (Preference to Make in India) Order issued by DPIIT, "
        "we certify that the local content in the offered goods exceeds <b>65.0%</b>, qualifying ABC Technologies Pvt Ltd as a "
        "<b>Class-I Local Supplier</b>. Local manufacturing and value addition are conducted at our Mumbai works."
    )
    story.append(Paragraph(local_content_text, body_style))
    story.append(Spacer(1, 8))

    # SECTION 10: NON-BLACKLISTING & INTEGRITY
    story.append(Paragraph("SECTION 10: NON-BLACKLISTING & STATUTORY INTEGRITY DECLARATION", sec_heading))
    integrity_text = (
        "We hereby affirm and swear under official corporate oath that <b>ABC Technologies Pvt Ltd</b>, its directors, and "
        "officers have not been debarred, blacklisted, or suspended by any Ministry, Government Department, PSU, GeM, or "
        "CVC. The company maintains an unblemished compliance record with no insolvency proceedings or statutory tax defaults."
    )
    story.append(Paragraph(integrity_text, body_style))
    story.append(Spacer(1, 8))

    # SECTION 11: DOCUMENT CHECKLIST
    story.append(Paragraph("SECTION 11: MANDATORY TENDER DOCUMENT MAPPING CHECKLIST", sec_heading))
    sec11_data = [
        [Paragraph("Required Tender Document", table_label), Paragraph("Attached File Reference", table_label), 
         Paragraph("Indexed Identifier", table_label), Paragraph("Format / Size", table_label)],
        [Paragraph("1. PAN Verification Certificate", table_val), Paragraph("ABC_Technologies_PAN_Card.pdf", table_val_mono), 
         Paragraph("PAN: ABCDE1001F", table_val), Paragraph("PDF / 245 KB", table_val)],
        [Paragraph("2. GSTIN Registration Certificate", table_val), Paragraph("ABC_Technologies_GST_Certificate.pdf", table_val_mono), 
         Paragraph("GSTIN: 29ABCDE1001F1Z7", table_val), Paragraph("PDF / 412 KB", table_val)],
        [Paragraph("3. BIS Licence Document", table_val), Paragraph("ABC_Technologies_BIS_Licence.pdf", table_val_mono), 
         Paragraph("Licence: CM/L-1000001 (IS 1520)", table_val), Paragraph("PDF / 620 KB", table_val)],
        [Paragraph("4. Audited Balance Sheet & Financials", table_val), Paragraph("ABC_Technologies_Audited_Accounts.pdf", table_val_mono), 
         Paragraph("Turnover: INR 180,000,000.00", table_val), Paragraph("PDF / 1.2 MB", table_val)],
    ]
    t11 = Table(sec11_data, colWidths=[140, 150, 135, 90])
    t11.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_header),
        ('BACKGROUND', (0,1), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t11)
    story.append(Spacer(1, 10))

    # SECTION 12: SIGNATORY DECLARATION
    story.append(Paragraph("SECTION 12: AUTHORIZED SIGNATORY ATTESTATION", sec_heading))
    sec12_data = [
        [
            Paragraph("<b>FOR AND ON BEHALF OF:</b><br/>"
                      "<b>ABC Technologies Pvt Ltd</b><br/>"
                      "CIN: U00001IN2020PTC000001<br/>"
                      "Registered Office: Mumbai, Maharashtra, India<br/>"
                      "Date of Signature: 06-09-2026", body_style),
            Paragraph("<b>AUTHORIZED SIGNATORY:</b><br/>"
                      "<b>Contact Person 1</b><br/>"
                      "Designation: Managing Director & CEO<br/>"
                      "Email: bidder1@example.com | Tel: +91 9000000001<br/>"
                      "<i>Digitally Signed via DSC Class-3 SHA256</i>", body_style)
        ]
    ]
    t12 = Table(sec12_data, colWidths=[250, 265])
    t12.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t12)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {PDF_PATH}")

    shutil.copyfile(PDF_PATH, PUBLIC_PDF_PATH)
    print(f"Copied to Public Download URL: {PUBLIC_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
