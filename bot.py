# from telegram import Update
# from telegram.ext import Updater, CommandHandler, CallbackContext
#
# # Функция, которая отвечает на команду /start
# def start(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text("Привет! Я бот для бронирования столов. Чем могу помочь?")
#
# # Основная функция для запуска бота
# def main():
#     # Замените YOUR_TOKEN_HERE на ваш токен
#     updater = Updater("YOUR_TOKEN_HERE")
#     dispatcher = updater.dispatcher
#
#     # Обработчик команды /start
#     dispatcher.add_handler(CommandHandler("start", start))
#
#     # Запуск бота
#     updater.start_polling()
#     updater.idle()
#
# if __name__ == "__main__":
#     main()
