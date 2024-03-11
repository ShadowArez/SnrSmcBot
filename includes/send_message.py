from datetime import date,timedelta
from includes.modules import types, FSMContext,json,requests,BeautifulSoup,State,StatesGroup
from includes.keyboards import Keyboards
from includes.sqlite import Database
from includes.states import ButtonStates
import random
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)

def write_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

class send_message:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle(self):
        button_data_list = []
        @self.dp.message_handler(lambda m:m.text == "ناردنی نامە 💌")
        async def send_message_cmd(message : types.Message):
            await ButtonStates.entering_message.set()
            await message.answer("تكایە ئەو نامەیە بنووسە كە دەتەوێت بینێریت :",reply_markup=keb.back_confirm())
        @self.dp.callback_query_handler(lambda c: c.data == 'add_photo', state='*')
        async def add_photo(callback_query: types.CallbackQuery, state: FSMContext):
            await ButtonStates.entering_photo.set()
            await callback_query.message.answer("زۆر باشە ، تكایە وێنە بنێرە :")
        @self.dp.message_handler(state=ButtonStates.entering_message)
        async def process_message(message: types.Message, state: FSMContext):
            if message.text == "پاشگەزبوونەوە":
                await message.answer("سەرەتا",reply_markup=keb.get_owner_keyboards(message.from_user.id))
                await state.finish()
            async with state.proxy() as data:
                data['message'] = message.text
            await ButtonStates.next()
            # Sending message with inline buttons
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="photos"),
                        types.InlineKeyboardButton(text="دووگمەكان", callback_data="buttons"),
                        types.InlineKeyboardButton(text="دووپاتكردنەوە", callback_data="confirm"),
                        types.InlineKeyboardButton(text="ڕەتكردنەوە", callback_data="decline"))
            await message.answer("تكایە یەكێك لە هەڵبژاردنەكان دیاری بكە :", reply_markup=keyboard)
        @self.dp.message_handler(content_types=['photo'], state=ButtonStates.entering_photo)
        async def process_photo(message: types.Message, state: FSMContext):
            photo_id = message.photo[-1].file_id
            async with state.proxy() as data:
                if 'photos_data' not in data:
                    data['photos_data'] = []
                data['photos_data'].append(photo_id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="photos"),
                        types.InlineKeyboardButton(text="دووگمەكان", callback_data="buttons"),
                        types.InlineKeyboardButton(text="دووپاتكردنەوە", callback_data="confirm"),
                        types.InlineKeyboardButton(text="ڕەتكردنەوە", callback_data="decline"))
            await self.bot.send_photo(chat_id=message.chat.id, photo=photo_id, caption=data.get('message', ""), reply_markup=keyboard)
        @self.dp.callback_query_handler(lambda c: c.data in ['photos', 'buttons', 'confirm', 'decline', 'back', 'add_button','confirm_yes','confirm_no'], state='*')
        async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
            await self.bot.answer_callback_query(callback_query.id)
            choice = callback_query.data
            async with state.proxy() as data:
                if choice == "back":
                    async with state.proxy() as data:
                        message_text = data.get('message', "Enter your message.")
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="photos"),
                        types.InlineKeyboardButton(text="دووگمەكان", callback_data="buttons"),
                        types.InlineKeyboardButton(text="دووپاتكردنەوە", callback_data="confirm"),
                        types.InlineKeyboardButton(text="ڕەتكردنەوە", callback_data="decline"))
                        if 'photos_data' in data and data['photos_data']:
                            image_id = data['photos_data'][0]
                            await self.bot.send_photo(chat_id=callback_query.message.chat.id, photo=image_id, caption=data.get('message', ""), reply_markup=keyboard)
                        else:
                            await callback_query.message.edit_text(message_text, reply_markup=keyboard)
                elif choice == "buttons":
                    inline_buttons = []
                    if 'buttons_data' in data and len(data['buttons_data']) > 0:
                        for button in data['buttons_data']:
                            inline_buttons.append(types.InlineKeyboardButton(text=button['label'], callback_data=f"button_{button['label']}"))
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    if inline_buttons:
                        keyboard.add(*inline_buttons)
                    keyboard.add(types.InlineKeyboardButton(text="زیادكردنی دووگمە", callback_data="add_button"),
                                types.InlineKeyboardButton(text="گەڕانەوە بۆ بەشەكان", callback_data="back"))
                    if callback_query.message.text:
                        await callback_query.message.edit_text("هەڵبژاردن دیاری بكە :", reply_markup=keyboard)
                    else:
                        await callback_query.message.answer("هەڵبژاردن دیاری بكە :", reply_markup=keyboard)
                elif choice == "add_button":
                    await ButtonStates.entering_button_title.set()
                    await callback_query.message.answer("ناوی دووگمە بنووسە:")
                elif choice == "decline":
                    await callback_query.message.answer("ڕەتكردنەوە دووپاتكرایەوە",reply_markup=keb.get_owner_keyboards(callback_query.message.from_user.id))
                    await state.finish()
                elif choice == "confirm":
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text="دووپاتكردنەوە", callback_data="confirm_yes"),
                                types.InlineKeyboardButton(text="ڕەتكردنەوە", callback_data="decline"))
                    await callback_query.message.answer("ئایا دڵنایی لە ناردنی ئەم نامەیە?", reply_markup=keyboard)
                elif choice == "confirm_yes":
                    button_key = "post_message"
                    users = db.userdata()
                    inline_aa = []
                    if 'buttons_data' in data and len(data['buttons_data']) > 0:
                        for button in data['buttons_data']:
                            db.add_inline_det_msg(button)
                    for user in users:
                        inline_buttons = []
                        if 'buttons_data' in data and len(data['buttons_data']) > 0:
                            for button in data['buttons_data']:
                                if button['type'] == 'url':
                                    msg_ee = button['msg_u']
                                    if "https://" not in msg_ee:
                                        msg_ee = "https://t.me/" + msg_ee
                                    inline_buttons.append(types.InlineKeyboardButton(text=button['label'], url=msg_ee))
                                else:
                                    inline_buttons.append(types.InlineKeyboardButton(text=button['label'], callback_data=f"buttongetpost_{button['hash_button']}"))
                        keyboard = types.InlineKeyboardMarkup(row_width=1)
                        if inline_buttons:
                            keyboard.add(*inline_buttons)
                        if 'photos_data' in data and data['photos_data']:
                            image_id = data['photos_data'][0]
                            if inline_buttons:
                                await self.bot.send_photo(chat_id=user[3], photo=image_id, caption=data.get('message', ""), reply_markup=keyboard)
                            else:
                                await self.bot.send_photo(chat_id=user[3], photo=image_id, caption=data.get('message', ""))
                        elif inline_buttons:
                            await self.bot.send_message(chat_id=user[3], text=data.get('message', ""),reply_markup=keyboard)
                        else:
                            await self.bot.send_message(chat_id=user[3], text=data.get('message', ""))
                    await state.finish()
                elif choice == "photos":
                    if 'photos_data' in data and len(data['photos_data']) > 0:
                        media_group = types.MediaGroup()
                        for photo in data['photos_data']:
                            media_group.attach_photo(photo)
                        await callback_query.message.answer_media_group(media=media_group)
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="add_photo"),
                                    types.InlineKeyboardButton(text="گەڕانەوە بۆ بەشەكان", callback_data="back"))
                        await callback_query.message.answer("هەڵبژاردن دیاری بكە :", reply_markup=keyboard)
                    else:
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(types.InlineKeyboardButton(text="زیادكردنی وێنە", callback_data="add_photo"),
                                    types.InlineKeyboardButton(text="گەڕانەوە بۆ بەشەكان", callback_data="back"))
                        await callback_query.message.answer("هیچ وێنەیەك نیە ، تكایە هەڵبژاردن دیاری بكە :", reply_markup=keyboard)
        @self.dp.message_handler(state=ButtonStates.entering_button_title)
        async def process_button_title(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['button_title'] = message.text
            await ButtonStates.choosing_button_type.set()
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="URL", callback_data="url"),
                        types.InlineKeyboardButton(text="نامە", callback_data="message"),
                        types.InlineKeyboardButton(text="ئاگاداری", callback_data="alert"),
                        types.InlineKeyboardButton(text="پاشگەزبوونەوە", callback_data="back"))
            await message.answer("جۆری دووگمە دیاری بكە :", reply_markup=keyboard)
        @self.dp.callback_query_handler(lambda c: c.data in ['url', 'message', 'alert', 'back'], state=ButtonStates.choosing_button_type)
        async def process_button_type(callback_query: types.CallbackQuery, state: FSMContext):
            await self.bot.answer_callback_query(callback_query.id)
            choice = callback_query.data
            if choice == "back":
                await callback_query.message.answer("ڕەتكردنەوە دووپاتكرایەوە",reply_markup=keb.get_owner_keyboards(callback_query.message.from_user.id))
                await state.finish()
            else:
                if choice == "url":
                    await callback_query.message.answer("تكایە لینك بنووسە :")
                else:
                    await callback_query.message.answer("تكایە دەق بنووسە :")
                async with state.proxy() as data:
                    data['button_choise'] = choice
                await ButtonStates.entering_msg_of_button.set()
        @self.dp.message_handler(state=ButtonStates.entering_msg_of_button)
        async def process_button_type(message: types.Message, state: FSMContext):
            message_text = message.text
            async with state.proxy() as data:
                if 'buttons_data' not in data:
                    data['buttons_data'] = []
                if data['button_choise'] == "url":
                    data['buttons_data'].append({"type": "url", "label": data['button_title'], "msg_u": message_text})
                if data['button_choise'] == "message":
                    hash_button_r = random.randint(10000000, 90000000)
                    data['buttons_data'].append({"type": "message", "label": data['button_title'],"hash_button": hash_button_r ,"msg_u": message_text})
                if data['button_choise'] == "alert":
                    hash_button_r = random.randint(10000000, 90000000)
                    data['buttons_data'].append({"type": "alert", "label": data['button_title'], "hash_button": hash_button_r,"msg_u": message_text})
            keyboard = types.InlineKeyboardMarkup()
            for button in data['buttons_data']:
                if button['type'] == "url":
                    keyboard.add(types.InlineKeyboardButton(text=button['label'],callback_data="button_aaaa"))
                elif button['type'] == "message":
                    keyboard.add(types.InlineKeyboardButton(text=button['label'],callback_data="button_aaaa"))
                elif button['type'] == "alert":
                    keyboard.add(types.InlineKeyboardButton(text=button['label'],callback_data="button_aaaa"))
            keyboard.add(types.InlineKeyboardButton(text="گەڕانەوە", callback_data="back"))
            keyboard.add(types.InlineKeyboardButton(text="زیادكردنی دووگمەی نوێ", callback_data="add_button"))
            await message.answer("دووگمەكە زیادكرا:", reply_markup=keyboard)
        @self.dp.callback_query_handler(lambda c:c.data.startswith("buttongetpost_"))
        async def answer_message_post(call : types.CallbackQuery):
            title = call.data.split("_")[1]
            detail = db.get_det_inine_msg(title)
            if detail[4] != "alert":
                await call.message.answer(detail[2])
            else:
                await call.answer(detail[2], show_alert=True)