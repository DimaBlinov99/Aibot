
import telebot


TOKEN = '8709272644:AAH7LwF9fMO83l2UL6MU22pc4oRMblTmpNc'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может помочь вам с картинками. Отправьте мне изображение, и я постараюсь его обработать.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not message.photo:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте изображение.")
        return

    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, f"Изображение {file_name} успешно получено и сохранено!")


bot.polling(none_stop=True)

