import io
import sqlite3
from io import BytesIO
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from minio_client import MinioClient
from ModelsWorkers.location import LocationModelWorker
from ModelsWorkers.restaurant import RestaurantModelWorker
from ModelsWorkers.table import TableModelWorker
 
router = Router()
 
# ==========================
# FSM для владельца
# ==========================
class OwnerStates(StatesGroup):
    waiting_for_restaurant_name = State()
    waiting_for_restaurant_address = State()
    waiting_for_table_capacity = State()
    waiting_for_table_photo = State()
    waiting_for_restaurant_location = State()
 
# ==========================
# Команда /start - выбор роли
# ==========================
@router.message(Command("start"))
async def start_command(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Клиент", callback_data="role:client"),
                InlineKeyboardButton(text="Владелец", callback_data="role:owner")
            ]
        ]
    )
    await message.answer("Вы хотите взаимодействовать как клиент или владелец?", reply_markup=keyboard)
 
# ==========================
# Обработчик выбора роли
# ==========================
@router.callback_query(F.data.startswith("role:"))
async def role_selected(callback: CallbackQuery):
    role = callback.data.split(":")[1]
    if role == "client":
        # Клиентский сценарий: вывод локаций
        locations = LocationModelWorker().get_all()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=loc['name'], callback_data=f"location:{loc['id']}")]
                for loc in locations
            ]
        )
        await callback.message.edit_text("Выберите вашу локацию:", reply_markup=keyboard)
    elif role == "owner":
        # Меню для владельца
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Добавить ресторан", callback_data="owner:add_restaurant")],
                [InlineKeyboardButton(text="Добавить столик", callback_data="owner:add_table")]
            ]
        )
        await callback.message.edit_text("Добро пожаловать, владелец. Выберите действие:", reply_markup=keyboard)
 
# ==========================
# Сценарий добавления ресторана (владелец)
# ==========================
@router.callback_query(F.data == "owner:add_restaurant")
async def owner_add_restaurant(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите название ресторана:")
    await state.set_state(OwnerStates.waiting_for_restaurant_name)
 
@router.message(OwnerStates.waiting_for_restaurant_name)
async def process_restaurant_name(message: Message, state: FSMContext):
    # Сохраняем введённое название и запрашиваем адрес
    await state.update_data(restaurant_name=message.text)
    await message.answer("Введите адрес ресторана:")
    await state.set_state(OwnerStates.waiting_for_restaurant_address)
 
@router.message(OwnerStates.waiting_for_restaurant_address)
async def process_restaurant_address(message: Message, state: FSMContext):
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    restaurant_address = message.text
    # Сохраняем ресторан в базе и связываем с владельцем (используем chat_id как идентификатор владельца)
    RestaurantModelWorker().add_restaurant(
        owner_id=message.from_user.id,
        name=restaurant_name,
        address=restaurant_address
    )
    await message.answer(f"Ресторан '{restaurant_name}' по адресу '{restaurant_address}' успешно добавлен!")
    await state.clear()
 
# ==========================
# Сценарий добавления столика (владелец)
# ==========================
@router.callback_query(F.data == "owner:add_table")
async def owner_add_table(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите количество мест за столиком:")
    await state.set_state(OwnerStates.waiting_for_table_capacity)
 
@router.message(OwnerStates.waiting_for_table_capacity)
async def process_table_capacity(message: Message, state: FSMContext):
    try:
        capacity = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число для количества мест.")
        return
    await state.update_data(table_capacity=capacity)
    await message.answer("Отправьте фото столика или введите 'пропустить', если фото не нужно:")
    await state.set_state(OwnerStates.waiting_for_table_photo)
 
@router.message(OwnerStates.waiting_for_table_photo)
async def process_table_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    capacity = data.get("table_capacity")
    photo_bytes = None
    if message.photo:
        # Выбираем самое большое фото
        file_id = message.photo[-1].file_id
        file = await message.bot.get_file(file_id)
        photo_stream = await message.bot.download_file(file.file_path)
        photo_bytes = photo_stream.getvalue()
    elif message.text and message.text.lower() == "пропустить":
        photo_bytes = None
    else:
        await message.answer("Отправьте фото или напишите 'пропустить'.")
        return
 
    # Получаем ресторан, добавленный владельцем (предполагается, что у владельца один ресторан)
    restaurant = RestaurantModelWorker().get_restaurant_by_owner(message.from_user.id)
    if restaurant:
        TableModelWorker().add_table(
            restaurant_id=restaurant['id'],
            capacity=capacity,
            photo=photo_bytes
        )
        await message.answer(f"Столик на {capacity} мест успешно добавлен!")
    else:
        await message.answer("Сначала добавьте ресторан!")
    await state.clear()
 
# ==========================
# Клиентский сценарий: Выбор локации
# ==========================
@router.callback_query(F.data.startswith("location:"))
async def location_selected(callback: CallbackQuery):
    location_id = int(callback.data.split(":")[1])
    restaurants = RestaurantModelWorker().get_restaurants_by_location(location_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=rest['name'], callback_data=f"restaurant:{rest['id']}:{location_id}")]
            for rest in restaurants
        ] + [[InlineKeyboardButton(text="Назад", callback_data="back:locations")]]
    )
    await callback.message.edit_text("Выберите ресторан:", reply_markup=keyboard)
 
# ==========================
# Клиентский сценарий: Выбор ресторана и столиков
# ==========================
@router.callback_query(F.data.startswith("restaurant:"))
async def restaurant_selected(callback: CallbackQuery):
    data = callback.data.split(":")
    restaurant_id = int(data[1])
    location_id = int(data[2])
    restaurant = RestaurantModelWorker().get_restaurant_by_id(restaurant_id)
    tables = TableModelWorker().get_tables_by_restaurant(restaurant_id)
    photos = MinioClient().get_tables_by_rest(str(restaurant.id), tables)
 
    if photos and len(photos) >= len(tables):
        # Удаляем сообщение с выбором ресторана
        await callback.message.delete()
        # Отправляем для каждого столика фото с кнопкой выбора
        for idx, table in enumerate(tables):
            photo = photos[idx]
            photo.seek(0)
            if len(photo.getvalue()) > 10 * 1024 * 1024:
                await callback.message.answer(f"Изображение столика слишком большое")
                continue

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"Выбрать столик на {table['capacity']} чел.",
                    callback_data=f"table:{table['id']}:{restaurant_id}"
                )]
            ])
            # try:
            #     from PIL import Image
            #     Image.open(io.BytesIO(photo))  # Проверка, что это валидное изображение
            # except Exception as e:
            #     await callback.message.answer("Ошибка: неверный формат изображения")
            #     return
            from aiogram.types.input_file import BufferedInputFile
            photo_file = BufferedInputFile(
                file=photo.read(),  # Читаем данные из BytesIO
                filename=f"table_{table['id']}.jpg"  # Указываем правильное расширение
            )
            await callback.message.answer_photo(
                photo=photo_file,
                caption=f"Столик на {table['capacity']} чел.",
                reply_markup=keyboard
            )
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data=f"back:restaurants:{location_id}")]
        ])
        await callback.message.answer("Для выбора другого ресторана нажмите 'Назад'.", reply_markup=back_keyboard)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"Столик на {table['capacity']} чел.",
                    callback_data=f"table:{table['id']}:{restaurant_id}"
                )] for table in tables
            ] + [[InlineKeyboardButton(text="Назад", callback_data=f"back:restaurants:{location_id}")]]
        )
        await callback.message.edit_text("Выберите столик:", reply_markup=keyboard)
 
# ==========================
# Клиентский сценарий: Возврат к выбору локации/ресторана
# ==========================
@router.callback_query(F.data.startswith("back:locations"))
async def back_to_locations(callback: CallbackQuery):
    locations = LocationModelWorker().get_all()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=loc['name'], callback_data=f"location:{loc['id']}")]
            for loc in locations
        ]
    )
    await callback.message.edit_text("Выберите вашу локацию:", reply_markup=keyboard)
 
@router.callback_query(F.data.startswith("back:restaurants:"))
async def back_to_restaurants(callback: CallbackQuery):
    location_id = int(callback.data.split(":")[2])
    restaurants = RestaurantModelWorker().get_restaurants_by_location(location_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=rest['name'], callback_data=f"restaurant:{rest['id']}:{location_id}")]
            for rest in restaurants
        ] + [[InlineKeyboardButton(text="Назад", callback_data="back:locations")]]
    )
    await callback.message.edit_text("Выберите ресторан:", reply_markup=keyboard)
 
# ==========================
# Клиентский сценарий: Бронирование столика
# ==========================
@router.callback_query(F.data.startswith("table:"))
async def table_selected(callback: CallbackQuery):
    data = callback.data.split(":")
    table_id = int(data[1])
    restaurant_id = int(data[2])
    # Здесь можно обновить статус столика в базе (бронирование)
    restaurant = RestaurantModelWorker().get_restaurant_by_id(restaurant_id)
    owner_chat_id = restaurant.owner_id # owner_chat_id должен сохраняться при добавлении ресторана
    TableModelWorker().reserve_table(table_id)

    if owner_chat_id:
        await callback.bot.send_message(
            owner_chat_id,
            f"Клиент забронировал столик {table_id} в ресторане '{restaurant.name}'."
        )
    await callback.message.answer(f"Вы выбрали столик с ID {table_id}. В скором времени он будет забронирован.")