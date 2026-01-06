import telebot

TOKEN = "8297620545:AAG-xyRqEw7y6fI7ju5JYTnpIJoSMTSAlq4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Бот запущен локально! Работает с твоего ПК!")

@bot.message_handler(commands=['test'])
def test(message):
    bot.reply_to(message, "✅ Тест пройден! Бот отвечает!")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"Эхо: {message.text}")

print("🔧 Бот запущен в режиме разработки...")
print("⚠️  Работает локально - выключится при закрытии скрипта")
bot.polling()