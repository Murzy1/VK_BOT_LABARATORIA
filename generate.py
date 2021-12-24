import keyboards
import random
from vk_api.keyboard import VkKeyboardColor


def payment_k():
    base_k = keyboards.time_K()
    random_id = random.randint(1000000,9000000)
    base_k.keyb.add_callback_button('Купить работу', color=VkKeyboardColor.POSITIVE, payload={'type':str(random_id)})
    base_k.keyb.add_line()
    base_k.keyb.add_callback_button(label='Вернуться в меню', color=VkKeyboardColor.NEGATIVE, payload={'type': 'return'})
    m = (base_k.keyb.get_keyboard(),random_id)
    base_k.keyb.lines = [[]]
    base_k.keyb.keyboard['buttons'] = base_k.keyb.lines
    return m


