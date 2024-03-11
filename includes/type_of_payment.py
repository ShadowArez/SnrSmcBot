from includes.modules import types, FSMContext,json,requests,BeautifulSoup,State,StatesGroup
from includes.keyboards import Keyboards
from includes.sqlite import Database
from includes.states import PaymentStates
import random
db=Database("your_database.db")
keb = Keyboards()
with open('config.json', 'r', encoding='utf8') as config:
    config = json.load(config)

def write_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

class type_payment:
    def __init__(self, dp,bot):
        self.dp = dp
        self.bot = bot
    def handle(self):
        @self.dp.message_handler(lambda m:m.text == "نرخی پارەدان 🏦")
        async def start(message: types.Message):
            with open('config.json', 'r', encoding='utf8') as config:
                config = json.load(config)
            keyboard = types.InlineKeyboardMarkup()
            if "type_of_payment" in config:
                for payment in config["type_of_payment"]:
                    if "payment" in payment:
                        if 'days' in payment['payment'] and 'price' in payment['payment']:
                            keyboard.add(types.InlineKeyboardButton(f"بۆ ماوەی {payment['payment']['days']} ڕۆژ : {payment['payment']['price']} دۆلار💵\n",callback_data=f"pay_off_button__{payment['payment']['days']}+{payment['payment']['price']}"))
            keyboard.add(types.InlineKeyboardButton(text="زیادكردنی نرخ",callback_data="add_new_type_of_payment"))
            await message.answer("فەرموو ئەمە سەرجەم نرخی پارەدانە :",reply_markup=keyboard)
        @self.dp.callback_query_handler(lambda c:c.data == "add_new_type_of_payment")
        async def process_adds(call: types.CallbackQuery, state: FSMContext):
            await call.message.answer("بۆ زیادركدنی نرخی پارەدان بڕی ڕۆژ بنووسە یان بە پێچەوانەوە پاشگەزبوونەوە دابگرە",reply_markup=keb.back_confirm())
            await PaymentStates.entering_amount_days.set()
        @self.dp.message_handler(state=PaymentStates.entering_amount_days)
        async def process_days(message: types.Message, state: FSMContext):
            if message.text == "پاشگەزبوونەوە":
                await state.finish()
                await message.answer("پاشگەزبوونەوە دووپاتكرایەوە",reply_markup=keb.get_owner_keyboards(message.from_user.id))
            else:
                await state.update_data(days=message.text)
                await PaymentStates.entering_price.set()
                await message.answer("زۆر باشە ، تكایە نرخی بەشداری كردن بنووسە")
        @self.dp.message_handler(state=PaymentStates.entering_price)
        async def process_price(message: types.Message, state: FSMContext):
            await state.update_data(price=message.text)
            data = await state.get_data()
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="بەڵێ", callback_data="confirm_add_t_pay"))
            keyboard.add(types.InlineKeyboardButton(text="نەخێر", callback_data="decline_add_t_pay"))
            await message.answer(f"""
زۆر باشە

ڕۆژی بەشداری كردن : {data['days']}
نرخی بەشداری كردن : {data['price']}

ئایا دڵنایی لە زیادكردنی ئەم نرخی پارەدانە ؟
""", reply_markup=keyboard)
            await PaymentStates.entering_done.set()
        @self.dp.callback_query_handler(lambda c: c.data in ['confirm_add_t_pay', 'decline_add_t_pay'], state=PaymentStates.entering_done)
        async def process_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
            choice = callback_query.data
            if choice == 'confirm_add_t_pay':
                data = await state.get_data()
                days = data.get('days')
                price = data.get('price')
                button_key = f"payment"
                button_value = {"days": f"{data.get('days')}", "price": f"{data.get('price')}"}
                config["type_of_payment"].append({button_key: button_value})
                write_config(config)
                await callback_query.message.answer(f"""
بەسەركەوتووی زیادكرا

ڕۆژ : {data.get("days")}
نرخ : {data.get("price")}
""",reply_markup=keb.get_owner_keyboards(callback_query.message.from_user.id))
            else:
                await message.answer("پاشگەزبوونەوە دووپاتكرایەوە",reply_markup=keb.get_owner_keyboards(callback_query.message.from_user.id))
            await state.finish()
        @self.dp.callback_query_handler(lambda c:c.data.startswith("pay_off_button__"))
        async def delet_disc(call : types.CallbackQuery):
            button_title = call.data.split("__")[1]
            await call.message.answer("ئایا دڵنایی لە ڕەشكردنەوەی ؟",reply_markup=keb.get_confrim_delete_dis(button_title))
        @self.dp.callback_query_handler(lambda c:c.data.startswith("yesy_deletes__"))
        async def delet_disc_confirm(call : types.CallbackQuery):
            button_title = call.data.split("__")[1]
            days = button_title.split('+')[0]
            price = button_title.split('+')[1]
            try:
                for payment_obj in config["type_of_payment"]:
                    if payment_obj and payment_obj.get("payment", {}).get("days") == str(days) and payment_obj.get("payment", {}).get("price") == str(price):
                        config["type_of_payment"].remove(payment_obj)
                        write_config(config)
                await call.message.answer("بەسەركەوتووی ڕەشكرایەوە",reply=keb.get_owner_keyboards(call.message.from_user.id))
            except Exception as e:
                print(e)
                await call.message.answer(f"ببورە كێشەیەك هەیە {e}")