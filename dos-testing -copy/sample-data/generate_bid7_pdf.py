import os
import sys
import shutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

OUTPUT_DIR = os.path.abspath("docs-and-testing/sample-data")
FRONTEND_PUBLIC_DIR = os.path.abspath("frontend/public/sample-documents")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRONTEND_PUBLIC_DIR, exist_ok=True)

PDF_PATH = os.path.join(OUTPUT_DIR, "bid_7_end_to_end_compliance_test.pdf")
PUBLIC_PDF_PATH = os.path.join(FRONTEND_PUBLIC_DIR, "bid_7_end_to_end_compliance_test.pdf")

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
            self.drawRightString(555, 812, "BID REF: BID-CPCL-0007 | TENDER: GEM/2026/B/1003")

        # Running Bottom Footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 42, 555, 42)
        self.drawString(40, 30, "Delta Manufacturing Pvt Ltd • Official Bid Submission Dossier • Self-Certified Document")
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
            Paragraph("<b>BID ID:</b> 7", meta_bar_style),
            Paragraph("<b>TENDER ID:</b> 3", meta_bar_style),
            Paragraph("<b>BIDDER ID:</b> 24", meta_bar_style),
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

    # SECTION 1: TENDER & INVITATION DETAILS
    story.append(Paragraph("SECTION 1: TENDER & INVITATION DETAILS", sec_heading))
    sec1_data = [
        [Paragraph("Tender Reference Number", table_label), Paragraph("GEM/2026/B/1003", table_val_mono),
         Paragraph("Tender Database ID", table_label), Paragraph("3", table_val)],
        [Paragraph("Tender Title", table_label), Paragraph("Procurement of Refinery Process Gas Compressors and Pumps", table_val),
         Paragraph("Procurement Category", table_label), Paragraph("Goods (Oil and Gas)", table_val)],
        [Paragraph("Procuring Organization", table_label), Paragraph("Bharat Petroleum Corporation Limited (BPCL)", table_val),
         Paragraph("Department", table_label), Paragraph("Refinery Operations", table_val)],
        [Paragraph("Site / Delivery Location", table_label), Paragraph("Kochi Kerala", table_val),
         Paragraph("Submission Deadline", table_label), Paragraph("15-12-2026 15:00:00 IST", table_val)],
        [Paragraph("Estimated Tender Value", table_label), Paragraph("INR 60,000,000.00 (INR 6.00 Cr)", table_val_mono),
         Paragraph("Scope Summary", table_label), Paragraph("Supply & performance testing of heavy-duty centrifugal gas compressors for refinery expansion", table_val)],
        [Paragraph("Statutory Criteria Thresholds", table_label), Paragraph("Min Turnover: INR 120,000,000 | Min Experience: 8 Years | OEM Status: REQUIRED", table_val),
         Paragraph("Mandatory Documents Required", table_label), Paragraph("PAN, GST, OEM_AUTHORIZATION, BIS_CERTIFICATE", table_val)],
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
        [Paragraph("Bid Dossier Number", table_label), Paragraph("BID-CPCL-0007 (Database ID: 7)", table_val_mono),
         Paragraph("Bidder Reference ID", table_label), Paragraph("24", table_val)],
        [Paragraph("Submitted Quoted Amount", table_label), Paragraph("INR 58,000,000.00 (INR 5.80 Cr)", table_val_mono),
         Paragraph("Budget Variance", table_label), Paragraph("96.7% of Estimated Budget (Competitive)", table_val)],
        [Paragraph("Submission Date & Time", table_label), Paragraph("06-09-2026 11:34:13 IST", table_val),
         Paragraph("Workflow Status", table_label), Paragraph("SUBMITTED", table_val_mono)],
        [Paragraph("Technical Proposal Scope", table_label), 
         Paragraph("Centrifugal process gas compressors with automated surge control and API 617 compliance.", table_val),
         Paragraph("Responsiveness", table_label), Paragraph("Fully Responsive to GeM NIT GEM/2026/B/1003", table_val)],
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
        [Paragraph("Company Legal Name", table_label), Paragraph("Delta Manufacturing Pvt Ltd", table_val_mono),
         Paragraph("Operating Trade Name", table_label), Paragraph("Delta Manufacturing Pvt Ltd", table_val)],
        [Paragraph("Constitution / Business Type", table_label), Paragraph("Private Limited (Non-govt company)", table_val),
         Paragraph("Date of Incorporation", table_label), Paragraph("12-07-2015 (RoC-Chennai)", table_val)],
        [Paragraph("Principal Registered Address", table_label), Paragraph("Chennai Tamil Nadu, India", table_val),
         Paragraph("State of Domicile", table_label), Paragraph("Tamil Nadu (State Code: 33/36)", table_val)],
        [Paragraph("Designated Contact Person", table_label), Paragraph("Contact Person 4", table_val),
         Paragraph("Official Contact Email", table_label), Paragraph("bidder4@example.com", table_val)],
        [Paragraph("Official Contact Phone", table_label), Paragraph("+91 9000000004", table_val),
         Paragraph("Industry Sector & Category", table_label), Paragraph("Oil and Gas • Gas Compression Systems", table_val)],
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

    # Clean Page Break
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SECTION 4, SECTION 5, SECTION 6, SECTION 7
    # =========================================================================
    story.append(Paragraph("SECTION 4: STATUTORY REGISTRATION IDENTIFIERS", sec_heading))
    sec4_data = [
        [Paragraph("Statutory Authority", table_label), Paragraph("Registration Number", table_label), 
         Paragraph("Registration Date", table_label), Paragraph("Verification State", table_label)],
        [Paragraph("Permanent Account Number (PAN)", table_val), Paragraph("DEFGH1004I", table_val_mono), 
         Paragraph("22-04-2017 (Issued: COMPANY)", table_val), Paragraph("ACTIVE / OPERATIVE", table_val_mono)],
        [Paragraph("GST Identification Number (GSTIN)", table_val), Paragraph("36DEFGH1004I1ZC", table_val_mono), 
         Paragraph("22-04-2017 (Regular Taxpayer)", table_val), Paragraph("ACTIVE / REGULAR", table_val_mono)],
        [Paragraph("Corporate Identity Number (CIN)", table_val), Paragraph("U00004IN2020PTC000004", table_val_mono), 
         Paragraph("12-07-2015 (RoC-Chennai)", table_val), Paragraph("ACTIVE / COMPLIANT", table_val_mono)],
        [Paragraph("MSME Udyam Registration", table_val), Paragraph("UDYAM-IN-12-0000004", table_val_mono), 
         Paragraph("05-10-2020 (Enterprise: MEDIUM)", table_val), Paragraph("ACTIVE / VERIFIED", table_val_mono)],
        [Paragraph("EPFO Establishment Code", table_val), Paragraph("EPFO-TN-10004", table_val_mono), 
         Paragraph("12-07-2015 (210 Employees)", table_val), Paragraph("COMPLIANT (Month: 2026-08)", table_val_mono)],
        [Paragraph("ESIC Establishment Number", table_val), Paragraph("31000000040001004", table_val_mono), 
         Paragraph("12-07-2015 (195 Employees)", table_val), Paragraph("COMPLIANT (Branch: Chennai North)", table_val_mono)],
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
        [Paragraph("Annual Certified Turnover", table_label), Paragraph("INR 300,000,000.00 (INR 30.00 Cr)", table_val_mono),
         Paragraph("Tender Min Requirement", table_label), Paragraph("INR 120,000,000.00 (MET: 250%)", table_val)],
        [Paragraph("Authorized Share Capital", table_label), Paragraph("INR 60,000,000.00 (INR 6.00 Cr)", table_val),
         Paragraph("Paid-up Share Capital", table_label), Paragraph("INR 35,000,000.00 (INR 3.50 Cr)", table_val)],
        [Paragraph("Cumulative Experience in Sector", table_label), Paragraph("11 Years (Since 2015)", table_val_mono),
         Paragraph("Tender Min Experience", table_label), Paragraph("8 Years (MET: Satisfied)", table_val)],
        [Paragraph("Income Tax Return (ITR) Ack No.", table_label), Paragraph("456789012345678", table_val_mono),
         Paragraph("Assessment Year Filed", table_label), Paragraph("AY 2023-24 (Filing Date: 22-07-2023)", table_val)],
        [Paragraph("Certified Total Income (ITR)", table_label), Paragraph("INR 3,000,000.00 (Status: FILED)", table_val),
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

    # SECTION 6: TECHNICAL SPECIFICATION & PRODUCT ELIGIBILITY
    story.append(Paragraph("SECTION 6: TECHNICAL SPECIFICATION & PRODUCT ELIGIBILITY", sec_heading))
    sec6_data = [
        [Paragraph("Product Name & Specification", table_label), 
         Paragraph("Gas Compression Systems • Centrifugal Process Gas Compressors & Pumps", table_val)],
        [Paragraph("Design & Construction Standard", table_label), 
         Paragraph("API 617 & API Spec 610 compliant, automated anti-surge controls, dry gas seal system", table_val)],
        [Paragraph("Applicable Indian Standard (BIS)", table_label), 
         Paragraph("IS 2825 (Unfired Pressure Vessels & High-Pressure Gas Systems)", table_val_mono)],
        [Paragraph("Target Operational Domain", table_label), 
         Paragraph("Refinery gas treating, catalytic cracking units, and hydrogen recovery process trains", table_val)],
        [Paragraph("Factory Location & In-House Testing", table_label), 
         Paragraph("Ambattur Industrial Estate Chennai, Tamil Nadu (Heavy dynamic test bay & closed-loop testing)", table_val)],
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
        "We, <b>Delta Manufacturing Pvt Ltd</b>, hereby solemnly declare and certify that we are the "
        "<b>Original Equipment Manufacturer (OEM)</b> of the offered heavy-duty centrifugal process gas compressors "
        "and centrifugal process pumps. The complete manufacturing, impeller milling, precision balancing, casing casting, "
        "and aerodynamic performance testing are executed at our facility in <b>Ambattur Industrial Estate Chennai, Tamil Nadu</b>. "
        "We satisfy the mandatory OEM qualification requirement specified in Tender GEM/2026/B/1003. "
        "We hold all proprietary design models, impeller finite element analyses, and OEM test certifications."
    )
    story.append(Paragraph(oem_text, body_style))

    # Clean Page Break
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SECTION 8, SECTION 9, SECTION 10, SECTION 11, SECTION 12
    # =========================================================================
    story.append(Paragraph("SECTION 8: QUALITY MARKS & STATUTORY CERTIFICATION DOCKET", sec_heading))
    sec8_data = [
        [Paragraph("Certification / Quality Standard", table_label), Paragraph("Registration / Licence No.", table_label), 
         Paragraph("Validity Period", table_label), Paragraph("Operative Status", table_label)],
        [Paragraph("Bureau of Indian Standards (BIS Mark)", table_val), Paragraph("CM/L-1000004 (Standard: IS 2825)", table_val_mono), 
         Paragraph("12-07-2015 to 31-12-2030", table_val), Paragraph("OPERATIVE / VALID", table_val_mono)],
        [Paragraph("American Petroleum Institute (API)", table_val), Paragraph("API Spec 610 / API 617 Certified", table_val_mono), 
         Paragraph("Valid through 31-12-2028", table_val), Paragraph("CERTIFIED", table_val_mono)],
        [Paragraph("NSIC Single Point Registration", table_val), Paragraph("NSIC-TN-10004 (Category: MEDIUM)", table_val_mono), 
         Paragraph("12-07-2015 to 31-12-2030", table_val), Paragraph("ACTIVE (Limit: 2.50 Cr)", table_val_mono)],
        [Paragraph("DPIIT Startup Recognition", table_val), Paragraph("DIPP10004 (Oil & Gas Sector)", table_val_mono), 
         Paragraph("22-08-2016 to 31-12-2030", table_val), Paragraph("ACTIVE / ELIGIBLE", table_val_mono)],
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
        "we certify that the local content in the offered process gas compression equipment exceeds <b>72.5%</b>, "
        "qualifying Delta Manufacturing Pvt Ltd as a <b>Class-I Local Supplier</b>. Local manufacturing, machining, "
        "and assembly are executed at Ambattur Industrial Estate, Chennai."
    )
    story.append(Paragraph(local_content_text, body_style))
    story.append(Spacer(1, 8))

    # SECTION 10: NON-BLACKLISTING & INTEGRITY
    story.append(Paragraph("SECTION 10: NON-BLACKLISTING & STATUTORY INTEGRITY DECLARATION", sec_heading))
    integrity_text = (
        "We hereby affirm and declare under official corporate attestation that <b>Delta Manufacturing Pvt Ltd</b>, its directors, "
        "and key management personnel have never been debarred, blacklisted, or suspended by BPCL, Ministry of Petroleum & "
        "Natural Gas, GeM, or any central/state public sector undertaking. The company is completely free of any statutory defaults."
    )
    story.append(Paragraph(integrity_text, body_style))
    story.append(Spacer(1, 8))

    # SECTION 11: DOCUMENT CHECKLIST
    story.append(Paragraph("SECTION 11: MANDATORY TENDER DOCUMENT MAPPING CHECKLIST", sec_heading))
    sec11_data = [
        [Paragraph("Required Tender Document", table_label), Paragraph("Attached File Reference", table_label), 
         Paragraph("Indexed Identifier", table_label), Paragraph("Format / Size", table_label)],
        [Paragraph("1. PAN Verification Certificate", table_val), Paragraph("Delta_Mfg_PAN_Card.pdf", table_val_mono), 
         Paragraph("PAN: DEFGH1004I", table_val), Paragraph("PDF / 280 KB", table_val)],
        [Paragraph("2. GSTIN Registration Certificate", table_val), Paragraph("Delta_Mfg_GST_Certificate.pdf", table_val_mono), 
         Paragraph("GSTIN: 36DEFGH1004I1ZC", table_val), Paragraph("PDF / 395 KB", table_val)],
        [Paragraph("3. OEM Self-Manufacturer Attestation", table_val), Paragraph("Delta_Mfg_OEM_Certificate.pdf", table_val_mono), 
         Paragraph("OEM Facility: Ambattur Chennai", table_val), Paragraph("PDF / 510 KB", table_val)],
        [Paragraph("4. BIS Licence Document", table_val), Paragraph("Delta_Mfg_BIS_Licence.pdf", table_val_mono), 
         Paragraph("Licence: CM/L-1000004 (IS 2825)", table_val), Paragraph("PDF / 640 KB", table_val)],
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
                      "<b>Delta Manufacturing Pvt Ltd</b><br/>"
                      "CIN: U00004IN2020PTC000004<br/>"
                      "Registered Office: Chennai, Tamil Nadu, India<br/>"
                      "Date of Signature: 06-09-2026", body_style),
            Paragraph("<b>AUTHORIZED SIGNATORY:</b><br/>"
                      "<b>Contact Person 4</b><br/>"
                      "Designation: Director of Operations & Engineering<br/>"
                      "Email: bidder4@example.com | Tel: +91 9000000004<br/>"
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
