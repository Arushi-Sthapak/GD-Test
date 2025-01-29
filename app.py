import streamlit as st
import sqlite3
import smtplib
import random
from email.mime.text import MIMEText

# Database setup
def init_db():
    conn = sqlite3.connect("gd_slots.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registrations 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, slot TEXT)''')
    conn.commit()
    conn.close()

# Add registration to DB
def register_user(email, slot):
    conn = sqlite3.connect("gd_slots.db")
    c = conn.cursor()
    c.execute("INSERT INTO registrations (email, slot) VALUES (?, ?)", (email, slot))
    conn.commit()
    conn.close()

# Get count of users in a slot
def get_slot_count(slot):
    conn = sqlite3.connect("gd_slots.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM registrations WHERE slot = ?", (slot,))
    count = c.fetchone()[0]
    conn.close()
    return count

# Send confirmation email
def send_email(to_email, slot):
    sender_email = "sthapakarushi@gmail.com"  # Replace with your email
    sender_password = "chgg rtly yyuj ljmu"  # Replace with app password
    subject = "GD Slot Confirmation"
    body = f"You have successfully registered for the GD session at {slot}.\nGoogle Meet Link: https://meet.google.com/example"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        st.error(f"Email failed: {e}")

# Predefined topics
topics = ["Impact of AI on Jobs", "Is Social Media a Boon or Bane?", "Work from Home vs Office"]

def main():
    st.title("Group Discussion Practice")
    init_db()
    
    slots = ["10:00 AM", "5:00 PM"]
    selected_slot = st.selectbox("Select Your GD Slot", slots)
    email = st.text_input("Enter your email:")
    
    if st.button("Register"):
        if email:
            if get_slot_count(selected_slot) < 6:
                register_user(email, selected_slot)
                send_email(email, selected_slot)
                st.success("Registered successfully! Check your email for details.")
            else:
                st.error("This slot is full. Try another slot.")
        else:
            st.error("Please enter a valid email.")
    
    st.subheader("Slot Availability")
    for slot in slots:
        st.write(f"{slot}: {get_slot_count(slot)} / 6 Participants")
    
    st.subheader("Today's GD Topic")
    st.write(random.choice(topics))
    
if __name__ == "__main__":
    main()
