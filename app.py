from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from config import Config
import random
from helper import cot
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
    # product_description = request.form.get("question")
    language = request.form.get("language")
    email = request.form.get("email")
    product_description = random.choice(list(products.values()))
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
    response = client.moderations.create(
    model="omni-moderation-latest",
    input=customer_comment,
    )

    moderation_output = response["results"][0]
    print(moderation_output)

    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with \
    {delimiter} characters.

    Classify each query into a primary category \
    and a secondary cate
    Primary categories: Billing, Techgory. 

    Provide your output in json format with the \
    keys: primary and secondary.
    nical Support, \
    Account Management, or General Inquiry.

    Billing secondary categories:
    Unsubscribe or upgrade
    Add a payment method
    Explanation for charge
    Dispute a charge

    Technical Support secondary categories:
    General troubleshooting
    Device compatibility
    Software updates

    Account Management secondary categories:
    Password reset
    Update personal information
    Close account
    Account security

    General Inquiry secondary categories:
    Product information
    Pricing
    Feedback
    Speak to a human

    """
    user_message = f"""\
    I want you to delete my profile and all of my user data"""

    # Combined messages to be sent to ChatGPT 
    messages =  [  
    {'role':'system', 
    'content': system_message},    
    {'role':'user', 
    'content': f"{delimiter}{customer_comment}{delimiter}"},  
    ] 

    # Get response from ChatGPT 
    response_classify = client.chat.completions.create(
    model=model,
    messages=messages
    )
    print(response_classify)
    
    #COT
    response_cot = client.chat.completions.create(
    model=model,
    messages=cot.messages
    )
    print(response_cot)

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
    check_response = client.moderations.create(
    model="omni-moderation-latest",
    input=customer_email,
    )
    print(check_response)

    from helper import eval
    print(eval.n_examples,eval.fraction_correct)
    # Send email to the customer
    msg = Message(email_subject, recipients=[email])
    msg.body = customer_email
    mail.send(msg)

    # Render the results back to the UI
    return render_template("index.html", question=customer_comment, answer=customer_email, language=language, email=email)

products = {
    "TechPro Ultrabook": {
        "name": "TechPro Ultrabook",
        "category": "Computers and Laptops",
        "brand": "TechPro",
        "model_number": "TP-UB100",
        "warranty": "1 year",
        "rating": 4.5,
        "features": ["13.3-inch display", "8GB RAM", "256GB SSD", "Intel Core i5 processor"],
        "description": "A sleek and lightweight ultrabook designed for everyday use, combining portability and power for an efficient computing experience.",
        "price": 799.99
    },
    "BlueWave Gaming Laptop": {
        "name": "BlueWave Gaming Laptop",
        "category": "Computers and Laptops",
        "brand": "BlueWave",
        "model_number": "BW-GL200",
        "warranty": "2 years",
        "rating": 4.7,
        "features": ["15.6-inch display", "16GB RAM", "512GB SSD", "NVIDIA GeForce RTX 3060"],
        "description": "A high-performance gaming laptop with immersive visuals and fast processing power, perfect for gaming enthusiasts.",
        "price": 1199.99
    },
    "PowerLite Convertible": {
        "name": "PowerLite Convertible",
        "category": "Computers and Laptops",
        "brand": "PowerLite",
        "model_number": "PL-CV300",
        "warranty": "1 year",
        "rating": 4.3,
        "features": ["14-inch touchscreen", "8GB RAM", "256GB SSD", "360-degree hinge"],
        "description": "A versatile convertible laptop featuring a touchscreen and a flexible 360-degree hinge, suitable for both work and entertainment.",
        "price": 699.99
    },
    "TechPro Desktop": {
        "name": "TechPro Desktop",
        "category": "Computers and Laptops",
        "brand": "TechPro",
        "model_number": "TP-DT500",
        "warranty": "1 year",
        "rating": 4.4,
        "features": ["Intel Core i7 processor", "16GB RAM", "1TB HDD", "NVIDIA GeForce GTX 1660"],
        "description": "A powerful desktop computer that excels in both productivity and gaming, delivering top-tier performance for all your tasks.",
        "price": 999.99
    },
    "BlueWave Chromebook": {
        "name": "BlueWave Chromebook",
        "category": "Computers and Laptops",
        "brand": "BlueWave",
        "model_number": "BW-CB100",
        "warranty": "1 year",
        "rating": 4.1,
        "features": ["11.6-inch display", "4GB RAM", "32GB eMMC", "Chrome OS"],
        "description": "A compact and affordable Chromebook, perfect for everyday tasks such as browsing the web and checking emails.",
        "price": 249.99
    },
    "SmartX ProPhone": {
        "name": "SmartX ProPhone",
        "category": "Smartphones and Accessories",
        "brand": "SmartX",
        "model_number": "SX-PP10",
        "warranty": "1 year",
        "rating": 4.6,
        "features": ["6.1-inch display", "128GB storage", "12MP dual camera", "5G"],
        "description": "A powerful smartphone that combines a sleek design with advanced camera features, perfect for capturing stunning photos and videos.",
        "price": 899.99
    },
    "MobiTech PowerCase": {
        "name": "MobiTech PowerCase",
        "category": "Smartphones and Accessories",
        "brand": "MobiTech",
        "model_number": "MT-PC20",
        "warranty": "1 year",
        "rating": 4.3,
        "features": ["5000mAh battery", "Wireless charging", "Compatible with SmartX ProPhone"],
        "description": "A protective case with a built-in battery that extends the life of your SmartX ProPhone, ideal for heavy users.",
        "price": 59.99
    },
    "SmartX MiniPhone": {
        "name": "SmartX MiniPhone",
        "category": "Smartphones and Accessories",
        "brand": "SmartX",
        "model_number": "SX-MP5",
        "warranty": "1 year",
        "rating": 4.2,
        "features": ["4.7-inch display", "64GB storage", "8MP camera", "4G"],
        "description": "A compact smartphone that offers essential features and smooth performance for users who prefer simplicity and affordability.",
        "price": 399.99
    },
    "MobiTech Wireless Charger": {
        "name": "MobiTech Wireless Charger",
        "category": "Smartphones and Accessories",
        "brand": "MobiTech",
        "model_number": "MT-WC10",
        "warranty": "1 year",
        "rating": 4.5,
        "features": ["10W fast charging", "Qi-compatible", "LED indicator", "Compact design"],
        "description": "A convenient wireless charger that offers fast and efficient charging, perfect for a clutter-free workspace.",
        "price": 29.99
    },
    "SmartX EarBuds": {
        "name": "SmartX EarBuds",
        "category": "Smartphones and Accessories",
        "brand": "SmartX",
        "model_number": "SX-EB20",
        "warranty": "1 year",
        "rating": 4.4,
        "features": ["True wireless", "Bluetooth 5.0", "Touch controls", "24-hour battery life"],
        "description": "Experience true wireless freedom with these comfortable earbuds, featuring excellent sound quality and a long-lasting battery.",
        "price": 99.99
    },
    "CineView 4K TV": {
        "name": "CineView 4K TV",
        "category": "Televisions and Home Theater Systems",
        "brand": "CineView",
        "model_number": "CV-4K55",
        "warranty": "2 years",
        "rating": 4.8,
        "features": ["55-inch display", "4K resolution", "HDR", "Smart TV"],
        "description": "A stunning 4K TV that offers vibrant colors and sharp detail, complete with smart features for a seamless viewing experience.",
        "price": 599.99
    },
    "SoundMax Home Theater": {
        "name": "SoundMax Home Theater",
        "category": "Televisions and Home Theater Systems",
        "brand": "SoundMax",
        "model_number": "SM-HT100",
        "warranty": "1 year",
        "rating": 4.4,
        "features": ["5.1 channel", "1000W output", "Wireless subwoofer", "Bluetooth"],
        "description": "A powerful home theater system that provides an immersive audio experience, ideal for movie nights and gaming.",
        "price": 399.99
    },
    "CineView 8K TV": {
        "name": "CineView 8K TV",
        "category": "Televisions and Home Theater Systems",
        "brand": "CineView",
        "model_number": "CV-8K65",
        "warranty": "2 years",
        "rating": 4.9,
        "features": ["65-inch display", "8K resolution", "HDR", "Smart TV"],
        "description": "Experience the future of television with this stunning 8K TV, offering unparalleled picture quality and smart functionality.",
        "price": 2999.99
    },
    "SoundMax Soundbar": {
        "name": "SoundMax Soundbar",
        "category": "Televisions and Home Theater Systems",
        "brand": "SoundMax",
        "model_number": "SM-SB50",
        "warranty": "1 year",
        "rating": 4.3,
        "features": ["2.1 channel", "300W output", "Wireless subwoofer", "Bluetooth"],
        "description": "Upgrade your TV’s audio with this sleek soundbar, delivering powerful sound with a compact design.",
        "price": 199.99
    },
    "CineView OLED TV": {
        "name": "CineView OLED TV",
        "category": "Televisions and Home Theater Systems",
        "brand": "CineView",
        "model_number": "CV-OLED55",
        "warranty": "2 years",
        "rating": 4.7,
        "features": ["55-inch display", "4K resolution", "HDR", "Smart TV"],
        "description": "Experience true blacks and vibrant colors with this OLED TV, offering a premium viewing experience with cutting-edge technology.",
        "price": 1499.99
    },
    "GameSphere X": {
        "name": "GameSphere X",
        "category": "Gaming Consoles and Accessories",
        "brand": "GameSphere",
        "model_number": "GS-X",
        "warranty": "1 year",
        "rating": 4.9,
        "features": ["4K gaming", "1TB storage", "Backward compatibility", "Online multiplayer"],
        "description": "The ultimate gaming console, offering 4K gaming and a vast library of games, both old and new.",
        "price": 499.99
    },
    "ProGamer Controller": {
        "name": "ProGamer Controller",
        "category": "Gaming Consoles and Accessories",
        "brand": "ProGamer",
        "model_number": "PG-C100",
        "warranty": "1 year",
        "rating": 4.2,
        "features": ["Wireless", "Customizable buttons", "Rechargeable battery", "Compatible with GameSphere X"],
        "description": "A high-performance wireless controller with customizable buttons, designed for serious gamers.",
        "price": 59.99
    },
    "GameSphere Y": {
        "name": "GameSphere Y",
        "category": "Gaming Consoles and Accessories",
        "brand": "GameSphere",
        "model_number": "GS-Y",
        "warranty": "1 year",
        "rating": 4.8,
        "features": ["8K gaming", "2TB storage", "Backward compatibility", "Online multiplayer"],
        "description": "Next-gen gaming with 8K support and massive storage, delivering an unparalleled gaming experience.",
        "price": 699.99
    }
}

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
