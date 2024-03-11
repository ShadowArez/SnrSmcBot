from includes.sqlite import Database
from includes.states import*
from includes.keyboards import Keyboards
from includes.modules import types,State,StatesGroup, FSMContext
from datetime import date,timedelta,datetime
db = Database("your_database.db")
keb = Keyboards()
class channel:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle(self):
        @self.dp.message_handler(lambda message: message.text in ['Channels', 'زیادكردنی كەناڵ'])
        async def channes(message: types.Message):
            if message.text == "Channels":
                user_data = db.userdata(message.from_user.id)
                if not user_data or user_data[4] != "owner":
                    return
                await message.answer("سەرجەم كەناڵەكان", reply_markup=keb.get_channels())
            else:
                await message.answer("نكایە ویزەرنەیمی كەناڵ بنێرە :")
                await AddJoinChannel.TITLE.set()
        @self.dp.message_handler(state=AddJoinChannel.TITLE)
        async def process_add_title(message: types.Message, state: FSMContext):
            await state.update_data(name=message.text)
            await message.answer(" دڵنیایی لە زیادكردنی كەناڵ ؟ :", reply_markup=keb.get_confirm_of_create_account())
            await AddJoinChannel.CONFIRM.set()

        @self.dp.message_handler(lambda message: message.text in ['بەڵێ', 'بەڵێ'], state=AddJoinChannel.CONFIRM)
        async def process_check_confirm(message: types.Message, state: FSMContext):
            data = await state.get_data()
            action_text = data.get("name") 
            keyboard = keb.get_owner_keyboards()
            if message.text == 'نەخێڕ':
                await message.answer("یەسەركەوتووی پاشگەز گرایەوە",reply_markup=keyboard())
            elif message.text == 'بەڵێ':
                action_text = action_text.replace("https://t.me/", "")
                if not '@' in action_text:
                    action_text = f"@{action_text}"
                try:
                    db.add_channel(action_text)
                    await message.answer("یەسەركەوتووی زیادكرا ، تكایە دڵنیابە لەوەی كە بۆتەكە ئەدمین بێت لە كەناڵەكە ",reply_markup=keyboard)
                except Exception as e:
                    await message.answer(f"جۆری كێشەكە {e}",reply_markup=keyboard)
            await state.finish()
