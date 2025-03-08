from flask import Flask, render_template, request, jsonify
import yagmail
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    user_name = request.json.get('name')
    num_tickets = request.json.get('tickets')
    user_email = request.json.get('email')
    response, show_additional_inputs = handle_user_message(user_message, user_name, num_tickets, user_email)
    return jsonify({'response': response, 'showAdditionalInputs': show_additional_inputs})

def handle_user_message(message, name, tickets, email):
    if "book ticket" in message.lower():
        return "Chatbot: Please provide your name, number of tickets, and email.", True
    elif name and tickets and email:
        return process_booking(name, tickets, email), False
    elif name or tickets or email:
        return "Chatbot: Please provide all required information (name, number of tickets, and email).", True
    else:
        return "Chatbot: How can I assist you with booking museum tickets?", False

def process_booking(name, tickets, email):
    if not name or not tickets or not email:
        return "Chatbot: Please provide all required information (name, number of tickets, and email)."
    
    # Mock booking process
    booking_name = name if name else "John Doe"
    amount_paid = 20.00 * int(tickets) if tickets else 20.00
    
    # Send confirmation email
    send_confirmation_email(booking_name, amount_paid, email)
    
    return f"Chatbot: Ticket booked successfully for {booking_name}. Amount paid: ${amount_paid}"

def send_confirmation_email(booking_name, amount_paid, receiver_email):
    sender_email = "test01ipa@gmail.com"
    password = "khrigvvgjxdsqrrg"

    subject = "Museum Ticket Booking Confirmation"
    contents = f"""
    Hi {booking_name},

    Thank you for booking {amount_paid/20} ticket(s) to the museum.
    Amount Paid: ${amount_paid}

    Best regards,
    Museum Team
    """
    create_ticket_pdf(booking_name, amount_paid, "ticket.pdf")
    pdf_buffer = 'ticket.pdf'

    yag = yagmail.SMTP(sender_email, password)
    yag.send(to=receiver_email, subject=subject, contents=contents, attachments=[pdf_buffer])

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_ticket_pdf(booking_name, amount_paid, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    _, height = letter
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