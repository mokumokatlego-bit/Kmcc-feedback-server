import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("market_trends.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            customer_id TEXT,
            message TEXT,
            category TEXT,
            timestamp DATETIME
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS response_rules (
            category TEXT PRIMARY KEY,
            auto_response TEXT
        )
    ''')
    
    cursor.execute("INSERT OR IGNORE INTO response_rules VALUES ('general', 'Thank you for reaching out to K.M.C.C.! How can we assist you today?')")
    cursor.execute("INSERT OR IGNORE INTO response_rules VALUES ('pricing', 'Thanks for inquiring! Check out our latest price list and offers.')")
    cursor.execute("INSERT OR IGNORE INTO response_rules VALUES ('delivery', 'We offer delivery across local routes. Let us know your location!')")
    
    conn.commit()
    conn.close()

def process_incoming_feedback(source, customer_id, message):
    conn = sqlite3.connect("market_trends.db")
    cursor = conn.cursor()
    
    msg_lower = message.lower()
    category = "general"
    if "price" in msg_lower or "cost" in msg_lower or "quote" in msg_lower:
        category = "pricing"
    elif "delivery" in msg_lower or "ship" in msg_lower or "order" in msg_lower:
        category = "delivery"

    cursor.execute(
        "INSERT INTO feedback (source, customer_id, message, category, timestamp) VALUES (?, ?, ?, ?, ?)",
        (source, customer_id, message, category, datetime.now())
    )
    
    cursor.execute("SELECT auto_response FROM response_rules WHERE category = ?", (category,))
    result = cursor.fetchone()
    response_text = result[0] if result else "Thank you for contacting K.M.C.C. Bakery!"
    
    conn.commit()
    conn.close()
    
    return category, response_text
