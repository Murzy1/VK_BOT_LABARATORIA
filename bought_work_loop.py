from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import keyboards
import database as db
import time
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

GROUP_ID = '207393442'
GROUP_TOKEN = 'a7dc5fc4c67bbaac52e46b3a29c3db21457bc797dcb2093a4edd4b90632e13a3183a9ccd828a73415cce2'
API_VERSION = '5.120'
work_request = {}
while True:
    try:
        work_status_mem = {}
        search_work = {}
        vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
        vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

        keyboard_kurs = keyboards.Select_year_of_unv_K()
        keyboard_bac_mag = keyboards.Select_bac_mag_K()
        keyboard_ls_type = keyboards.choice_lesson_type_K()
        keyboard_return = keyboards.return_K()
        for event in longpoll.listen():
            # отправляем меню 1го вида на любое текстовое сообщение от пользователя
            if event.type == VkBotEventType.MESSAGE_NEW:
                if db.check(event.obj.message['from_id']):

                    if event.obj.message['text'] != 'd':
                        base_reqest = db.search_teacher(event.obj.message['text'])
                        time_K = keyboards.time_K
                        time_K.keyb.add_callback_button(label=(base_reqest[0][0]).capitalize(),
                                                        payload={'type': base_reqest[0][0]})
                        time_K.keyb.add_line()
                        time_K.keyb.add_callback_button(label='Вернуться в меню', color=VkKeyboardColor.NEGATIVE,
                                                        payload={'type': 'return'})
                        search_work[event.object.message['from_id']] = {'teacher': base_reqest[0][0]}
                        vk.messages.send(
                            user_id=event.object.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.object.message['from_id'],
                            keyboard=time_K.keyb.get_keyboard(),
                            message='Временно похуй')
                    else:
                        vk.messages.send(
                            user_id=event.object.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.object.message['from_id'],
                            message='Временно похуй',
                            attachment='photo235254478_457250077')


    except requests.exceptions.ReadTimeout:
        print('Переподключение')
        time.sleep(10)

if __name__ == '__main__':
    pass
