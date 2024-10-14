from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from config import Config

# Load environment variables from .env file
load_dotenv()
client = OpenAI()

# Set up OpenAI API key from .env
# openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
model = 'gpt-3.5-turbo'
config = Config()
# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config.SMTP_USERNAME  # Your email address
app.config['MAIL_PASSWORD'] = config.SMTP_PASSWORD  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = config.SMTP_USERNAME   # Default sender email

mail = Mail(app)
# Main page route
@app.route('/')
def index():
    return render_template('index.html', question='', answer='', language='')

# Step 1: Generate customer comment
@app.route('/submit', methods=['POST'])
def submit():
    product_description = request.form.get("question")
    language = request.form.get("language")
    email = request.form.get("email")
    #the headphones is good with bluetooth and wire connection
    
    # Generate customer comment based on product description
    # response_comment = client.chat.completions.create(
    #     model="text-davinci-003",
    #     prompt=f"Generate a 100-word comment about the following product description: {product_description}",
    #     max_tokens=100
    # )
    # customer_comment = response_comment['choices'][0]['text'].strip()
    response_comment = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Generate a 100-word comment about the following product description: {product_description}"
                }
            ]
    )
    customer_comment = response_comment.choices[0].message.content

    # Step 2: Generate email subject from customer comment
    # response_subject = client.chat.completions.create(
    #     model="text-davinci-003",
    #     prompt=f"Generate an email subject from the following comment: {customer_comment}",
    #     max_tokens=20
    # )
    # email_subject = response_subject['choices'][0]['text'].strip()
    response_subject = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Asuming that you provide customer support for an electronic product company.The following text is the customer's comment about the products, please generate a subject in English of the comment. The subject will be used as the subject of the email to be sent to the customer==>: {customer_comment}"
                }
            ],
    max_tokens=100
    )
    email_subject = response_subject.choices[0].message.content

    # Step 3: Generate a summary of the customer's comment
    response_summary = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Asuming that you provide customer support for an electronic product company.The following text is the comment of products, please generate a summary of the comment. Please generate an English summary of the comment==>: {customer_comment}"
                }
            ]
    )
    comment_summary = response_summary.choices[0].message.content

    # Step 4: Analyze sentiment of the comment
    # response_sentiment = client.chat.completions.create(
    #     model="text-davinci-003",
    #     prompt=f"Analyze the sentiment (Positive or Negative) of the following comment: {customer_comment}",
    #     max_tokens=10
    # )
    # sentiment_analysis = response_sentiment['choices'][0]['text'].strip()
    response_sentiment = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Asuming that you provide customer support for an electronic product company.Please do sentiment analysis based on the following comment. The result of the sentiment analysis shows whether the customer's comment is Positive or Negative===>: {customer_comment}",
                }
            ]
    )
    sentiment_analysis = response_sentiment.choices[0].message.content

    # Step 5: Generate the final email
    # response_email = client.chat.completions.create(
    #     model="text-davinci-003",
    #     prompt=f"Create an email based on the comment: {customer_comment}, summary: {comment_summary}, subject: {email_subject}, sentiment: {sentiment_analysis}",
    #     max_tokens=200
    # )
    # customer_email = response_email['choices'][0]['text'].strip()
    response_email = client.chat.completions.create(
    model=model,
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f" Asuming that you provide customer support for an electronic product company.Create an email in {language} language to be sent to the customer based on based on the comment==>: {customer_comment}, summary: {comment_summary}, subject: {email_subject}, sentiment: {sentiment_analysis}. Address the Customer with ->Dear Customer and atlast With Reagrds The Support Team.",
                }
            ],
    )
    customer_email = response_email.choices[0].message.content
    # Send email to the customer
    msg = Message(email_subject, recipients=[email])
    msg.body = customer_email
    mail.send(msg)

    # Render the results back to the UI
    return render_template("index.html", question=product_description, answer=customer_email, language=language, email=email)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
