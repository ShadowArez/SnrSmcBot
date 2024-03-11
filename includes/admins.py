from includes.modules import types, FSMContext,json,requests,BeautifulSoup,State,StatesGroup
from includes.keyboards import Keyboards
from includes.sqlite import Database
from includes.states import AdminsStates
import random
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)

def write_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

class admins:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle(self):
        button_data_list = []
        @self.dp.message_handler(lambda m:m.text == "ئەدمینەکان 🛡️")
        async def send_message_cmd(message : types.Message):
            if db.get_admins(user_id2=message.from_user.id,Role2="owner"):
                admins = db.get_admins(role='admin')
                keyboard = types.InlineKeyboardMarkup()
                for admin in admins:
                    keyboard.add(types.InlineKeyboardButton(admin[1], callback_data=f"admin_details:{admin[0]}"))
                keyboard.add(types.InlineKeyboardButton("زیادكردنی ئەدمین", callback_data="add_new_admin"))
                await message.answer("سەرجەم ئەدمینەكان:", reply_markup=keyboard)
            else:
                await message.answer("تكایە /start دابگرە")
        @self.dp.callback_query_handler(lambda c: c.data.startswith("admin_details:"))
        async def show_admin_details(callback_query: types.CallbackQuery):
            admin_id = callback_query.data.split(":")[1]
            admin = db.userdata(id=admin_id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("گۆڕینی ڕۆڵ", callback_data=f"change_role:{admin[0]}"))
            keyboard.add(types.InlineKeyboardButton("گەڕانەوە", callback_data="back_to_admins"))
            await callback_query.message.edit_text(f"زانیاری ئەدمین : {admin[1]}\n@{admin[2]}\n{admin[4]}", reply_markup=keyboard)
        @self.dp.callback_query_handler(lambda c: c.data.startswith("change_role:"))
        async def change_admin_role(callback_query: types.CallbackQuery, state: FSMContext):
            admin_id = callback_query.data.split(":")[1]
            await AdminsStates.CHANGE_ROLE.set()
            await state.update_data(admin_id=admin_id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("دووپاتكردنەوە", callback_data="confirm_change_role"))
            keyboard.add(types.InlineKeyboardButton("پاشگەزبوونەوە", callback_data="decline_change_role"))
            await callback_query.message.edit_text("ئایا دڵنیایی لەوەی ڕۆڵەكەی لە ئەدمینەوە بگۆری بۆ میمبەر ؟", reply_markup=keyboard)
        @self.dp.callback_query_handler(lambda c: c.data == "confirm_change_role", state=AdminsStates.CHANGE_ROLE)
        async def confirm_change_role(callback_query: types.CallbackQuery, state: FSMContext):
            data = await state.get_data()
            admin_id = data["admin_id"]
            keyboard = types.InlineKeyboardMarkup()
            admins = db.get_admins(role='admin')
            for admin in admins:
                keyboard.add(types.InlineKeyboardButton(admin[1], callback_data=f"admin_details:{admin[0]}"))
            keyboard.add(types.InlineKeyboardButton("زیادكردنی ئەدمین", callback_data="add_new_admin"))
            db.update_column(name_table="users",column_to_change="role",change_text="user",where="id",where_equal=admin_id)
            await callback_query.message.edit_text("ڕۆڵی ئەدمینەكە گۆڕا بۆ میمبەر",reply_markup=keyboard)
            await state.finish()

        @self.dp.callback_query_handler(lambda c: c.data == "back_to_admins")
        async def decline_change_role(callback_query: types.CallbackQuery, state: FSMContext):
            keyboard = types.InlineKeyboardMarkup()
            admins = db.get_admins(role='admin')
            for admin in admins:
                keyboard.add(types.InlineKeyboardButton(admin[1], callback_data=f"admin_details:{admin[0]}"))
            keyboard.add(types.InlineKeyboardButton("زیادكردنی ئەدمین", callback_data="add_new_admin"))
            await callback_query.message.edit_text("سەرجەم ئەدمینەكان:",reply_markup=keyboard)
            await state.finish()
        @self.dp.callback_query_handler(lambda c: c.data == "decline_change_role", state=AdminsStates.CHANGE_ROLE)
        async def decline_change_role(callback_query: types.CallbackQuery, state: FSMContext):
            keyboard = types.InlineKeyboardMarkup()
            admins = db.get_admins(role='admin')
            for admin in admins:
                keyboard.add(types.InlineKeyboardButton(admin[1], callback_data=f"admin_details:{admin[0]}"))
            keyboard.add(types.InlineKeyboardButton("زیادكردنی ئەدمین", callback_data="add_new_admin"))
            await callback_query.message.edit_text("سەرجەم ئەدمینەكان:",reply_markup=keyboard)
            await state.finish()

        @self.dp.callback_query_handler(lambda c: c.data == "add_new_admin")
        async def add_new_admin(callback_query: types.CallbackQuery):
            await AdminsStates.ADD_NEW_ADMIN.set()
            await callback_query.message.answer("بۆ زیادكردنی ئەدمین ویزەری بنووسە بەم شێوازە > @username",reply_markup=keb.back_confirm())

        @self.dp.message_handler(state=AdminsStates.ADD_NEW_ADMIN)
        async def process_new_admin_username(message: types.Message, state: FSMContext):
            username = message.text
            if '@' in str(username):
                username = username.replace("@", "")
            if 'https://t.me/' in str(username):
                username = username.replace("https://t.me/", "")
            if username == "پاشگەزبوونەوە":
                await message.answer("پاشگەزكرایەوە",reply_markup=keb.get_owner_keyboards(message.from_user.id))
            else:
                await message.answer(f"ئایا دڵنایی لە زیادكردنی {username} بۆ ئەدمینی ؟", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("بەڵێ", callback_data=f"confirm_add_new_admin:{username}")).add(types.InlineKeyboardButton("نەخێر", callback_data="decline_add_new_admin")))
            await state.finish()
        @self.dp.callback_query_handler(lambda c: c.data.startswith("confirm_add_new_admin"))
        async def confirm_add_new_admin(callback_query: types.CallbackQuery):
            username = callback_query.data.split(":")[1]
            try:
                user_ex = db.userdata(username=username)
                if user_ex:
                    db.update_column(name_table="users",column_to_change="role",change_text="admin",where="username",where_equal=username)
                    await callback_query.message.answer(f"{username} بەسەركەوتووی زیادكرا.",reply_markup=keb.get_owner_keyboards(callback_query.from_user.id))
                else:
                    await callback_query.message.answer("ببورە ئەو ویزەر نەیمە بوونی نیە",reply_markup=keb.get_owner_keyboards(callback_query.from_user.id))
            except Exception as e:
                if 'admin_id' in str(e):
                    await callback_query.message.answer("ببورە ئەو ویزەرنەیمە بوونی نیە",reply_markup=keb.get_owner_keyboards(callback_query.from_user.id))
                else:
                    await callback_query.message.answer("ببورە هەڵەیەك هەیە",reply_markup=keb.get_owner_keyboards(callback_query.from_user.id))
        @self.dp.callback_query_handler(lambda c: c.data == "decline_add_new_admin")
        async def decline_add_new_admin(callback_query: types.CallbackQuery, state: FSMContext):
            await callback_query.message.answer("پاشگەزكرایەوە",reply_markup=keb.get_owner_keyboards(callback_query.from_user.id))
            await state.finish()