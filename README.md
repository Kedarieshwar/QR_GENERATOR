Python Event Ticket Generator
This is a simple command-line application written in Python that allows a user to register for an event and receive a unique PDF ticket with a QR code via email.

Features:

 ==> Registers user's name and email.

==> Saves attendee information to a local attendees.csv file.

==> Generates a unique QR code for each ticket.

==> Creates a professional-looking PDF ticket.

==> Sends the ticket directly to the user's email address as a PDF attachment.

Setup & Usage:

Clone the repository

git clone [https://github.com/YOUR_USERNAME/python-ticket-generator.git](https://github.com/YOUR_USERNAME/python-ticket-generator.git)
cd python-ticket-generator

Install the required libraries:

pip install "qrcode[pil]" pandas fpdf

Configure your email credentials:
Open app.py and update the SENDER_EMAIL and SENDER_APP_PASSWORD variables with your Gmail address and a 16-digit Google App Password.

Run the script:

python app.py

Follow the prompts to enter a name and email address. The ticket will be sent to the specified email.
