from includes.modules import types,json
from includes.keyboards import Keyboards
from includes.sqlite import Database
from unidecode import unidecode
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)
class faq:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle_faq(self):
        @self.dp.message_handler(lambda message: message.text == "پرسیار و زایارییەكان ⁉️")
        async def cmd_faq(message: types.Message):
            await message.answer("یەکێک لە پرسیارەکان دیاری بکە بۆ بینینی وەڵام...",reply_markup=keb.get_faq_buttons())            
        @self.dp.message_handler(lambda message: any(message.text in button[1] for button in db.get_faqs()))
        async def answer_faq(message: types.Message):
            buttons = db.get_faqs(msg=message.text)
            await message.answer(buttons[2],reply_markup=keb.get_inline_buttons(id=buttons[0]))                
        @self.dp.callback_query_handler(lambda c: c.data.startswith('buttonfaq_'))
        async def answer_call_faq(call: types.CallbackQuery):
            text = call.data.split('_')[1]
            detail = db.get_faqs(id=text)
            for i in detail:
                if int(text) == int(i[0]):
                    await call.message.answer(i[2])