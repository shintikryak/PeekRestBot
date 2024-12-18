import sqlite3
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

# Функция для получения всех объектов
def get_locations():
    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM locations")
    locations = cursor.fetchall()
    conn.close()
    return locations

def get_restaurants_by_location(location_id):
    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM restaurants WHERE location_id = ?", (location_id,))
    restaurants = cursor.fetchall()
    conn.close()
    return restaurants

def get_tables_by_restaurant(restaurant_id):
    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, capacity FROM tables WHERE restaurant_id = ? AND available = 1", (restaurant_id,))
    tables = cursor.fetchall()
    conn.close()
    return tables

# Команда /start
@router.message(Command("start"))
async def start_command(message: Message):
    locations = get_locations()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"location:{id}")]
            for id, name in locations
        ]
    )
    await message.answer("Выберите вашу локацию:", reply_markup=keyboard)

# Локация → Рестораны
@router.callback_query(F.data.startswith("location:"))
async def location_selected(callback: CallbackQuery):
    location_id = int(callback.data.split(":")[1])
    restaurants = get_restaurants_by_location(location_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"restaurant:{id}:{location_id}")]
            for id, name in restaurants
        ] + [[InlineKeyboardButton(text="Назад", callback_data="back:locations")]]
    )
    await callback.message.edit_text("Выберите ресторан:", reply_markup=keyboard)

# Рестораны → Столики
@router.callback_query(F.data.startswith("restaurant:"))
async def restaurant_selected(callback: CallbackQuery):
    data = callback.data.split(":")
    restaurant_id = int(data[1])
    location_id = int(data[2])
    tables = get_tables_by_restaurant(restaurant_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Столик на {capacity} чел.", callback_data=f"table:{id}:{restaurant_id}")]
            for id, capacity in tables
        ] + [[InlineKeyboardButton(text="Назад", callback_data=f"back:restaurants:{location_id}")]]
    )
    await callback.message.edit_text("Выберите столик:", reply_markup=keyboard)

# Столики → Рестораны
@router.callback_query(F.data.startswith("back:restaurants:"))
async def back_to_restaurants(callback: CallbackQuery):
    location_id = int(callback.data.split(":")[2])
    restaurants = get_restaurants_by_location(location_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"restaurant:{id}:{location_id}")]
            for id, name in restaurants
        ] + [[InlineKeyboardButton(text="Назад", callback_data="back:locations")]]
    )
    await callback.message.edit_text("Выберите ресторан:", reply_markup=keyboard)

# Рестораны → Локации
@router.callback_query(F.data == "back:locations")
async def back_to_locations(callback: CallbackQuery):
    locations = get_locations()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"location:{id}")]
            for id, name in locations
        ]
    )
    await callback.message.edit_text("Выберите вашу локацию:", reply_markup=keyboard)

# Выбор столика
@router.callback_query(F.data.startswith("table:"))
async def table_selected(callback: CallbackQuery):
    table_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(f"Вы выбрали столик с ID {table_id}. Свяжитесь с администратором для бронирования.")
