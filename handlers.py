from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def start_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать рестораны", callback_data="show_restaurants")],
    ])
    await message.answer("Привет! Я бот для бронирования столов. Выберите действие:", reply_markup=keyboard)

# Обработчик кнопки "Показать рестораны"
@router.callback_query(lambda callback: callback.data == "show_restaurants")
async def show_restaurants(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ресторан А", callback_data="restaurant_a")],
        [InlineKeyboardButton(text="Ресторан Б", callback_data="restaurant_b")],
        [InlineKeyboardButton(text="Ресторан В", callback_data="restaurant_c")],
    ])
    await callback.message.edit_text("Выберите ресторан:", reply_markup=keyboard)
    await callback.answer()

# Обработчик выбора ресторана
@router.callback_query(lambda callback: callback.data in ["restaurant_a", "restaurant_b", "restaurant_c"])
async def restaurant_selected(callback: CallbackQuery):
    restaurant_name = {
        "restaurant_a": "Ресторан А",
        "restaurant_b": "Ресторан Б",
        "restaurant_c": "Ресторан В"
    }.get(callback.data, "Неизвестный ресторан")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Свободные столики", callback_data=f"tables_{callback.data}")],
    ])
    await callback.message.edit_text(f"Вы выбрали {restaurant_name}. Что дальше?", reply_markup=keyboard)
    await callback.answer()

# Обработчик кнопки "Свободные столики"
@router.callback_query(lambda callback: callback.data.startswith("tables_"))
async def show_tables(callback: CallbackQuery):
    restaurant_code = callback.data.split("_")[1]

    # Заглушка для столиков
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Столик на двоих", callback_data="table_2")],
        [InlineKeyboardButton(text="Столик на четверых", callback_data="table_4")],
        [InlineKeyboardButton(text="VIP-зона", callback_data="table_vip")],
    ])
    await callback.message.edit_text(f"Свободные столики в {restaurant_code}:", reply_markup=keyboard)
    await callback.answer()

# Обработчик выбора конкретного столика
@router.callback_query(lambda callback: callback.data.startswith("table_"))
async def table_selected(callback: CallbackQuery):
    table_name = {
        "table_2": "Столик на двоих",
        "table_4": "Столик на четверых",
        "table_vip": "VIP-зона"
    }.get(callback.data, "Неизвестный столик")

    await callback.message.edit_text(f"Вы выбрали {table_name}. Чтобы забронировать, свяжитесь с администратором.")
    await callback.answer()
