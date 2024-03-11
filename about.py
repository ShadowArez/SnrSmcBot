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
class about:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle(self):
        @self.dp.message_handler(lambda m:m.text == "دەربارە ℹ️")
        async def send_message_cmd(message : types.Message):
            await message.answer("کۆمپانیای SNR SMC لە لایەن شوان رواندزی شارەزای بازارە داراییەکان دامەزراوە لە ساڵی 2022. کۆمەڵێک خزمەت گوزاری بازارە داراییەکان پێشکەشی بازرگانن ئەکات وەک هەژماری فۆرئێکس _ سیگناڵ _ شیکاری _ فێرکاری.")