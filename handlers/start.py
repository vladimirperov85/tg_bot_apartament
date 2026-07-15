from aiogram import Router
from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,ReplyKeyboardRemove
from states import EstimateForm

router = Router(name=__name__)

@router.message(CommandStart())
async def command_start(message:Message,state:FSMContext):

    await state.clear()
    await state.set_state(EstimateForm.area)
    await message.answer("Здравствуйте.Расчет стоимости ремонта квартиры\n\n"
                        "Введите площадь квартиры в кв. метрах(45.5)",
                        reply_markup=ReplyKeyboardRemove())

@router.message(Command('cancel'))
async def command_cancel(message: Message, state:FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активного расчета.Начните с /start")
        return
    await state.clear()
    await message.answer('Расчет отменен.Нажмите /start, чтобы начать',reply_markup=ReplyKeyboardRemove())
