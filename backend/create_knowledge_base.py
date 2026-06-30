# create_knowledge_base.py
# Run once to generate all company PDFs into the knowledge_base/ folder
# Usage: python3 create_knowledge_base.py

from fpdf import FPDF
import os

OUTPUT_DIR = "../knowledge_base"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def make_pdf(filename: str, title: str, content: str):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", size=11)
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue
        pdf.multi_cell(0, 7, line, new_x="LMARGIN", new_y="NEXT")

    path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(path)
    print(f"Created: {path}")


# ── 1. FAQ ────────────────────────────────────────────────────────────────────
make_pdf("FAQ.pdf", "TechMart Electronics- Frequently Asked Questions", """
Q: What is TechMart Electronics?
A: TechMart Electronics is an online retailer specializing in consumer electronics including laptops, smartphones, tablets, smart home devices, and accessories.

Q: Where is TechMart Electronics located?
A: Our headquarters is in Bangalore, India. We operate entirely online and ship across India.

Q: What are your customer support hours?
A: Our AI support is available 24/7. Human agents are available Monday to Saturday, 9 AM to 7 PM IST.

Q: How do I contact support?
A: You can chat with us here, email support@techmart.in, or call 1800-123-4567 (toll free, Mon-Sat 9AM-7PM IST).

Q: Do you have a physical store?
A: No, TechMart Electronics is an online-only store.

Q: What payment methods do you accept?
A: We accept UPI, net banking, all major credit and debit cards, EMI (3/6/12 months), and cash on delivery for orders under Rs. 10,000.

Q: Is my payment information secure?
A: Yes. All payments are processed through PCI-DSS compliant gateways. We never store your card details.

Q: Can I change or cancel my order?
A: Orders can be cancelled or modified within 2 hours of placement, before they enter the packing stage.

Q: Do you offer EMI?
A: Yes, no-cost EMI is available on orders above Rs. 5,000 for 3, 6, and 12 month tenures with select banks.

Q: How do I track my order?
A: Once shipped, you will receive an SMS and email with your tracking number. You can also track at techmart.in/track.
""")


# ── 2. Refund Policy ──────────────────────────────────────────────────────────
make_pdf("RefundPolicy.pdf", "TechMart Electronics- Refund & Return Policy", """
RETURN WINDOW
Customers may return most products within 10 days of delivery. Opened smartphones and laptops must be returned within 7 days. Products marked "non-returnable" on the product page cannot be returned.

ELIGIBILITY FOR RETURN
To be eligible for a return, the product must be:
- Unused and in original condition (for 10-day returns)
- In original packaging with all accessories, manuals, and warranty cards
- Accompanied by the original invoice

DAMAGED OR DEFECTIVE PRODUCTS
If you receive a damaged or defective product, report it within 48 hours of delivery via the app or by calling 1800-123-4567. We will arrange a free pickup and send a replacement or full refund.

REFUND PROCESS
Once we receive and inspect the returned product, refunds are processed within 5-7 business days. Refunds are credited to the original payment method.
- UPI / Net Banking: 3-5 business days
- Credit / Debit Card: 5-7 business days
- Cash on Delivery: Refund via bank transfer within 7 business days (IFSC and account number required)

NON-REFUNDABLE ITEMS
- Software, digital products, and game codes once activated
- Products with broken seals (unless defective)
- Items damaged due to misuse or physical damage by the customer

HOW TO INITIATE A RETURN
1. Log in to techmart.in and go to My Orders
2. Select the order and click "Return / Exchange"
3. Choose reason and upload a photo if defective
4. Schedule a free pickup or drop off at a partner centre
""")


# ── 3. Shipping Policy ────────────────────────────────────────────────────────
make_pdf("ShippingPolicy.pdf", "TechMart Electronics- Shipping Policy", """
DELIVERY TIMEFRAMES
- Metro cities (Bangalore, Mumbai, Delhi, Chennai, Hyderabad, Pune): 1-2 business days
- Tier 2 cities: 2-4 business days
- Tier 3 cities and rural areas: 4-7 business days

SHIPPING CHARGES
- Orders above Rs. 499: Free shipping
- Orders below Rs. 499: Flat Rs. 49 shipping fee
- Express delivery (available in metro cities): Rs. 99 extra, delivered same day if ordered before 12 PM

SAME DAY DELIVERY
Same day delivery is available in Bangalore, Mumbai, Delhi, Chennai, Hyderabad, and Pune for orders placed before 12 PM IST on business days.

TRACKING YOUR ORDER
You will receive tracking details via SMS and email once your order is dispatched. Live tracking is available on techmart.in/track using your order ID or tracking number.

DELIVERY PARTNERS
We ship via Delhivery, BlueDart, Ekart, and India Post depending on your location. High-value orders above Rs. 20,000 are shipped only via BlueDart with signature confirmation.

FAILED DELIVERY
If delivery fails after 3 attempts, the package is returned to our warehouse. Contact support within 7 days to reschedule; after that the order is cancelled and refunded.

INTERNATIONAL SHIPPING
TechMart Electronics currently ships only within India.

HOLIDAYS
Orders are not dispatched on national public holidays. This may add 1 business day to delivery estimates.
""")


# ── 4. Pricing & Plans ────────────────────────────────────────────────────────
make_pdf("Pricing.pdf", "TechMart Electronics- Product Pricing & Subscription Plans", """
SMARTPHONE RANGE
- TechMart Basic A10: Rs. 8,999
- TechMart Pro X20: Rs. 18,999
- TechMart Ultra Z30: Rs. 34,999
- TechMart Elite Z50: Rs. 54,999

LAPTOP RANGE
- TechMart Laptop Lite (Intel i3, 8GB, 256GB SSD): Rs. 32,999
- TechMart Laptop Pro (Intel i5, 16GB, 512GB SSD): Rs. 54,999
- TechMart Laptop Ultra (Intel i7, 16GB, 1TB SSD): Rs. 79,999

TABLETS
- TechMart Tab 8 (Wi-Fi): Rs. 12,999
- TechMart Tab 10 Pro (Wi-Fi + 5G): Rs. 24,999

ACCESSORIES
- TechMart TWS Earbuds: Rs. 1,999
- TechMart Smartwatch S1: Rs. 4,999
- TechMart 65W Fast Charger: Rs. 999
- TechMart USB-C Hub (7-in-1): Rs. 1,499

TECHMART CARE PLANS (optional extended warranty + support)
- TechMart Care Basic: Rs. 499/year- covers manufacturing defects, extends warranty by 1 year
- TechMart Care Plus: Rs. 999/year- covers defects + accidental screen damage (1 claim/year)
- TechMart Care Max: Rs. 1,999/year- covers defects + accidental damage + theft (2 claims/year)

PRICE MATCH GUARANTEE
If you find the same product cheaper on Flipkart or Amazon within 24 hours of purchase, we will refund the difference. Contact support with a screenshot of the lower price.
""")


# ── 5. Warranty ───────────────────────────────────────────────────────────────
make_pdf("Warranty.pdf", "TechMart Electronics- Warranty Policy", """
STANDARD WARRANTY PERIODS
- Smartphones: 1 year manufacturer warranty
- Laptops: 1 year manufacturer warranty
- Tablets: 1 year manufacturer warranty
- Smartwatches: 1 year manufacturer warranty
- TWS Earbuds: 6 months manufacturer warranty
- Chargers and Cables: 6 months manufacturer warranty
- USB Hubs and Accessories: 6 months manufacturer warranty

WHAT IS COVERED
- Manufacturing defects
- Hardware failure under normal use
- Battery defects (capacity below 80% within warranty period)
- Display defects not caused by physical damage

WHAT IS NOT COVERED
- Physical damage (cracked screen, dents, water damage)
- Damage from unauthorised repair or modification
- Software issues caused by third-party apps
- Consumable parts (stylus tips, ear tips)
- Cosmetic damage (scratches on body)

HOW TO CLAIM WARRANTY
1. Contact support at 1800-123-4567 or support@techmart.in
2. Provide your order ID and describe the issue
3. Our team will diagnose remotely or arrange pickup for inspection
4. If the defect is covered, we will repair or replace the product at no charge
5. Turnaround time for warranty repair: 7-10 business days

EXTENDED WARRANTY
Extended warranty can be purchased via TechMart Care plans (see Pricing document) up to 30 days after the original purchase.

OUT-OF-WARRANTY REPAIRS
We offer paid repair services for out-of-warranty products. Diagnosis fee of Rs. 199 is charged upfront and adjusted against repair cost if you proceed.
""")


# ── 6. Technical Troubleshooting Guide ───────────────────────────────────────
make_pdf("TechSupport.pdf", "TechMart Electronics- Technical Troubleshooting Guide", """
SMARTPHONE ISSUES

Problem: Phone won't turn on
Solution: Charge for at least 30 minutes. Hold power button for 10 seconds. If no response, contact support.

Problem: Phone overheating
Solution: Remove case, close all background apps, avoid charging while gaming. If persistent, could indicate battery issue- contact support.

Problem: Touch screen not responding
Solution: Restart the device. Clean screen with dry cloth. If unresponsive after restart, contact support for hardware check.

Problem: Cannot connect to Wi-Fi
Solution: Forget the network and reconnect. Restart router. Check if other devices connect. Reset network settings under Settings > General > Reset.

LAPTOP ISSUES

Problem: Laptop won't boot
Solution: Hold power button 10 seconds to force shutdown. Disconnect all peripherals. Try booting again. If no display, contact support.

Problem: Laptop running slowly
Solution: Check for background processes in Task Manager. Ensure less than 90% disk usage. Restart and run system updates.

Problem: Battery draining fast
Solution: Reduce screen brightness. Disable Bluetooth and Wi-Fi when not needed. Check battery health in settings. Contact support if below 80% capacity within warranty.

Problem: Keyboard keys not working
Solution: Restart device. Check for debris under keys. Connect external keyboard to confirm if hardware issue. Contact support if confirmed hardware fault.

ACCOUNT ISSUES

Problem: Cannot log in to TechMart account
Solution: Use "Forgot Password" on login page. Check email for reset link (check spam folder). If account is locked after 5 failed attempts, wait 30 minutes or contact support.

Problem: OTP not received
Solution: Check mobile signal. Try "Resend OTP" after 60 seconds. Ensure your registered mobile number is correct. Contact support to update mobile number.

GENERAL

Problem: App crashing
Solution: Update the TechMart app to the latest version. Clear app cache under phone settings. Uninstall and reinstall if issue persists.

Problem: Order not showing in account
Solution: Confirm you placed the order on the correct account email. Check spam for order confirmation. Contact support with payment reference number.
""")

print("\nAll PDFs created successfully in knowledge_base/")
print("You can now run: python3 rag/ingest.py")