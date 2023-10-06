import telebot
from datetime import datetime
import calendar

TOKEN = '6659677963:AAHg4DNE6hqhVB6UidmoH81RGP1dVCEL4qQ'
bot = telebot.TeleBot(TOKEN)

users_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.reply_to(message, "שלום! אנא הכנס את ההכנסה הצפויה שלך בחודש.")
    bot.register_next_step_handler(msg, get_monthly_income)

def get_monthly_income(message):
    chat_id = message.chat.id
    monthly_income = message.text
    users_data[chat_id] = {'monthly_income': monthly_income}
    msg = bot.reply_to(message, "כמה אתה רוצה שיהיה לך בשקלים בחודש?")
    bot.register_next_step_handler(msg, get_desired_savings)

def get_desired_savings(message):
    chat_id = message.chat.id
    desired_savings = message.text
    users_data[chat_id]['desired_savings'] = desired_savings
    msg = bot.reply_to(message, "אנא הכנס את השכר השעתי שלך.")
    bot.register_next_step_handler(msg, get_hourly_wage)

def get_hourly_wage(message):
    chat_id = message.chat.id
    hourly_wage = float(message.text)
    users_data[chat_id]['hourly_wage'] = hourly_wage

    today = datetime.today()
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    working_days_in_month = len([1 for i in range(1, last_day_of_month + 1) if datetime(today.year, today.month, i).weekday() < 5])
    hours_needed = (float(users_data[chat_id]['monthly_income']) - float(users_data[chat_id]['desired_savings'])) / hourly_wage
    hours_per_week = hours_needed / (working_days_in_month / 5)

    bot.reply_to(message, f"אתה צריך לעבוד כ-{hours_needed:.2f} שעות בחודש, כלומר כ-{hours_per_week:.2f} שעות בשבוע.")

bot.polling()
