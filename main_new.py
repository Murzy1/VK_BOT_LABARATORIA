from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import keyboards
import database as db
import database_search_work as db_search
import time
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import generate
import payment

GROUP_ID = '207393442'
GROUP_TOKEN = 'a7dc5fc4c67bbaac52e46b3a29c3db21457bc797dcb2093a4edd4b90632e13a3183a9ccd828a73415cce2'
API_VERSION = '5.120'


def check():
    try:
        what = search_work[event.object['user_id']]['teacher']
        return what
    except:
        return 'NaN'

while True:
    try:
        db.update_all_status()
        vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
        vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

        keyboard_main = keyboards.Main_K()
        keyboard_kurs = keyboards.Select_year_of_unv_K()
        keyboard_bac_mag = keyboards.Select_bac_mag_K()
        keyboard_faq = keyboards.Faq_K()
        keyboard_add_work = keyboards.Add_work_K()
        keyboard_ls_type = keyboards.choice_lesson_type_K()
        keyboard_variants = keyboards.variants_K()
        keyboard_add_work_check = keyboards.add_work_check_K()
        keyboard_price = keyboards.work_price_K()
        keyboard_return = keyboards.return_K()

        type_bac_mag = ['bacalavr', 'magistr']
        type_kurs = ['kurs_first', 'kurs_second', 'kurs_third', 'kurs_four']
        lesson_types = ['lab_task', 'refer_task', 'kr_task', 'ot_task', 'pr_task']
        prices = ['price_150','price_200','price_250','price_400']
        transcript_values = {'bacalavr': 'Бакалавриат', 'magistr':'Магистратура','kurs_first':'Первый курс',
                              'kurs_second':'Второй курс', 'kurs_third':'Третий курс', 'kurs_four':'Четвертый курс',
                              'lab_task':'Лабараторная работа', 'refer_task':'Реферат', 'kr_task':'Контрольная работа',
                              'ot_task':'Отчет по практике', 'pr_task':'Практическая работа'}
        memory_users_new = {}
        users_documents = {}
        work_status_mem = {}
        search_work = {}
        reqest_work_payment = {}

        for event in longpoll.listen():
            # отправляем меню 1го вида на любое текстовое сообщение от пользователя
            if event.type == VkBotEventType.MESSAGE_NEW:
                if db.check(event.obj.message['from_id']):
                    """Условия для добавления работы в базу"""
                    if event.obj.message['text'] != '' or event.obj.message['attachments'][0]['type'] in ['doc','photo']:
                        if event.from_user:
                            # Если клиент пользователя не поддерживает callback-кнопки,
                            # нажатие на них будет отправлять текстовые
                            # сообщения. Т.е. они будут работать как обычные inline кнопки.
                            if 'callback' not in event.obj.client_info['button_actions']:
                                print(f'Клиент {event.obj.message["from_id"]} не поддерж. callback')

                            if db.user_check_status(event.obj.message['from_id']) and work_status_mem[
                                event.obj.message['from_id']] == 'add_work_teacher':
                                users_documents[event.obj.message['from_id']]['teacher'] = str(
                                    event.object.message['text']).lower()
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 random_id=get_random_id(),
                                                 peer_id=event.obj.message['from_id'],
                                                 keyboard=keyboard_ls_type.keyb.get_keyboard(),
                                                 message='Укажите тип работы  ')
                            elif db.user_check_status(event.obj.message['from_id']) and work_status_mem[
                                event.obj.message['from_id']] == 'task':
                                users_documents[event.obj.message['from_id']]['task'] = str(
                                    event.object.message['text'])
                                work_status_mem[event.object.message['from_id']] = 'discription'
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 random_id=get_random_id(),
                                                 peer_id=event.obj.message['from_id'],
                                                 message='Отправьте фото с заданиями из работы, что бы покупатели знали'
                                                         ' точно, какую работу они покупают\n')
                            elif db.user_check_status(event.obj.message['from_id']) and work_status_mem[
                                event.obj.message['from_id']] == 'discription':
                                if event.object.message['attachments'][0]['type'] == 'photo':
                                    users_documents[event.obj.message['from_id']]['discription'] = 'photo'+ str(event.object.message['attachments'][0]['photo']['owner_id'])+'_' + str(event.object.message['attachments'][0]['photo']['id'])+'_'+str(event.object.message['attachments'][0]['photo']['access_key'])
                                work_status_mem[event.object.message['from_id']] = 'variant'
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 random_id=get_random_id(),
                                                 peer_id=event.obj.message['from_id'],
                                                 keyboard=keyboard_variants.keyb.get_keyboard(),
                                                 message='Если работа по вариантам укажите только номер варианта.\n'
                                                         'Иначе нажмите кнопку "Без варианта"')
                            elif db.user_check_status(event.obj.message['from_id']) and work_status_mem[event.obj.message['from_id']] == 'variant':
                                try:
                                    users_documents[event.obj.message['from_id']]['variant'] = int(
                                        event.object.message['text'])
                                    work_status_mem[event.object.message['from_id']] = 'document'
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     random_id=get_random_id(),
                                                     peer_id=event.obj.message['from_id'],
                                                     message='Отправьте нам документ который хотите загрузить')
                                except ValueError or TypeError:
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     random_id=get_random_id(),
                                                     peer_id=event.obj.message['from_id'],
                                                     keyboard=keyboard_variants.keyb.get_keyboard(),
                                                     message='Отправьте только число')
                                    continue
                            elif db.user_check_status(event.obj.message['from_id']) and work_status_mem[
                                event.obj.message['from_id']] == 'document' and len(event.object.message['attachments'])>1:
                                try:
                                    users_documents[event.obj.message['from_id']] = {}
                                    users_documents[event.obj.message['from_id']]['document_url'] = []
                                    users_documents[event.obj.message['from_id']]['document_tittle'] = []
                                    for elements in event.object.message['attachments']:
                                        users_documents[event.obj.message['from_id']]['document_url'].append(str(
                                            event.object.message['attachments'][0]['doc']['url']))
                                        users_documents[event.obj.message['from_id']]['document_tittle'].append(str(
                                            event.object.message['attachments'][0]['doc']['title']))

                                    work_status_mem[event.object.message['from_id']] = 'phone'
                                    vk.messages.send(
                                            user_id=event.obj.message['from_id'],
                                            random_id=get_random_id(),
                                            peer_id=event.obj.message['from_id'],
                                            message='Введите свой номер телефона для получения оплты по системе быстрых платежей')
                                except:
                                    vk.messages.send(
                                        user_id=event.obj.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.obj.message['from_id'],
                                        message='Отправьте только документ без лишнего текста)')

                                """Условия для поиска работы в базе"""
                            elif work_status_mem.get(event.obj.message['from_id']) == 'teacher':
                                base_reqest = db.search_teacher(event.obj.message['text'])
                                time_K = keyboards.time_K()
                                if type(base_reqest) is tuple and len(base_reqest) != 0 and base_reqest[1] >= 50:
                                    time_K.keyb.add_callback_button(label=(base_reqest[0][0]).capitalize(),
                                                                    payload={'type': base_reqest[0][0]})
                                    time_K.keyb.add_line()
                                time_K.keyb.add_callback_button(label='Вернуться в меню',
                                                                color=VkKeyboardColor.NEGATIVE,
                                                                payload={'type': 'return'})
                                if base_reqest != None:
                                    search_work[event.object.message['from_id']] = {'teacher': base_reqest[0][0]}
                                time_K.keyb.keyboard['buttons'] = time_K.keyb.lines
                                vk.messages.send(
                                    user_id=event.object.message['from_id'],
                                    random_id=get_random_id(),
                                    peer_id=event.object.message['from_id'],
                                    keyboard=time_K.keyb.get_keyboard(),
                                    message='Возможно, вы имели ввиду этого преподавателя, если да, то нажмите на кнопку'
                                            ' с фамилией преподавателя.\n Если кнопка отсутствует, то такого преподавателя у нас нет')
                                time_K.keyb.lines = [[]]
                                time_K.keyb.keyboard['buttons'] = time_K.keyb.lines

                            elif work_status_mem.get(event.object.message['from_id']) == 'choice_work':

                                try:
                                    choice = int(event.object.message['text'])
                                    work_id = search_work[event.object.message['from_id']]['works_id'][choice]
                                    m = db_search.get_work_info(work_id)
                                    local_keyboard = generate.payment_k()
                                    vk.messages.send(
                                        user_id=event.object.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.object.message['from_id'],
                                        message=('\nКурс: {0}\nПреподаватель: {1}\n'
                                                    'Тип работы: {2}\nНазвание работы: {3}\nВариант: {4}\n'
                                                    '\nЦена: {5}р \n'.format(transcript_values.get(m[0]),
                                                                             str(m[1]).capitalize(),
                                                            transcript_values.get(m[2]), m[3], m[4],str(int(m[5])+100))),
                                        attachment= m[6],
                                        keyboard=local_keyboard[0])
                                    reqest_work_payment.update([(str(local_keyboard[1]), work_id)])
                                    work_status_mem[event.object.message['from_id']]= 'WHAT'
                                except:
                                    vk.messages.send(
                                        user_id=event.object.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.object.message['from_id'],
                                        keyboard= keyboard_return.keyb.get_keyboard(),
                                        message=('Отправьте цифру'))



                            elif db.user_check_status(event.obj.message['from_id']) and work_status_mem[
                                event.obj.message['from_id']] == 'phone':
                                users_documents[event.obj.message['from_id']]['phone'] = str(
                                    event.object.message['text'])
                                work_status_mem[event.object.message['from_id']] = 'price'
                                vk.messages.send(user_id=event.object.message['from_id'],
                                                 random_id=get_random_id(),
                                                 peer_id=event.object.message['from_id'],
                                                 keyboard=keyboard_price.keyb.get_keyboard(),
                                                 message='Выберите цену за которую вы готовы выставить свою работу')

                            elif work_status_mem.get(event.obj.message['from_id']) == 'rate' and \
                                db.check(event.obj.message['from_id']):
                                vk.messages.send(user_id=event.object.message['from_id'],
                                                 random_id=get_random_id(),
                                                 peer_id=event.object.message['from_id'],
                                                 message='Спасибо большое! Мы блогадарим вас за отзыв.'
                                                         ' В случае,если это жалоба, Мы обязательно Вам отвтетим.')
                                vk.messages.send(user_id=235254478,
                                                 random_id=get_random_id(),
                                                 peer_id=event.object.message['from_id'],
                                                 message=event.object.message['text'])
                                db.update_status(event.object.message['from_id'], 'main')
                                work_status_mem[event.object.message['from_id']] = 'main'



                            else:
                                vk.messages.send(
                                    user_id=event.obj.message['from_id'],
                                    random_id=get_random_id(),
                                    peer_id=event.obj.message['from_id'],
                                    keyboard=keyboard_main.keyb.get_keyboard(),
                                    message='Выберите одну из наших услуг')

                else:
                    db.add_users(event.obj.message['from_id'])
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=keyboard_bac_mag.keyb.get_keyboard(),
                        message='Для Вашего удобства работы с Лаюоратрией ГУАП, пожалуйста'
                                ' укажите на каком Вы этапе обучеия: бакалавриат или магистратура,'
                                ' и курс на котором Вы учитесь')

            elif event.type == VkBotEventType.MESSAGE_EVENT:
                """Действия с кнопками"""
                if (db.check(event.object['user_id'])):
                    """ПРоверка на наличе данных пользователя в базе данных"""
                    if event.object.payload.get('type') == 'add_work':
                        vk.messages.send(
                            random_id=get_random_id(),
                            peer_id=event.object.peer_id,
                            keyboard=keyboard_add_work.keyb.get_keyboard(),
                            conversation_message_id=event.object.conversation_message_id,
                            message='Выбрана функция размещения собственной работы.\n\n '
                                    'Следуйте указаниям и у вас все получится'
                                    '\nПроизводится модерация работ.\n !ВАЖНО!\n '
                                    'Загрузка архивов и исполняемых файлов невозможна.\n'
                                    'Перед загрузкой работы УБЕДИТЕСь, что в работе отстутсвует ваши ФИО и номер группы.')

                    elif event.object.payload.get('type') == 'work_add_start':
                        db.update_status(event.object['user_id'], 'work_added')
                        vk.messages.send(user_id=event.object['user_id'],
                                         random_id=get_random_id(),
                                         peer_id=event.object['user_id'],
                                         keyboard=keyboard_bac_mag.keyb.get_keyboard(),
                                         message='Укажите, для какого типа обучения вы хотите добавить работу ')

                    elif event.object.payload.get('type') == 'return':
                        db.update_status(event.object['user_id'], 'main')
                        vk.messages.edit(
                            peer_id=event.object.peer_id,
                            keyboard=keyboard_main.keyb.get_keyboard(),
                            conversation_message_id=event.object.conversation_message_id,
                            message='Выберите одну из наших функций')

                    elif (event.object.payload.get('type') in type_bac_mag) and (
                            db.user_check_status(event.object['user_id'])) and (users_documents.get(event.object['user_id']) != 'NoneType'):
                        users_documents[event.object['user_id']] = {'bac_mag': event.object.payload.get('type')}
                        vk.messages.edit(
                            peer_id=event.object.peer_id,
                            conversation_message_id=event.object.conversation_message_id,
                            message='Тип обучения добавлен')
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.object['user_id'],
                            keyboard=keyboard_kurs.keyb.get_keyboard(),
                            message='Для какого курса вы хотите добавить работу')

                    elif (event.object.payload.get('type') == 'variant_out') and (
                            db.user_check_status(event.object['user_id'])) and (users_documents.get(event.object['user_id']) != 'NoneType'):
                        users_documents[event.object['user_id']]['variant'] = 'NO'
                        vk.messages.edit(
                            peer_id=event.object.peer_id,
                            conversation_message_id=event.object.conversation_message_id,
                            message='Данные добавлены')
                        work_status_mem[event.object['user_id']] = 'document'
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.object['user_id'],
                            message='Отправьте нам документ оцененный на высокий балл')

                    elif event.object.payload.get('type') in type_kurs and (
                            db.user_check_status(event.object['user_id'])) and (users_documents.get(event.object['user_id']) != 'NoneType'):
                        users_documents[event.object['user_id']]['kurs'] = event.object.payload.get('type')
                        vk.messages.edit(
                            peer_id=event.object.peer_id,
                            conversation_message_id=event.object.conversation_message_id,
                            message=' Курс добавлен')
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.object['user_id'],
                            message='Отправьте только фамилию преподавателя')
                        work_status_mem[event.object['user_id']] = 'add_work_teacher'

                    elif event.object.payload.get('type') in lesson_types and (
                            db.user_check_status(event.object['user_id'])) and (users_documents.get(event.object['user_id']) != 'NoneType') :
                        users_documents[event.object['user_id']]['type_lesson'] = event.object.payload.get('type')
                        work_status_mem[event.object['user_id']] = 'task'
                        vk.messages.edit(
                            peer_id=event.object.peer_id,
                            conversation_message_id=event.object.conversation_message_id,
                            message='Тип работы сохранен добавлен')
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.object['user_id'],
                            message='Отправьте название работы(так же как в личном кабинете)')

                    elif event.object.payload.get('type') == 'upload_work' and (users_documents.get(event.object['user_id']) != 'NoneType'):
                        db.upload_work(users_documents[event.object['user_id']], event.object['user_id'])
                        vk.messages.edit(
                            peer_id=event.object.peer_id,
                            conversation_message_id=event.object.conversation_message_id,
                            message='Ваша работа добавлена в базу')
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.object['user_id'],
                            keyboard=keyboard_main.keyb.get_keyboard(),
                            message='Выберите однин из пунктов')
                        users_documents[event.object['user_id']].clear()

                    elif event.object.payload.get('type') in prices and db.user_check_status(event.object['user_id']) and (users_documents.get(event.object['user_id']) != 'NoneType'):
                        work_status_mem[event.object['user_id']] = 'add_work_ready'
                        pr = {'price_150':150,'price_200':200,'price_250':250,'price_400':400}
                        users_documents[event.object['user_id']]['price'] = pr[event.object.payload.get('type')]
                        vk.messages.send(
                            user_id=event.obj['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj['user_id'],
                            keyboard=keyboard_add_work_check.keyb.get_keyboard(),
                            message='Тип обучения: {0}\nКурс: {1}\nПреподаватель: {2}\n'
                                    'Тип работы: {3}\nНазвание работы: {4}\nВариант: {5}\n'
                                    'Документы: {6}\nЦена: {7} \nНомер телефона(Не'
                                    ' виден другим пользователям): {8}'.format(
                                transcript_values.get(users_documents[event.obj['user_id']]['bac_mag']),
                                transcript_values.get(users_documents[event.obj['user_id']]['kurs']),
                                users_documents[event.obj['user_id']]['teacher'].capitalize(),
                                transcript_values.get(users_documents[event.obj['user_id']]['type_lesson']),
                                users_documents[event.obj['user_id']]['task'],
                                users_documents[event.obj['user_id']]['variant'],
                                users_documents[event.obj['user_id']]['document_tittle'],
                                users_documents[event.object['user_id']]['price'],
                                users_documents[event.obj['user_id']]['phone']),
                            attachment=users_documents[event.obj['user_id']]['discription'])
                    elif event.object.payload.get('type') == 'buy_work':
                        try:
                            vk.messages.edit(
                                peer_id=event.object.peer_id,
                                keyboard=keyboard_return.keyb.get_keyboard(),
                                conversation_message_id=event.object.conversation_message_id,
                                message='Здесь вы можете купить работу которая есть у нас в базе. '
                                        '\nНадеемся, что Вам удасться найти то, что вы ищите')
                        except:
                            vk.messages.send(
                                    user_id=event.object['user_id'],
                                    random_id=get_random_id(),
                                    peer_id=event.object['user_id'],
                                    keyboard=keyboard_return.keyb.get_keyboard(),
                                    message='Здесь вы можете купить работу которая есть у нас в базе. '
                                            '\nНадеемся, что Вам удасться найти то, что вы ищите.\n'
                                            'Введите фамилию преподавателя')
                        vk.messages.send(
                                user_id=event.object['user_id'],
                                random_id=get_random_id(),
                                peer_id=event.object['user_id'],
                                message='Укажите только фамилию преподавателя')
                        work_status_mem[event.object['user_id']] = 'teacher'

                    #поиск работы в базе


                    elif event.object.payload.get('type') == check():
                        try:
                            vk.messages.edit(
                                peer_id=event.object.peer_id,
                                keyboard=keyboard_return.keyb.get_keyboard(),
                                conversation_message_id=event.object.conversation_message_id,
                                message='Выбор преподавателя: '+ str(search_work[event.object['user_id']]['teacher']).capitalize())
                        except:
                            vk.messages.send(
                                user_id=event.object['user_id'],
                                random_id=get_random_id(),
                                peer_id=event.object['user_id'],
                                message='Выбор преподавателя: '+ str(search_work[event.object['user_id']]['teacher']).capitalize())
                        a = db_search.search_work(search_work[event.object['user_id']]['teacher'], event.object['user_id'])
                        m = ''
                        i = 1
                        search_work[event.object['user_id']]['works_id'] = {}
                        for elem in a:
                            search_work[event.object['user_id']]['works_id'].update([(i,elem[0])])
                            m += '{}.Название работы: {}\n Вариант: {}\n ' \
                               'Тип Работы: {}\n\n'.format(i,elem[1], elem[2], transcript_values.get(elem[3]))
                            i += 1
                        if i > 1:
                            vk.messages.send(
                                user_id=event.object['user_id'],
                                random_id=get_random_id(),
                                peer_id=event.object['user_id'],
                                message='Список всех работ преподавателя для вашего курса и типа обучения\n'+m)
                            vk.messages.send(
                                user_id=event.object['user_id'],
                                random_id=get_random_id(),
                                peer_id=event.object['user_id'],
                                keayboard=keyboard_return.keyb.get_keyboard(),
                                message='Выберите работу которую хотите скачать и отправьте цифру этой работы'
                            )

                        else:
                            vk.messages.send(
                                user_id=event.object['user_id'],
                                random_id=get_random_id(),
                                peer_id=event.object['user_id'],
                                message='К сожалению на данный момент для вашего курса и типа обучения'
                                        ' отсутствуют работы от этого преподавателя')
                        work_status_mem[event.object['user_id']] = 'choice_work'

                    # покупка работы
                    elif event.object.payload.get('type') in list(reqest_work_payment.keys()):
                        work_id = event.object.payload.get('type')
                        m = db_search.get_work_info(reqest_work_payment.get(work_id))
                        generated_pay = payment.generate_url(int(m[5]), event.object.payload.get('type'), m[7], reqest_work_payment.get(work_id),event.object['user_id'])
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.object['user_id'],
                            message='Для того чтобы получить работу, совершите перевод денежных средств по номеру'
                                    ' +79221385525 '
                                    'на сумму {} и ОБЯЗАТЕЛЬНО укажите в коментарии данную комбинацию '
                                    'цифр {}.\n\n После совершения платежа, в течение 15 минут вам будет отправлена'
                                    ' ссылка на скачивание работы'.format(str(generated_pay[0]), generated_pay[1])
                        )

                    elif event.object.payload.get('type') == 'rate':
                        work_status_mem[event.object['user_id']] = 'rate'
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            peer_id=event.object.peer_id,
                            random_id=get_random_id(),
                            keyboard=keyboard_return.keyb.get_keyboard(),
                            conversation_message_id=event.object.conversation_message_id,
                            message='Теперь Вы можете оставить анонимный отзыв о сервисе, либо пожелание по улучшению сервиса, '
                                    'либо жалобу, которую мы рассмотрим в обязательном порядке. Для этого напишите свой отзыв.')
                    else:
                        db.update_status(event.object['user_id'], 'main')
                        vk.messages.send(
                            user_id=event.object['user_id'],
                            peer_id=event.object.peer_id,
                            random_id=get_random_id(),
                            keyboard=keyboard_main.keyb.get_keyboard(),
                            conversation_message_id=event.object.conversation_message_id,
                            message='Произошел сбой...\nВыберите одну из наших функций')

                else:
                    """Добавление данных о новом пользователе"""
                    if event.object.payload.get('type') in type_bac_mag:
                        memory_users_new[event.object['user_id']] = [event.object.payload.get('type')]
                        edited = vk.messages.edit(
                            peer_id=event.object.peer_id,
                            message='Выберите курс',
                            conversation_message_id=event.object.conversation_message_id,
                            keyboard=keyboard_kurs.keyb.get_keyboard())
                    elif event.object.payload.get('type') in type_kurs:
                        memory_users_new[event.object['user_id']].append(event.object.payload.get('type'))
                        edited = vk.messages.edit(
                            peer_id=event.object.peer_id,
                            message='Профиль сохранен',
                            conversation_message_id=event.object.conversation_message_id, )
                        if len(memory_users_new[event.object['user_id']]) == 2:
                            db.update(memory_users_new[event.object['user_id']][1],
                                      memory_users_new[event.object['user_id']][0],
                                      event.object['user_id'])
                        sender = vk.messages.send(
                            user_id=event.object['user_id'],
                            random_id=get_random_id(),
                            peer_id=event.object['user_id'],
                            keyboard=keyboard_main.keyb.get_keyboard(),
                            message='Теперь Вы можете пользоваться с удобством нашим серивсом')

    except requests.exceptions.ReadTimeout:
        print('Переподключение')
        time.sleep(10)

if __name__ == '__main__':
    pass
