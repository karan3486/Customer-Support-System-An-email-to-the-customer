
![image](https://github.com/user-attachments/assets/8b80f50a-bcd4-4dad-a2c2-f51a5c169c0c)

![image](https://github.com/user-attachments/assets/579a5f6d-6904-42da-bdc1-94f78171a611)


---

# OpenAI Flask Email Generator

This project is a Flask-based web application that integrates OpenAI's GPT-3.5-turbo model to automatically generate customer comments, email subjects, perform sentiment analysis, and generate the final email content. The emails are then sent to the customer using Flask-Mail.

## Features

- Generate customer comments based on a product description using OpenAI API
- Perform sentiment analysis on customer comments
- Generate email subjects based on comments
- Generate email content in multiple languages
- Send generated emails to customers using Flask-Mail

## Project Structure

```
.
├── app.py               # Main application logic
├── config.py            # Configuration for Flask and Flask-Mail
├── .env                 # Environment variables
├── templates/
│   └── index.html       # HTML template for the web interface
├── static/
│   └── css/
│       └── style.css    # Styling for the web interface
└── __pycache__/         # Compiled Python files
```

## Prerequisites

Before running the application, make sure you have the following installed:

- **Python 3.8+**
- **Flask**: Web framework used for this project
- **OpenAI Python SDK**: To access OpenAI's GPT models
- **Flask-Mail**: To send emails from the application
- **python-dotenv**: For managing environment variables

## Setup and Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/OpenAI-Flask-Email-Generator.git
   cd OpenAI-Flask-Email-Generator
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables. Create a `.env` file in the root of the project and add the following:

   ```bash
   OPENAI_API_KEY=<your_openai_api_key>
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=465
   MAIL_USERNAME=<your_email_address>
   MAIL_PASSWORD=<your_email_password>
   MAIL_USE_TLS=False
   MAIL_USE_SSL=True
   ```

   Replace the placeholder values with your actual credentials.

## Running the Application

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

3. Enter the product description and email address in the form, then click submit. The generated email content will be displayed, and an email will be sent to the provided address.

## How It Works

1. **Input**: User submits a product description and selects a preferred language.
2. **OpenAI API**: The product description is sent to OpenAI's GPT-3.5-turbo model, which generates a customer comment.
3. **Email Subject**: The app generates an appropriate subject line based on the comment.
4. **Sentiment Analysis**: The app performs sentiment analysis on the comment.
5. **Final Email**: A personalized email is generated based on the comment, subject, and sentiment, and then sent using Flask-Mail.

## Example Usage

1. Enter a product description (e.g., "The headphones are great with both Bluetooth and wired connections").
2. The app will generate a customer comment like, "These headphones offer excellent sound quality, and the versatility of both Bluetooth and wired options make them a great choice."
3. The subject, sentiment, and email body will be generated and sent to the provided email address.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

This README provides clear instructions for setting up, running, and understanding the project. You can adjust the clone URL or any specific details to fit your repository.
