from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Main_K():
    settings = dict(one_time=False, inline=True)
    # №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
    keyb = VkKeyboard(**settings)
    # pop-up кнопка
    keyb.add_callback_button(label='Купить готовое задание', color=VkKeyboardColor.POSITIVE,
                             payload={"type": "buy_work"})
    keyb.add_line()
    # кнопка с URL
    keyb.add_callback_button(label='Добавить работу', color=VkKeyboardColor.NEGATIVE,
                             payload={"type": "add_work"})
    keyb.add_line()
    # кнопка по открытию ВК-приложения
    #keyb.add_callback_button(label='Использовать помощь для задачи', color=VkKeyboardColor.POSITIVE,
    #                         payload={"type": "get_help_from_users"})
    #keyb.add_line()
    #keyb.add_callback_button(label='Разместить услги', color=VkKeyboardColor.PRIMARY,
     #                        payload={"type": "offer_assistante"})
    #keyb.add_line()

    keyb.add_callback_button(label='Оставить отзыв о работе сервиса', color=VkKeyboardColor.POSITIVE,
                             payload={"type": "rate"})


# №2. Клавиатура с одной красной callback-кнопкой. Нажатие изменяет меню на предыдущее.
class Select_year_of_unv_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='1 курс', payload={'type': 'kurs_first'})
    keyb.add_callback_button(label='2 курс', payload={'type': 'kurs_second'})
    keyb.add_line()
    keyb.add_callback_button(label='3 курс', payload={'type': 'kurs_third'})
    keyb.add_callback_button(label='4 курс', payload={'type': 'kurs_four'})


class Select_bac_mag_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='Баклавриат', payload={'type': 'bacalavr'})
    keyb.add_line()
    keyb.add_callback_button(label='Магистратура', payload={'type': 'magistr'})


class Faq_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='Вернуться в меню',color=VkKeyboardColor.NEGATIVE, payload={'type': 'return'})


class Add_work_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='Начать процесс добавления работы', color=VkKeyboardColor.POSITIVE,
                             payload={'type': 'work_add_start'})
    keyb.add_line()
    keyb.add_callback_button(label='Вернуться в меню',color=VkKeyboardColor.NEGATIVE, payload={'type': 'return'})

class choice_lesson_type_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='Лабораторная работа', payload={'type':'lab_task'})
    keyb.add_callback_button(label='Реферат', payload={'type':'refer_task'})
    keyb.add_line()
    keyb.add_callback_button(label='Контроьная работа', payload={'type':'kr_task'})
    keyb.add_callback_button(label='Отчет по практике', payload={'type':'ot_task'})
    keyb.add_line()
    keyb.add_callback_button(label='Практическое задание', payload={'type':'pr_task'})
    keyb.add_line()
    keyb.add_callback_button(label='Вернуться в меню',color=VkKeyboardColor.NEGATIVE, payload={'type': 'return'})

class variants_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='Без варианта', payload={'type': 'variant_out'})
    keyb.add_line()
    keyb.add_callback_button(label='Вернуться в меню', payload={'type': 'return'})
class work_price_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='150', payload={'type': 'price_150'})
    keyb.add_line()
    keyb.add_callback_button(label='200', payload={'type': 'price_200'})
    keyb.add_line()
    keyb.add_callback_button(label='250', payload={'type': 'price_250'})
    keyb.add_line()
    keyb.add_callback_button(label='400', payload={'type': 'price_400'})
    keyb.add_line()
    keyb.add_callback_button(label='Вернуться в меню',color=VkKeyboardColor.NEGATIVE, payload={'type': 'return'})

class add_work_check_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='Загрузить работу', color=VkKeyboardColor.POSITIVE, payload={'type': 'upload_work'})
    keyb.add_line()
    keyb.add_callback_button(label='Отменить загрузку',color=VkKeyboardColor.NEGATIVE, payload={'type': 'return'})

class time_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)


class return_K():
    settings = dict(one_time=False, inline=True)
    keyb = VkKeyboard(**settings)
    keyb.add_callback_button(label='Вернуться в меню',color=VkKeyboardColor.NEGATIVE, payload={'type': 'return'})
