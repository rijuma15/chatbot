import re
from datetime import datetime, timedelta
import chainlit as cl
from document_query import query_documents
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key='AIzaSyC9sCDwIjo3tRjoqGDY_clTPq8ypRUltyc')

# Define validation functions
def validate_email(email):
    is_valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None
    print(f"Validating email: {email} -> {is_valid}")
    return is_valid

def validate_phone(phone):
    is_valid = re.match(r"^\+?1?\d{9,15}$", phone) is not None
    print(f"Validating phone: {phone} -> {is_valid}")
    return is_valid

# Function to convert phrases like "next Tuesday" to a date
def extract_date(user_input):
    today = datetime.today()
    days_of_week = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    user_input_lower = user_input.lower()
    for day, value in days_of_week.items():
        if f"next {day}" in user_input_lower:
            days_ahead = value - today.weekday() + 7
            return (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

    # Attempt to parse direct date formats
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y'):
        try:
            return datetime.strptime(user_input, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue

    # Handle relative dates like "tomorrow", "today"
    if 'tomorrow' in user_input_lower:
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    if 'today' in user_input_lower:
        return today.strftime('%Y-%m-%d')

    return None

def book_appointment(name, phone, email, appointment_date):
    # Implement your appointment booking logic here
    return f"Appointment booked for {name} on {appointment_date}. We will contact you at {phone} or {email}."

# Global context dictionary to maintain user session
user_contexts = {}

# Function to handle user inputs
async def handle_user_input(user_input, user_id):
    context = user_contexts.get(user_id, {'step': None, 'initial_query': user_input})

    if context.get('step') == 'collect_name':
        context['name'] = user_input
        context['step'] = 'collect_phone'
        user_contexts[user_id] = context
        return "Please provide your phone number."

    if context.get('step') == 'collect_phone':
        if not validate_phone(user_input):
            return "Invalid phone number format. Please provide a valid phone number."
        context['phone'] = user_input
        context['step'] = 'collect_email'
        user_contexts[user_id] = context
        return "Please provide your email address."

    if context.get('step') == 'collect_email':
        if not validate_email(user_input):
            return "Invalid email format. Please provide a valid email address."
        context['email'] = user_input
        appointment_date = extract_date(context.get('initial_query', ''))
        if not appointment_date:
            context['step'] = 'collect_date'
            user_contexts[user_id] = context
            return "Couldn't understand the appointment date. Please specify a clear date."
        
        booking_confirmation = book_appointment(context['name'], context['phone'], context['email'], appointment_date)
        context['step'] = None  # Reset the step
        user_contexts[user_id] = context
        return booking_confirmation

    if context.get('step') == 'collect_date':
        appointment_date = extract_date(user_input)
        if not appointment_date:
            return "Couldn't understand the appointment date. Please specify a clear date."
        context['appointment_date'] = appointment_date

        booking_confirmation = book_appointment(context['name'], context['phone'], context['email'], appointment_date)
        context['step'] = None  # Reset the step
        user_contexts[user_id] = context
        return booking_confirmation

    if "call me" in user_input.lower():
        context['step'] = 'collect_name'
        user_contexts[user_id] = context
        return "Please provide your name."

    # Generate a response using Google Generative AI if no form-related context
    response = query_documents(user_input)
    return response

# Chat start event
@cl.on_chat_start
async def main():
    await cl.Message(content="Hello! How can I assist you today? For the appointment booking please type 'Call me'.").send()

# Message handling event
@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content
    user_id = message.author  # Use the 'author' attribute to get a unique user ID
    response = await handle_user_input(user_input, user_id)
    await cl.Message(content=response).send()
