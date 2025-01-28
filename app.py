from flask import Flask, render_template, request, jsonify
import yagmail
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    response = handle_user_message(user_message)
    return jsonify({'response': response})

def handle_user_message(message):
    if "book ticket" in message.lower():
        return process_booking()
    else:
        return "Chatbot: How can I assist you with booking museum tickets?"

def process_booking():
    # Mock booking process
    booking_name = "John Doe"
    amount_paid = "20.00"
    
    # Send confirmation email
    send_confirmation_email(booking_name, amount_paid)
    
    return f"Chatbot: Ticket booked successfully for {booking_name}. Amount paid: ${amount_paid}"
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_ticket_pdf(booking_name, amount_paid, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Add logo
    logo_path = "logo.png"
    c.drawImage(logo_path, 50, height - 100, width=100, height=50)

    # Add booking details
    c.drawString(50, height - 150, f"Booking Name: {booking_name}")
    c.drawString(50, height - 170, f"Amount Paid: ${amount_paid}")

    c.showPage()
    c.save()

def send_confirmation_email(booking_name, amount_paid):
    sender_email = "test01ipa@gmail.com"
    receiver_email = "test1ofpython@gmail.com"
    password = "khrigvvgjxdsqrrg"

    subject = "Museum Ticket Booking Confirmation"
    contents = f"""
    Hi {booking_name},

    Thank you for booking a ticket to the museum.
    Amount Paid: ${amount_paid}

    Best regards,
    Museum Team
    """
    create_ticket_pdf(booking_name, amount_paid,"ticket.pdf")
    pdf_buffer = 'ticket.pdf'

    yag = yagmail.SMTP(sender_email, password)
    yag.send(to=receiver_email, subject=subject, contents=contents, attachments=[pdf_buffer])

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_ticket_pdf(booking_name, amount_paid, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Add logo
    logo_path = "logo.png"
    c.drawImage(logo_path, 50, height - 100, width=100, height=50)

    # Add booking details
    c.drawString(50, height - 150, f"Booking Name: {booking_name}")
    c.drawString(50, height - 170, f"Amount Paid: ${amount_paid}")

    c.showPage()
    c.save()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)