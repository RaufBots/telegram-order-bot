import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Главное меню
main_menu = ReplyKeyboardMarkup(
    [["Завтрак", "Обед", "Ужин"]],
    resize_keyboard=True
)

# Меню обеда
lunch_menu = ReplyKeyboardMarkup(
    [["Плов", "Салат"], ["Суп"], ["Оформить заказ"], ["Назад"]],
    resize_keyboard=True
)

# Словарь для хранения заказов
user_orders = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_orders[user_id] = []
    await update.message.reply_text(
        "Привет! Я бот для заказа еды. Выберите категорию:",
        reply_markup=main_menu
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # Если пользователь новый
    if user_id not in user_orders:
        user_orders[user_id] = []

    if text == "обед":
        await update.message.reply_text("Выберите блюдо:", reply_markup=lunch_menu)

    elif text in ["плов", "салат", "суп"]:
        user_orders[user_id].append(text.capitalize())
        await update.message.reply_text(f"{text.capitalize()} добавлен в заказ!")

    elif text == "оформить заказ":
        order = user_orders.get(user_id, [])
        if order:
            await update.message.reply_text("Ваш заказ:\n- " + "\n- ".join(order))
        else:
            await update.message.reply_text("Вы пока ничего не выбрали.")
        user_orders[user_id] = []

    elif text == "назад":
        await update.message.reply_text("Возвращаемся в главное меню.", reply_markup=main_menu)

    else:
        await update.message.reply_text("Я не понимаю. Выберите из меню.")

# Бот
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Бот запущен!")
app.run_polling()