import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.main import contact,menu
from aiogram.dispatcher import FSMContext
from api import post_user, order_product, limit_item, get_garden
from keyboards.inline.buyurtma import tugma, tasdiqlash
from loader import dp, db, bot
from states.holatlar import Register,Maxsulot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.utils.callback_data import CallbackData
from data.config import ADMINS


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f" Assalomu alaykum, {message.from_user.full_name}!\n "
                         f"Iltimos Telefon raqamingizni yuboring !",reply_markup=contact)
    await Register.contact.set()

@dp.message_handler(state=Register.contact,content_types=types.ContentType.CONTACT,is_sender_contact=True)
async def check_user(message:types.Message, state:FSMContext):
    phone = message.contact['phone_number']
    user_id = message.from_user.id
    name = message.from_user.full_name
    user = post_user(phone_number=phone,user_id=user_id)
    if 'detail' in user:
        await message.answer("❌ Kechirasiz siz ro'yhatdan o'tmagansiz!")
    else:
        await message.answer(f"🏠 Bog'cha  - {user['name']}\n"
                             f"🤵‍♂️ Ism Familiya - {user['person']}\n"
                             f"📞 Telefon raqami - {user['phone_number']}",reply_markup=menu)

    await state.finish()

action_cb = CallbackData("action", "value")
@dp.message_handler(text="📝 Buyurtma berish")
async def show_product(message: types.Message):
    telegram_id = message.from_user.id
    products = order_product(telegram_id=telegram_id)
    if products['items']:
        button = InlineKeyboardMarkup()
        for i, j in enumerate(products['items']):
            check = db.check(user_id=telegram_id, id=j['product']['id'])
            if i % 2 == 0:
                if check:
                    button.row(InlineKeyboardButton(text=f"{j['product']['name']}-{check[0][4]} {check[0][-1]}", callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
                else:
                    button.row(InlineKeyboardButton(text=f"{j['product']['name']}",callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
            else:
                if check:
                    button.insert(InlineKeyboardButton(text=f"{j['product']['name']}-{check[0][4]} {check[0][-1]}", callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
                else:
                    button.insert(InlineKeyboardButton(text=f"{j['product']['name']}", callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
        await message.answer("Kerakli tugmani tanlang : ", reply_markup=button)

    else:
        await message.answer(text="❌ Kechirasiz, sizda hali limit bergilanmagan.")

@dp.callback_query_handler(action_cb.filter())
async def action_callback_handler(callback_query: CallbackQuery, callback_data: dict,state: FSMContext):
    value = callback_data["value"]
    if value.startswith("product"):
        await callback_query.answer(cache_time=60)
        await callback_query.message.answer("Maxsulot miqdorini kirting : ")
        id = value.split('-')[1]
        name = value.split('-')[-1]
        turi = value.split('-')[2]
        await state.set_data({
            'id':id,
            "name":name,
            'turi':turi

        })
        await Maxsulot.miqdori.set()

@dp.message_handler(state=Maxsulot.miqdori)
async def get_miqdor(message:types.Message,state: FSMContext):
    miqdori = message.text
    umumiy_maxsulot = await state.get_data()
    id = umumiy_maxsulot['id']
    user_id = message.from_user.id
    name = umumiy_maxsulot['name']
    turi = umumiy_maxsulot['turi']
    check = db.check(user_id, id)
    if check:
        db.update_product(miqdori, user_id, id)
    else:
        db.add_product(id, user_id, name, miqdori, turi)

    check_user=db.select_product_by_user(user_id)
    natija_product = "✍️ Siz tanlagan maxsulotlar: \n"
    for i,j in enumerate(check_user):
        natija_product += f"{i+1}. {j[3]} - {j[4]}  {j[-1]}\n"
    await message.answer(natija_product,reply_markup=tugma)
    await state.finish()

@dp.callback_query_handler(text="maxsulot_qoshish")
async def add_maxsulot(call:CallbackQuery,state: FSMContext):
    await call.answer(cache_time=60)
    telegram_id = call.from_user.id

    products = order_product(telegram_id=telegram_id)
    if products['items']:
        button = InlineKeyboardMarkup()
        for i, j in enumerate(products['items']):
            check = db.check(user_id=telegram_id, id=j['product']['id'])
            if i % 2 == 0:
                if check:
                    button.row(InlineKeyboardButton(text=f"{j['product']['name']}-{check[0][4]} {check[0][-1]}",callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
                else:
                    button.row(InlineKeyboardButton(text=f"{j['product']['name']}", callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
            else:
                if check:
                    button.insert(InlineKeyboardButton(text=f"{j['product']['name']}-{check[0][4]} {check[0][-1]}",callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
                else:
                    button.insert(InlineKeyboardButton(text=f"{j['product']['name']}", callback_data=action_cb.new(value=f"product-{j['product']['id']}-{j['product']['measure']}-{j['product']['name']}")))
        await call.message.answer("Kerakli tugmani tanlang : ", reply_markup=button)



@dp.callback_query_handler(text_contains="bekor_qilish")
async def cancel(call:CallbackQuery):
    await call.answer(cache_time=60)
    telegram_id = call.from_user.id
    db.delete_products_by_user(str(telegram_id))
    await call.message.answer("Maxsulotlar bekor qilindi",reply_markup=menu)

@dp.callback_query_handler(text="Tasdiqlash")
async def check(call:CallbackQuery):
    await call.answer(cache_time=60)
    telegram_id = call.from_user.id
    product = db.select_product_by_user(telegram_id)
    # items = [{'product_id': i[1],"quantity":i[4]} for i in product]
    # print(items)
    user = get_garden(telegram_id=telegram_id)
    # print(user)
    text = f"Sizga {user['name']} bog'chasidan buyurtmalar bor\n"
    check_user = db.select_product_by_user(telegram_id)
    for i, j in enumerate(check_user):
        text += f"{i + 1}. {j[3]} - {j[4]}  {j[-1]}\n"
    await call.message.answer("Sizning buyurtmalaringiz Ta'minotchiga yuborildi!",reply_markup=menu)
    await bot.send_message(chat_id=ADMINS[1],text=text ,reply_markup=tasdiqlash)



@dp.message_handler(text="🧮 Berilgan limit")
async def limit(message:types.Message):
    telegram_id = message.from_user.id
    b_limit = limit_item(telegram_id=telegram_id)
    berilgan_limit = f"{b_limit['monthly']['year']}-yil {b_limit['monthly']['month']} oyi uchun sizga quyidagi limit belgilangan :\n\n"
    if b_limit['items']:
        for i, j in enumerate(b_limit['items']):
            if (str(j['limit_quantity']))[-2:] == ".0":
                berilgan_limit += f"{i+1}. {j['product']['name']} - {(str(j['limit_quantity']))[:-2]} {j['product']['measure']}\n"
            else:
                berilgan_limit += f"{i + 1}. {j['product']['name']} - {j['limit_quantity']} {j['product']['measure']}\n"
        await message.answer(berilgan_limit,reply_markup=menu)
    else:
        await message.answer("❌ Kechirasiz sizda bu oy uchun limit bergilanmagan!")


@dp.message_handler(text="🗳 Qoldiq hisob")
async def qoldiq_limit(message:types.Message):
    telegram_id = message.from_user.id
    q_limit = limit_item(telegram_id=telegram_id)
    qolgan_limit = f"{q_limit['monthly']['year']}-yil {q_limit['monthly']['month']} oyi uchun sizga quyidagi  qoldiq :\n\n"
    if q_limit['items']:
        for i, j in enumerate(q_limit['items']):
            if (str(j['limit_quantity']))[-2:] == ".0":
                qolgan_limit += f"{i+1}. {j['product']['name']} - {(str(j['remaining_quantity']))[:-2]} {j['product']['measure']}\n"
            else:
                qolgan_limit += f"{i + 1}. {j['product']['name']} - {j['remaining_quantity']} {j['product']['measure']}\n"
        await message.answer(qolgan_limit,reply_markup=menu)
    else:
        await message.answer("❌ Kechirasiz sizda bu oy uchun qoldiq mavjud emas!")