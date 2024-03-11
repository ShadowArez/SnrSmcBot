from includes.modules import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from includes.sqlite import Database
import json
db = Database("your_database.db")
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)

class Keyboards:
    @staticmethod
    def get_owner_keyboards(user_id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        if db.get_admins(user_id2=user_id,Role2="owner"):
            keyboard.add("ناردنی نامە 💌")
            keyboard.add("نرخی پارەدان 🏦", "جۆری پارەدان 💳")
            keyboard.add("كۆدی داشكان 🔑")
            keyboard.add("ئەدمینەکان 🛡️","داتاكان 📋")
        else:
            keyboard.add("ناردنی نامە 💌")
            keyboard.add("نرخی پارەدان 🏦", "جۆری پارەدان 💳")
            keyboard.add("كۆدی داشكان 🔑")
        return keyboard
    @staticmethod
    def get_user_keyboards():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("فۆڕێكس 💱")
        keyboard.add("گرووپی سیگناڵ 📡")
        keyboard.add("درووستكردنی هەژماری فۆڕێكس 📊")
        keyboard.add("دەربارە ℹ️")
        return keyboard
    @staticmethod
    def get_affiliate():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("دەستپێكردن")
        keyboard.add("زانیاری پشتگیری")
        keyboard.add("ماركێت")
        return keyboard
    @staticmethod
    def get_start_button():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("بەڵێ")
        keyboard.add("نەخێر")
        return keyboard
    @staticmethod
    def get_affiliate_and_back():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("بەڵی")
        keyboard.add("گەڕانەوە")
        return keyboard
    @staticmethod
    def back_confirm():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("پاشگەزبوونەوە")
        return keyboard
    @staticmethod
    def get_sigal_group():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("پارەدان")
        keyboard.add("بڕۆكەر")
        keyboard.add("گەڕانەوە")
        return keyboard
    @staticmethod
    def get_signal_broker():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keyboard.add("Multi Bank")
        keyboard.add("INGOT")
        keyboard.add("گەڕانەوە")
        return keyboard
    @staticmethod
    def get_broker_account():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keyboard.add("بەڵێ").add("درووستكردنی هەژمار")
        keyboard.add("گەڕانەوە")
        return keyboard
    @staticmethod
    def get_confirm_account_creation():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keyboard.add("بەڵێ").add("نەخێر")
        return keyboard
    @staticmethod
    def get_brokers_name():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keyboard.add("Multi Bank")
        keyboard.add("Ingot")
        return keyboard
    @staticmethod
    def get_confirm_of_create_account():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keyboard.add("بەڵێ").add("نەخێر")
        return keyboard
    @staticmethod
    def get_confrim_delete_dis(button,he=None,ne=None):
        keyboard = InlineKeyboardMarkup()
        if he:
            keyboard.add(InlineKeyboardButton(text="بەڵێ",callback_data=f"yesy_delete__{button}"))
        elif he:
            keyboard.add(InlineKeyboardButton(text="بەڵێ",callback_data=f"yesy_deletes__{button}"))
        else:
            keyboard.add(InlineKeyboardButton(text="بەڵێ",callback_data=f"yesy_deletess__{button}"))

        return keyboard
    @staticmethod
    def back():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keyboard.add("گەڕانەوە")
        return keyboard
    @staticmethod
    def send_message_to_admins_confirm_account_creation(user_id,type,username):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("قبوڵ كردن",callback_data=f"accept_{user_id}__{type}"))
        keyboard.add(InlineKeyboardButton("ڕەتكردنەوە",callback_data=f"reject_{user_id}__{type}"))
        keyboard.add(InlineKeyboardButton("قسەكردن",url=f"https://t.me/{username}"))
        return keyboard
    @staticmethod
    def get_payment_method_buttons():
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        for button in db.get_payment_methods():
            keyboard.add(InlineKeyboardButton(text=button[1],callback_data=f"deletebuttons_{button[1]}"))
        keyboard.add(InlineKeyboardButton(text="زیادكردن",callback_data="add_pay_buttonk"))
        return keyboard
    @staticmethod
    def add_payment_method(photo=None):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        if photo:
            keyboard.add("دووپاتكردنەوە")
        else:
            keyboard.add("دووپاتكردنەوە").add("زیادكردنی وێنە")
        keyboard.add("گەڕانەوە")
        return keyboard
    @staticmethod
    def get_payment_method(back=None):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for payment in db.get_payment_methods():
            keyboard.add(payment[1])
        if back:
            keyboard.add("گەڕانەوە")
        return keyboard

    @staticmethod
    def discount_code():
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text="وێنە",callback_data=f"photos_discount"))
        keyboard.add(InlineKeyboardButton(text="دووگمەكان",callback_data=f"buttons_discount"))
        keyboard.add(InlineKeyboardButton(text="دووپاتكردنەوە",callback_data=f"confirm_discount"))
        keyboard.add(InlineKeyboardButton(text="ڕەتكردنەوە",callback_data=f"decline_descount"))
        return keyboard
    @staticmethod
    def photos_discount():
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text="زیادكردنی وێنە",callback_data=f"add_photo_discount"))
        keyboard.add(InlineKeyboardButton(text="گەڕانەوە",callback_data=f"back_discount"))
        return keyboard
    @staticmethod
    def buttons_discount(inline):
        keyboard = InlineKeyboardMarkup()
        if inline:
            keyboard.add(InlineKeyboardButton("ڕەشكردنەوەی دووگمە", callback_data='remove_photo_discount'))
            keyboard.add(InlineKeyboardButton("زیادكردنی دووگمە", callback_data='add_inline_discount'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='back_discount'))
        else:
            keyboard.add(InlineKeyboardButton("زیادكردنی دووگمە", callback_data='add_inline_discount'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='back_discount'))
    @staticmethod
    def buttons_discount_delete(button):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("ڕەشكردنەوە", callback_data=f'delete_dis_code__{button}'))
        return keyboard

    @staticmethod
    def get_pay_price_date():
        with open('config.json', 'r', encoding='utf8') as config:
            config = json.load(config)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        if "type_of_payment" in config:
                for payment in config["type_of_payment"]:
                    if "payment" in payment:
                        keyboard.add(f"بۆ ماوەی {payment['payment']['days']} ڕۆژ : {payment['payment']['price']} دۆلار💵")
        return keyboard
    @staticmethod
    def get_admins():
        keyboard = InlineKeyboardMarkup()
        admins = db.get_admins(role="admin")
        for admin in admins:
            keyboard.add(InlineKeyboardButton(text="ئەدمین",url=f"https://t.me/@{admin[2]}"))
        return keyboard
    @staticmethod
    def get_expired_buttons(hash_id):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text="دووبارە بەشداریكردنەوە",callback_data=f"again_pay__{hash_id}"))
        keyboard.add(InlineKeyboardButton(text="دەرچوون",callback_data=f"cancel_again_pay__{hash_id}"))
        return keyboard
    @staticmethod
    def get_channels():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        channels = db.get_channels()
        keyboard.add('زیادكردنی كەناڵ', 'گەڕانەوە')
        if channels:
            for channel in channels:
                keyboard.add(channel[1])
        return keyboard
    @staticmethod
    def get_challnges_button():
        inline = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = db.get_challenges()
        inline.add("گەڕانەوە")
        row = []

        for button in buttons:
            for word in button[1].split(','):
                word = word.strip()
                row.append(button[1])
                if len(row) == 2:
                    inline.add(*row)
                    row = []
        if row:
            inline.add(*row)
        return inline
    @staticmethod
    def get_discount_code_button(admin=None):
        inline = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = db.get_discount_codes()
        inline.add("گەڕانەوە")
        row = []
        for button in buttons:
            row.append(button[1])
            if len(row) == 3:
                inline.add(*row)
                row = []
        if row:
            inline.add(*row)
        if admin:
            inline.add("زيادكردنی كۆدی داشكان")
        return inline
    @staticmethod
    def get_inline_of_challenges(msg):
        inline = InlineKeyboardMarkup()
        buttons = db.get_challenges(title=msg)
        for word in buttons[3].split(','):
            word = word.strip()
            inline.add(InlineKeyboardButton(text=word,callback_data=f"buttons_challenge__{msg}___{word}"))
        return inline

    @staticmethod
    def get_faq_buttons():
        buttons = db.get_faqs()

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        row = []
        keyboard.add("گەڕانەوە")
        for button in buttons:
            row.append(button[1])
            if len(row) == 2:
                keyboard.add(*row)
                row = []
        if row:
            keyboard.add(*row)
        return keyboard
    @staticmethod
    def get_inline_buttons(id):
        keyboard = InlineKeyboardMarkup()
        detail = db.get_faqs(id=True)
        for i in detail:
            select_column = i[4]
            if int(select_column) == int(id):
                keyboard.add(InlineKeyboardButton(text=str(i[1]),callback_data=f"buttonfaq_{i[0]}"))
        return keyboard
    @staticmethod
    def get_answer_faq_buttons(title):
        buttons = db.get_faqs(msg=title)
        data_list = [item.strip() for item in buttons[3].split(',')]
        inline_keyboard = InlineKeyboardMarkup()
        for data in data_list:
            callback_data = f'buttonfaq_{buttons[0]}'
            button = InlineKeyboardButton(text=data, callback_data=callback_data)
            inline_keyboard.add(button)
        return inline_keyboard
    @staticmethod
    def welcome_message_admin():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("گۆڕینی نامە", callback_data='change_message'))
        # keyboard.add(InlineKeyboardButton("وێنە", callback_data='photo_cmd'))
        # keyboard.add(InlineKeyboardButton("دووگمە", callback_data='inline_button'))
        return keyboard
    @staticmethod
    def inline_welcome_msg(inline=None):
        keyboard = InlineKeyboardMarkup()
        if inline:
            keyboard.add(InlineKeyboardButton("ڕەشكردنەوەی دووگمە", callback_data='remove_photo_wlc'))
            keyboard.add(InlineKeyboardButton("زیادكردنی دووگمە", callback_data='add_inline_wlc'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='photo_cmd'))
        else:
            keyboard.add(InlineKeyboardButton("زیادكردنی دووگمە", callback_data='add_inline_wlc'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='photo_cmd'))
        return keyboard
    @staticmethod
    def photo_welcome_msg(photo=None):
        keyboard = InlineKeyboardMarkup()
        if photo:
            keyboard.add(InlineKeyboardButton("ڕەشكردنەوەی وێنە", callback_data='remove_photo_wlc'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='photo_cmd'))
        else:
            keyboard.add(InlineKeyboardButton("زیادكردنی وێنە", callback_data='add_photo_wlc'))
            keyboard.add(InlineKeyboardButton("ڕەشكردنەوەی وێنە", callback_data='remove_photo_wlc'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='photo_cmd'))
        return keyboard
    @staticmethod
    def get_analaytics_buttons():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("بەشداربوانی گرووپی تایبەت")
        keyboard.add("بەشداربووانی بۆت")
        keyboard.add("نامەی بەخێرهاتن")
        keyboard.add("ئەدمینەكان")
        keyboard.add("نرخی گرووپی سیگناڵ")
        keyboard.add("گەڕانەوە")
        return keyboard
    @staticmethod
    def send_message_cm_admin():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("گۆڕینی نامە", callback_data='change_send_message'))
        keyboard.add(InlineKeyboardButton("وێنە", callback_data='2s1s'))
        keyboard.add(InlineKeyboardButton("دووگمەكان", callback_data="hello_boss"))
        return keyboard
    @staticmethod
    async def inline_send_message_msg(data,message):
        keyboard = InlineKeyboardMarkup()
        if data is None:
            keyboard.add(InlineKeyboardButton("زیادكردنی دووگمە", callback_data='add_inline_snd_msg'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='back_to_smca'))
            await message.answer("هیچ دووگمەیەك نیە بۆ زیادكردنی گرتە بكە لە زیادكردنی دووگمە :")
        else:
            for dat in data:
                keyboard.add(InlineKeyboardButton(f"{dat.split(' - ')[0]}", callback_data=f"wlc_msg_c__{dat.split(' - ')[0]}"))
            keyboard.add(InlineKeyboardButton("زیادكردنی دووگمە", callback_data='add_inline_snd_msg'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='back_to_smca'))
            await message.answer("ddd",reply_markup=keyboard)
    @staticmethod
    def photo_send_message_msg(photo=None):
        keyboard = InlineKeyboardMarkup()
        if photo:
            keyboard.add(InlineKeyboardButton("ڕەشكردنەوەی وێنە", callback_data='remove_photo_snd_msg'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='photo_cmd'))
        else:
            keyboard.add(InlineKeyboardButton("زیادكردنی وێنە", callback_data='add_photo_snd_msg'))
            keyboard.add(InlineKeyboardButton("ڕەشكردنەوەی وێنە", callback_data='remove_photo_snd_msg'))
            keyboard.add(InlineKeyboardButton("گەڕانەوە", callback_data='photo_cmd'))
        return keyboard
class Analytics_Keyboard:
    @staticmethod
    def vip_signal_member():
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("سەرجەم بەشداربووەكان")
        keyboard.add("سەرجەم بەردامبووەكان")
        keyboard.add("سەرجەم بەسەرچووەكان")
        keyboard.add("سەرجەم چاوەڕوانی پارەدان")
        keyboard.add("گەڕانەوە بۆ داتاكان")
        return keyboard
    @staticmethod
    def vip_signals_price(payment = None):
        inline = InlineKeyboardMarkup()
        if payment:
            title = payment
            for pay in payment:
                inline.add(InlineKeyboardButton(text=pay,callback_data=f"pay_vip_signal__{pay}"))
                inline.add(InlineKeyboardButton(text="زیادكردنی نرخ",callback_data="add_payment_price"))
        else:
            inline.add(InlineKeyboardButton(text="زیادكردنی نرخ",callback_data="add_payment_price"))
        return inline
    @staticmethod
    def get_admin_anal():
        inline = InlineKeyboardMarkup()
        if db.get_admins(role="admin"):
            for admin in db.get_admins(role="admin"):
                inline.add(InlineKeyboardButton(admin[1],callback_data=f"admin_cl__{admin[3]}"))
        inline.add(InlineKeyboardButton(text="زیادكردنی ئەدمین",callback_data="add_admin"))
        return inline
    @staticmethod
    def remove_admin(user_id):
        inline = InlineKeyboardMarkup()
        inline.add(InlineKeyboardButton(text="ڕەشكردنەوە",callback_data=f"delete_admin__{user_id}"))
        return inline
