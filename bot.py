import vk_api
import time
import wikipedia


def send_message(msg=None, att=None):
    vk.get_api().messages.send(message=msg,
                               attachment=att,
                               chat_id=item['chat_id'],
                               forward_messages=item['id'])

# ======================== Команды бота ============================================


def descr(*args):
    send_message('Описание бота')


def hello(*args):
        username = vk.get_api().users.get(user_ids=item['user_id'])
        send_message('Привет, {} {}'.format(username[0]['first_name'], username[0]['last_name']))


def cmds(*args):
    string = ''
    for key in commands_dict:
        string += bot_name + ', ' + key + '\n'
    send_message(string)


def wiki(wiki, *wikiquery):
    wikipedia.set_lang('ru')
    try:
        send_message(wikipedia.summary(' '.join(wikiquery)))
    except Exception:
        send_message('Неверный запрос в вики')


def news(*args):
    wall = vk.get_api().wall.get(domain=group_name, count=1)
    send_message(att='wall{}_{}'.format(wall['items'][0]['owner_id'],
                                        wall['items'][0]['id']))


def post_alph(letter, *args):
    # Вставить ссылки на картинки
    alphabet = {'А': '',
                'Б': '',
                'В': '',
                'Г': '',
                'Д': '',
                'Е': '',
                'Ж': '',
                'З': '',
                'И': '',
                'К': '',
                'Л': '',
                'М': '',
                'Н': ''}
    if letter.upper() in alphabet.keys():
        send_message(att=alphabet[letter.upper()])


# ======================== Переменные ===============================================
login = ''              # логин в вк
password = ''           # пароль в вк
bot_name = 'Гилберт'    # имя бота можно менять, от этого зависит команда обращения
group_name = ''         # id группы, откуда берётся пост
last_message = None
vk = vk_api.VkApi(login=login, password=password)

commands_dict = {'ОПИСАНИЕ':   descr,   # описание бота
                 'ПРИВЕТ':     hello,   # приветствие
                 'КОМАНДЫ':     cmds,   # генетатор списка команд из этого словаря
                 'ВИКИ':        wiki,   # поиск в вики по слову
                 'НОВОСТИ':     news,   # последний пост в группе group_name
                 'А':      post_alph,   # картинки, каждая буква - отдельная картинка
                 'Б':      post_alph,   # ссылки на картинки вставляются в функцию post_alph
                 'В':      post_alph,
                 'Г':      post_alph,
                 'Д':      post_alph,
                 'Е':      post_alph,
                 'Ж':      post_alph,
                 'З':      post_alph,
                 'И':      post_alph,
                 'К':      post_alph,
                 'Л':      post_alph,
                 'М':      post_alph,
                 'Н':      post_alph}

# ======================== Основной код =============================================

vk.auth()
while True:
    # запрос к серверу
    response = vk.get_api().messages.get(out=0,
                                         count=10,
                                         time_offset=5,
                                         last_message_id=last_message)
    # парсинг сообщений и проверка на наличие команд в них
    if response['items']:
        last_message = response['items'][0]['id']
    for item in response['items']:
        if item['body']:
            parsed_message = item['body'].split()
            if parsed_message[0].upper() == bot_name.upper() + ', ':
                user = vk.get_api().users.get(user_ids=item['user_id'])
                print(time.time(), user[0]['first_name'], user[0]['last_name'], '=>', item['body'])
                if parsed_message[1].upper() in commands_dict.keys():
                    commands_dict[parsed_message[1].upper()](*parsed_message[1:])
                else:
                    send_message('Нет такой команды.')
    time.sleep(1)
