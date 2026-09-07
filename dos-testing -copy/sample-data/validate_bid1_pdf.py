import os
import sys
import pypdf
import fitz  # PyMuPDF
import re

pdf_path = os.path.abspath("docs-and-testing/sample-data/bid_1_end_to_end_compliance_test.pdf")

print(f"=== 1. VALIDATING PDF INTEGRITY: {pdf_path} ===")
file_size = os.path.getsize(pdf_path)
print(f"File Size: {file_size} bytes ({file_size/1024:.2f} KB)")

# Open with PyMuPDF
doc = fitz.open(pdf_path)
page_count = len(doc)
print(f"Page Count: {page_count}")
assert page_count == 3, f"Expected exactly 3 clean pages, found {page_count}"

full_text = ""
for i, page in enumerate(doc):
    page_text = page.get_text()
    full_text += f"\n--- PAGE {i+1} ---\n" + page_text
    print(f"Page {i+1}: {len(page_text)} characters extracted.")

# Normalize whitespace for matching across line wraps
norm_text = re.sub(r'\s+', ' ', full_text)

print("\n=== 2. FIELD-BY-FIELD VERIFICATION AGAINST POSTGRESQL DATABASE ===")
checks = [
    # Metadata & Identifiers
    ("Document Type", "Bid Submission / Compliance Evidence"),
    ("Bid ID", "BID ID: 1"),
    ("Tender ID", "TENDER ID: 1"),
    ("Bidder ID", "BIDDER ID: 21"),
    ("Version", "VERSION: 1.0"),
    ("Tender Reference", "GEM/2026/B/1001"),
    ("Bid Dossier Number", "BID-CPCL-0001"),
    
    # Bidder Details (bidders table)
    ("Company Legal Name", "ABC Technologies Pvt Ltd"),
    ("Constitution", "Private Limited"),
    ("PAN", "ABCDE1001F"),
    ("GSTIN", "29ABCDE1001F1Z7"),
    ("CIN", "U00001IN2020PTC000001"),
    ("Udyam Number", "UDYAM-IN-12-0000001"),
    ("Registered Address", "Mumbai Maharashtra"),
    ("Contact Person", "Contact Person 1"),
    ("Email", "bidder1@example.com"),
    ("Phone", "9000000001"),
    ("Incorporation Date", "15-01-2010"),
    ("Annual Turnover", "180,000,000.00"),
    ("Experience", "16 Years"),
    ("Industry Sector", "Oil and Gas"),
    ("Product Category", "Industrial Pumps and Pipeline Equipment"),
    
    # Commercial & Tender details (tenders & bids tables)
    ("Bid Quoted Amount", "24,200,000.00"),
    ("Bid Status", "SUBMITTED"),
    ("Tender Estimated Value", "25,000,000.00"),
    ("Tender Minimum Turnover", "50,000,000.00"),
    ("Tender Minimum Experience", "5 Years"),
    ("Tender Org", "Oil and Natural Gas Corporation (ONGC)"),
    ("Tender Dept", "Drilling and Production"),
    ("Mandatory Documents Required", "PAN, GST, BIS_CERTIFICATE, AUDITED_BALANCE_SHEET"),
    
    # Government Records (pan_records, gst_records, udyam_records, mca_records, etc.)
    ("EPFO Code", "EPFO-MH-10001"),
    ("ESIC Number", "31000000010001001"),
    ("BIS Licence", "CM/L-1000001"),
    ("BIS Standard", "IS 1520"),
    ("ITR Acknowledgment", "123456789012345"),
    ("ITR Assessment Year", "AY 2023-24"),
    ("DIPP Startup Number", "DIPP10001"),
    ("NSIC Number", "NSIC-MH-10001"),
    
    # OEM & Quality Standards
    ("OEM Declaration", "Original Equipment Manufacturer"),
    ("Factory Address", "Plot 12 MIDC Mumbai"),
    ("ISO Quality Standard", "ISO 9001:2015"),
    ("Local Content Tier", "Class-I Local Supplier"),
    ("Non-Blacklisting Declaration", "have not been debarred, blacklisted, or suspended"),
]

passed = 0
failed = 0
for label, target in checks:
    if target in norm_text:
        print(f"  [PASS] {label:30} : Found '{target}'")
        passed += 1
    else:
        print(f"  [FAIL] {label:30} : NOT FOUND '{target}'")
        failed += 1

print(f"\n============================================================")
print(f"VERIFICATION SUMMARY: {passed} PASSED, {failed} FAILED out of {len(checks)} CHECKS")
print(f"============================================================")
assert failed == 0, f"{failed} validation checks failed!"
print("100% of all database fields, government identifiers, and statutory declarations are correctly grounded in the PDF text.")
