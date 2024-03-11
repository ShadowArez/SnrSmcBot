from includes.keyboards import Keyboards
from includes.sqlite import Database
from includes.modules import types
import re,random,json
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)
class challnges:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle_challenges(self):
        @self.dp.message_handler(lambda message: message.text == "زانیاری و نرخی چاڵێنجەكان 🏆")
        async def group_challenges(message: types.Message):
            await message.answer("سەرجەم چاڵێنجەكانی TFT تكایە یەكێك دیاری بكە :",reply_markup=keb.get_challnges_button())
        buttons_bracked = []
        buttons = db.get_challenges()
        for button in buttons:
            for word in button[1].split(','):
                word = word.strip()
                buttons_bracked.append(word)
        @self.dp.message_handler(lambda message: message.text in buttons_bracked)
        async def group_challenges(message: types.Message):
            inline_button = []
            for msg in buttons_bracked:
                if message.text == msg:
                    deail = db.get_challenges(title=msg)
                    await message.answer(deail[2],reply_markup=keb.get_inline_of_challenges(msg=message.text))
        @self.dp.callback_query_handler(lambda c:c.data.startswith("buttons_challenge__"))
        async def answer_inline_challneges(call:types.CallbackQuery):
            text = call.data.split("__")[1]
            word = call.data.split("___")[1]
            buttons_title = db.get_challenges(title=text)
            amount_bracket = []
            descamount_bracked =[]
            for amount in buttons_title[3].split(","):
                amount_bracket.append(amount.strip())
            for descamount in buttons_title[4].split(','):
                descamount_bracked.append(descamount.strip())
            mapping = dict(zip(amount_bracket, descamount_bracked))
            if word in mapping:
                    await call.message.answer(f"""
نرخی ئەم چاڵێنجە بەبێ كۆدی داشكان

{mapping[word]}

""")