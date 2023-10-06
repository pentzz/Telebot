import datetime
import telebot

TOKEN = "6659677963:AAHg4DNE6hqhVB6UidmoH81RGP1dVCEL4qQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "שלום! ברוך הבא לבוט הכלכלה שלך. נתחיל: כמה אתה מצפה להרוויח בחודש?")
    bot.register_next_step_handler(message, get_monthly_income)

def get_monthly_income(message):
    monthly_income = float(message.text)
    bot.send_message(message.chat.id, "איזה שכר שעתי יש לך?")
    bot.register_next_step_handler(message, get_hourly_wage, monthly_income)

def get_hourly_wage(message, monthly_income):
    hourly_wage = float(message.text)
    
    # Calculate number of hours he needs to work in a month
    monthly_hours_required = monthly_income / hourly_wage

    # Get the current month to calculate number of working days
    today = datetime.date.today()
    working_days_in_month = len([1 for i in range(today.month) if datetime.date(today.year, today.month, i).weekday() < 5])
    
    hours_per_day = monthly_hours_required / working_days_in_month
    shifts_per_week = hours_per_day / 8  # Assuming a shift is 8 hours

    bot.send_message(message.chat.id, f"תצטרך לעבוד {monthly_hours_required} שעות בחודש, כלומר {hours_per_day} שעות ביום ו-{shifts_per_week} משמרות בשבוע.")
    
    # Add code here to gather information on monthly expenses...

bot.polling()
