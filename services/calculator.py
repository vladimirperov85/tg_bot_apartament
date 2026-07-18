from dataclasses import dataclass

@dataclass
class RepairRates:
    # стоимость стен
    wall_labor:int

    # стоимость материалов для стен
    wall_materials:int

    # стоимость работ по полу
    floor_labor :int

    # стоимость материалвов для пола
    floor_materails: int

    # стоимость работ по потолку
    ceiling_labor :int

    # стоимость материалвов для потолка
    celing_materails: int

RATES_BY_CLASS = {
    "Эконом": RepairRates(
        wall_labor=430,
        wall_materials=260,
        floor_labor=520,
        floor_materails=900,
        ceiling_labor=300,
        celing_materails=160
        ),
    "Стандарт": RepairRates(
        wall_labor=530,
        wall_materials=360,
        floor_labor=620,
        floor_materails=1000,
        ceiling_labor=400,
        celing_materails=260
        ),
    "Премиум": RepairRates(
        wall_labor=630,
        wall_materials=460,
        floor_labor=620,
        floor_materails=1100,
        ceiling_labor=500,
        celing_materails=260
        ),
}

def calculate_estimated(area,ceiling_height,rooms,repair_class):
    # получаем расценки
    rates = RATES_BY_CLASS[repair_class]
    # площадь стен

    wall_area = area * ceiling_height * 1.8

    # считаем что площадь пола и потолка примерно равна площади квартиры
    floor_area=area
    ceiling_area=area

    # сумма по стенам = площадь стен * (работы + материалы)
    wall_total = wall_area * (rates.wall_labor + rates.wall_materials)

    # сумма по полу = площадь пола * (работы + материалы)
    floor_total = floor_area*(rates.floor_labor+rates.floor_materails)

    #cумма по потолку = площадь потолка *( работы+материал)
    ceiling_total = ceiling_area*(rates.ceiling_labor+ rates.celing_materails)
    
    # за каждую комнату после 1 добавляем 5% от общей суммы
    room_complexity = 1 + max(0,rooms-1)* 0.05

    # доставка и уборка
    delivery_and_cleanup = area * 180

    # предварительнная сумма(цена)
    subtotal= wall_total + floor_total + ceiling_total + delivery_and_cleanup

    # итоговая стоимость
    total = subtotal * room_complexity

    return{
        "wall_area": wall_area,
        'floor_area':floor_area,
        'ceiling_area' :ceiling_area,
        'wall_total':wall_total,
        'floor_total':floor_total,
        'ceiling_total':ceiling_total,
        'delivery_and_cleanup':delivery_and_cleanup,
        'room_complexity':room_complexity,
        'total':total

    }

# Псевдоним для calculate_estimate
#calculate_estimate = calculate_estimated

def format_money(value):
    return f"${value:,.0f}".replace(",", " ") + "руб."

def format_estimate(
        *,
        area,
        ceiling_height,
        rooms,
        repair_class,
        estimate
):
    """Собираем html сметы для отправки пользователю"""
    complexity_percent = round((estimate['room_complexity'] -1) * 100)
    return (
        "<b>Расчеитная стоимость ремонта:</b>\n\n"
        "<b> Исходные данные: </b>\n"
        f"Площадь помещения:<b>{area:g}кв.м</b>\n "
        f"Высота потолков:<b>{ceiling_height:g}кв.м</b>\n "
        f"Количество комнат:<b>{rooms:g}кв.м</b>\n "
        f"Класс ремонта:<b>{repair_class}</b>\n "
        "</b> Исходные данные</b>\n"
        f"Стены:<b>{estimate['wall_area']:.1f}кв.м</b>\n"
        f"Потолок:<b>{estimate['ceiling_area']:.1f}кв.м</b>\n"
        f"Пол:<b>{estimate['floor_area']:.1f}кв.м</b>\n"
        "<b>Смета:</b>\n"
        f"Стены:{format_money(estimate['wall_total'])}\n"
        f"Пол:{format_money(estimate['floor_total'])}\n"
        f"Потолок:{format_money(estimate['ceiling_total'])}\n"
        f"Доставка и уборка:{format_money(estimate['delivery_and_cleanup'])}\n"
        f"Коэф. комнат: + {complexity_percent}%\n"
        f"<b>Итого: {format_money(estimate['total'])}</b>\n\n"
        'Чтобы посчитать заново, нажмите /start'
)
