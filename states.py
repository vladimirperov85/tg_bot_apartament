from aiogram import State, StatesGroup

class EstimateForm(StatesGroup):
    area = State()
    ceiling_height = State()
    rooms = State()
    repair_class = State()