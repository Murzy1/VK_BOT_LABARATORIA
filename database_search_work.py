import sqlite3 as db
import yadisk

def search_work(teacher: str, user_id):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("SELECT bac_mag, kurs from users WHERE vk_user_id=?", (user_id,))
    bac_mag, kurs = cursorObj.fetchone()
    works = cursorObj.execute('SELECT id, task, variant , type_lesson from documents WHERE bac_mag = ? AND teacher = ? AND kurs = ?', (bac_mag, teacher,kurs))
    return works.fetchall()

def get_work_info(id):
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("SELECT kurs, teacher, type_lesson, task, variant, price ,description, vk_user_id from documents WHERE id=?", (id,))
    work = cursorObj.fetchone()
    return work

def add_payment_info(payment_id, seller_id, work_id, recipient_id,price):
    """Функция для добавления данных о созданном платеже """
    dtb = db.connect('users_info.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("SELECT yan_down_url from documents WHERE id=?",(work_id,))
    work_url = cursorObj.fetchone()

    y = yadisk.YaDisk(token='AQAAAAAUFYsKAAd0OcqOFFybTErUvXiFG44zuZU')
    a = y.get_meta(path=work_url[0])
    if a['public_key'] != None:
        ur = a['public_url']
    else:
        y.publish(path=work_url[0])
        a = y.get_meta(path=work_url)
        ur = a['public_url']
    dtb.close()
    dtb = db.connect('bought_work_leads.db')
    cursorObj = dtb.cursor()
    cursorObj.execute("INSERT INTO leads(vk_user_id, adressant_vk_id,"
                          "work_id, payment_id, documents_url, operation_status, "
                          "price) VALUES(?,?,?,?,?,?,?)",(seller_id,recipient_id,work_id,payment_id,ur,'Wait',price))
    dtb.commit()
    dtb.close()
if __name__ == "__main__":
    pass