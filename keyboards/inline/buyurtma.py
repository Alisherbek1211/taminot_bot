from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

tugma = InlineKeyboardMarkup()
tugma.row(InlineKeyboardButton(text="➕ Boshqa maxsulot qo'shish",callback_data="maxsulot_qoshish"))
tugma.row(InlineKeyboardButton(text="✅ Tasdiqlash",callback_data="Tasdiqlash"))
tugma.insert(InlineKeyboardButton(text="❌ Bekor qilish",callback_data="bekor_qilish"))


tasdiqlash = InlineKeyboardMarkup()
tasdiqlash.row(InlineKeyboardButton(text="✅ Tasdiqlash",callback_data="Tasdiqlash_admin"))
tasdiqlash.insert(InlineKeyboardButton(text="❌ Bekor qilish",callback_data="bekor_qilish_admin"))

