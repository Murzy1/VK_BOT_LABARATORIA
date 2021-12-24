import sqlite3 as db
import time

import os
from vk_api import VkApi
from vk_api.utils import get_random_id
import requests


GROUP_ID = '207393442'
GROUP_TOKEN = 'a7dc5fc4c67bbaac52e46b3a29c3db21457bc797dcb2093a4edd4b90632e13a3183a9ccd828a73415cce2'
API_VERSION = '5.120'


db_file = os.path.getmtime('bought_work_leads.db')
dt_time = time.perf_counter()
while True:
    try:
        vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
        vk = vk_session.get_api()
        while True:
            work_id_lissener = int(input('Введите индентефикатор: '))
            db_file = os.path.getmtime('bought_work_leads.db')

            dtb = db.connect('bought_work_leads.db')
            cursorObj = dtb.cursor()
            cursorObj.execute("SELECT * from leads WHERE payment_id=?", (str(work_id_lissener),))
            leads = cursorObj.fetchone()
            try:
                vk.messages.send(
                        user_id=leads[2],
                        random_id=get_random_id(),
                        peer_id=leads[2],
                        message='Ссылка на скачиване купленной работы: '+leads[5])
                cursorObj.execute("UPDATE leads SET operation_status = ? WHERE payment_id = ?",
                                                  ('OPLACHENO', leads[4],))
                dtb.commit()
                dtb = db.connect('users_info.db')
                cursorObj = dtb.cursor()
                cursorObj.execute("SELECT phone_number, price from documents WHERE id=?", (str(leads[3]),))
                sender_info = cursorObj.fetchone()
                print('Отправлено и обработано, перевести деньги продавцу по номеру {}, '
                      'сумма {}'.format(sender_info[0],sender_info[1]))
            except:
                continue
    except requests.exceptions.ReadTimeout:
        pass
if __name__=='__main__':
    pass