import os
import sys
import pypdf
import fitz  # PyMuPDF
import re

pdf_path = os.path.abspath("docs-and-testing/sample-data/bid_7_end_to_end_compliance_test.pdf")

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
    ("Bid ID", "BID ID: 7"),
    ("Tender ID", "TENDER ID: 3"),
    ("Bidder ID", "BIDDER ID: 24"),
    ("Version", "VERSION: 1.0"),
    ("Tender Reference", "GEM/2026/B/1003"),
    ("Bid Dossier Number", "BID-CPCL-0007"),
    
    # Bidder Details (bidders table)
    ("Company Legal Name", "Delta Manufacturing Pvt Ltd"),
    ("Constitution", "Private Limited"),
    ("PAN", "DEFGH1004I"),
    ("GSTIN", "36DEFGH1004I1ZC"),
    ("CIN", "U00004IN2020PTC000004"),
    ("Udyam Number", "UDYAM-IN-12-0000004"),
    ("Registered Address", "Chennai Tamil Nadu"),
    ("Contact Person", "Contact Person 4"),
    ("Email", "bidder4@example.com"),
    ("Phone", "9000000004"),
    ("Incorporation Date", "12-07-2015"),
    ("Annual Turnover", "300,000,000.00"),
    ("Experience", "11 Years"),
    ("Industry Sector", "Oil and Gas"),
    ("Product Category", "Gas Compression Systems"),
    
    # Commercial & Tender details (tenders & bids tables)
    ("Bid Quoted Amount", "58,000,000.00"),
    ("Bid Status", "SUBMITTED"),
    ("Tender Estimated Value", "60,000,000.00"),
    ("Tender Minimum Turnover", "120,000,000.00"),
    ("Tender Minimum Experience", "8 Years"),
    ("Tender Org", "Bharat Petroleum Corporation Limited (BPCL)"),
    ("Tender Dept", "Refinery Operations"),
    ("Mandatory Documents Required", "PAN, GST, OEM_AUTHORIZATION, BIS_CERTIFICATE"),
    
    # Government Records (pan_records, gst_records, udyam_records, mca_records, etc.)
    ("EPFO Code", "EPFO-TN-10004"),
    ("ESIC Number", "31000000040001004"),
    ("BIS Licence", "CM/L-1000004"),
    ("BIS Standard", "IS 2825"),
    ("ITR Acknowledgment", "456789012345678"),
    ("ITR Assessment Year", "AY 2023-24"),
    ("DIPP Startup Number", "DIPP10004"),
    ("NSIC Number", "NSIC-TN-10004"),
    
    # OEM & Quality Standards
    ("OEM Declaration", "Original Equipment Manufacturer"),
    ("Factory Address", "Ambattur Industrial Estate Chennai"),
    ("API Quality Standard", "API Spec 610 / API 617"),
    ("Local Content Tier", "Class-I Local Supplier"),
    ("Non-Blacklisting Declaration", "have never been debarred, blacklisted, or suspended"),
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
print("SUCCESS: 100% of all database fields, government identifiers, and statutory declarations are verified in the PDF text!")
