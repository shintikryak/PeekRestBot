from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command  # Добавьте импорт Command

# Создаем роутер
router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот для бронирования столов. Чем могу помочь?", parse_mode="HTML")

# Обработчик команды /restaurants
@router.message(Command("restaurants"))
async def show_restaurants(message: Message):
    # Заглушка для списка ресторанов
    await message.answer("Список ресторанов:\n1. Ресторан А\n2. Ресторан Б\n3. Ресторан В")

# Обработчик команды /tables
@router.message(Command("tables"))
async def show_tables(message: Message):
    # Заглушка для списка столиков
    await message.answer("Свободные столики:\n1. Столик на двоих\n2. Столик на четверых\n3. VIP-зона")
