import sqlite3
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from ModelsWorkers.location import LocationModelWorker
from ModelsWorkers.restaurant import RestaurantModelWorker
from ModelsWorkers.table import TableModelWorker
from minio_client import MinioClient

router = Router()

def get_locations():
    return LocationModelWorker().get_all()

def get_restaurants_by_location(location_id):
    return RestaurantModelWorker().get_restaurants_by_location(location_id)

def get_tables_by_restaurant(restaurant_id):
    return TableModelWorker().get_tables_by_restaurant(restaurant_id)

def get_restaurant_by_id(id):
    return RestaurantModelWorker().get_restaurant_by_id(id)

# Команда /start
@router.message(Command("start"))
async def start_command(message: Message):
    locations = get_locations()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=piece['name'], callback_data=f"location:{piece['id']}")]
            for piece in locations
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
            [InlineKeyboardButton(text=piece['name'], callback_data=f"restaurant:{piece['id']}:{location_id}")]
            for piece in restaurants
        ] + [[InlineKeyboardButton(text="Назад", callback_data="back:locations")]]
    )
    await callback.message.edit_text("Выберите ресторан:", reply_markup=keyboard)

# Рестораны → Столики
@router.callback_query(F.data.startswith("restaurant:"))
async def restaurant_selected(callback: CallbackQuery):
    data = callback.data.split(":")
    restaurant_id = int(data[1])
    location_id = int(data[2])

    restaurant = get_restaurant_by_id(restaurant_id)
    tables = get_tables_by_restaurant(restaurant_id)
    photos = MinioClient().get_tables_by_rest(restaurant.name)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Столик на {piece['capacity']} чел.", callback_data=f"table:{piece['id']}:{restaurant_id}")]
            for piece in tables
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
