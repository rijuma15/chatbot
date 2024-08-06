<<<<<<< HEAD

# Chatbot Project

## Overview

This project is a chatbot that can answer user queries from documents and collect user information (Name, Phone Number, Email) when the user requests a call. It uses LangChain, Google Generative AI (Gemini), and Chainlit.

## Features

- Answer user queries based on the content of documents.
- Collect user information to book an appointment.
- Validate user input (email, phone number).
- Extract dates from user input in various formats.


## Implementation
**main.py**
main.py contains the main logic for handling user inputs, integrating conversational forms, and querying documents.

Key Components:
Google Generative AI Configuration: Configures and initializes the Google Generative AI model (gemini-1.5-flash) for generating responses.

Validation Functions:
validate_email(email): Validates email addresses using a regular expression.
validate_phone(phone): Validates phone numbers using a regular expression.

Date Extraction:
extract_date(user_input): Converts phrases like "next Tuesday" or "tomorrow" into a standardized date format (YYYY-MM-DD).

Appointment Booking:
book_appointment(name, phone, email, appointment_date): Simulates the booking of an appointment and returns a confirmation message.

User Input Handling:
handle_user_input(user_input, user_id): Manages different stages of the conversational form for collecting user information (name, phone number, email) and integrates the appointment booking logic.

Chainlit Integration:
Uses Chainlit to start a chat session and handle incoming messages, invoking the appropriate functions based on user input.


**document_query.py**
document_query.py handles querying of documents and generating responses using Google Generative AI.

Key Components:
Google Generative AI Configuration: Configures the Google Generative AI model (gemini-1.5-flash) for querying documents.

Document Loading:

- load_documents(): Uses TextLoader from the langchain_community to load documents from specified paths and prints their content for verification.
Querying Documents:

- query_documents(query): Searches for relevant documents based on the user query, combines their content, and queries Google Generative AI to generate a response.
Use of LangChain

- Document Loading with LangChain:
The TextLoader class from langchain_community is used to simplify the loading and processing of text documents. It handles reading document files and prepares them for querying.
Integration with Language Models:
LangChain provides abstractions that facilitate the integration of document content with language models. By using LangChain’s tools, we ensure smooth processing of documents and compatibility with language model querying.


## Start the Chatbot:

chainlit main.py
Interact with the Chatbot:

- Use Chainlit’s interface to start a chat session.
- Type 'Call me' to initiate the conversational form for booking an appointment.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/rijuma15/chatbot.git
cd chatbot
>>>>>>>


