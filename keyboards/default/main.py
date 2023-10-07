from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
contact = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📞 Share Contact",request_contact=True)
        ],
    ]
)

menu = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📝 Buyurtma berish"),
            KeyboardButton(text="🧮 Berilgan limit")
        ],
        [
            KeyboardButton(text="🗳 Qoldiq hisob"),
            KeyboardButton(text="📋 Buyurtmalar")
        ],
    ]
)