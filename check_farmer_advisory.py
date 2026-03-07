import sqlite3

conn = sqlite3.connect('krishimitra.db')
cursor = conn.cursor()

# Check farmer language
cursor.execute("SELECT farmer_id, phone_number, preferred_language FROM farmers WHERE phone_number = '+918095666788'")
farmer = cursor.fetchone()

if farmer:
    farmer_id, phone, lang = farmer
    print(f"Farmer: {phone}")
    print(f"Language: {lang}")
    print(f"Farmer ID: {farmer_id}")
    print()
    
    # Check latest advisory
    cursor.execute("""
        SELECT advisory_id, advisory_text, risk_score, created_at 
        FROM advisories 
        WHERE farmer_id = ?
        ORDER BY created_at DESC 
        LIMIT 1
    """, (farmer_id,))
    
    advisory = cursor.fetchone()
    if advisory:
        adv_id, text, risk, created = advisory
        print(f"Latest Advisory:")
        print(f"  ID: {adv_id}")
        print(f"  Created: {created}")
        print(f"  Risk Score: {risk}")
        print(f"  Text preview: {text[:200] if text else 'NULL'}...")
    else:
        print("No advisories found")
else:
    print("Farmer not found")

conn.close()
