from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,ReplyKeyboardRemove


from keyboards import REPAIR_CLASSES, repair_classes_keyboard
from services.calculator import calculate_estimated,format_estimate
from states import EstimateForm
from utils.parsers import parse_positive_int, parse_positive_float

router = Router(name=__name__)

@router.message(EstimateForm.area,F.text)
async def process_area(message: Message,state:FSMContext):
    area = parse_positive_float(message.text)
    if area is None or not 10 <=area<=1000:
        await message.answer("Площадь должна быть в диапазоне от 10 до 1000")
        return
    
    await state.update_data(area=area)
    await state.set_state(EstimateForm.ceiling_height)
    await message.answer('Введите высоту потолков')



@router.message(EstimateForm.ceiling_height,F.text)
async def process_ceiling_height(message: Message,state:FSMContext):
    ceiling_height = parse_positive_float(message.text)
    if ceiling_height is None or not 2 <=ceiling_height<=5:
        await message.answer("Высота должна быть в диапазоне от 2 до 5")
        return
    
    await state.update_data(ceiling_height=ceiling_height)
    await state.set_state(EstimateForm.rooms)
    await message.answer('Введите количество комнат')


@router.message(EstimateForm.rooms,F.text)
async def process_rooms(message: Message,state:FSMContext):
    rooms = parse_positive_int(message.text)
    if rooms is None or not 1 <=rooms<=15:
        await message.answer("Введите количество комнат должна быть в диапазоне от 1 до 15")
        return
    
    await state.update_data(rooms=rooms)
    await state.set_state(EstimateForm.repair_class)
    await message.answer('Выбирете класс ремонта',reply_markup=repair_classes_keyboard())


@router.message(EstimateForm.repair_class,F.text)
async def process_repair_class(message: Message,state:FSMContext):
    repair_class = (message.text).strip().capitalize()
    if repair_class not in REPAIR_CLASSES:
        await message.answer("Выберете один зи вариантов на клавиатуре",reply_markup=repair_classes_keyboard())
        return
    
    data = await state.update_data(repair_class=repair_class)
    await state.clear()
    estimate = calculate_estimated(
        area=data["area"],
        ceiling_height=(data['ceiling_height']),
        rooms=data['rooms'],
        repair_class=repair_class,
    )

    result_text = format_estimate(
        area=data["area"],
        ceiling_height=(data['ceiling_height']),
        rooms=data['rooms'],
        repair_class=repair_class,
        estimate=estimate
    )

    await message.answer(result_text,reply_markup=ReplyKeyboardRemove())

@router.message(EstimateForm.area)
@router.message(EstimateForm.ceiling_height)
@router.message(EstimateForm.rooms)
@router.message(EstimateForm.repair_class)
async def process_not_text(message: Message):
    await message.answer('Пожалуйста отправьте текстовое сообщение')
