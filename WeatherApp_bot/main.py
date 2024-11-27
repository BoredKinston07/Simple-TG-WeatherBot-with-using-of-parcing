from bs4 import BeautifulSoup as BS4
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Напиши назву країни та міста англійською, щоб дізнатися погоду. Приклад: `Ukraine Kyiv`")

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.split()
    
    if len(user_input) < 2:
        await update.message.reply_text("Будь ласка, введіть назву країни та міста. Наприклад: `Ukraine Kyiv`")
        return

    country = user_input[0]
    city = " ".join(user_input[1:])
    
    city_formatted = city.lower().replace(" ", "-")
    country_formatted = country.lower()
    url = f"https://www.timeanddate.com/weather/{country_formatted}/{city_formatted}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BS4(response.text, 'html.parser')
        temperature = soup.find("div", class_="h2").get_text(strip=True)
        await update.message.reply_text(f"🌡 Температура у {city.title()}, {country.title()}: {temperature}")
    except AttributeError:
        await update.message.reply_text("❌ Місто або країна не знайдені. Перевірте правильність введення.")
    except requests.exceptions.RequestException:
        await update.message.reply_text("❌ Не вдалося підключитися до сайту для отримання даних.")

def main():
    TOKEN = '8119550119:AAEVmSjBYVIN8gITMcSsPLyaVte6y-2Gq8w'
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))
    
    app.run_polling()

if __name__ == '__main__':
    main()
