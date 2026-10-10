import telebot
import keras.models import koad_model
from PIL import Image, ImageOps
import numpy as np

TOKEN = '8709272644:AAH7LwF9fMO83l2UL6MU22pc4oRMblTmpNc'
bot = telebot.TeleBot(TOKEN)

def get_class(model_path, labels_path, image_path):
    np.set_printoptions(supperess=True)
    model = load_model(model_path, compile=False)
    class_names = open(labels_path, "r", encoding="utf-8").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANSZOS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return(class_name[2:], confidence_score)


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


        result = get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=file_name)

    bot.send_message(message.chat.id, f"Изображение {file_name} успешно получено и сохранено! Результат обработан: {result}")


bot.polling(none_stop=True)

