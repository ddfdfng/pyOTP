import telebot
import pyotp
import logging

API_TOKEN = '7021497606:AAGdjM0kAa0wFKL_4Rq_nlwhlYCTdAZSgJU'
bot = telebot.TeleBot(API_TOKEN)

otp_store = {}

logging.basicConfig(level=logging.INFO)

# Command handler for /start
@bot.message_handler(commands=['start'])
def start(message):
    # Send a welcome message and instructions to the user
    bot.reply_to(message, "Welcome! Use /generate to get an OTP and /verify <otp> to verify it.")

# Command handler for /generate
@bot.message_handler(commands=['generate'])
def generate_otp(message):
    user_id = message.from_user.id

    # Generate a new OTP secret for the user
    otp_secret = pyotp.random_base32()
    totp = pyotp.TOTP(otp_secret)
    otp_code = totp.now()

    # Store the OTP secret and code in the dictionary
    otp_store[user_id] = (otp_secret, otp_code)

    # Send the OTP code to the user
    bot.reply_to(message, f"Your OTP is: {otp_code}. It is valid for the next 30 seconds.")

# Command handler for /verify
@bot.message_handler(commands=['verify'])
def verify_otp(message):
    user_id = message.from_user.id

    if user_id not in otp_store:
        # No OTP has been generated for this user
        bot.reply_to(message, "No OTP generated. Use /generate to get an OTP.")
        return

    otp_secret, correct_otp = otp_store[user_id]
    totp = pyotp.TOTP(otp_secret)

    # Get the OTP input from the message
    otp_input = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else ''

    # Verify the OTP
    if totp.verify(otp_input):
        bot.reply_to(message, "OTP verified successfully!")
    else:
        bot.reply_to(message, "Invalid OTP. Please try again.")

    # Remove the OTP data after verification
    del otp_store[user_id]

bot.polling(none_stop=True)
