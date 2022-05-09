import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import wikipedia

# Запускаем логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

TOKEN = '5324281392:AAER7VmCIcH9GymqqJcLmtAY67HIGZQe0-g'

# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")


# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def get_wiki(update, ctx):
    try:
        s_res = wikipedia.search(update.message.text)
        ny = wikipedia.summary(s_res[0])
        # Получаем первую тысячу символов
        wikitext = ny[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if len((x.strip())) > 3:
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Возвращаем текстовую строку
        update.message.reply_text(wikitext2)
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        update.message.reply_text('В энциклопедии нет информации об этом.')


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Зарегистрируем их в диспетчере рядом
    # с регистрацией обработчиков текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stop", stop))

    # обработчик не распознных команд
    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.

    text_handler = MessageHandler(Filters.text, get_wiki)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


def start(update, context):
    update.message.reply_text("Привет! Я Жаба-бот. Напишите мне какой-нибудь слово, и я пришлю его определение с сайта Википедии.")


def help(update, context):
    update.message.reply_text("Команды, которыми можно пользоваться: /start, /help, /stop.\nБольше я яще не умею(")


def stop(update, context):
    update.message.reply_text("Ква! Пока, если что-то надо приходи в моё болото ещё.")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Извините, я не знаю такой команды.")


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()