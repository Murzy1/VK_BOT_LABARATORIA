import yookassa as yk
import database_search_work as db


def generate_url(price, payment_id, seller_id, work_id, recipient_id):
    payment ={
        "viewed_price": str(int(price) + 100) + ' Р',
        "price": int(price)+100,
        "description": "Заказ №" + str(payment_id),
        "metadata": {
            'seller_id': seller_id,
            'work_id': work_id,
            'recipient': recipient_id
        }
    }

    #Добавляем данные о созданном платеже в базу
    db.add_payment_info(payment_id, seller_id, work_id, recipient_id,payment['price'])
    return (payment['viewed_price'], str(payment_id))


if __name__ == '__main__':
    pass
