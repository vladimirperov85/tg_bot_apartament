from aiogram import Router
from . import estimate, start

def get_routers():
    return (start.router,estimate.router)