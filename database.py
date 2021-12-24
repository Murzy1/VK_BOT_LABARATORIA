import sqlite3 as db
import yadisk
from fuzzywuzzy import process
import time


def start():
    try:
        dtb = db.connect('users_info.db')
        cursorObj = dtb.cursor()
        cursorObj.execute("CREATE TABLE users(id integer PRIMARY KEY, vk_user_id integer , "
                          "bac_mag text, kurs text, documents integer,status text, UNIQUE(vk_user_id))")
    except:
        print('error')
        exit()

def create_lead_work():
    try:
        dtb = db.connect('bought_work_leads.db')
        cursorObj = dtb.cursor()
        cursorObj.execute("CREATE TABLE leads(id integer PRIMARY KEY, vk_user_id integer , adressant__vk_id integer,"
                          "work_id text, payment_id bloob, documents_url bloob, operation_status text DEFAULT Wait, "
                          "send_status text)")
        dtb.commit()
        dtb.close()
    except:
        print('error')
        exit()

def create_table_documents():
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("CREATE TABLE documents(id integer PRIMARY KEY, vk_user_id integer , "
                      "bac_mag text, kurs text, teacher text,type_lesson text, task text, description text, "
                      "variant text, doc_type text, doc_url text, phone_number text, price integer,yan_down_url text)")
    dtb.commit()
    dtb.close()


def add_users(vk_user_id):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute('INSERT OR IGNORE INTO  users(vk_user_id, bac_mag, kurs, documents) VALUES(?,?,?,?)',
                      (vk_user_id, 'Null', 'Null', 0))
    dtb.commit()
    dtb.close()


def update(kurs, bac_mag, vk_user_id):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("UPDATE users SET bac_mag= ?, kurs=? WHERE vk_user_id = ? ", (bac_mag, kurs, vk_user_id))
    dtb.commit()
    dtb.close()


def check(user_id):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    checker = cursorObj.execute("SELECT * from users WHERE vk_user_id = ? AND (kurs != 'Null' or bac_mag != 'Null')",
                                (user_id,))
    if checker.fetchone() is None:
        return 0
    else:
        return 1
    dtb.close()


def update_status(vk_user_id, status):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("UPDATE users SET status = ? WHERE vk_user_id = ?", (status, vk_user_id))
    dtb.commit()
    dtb.close()


def user_check_status(vk_user_id):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    checker = cursorObj.execute("SELECT * from users WHERE vk_user_id = ? AND status = 'work_added'", (vk_user_id,))
    if checker.fetchone() is None:
        return 0
    else:
        return 1
    dtb.close()


def update_all_status():
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("SELECT status FROM users")
    massive_big = cursorObj.fetchall()
    for i in range(len(massive_big)):
        cursorObj.execute("UPDATE users SET status = 'main' ")
    dtb.commit()
    dtb.close()

def upload_work(doc: dict, user: int):
    f = doc
    y = yadisk.YaDisk(token='AQAAAAAUFYsKAAd0OcqOFFybTErUvXiFG44zuZU')
    exi = y.exists('{0}/'.format(user))
    grape = ''
    if len(f['document_tittle']) >= 1 and exi:
        y.mkdir('{0}/{1}'.format(user,f['task']))
        for elem in range(len(f['document_tittle'])):
            m = '{0}/{1}/{2}_{3}_{4}_{5}.{6}'.format(user, f['task'], f['teacher'].split(' ')[0], f['kurs'],
                                                     f['task'], f['variant'],
                                                     f['document_tittle'][elem].split('.')[-1])
            y.upload_url(path=m, url=f['document_url'][elem])
            grape = '{0}/{1}'.format(user,f['task'])
    elif len(f['document_tittle']) >= 1 :
            y.mkdir('{0}'.format(user))
            y.mkdir('{0}/{1}'.format(user, f['task']))
            for elem in range(len(f['document_tittle'])):
                m = '{0}/{1}/{2}_{3}_{4}_{5}.{6}'.format(user, f['task'], f['teacher'].split(' ')[0], f['kurs'],
                                                     f['task'], f['variant'],
                                                     f['document_tittle'][elem].split('.')[-1])
                y.upload_url(path=m, url=f['document_url'][elem])
    y.publish(path=grape)
    a = y.get_meta(path=grape)
    ur = a['public_url']

    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("INSERT INTO  documents(vk_user_id, "
                      "bac_mag, kurs, teacher ,type_lesson, task, description, "
                      "variant, doc_type, doc_url, phone_number, price, yan_down_url ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (user,
                      f['bac_mag'], f['kurs'], f['teacher'], f['type_lesson'], f['task'],
                      f['discription'], f['variant'], f['task'], 'noone',
                      f['phone'], f['price'], '{}'.format(ur)))
    dtb.commit()
    dtb.close()

def search_teacher(last_name: str):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    m = cursorObj.execute('SELECT DISTINCT teacher FROM documents')
    a = process.extractOne(last_name, m)
    dtb.close()
    return a
def user_work_status(uesr_id: str,status: str):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("CREATE TABLE work_status(id integer PRIMARY KEY, vk_user_id integer , "
                      "status text UNIQUE(vk_user_id))")
if __name__ == '__main__':
    create_lead_work()
