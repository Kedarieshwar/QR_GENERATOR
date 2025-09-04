import qrcode
import pandas as pd
import uuid
from fpdf import FPDF
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# --- CONFIGURATION ---
SENDER_EMAIL = "kedarieshwarkrishna@gmail.com"
SENDER_APP_PASSWORD = "roadblkeeuxxcqom" 

def send_email_with_ticket(recipient_email, user_name, pdf_file_path):
    """
    Connects to the email server and sends the generated ticket.
    """
    if not SENDER_EMAIL or "your_email" in SENDER_EMAIL:
        print("\n--- EMAIL NOT SENT ---")
        print("Please configure SENDER_EMAIL and SENDER_APP_PASSWORD at the top of the script.")
        return

    print(f"\nPreparing to send ticket to {recipient_email}...")

    try:
        # Create the email message object
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = "Your Event Ticket is Here!"

        # Add the email body
        body = f"Hi {user_name},\n\nThank you for registering! Your event ticket is attached to this email.\n\nWe look forward to seeing you!\n"
        msg.attach(MIMEText(body, 'plain'))

        # Attach the PDF file
        with open(pdf_file_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_file_path))
        msg.attach(attach)

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() # Secure the connection
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
        
        print("Email sent successfully!")

    except Exception as e:
        print(f"\n--- ERROR: FAILED TO SEND EMAIL ---")
        print(f"An error occurred: {e}")
        print("Please check your email credentials and ensure 'Less secure app access' is not needed for App Passwords.")


def register_and_generate_ticket():
    """
    Handles registration, QR generation, PDF creation, and emailing the ticket.
    """
    # 1. Get User Details
    name = input("Enter your full name: ")
    email = input("Enter your email address: ")

    # 2. Generate a Unique Ticket ID
    ticket_id = str(uuid.uuid4())
    database_file = 'attendees.csv'

    # 3. Save Attendee Info to CSV
    new_attendee = pd.DataFrame({
        'name': [name], 'email': [email], 'ticket_id': [ticket_id], 'checked_in': [False]
    })
    try:
        attendees_df = pd.read_csv(database_file)
        attendees_df = pd.concat([attendees_df, new_attendee], ignore_index=True)
    except FileNotFoundError:
        attendees_df = new_attendee
    attendees_df.to_csv(database_file, index=False)
    print(f"Registration successful! Your ticket ID is: {ticket_id}")

    # 4. Generate QR Code Image (temporarily)
    qr_image_path = f"{ticket_id}.png"
    qr_img = qrcode.make(ticket_id)
    qr_img.save(qr_image_path)
    print(f"QR code generated and saved as {qr_image_path}")

    # 5. Create the PDF Ticket
    pdf_file_name = f"Ticket_{name.replace(' ', '_')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 20, "Event Ticket", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 16)
    pdf.cell(0, 10, f"Name: {name}", 0, 1)
    pdf.cell(0, 10, f"Email: {email}", 0, 1)
    pdf.image(qr_image_path, x=60, y=80, w=90)
    pdf.output(pdf_file_name)
    print(f"PDF ticket saved as {pdf_file_name}")

    # Clean up the temporary QR code image
    os.remove(qr_image_path)
    print(f"Cleaned up temporary file: {qr_image_path}")

    # 6. SEND THE EMAIL WITH THE TICKET
    send_email_with_ticket(email, name, pdf_file_name)

    # 7. Clean up the PDF file after sending
    os.remove(pdf_file_name)
    print(f"Cleaned up local ticket file: {pdf_file_name}")


if __name__ == "__main__":
    register_and_generate_ticket()



