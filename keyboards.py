from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

REPAIR_CLASSES = ('Эконом','Стандарт','Премиум')

def repair_classes_keyboard():
    """
    создает телеграмм клавиатуру,появляется вместо стандартной
    """
    return ReplyKeyboardMarkup(
        # каждый список это строка с кнопками на экране
        keyboard=[
            [KeyboardButton(text='Эконом')],
            [KeyboardButton(text='Стандарт')],
            [KeyboardButton(text='Премиум')]

        ],
        # компактная клавиатура
        resize_keyboard=True,
        # убрать кнопку, после выбора
        one_time_keyboard=True,
        input_field_placeholder="Введите класс ремонта"

    )

