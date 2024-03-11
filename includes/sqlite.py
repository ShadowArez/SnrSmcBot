from includes.modules import sqlite3,datetime,types

class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                user_id INTEGER,
                role TEXT,
                affiliate TEXT,
                date TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS buttons (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                photo TEXT,
                type TEXT,
                place TEXT,
                verb TEXT,
                name_verb TEXT,
                button_to TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS discount (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                photo TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS affiliates (
                user_id INTEGER PRIMARY KEY,
                affiliate_code TEXT(255),
                points INTEGER DEFAULT 0,
                key TEXT,
                date TEXT,
                status TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_method (
                id INTEGER PRIMARY KEY,
                title TEXT,
                descraption TEXT,
                photo TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vip_signals (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                start_date TEXT,
                end_date TEXT,
                type_offer TEXT,
                status TEXT,
                price TEXT,
                payment_method TEXT,
                hash_id TEXT,
                dolar TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq (
                id INTEGER PRIMARY KEY,
                msg TEXT,
                descraption TEXT,
                inline_button TEXT,
                msg_inline_button TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expired_vipsignals (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                start_date TEXT,
                end_date TEXT,
                expired_date TEXT,
                status TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS challneges (
                id INTEGER PRIMARY KEY,
                name TEXT,
                descraption TEXT,
                inline_buttons TEXT,
                inline_descraption TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS buttons_inline_msg (
                id INTEGER PRIMARY KEY,
                title TEXT,
                descraption TEXT,
                hash_id TEXT,
                type TEXT
            )
        ''')
        
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def userdata(self, user_id=None,id=None,username=None):
        if user_id:
            return self.cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'").fetchone()
        elif id:
            return self.cursor.execute(f"SELECT * FROM users WHERE id = '{id}'").fetchone()
        elif username:
            return self.cursor.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchone()
            
        else:
            return self.cursor.execute(f"SELECT * FROM users").fetchall()
    def add_discount_code(self, data, photo=None):
        if photo:
            self.cursor.execute("INSERT INTO discount (title, description, photo) VALUES (?, ?, ?)",
                                (data['title'], data['message'], photo))
        else:
            self.cursor.execute("INSERT INTO discount (title, description) VALUES (?, ?)",
                                (data['title'], data['message']))
        self.conn.commit()

    def get_discount_codes(self):
        return self.cursor.execute("SELECT * FROM discount").fetchall()


    def get_det_inine_msg(self,hash_id):
        return self.cursor.execute(f"SELECT * FROM buttons_inline_msg WHERE hash_id = '{hash_id}'").fetchone()
    def add_inline_det_msg(self,state):
        if state['type'] == "url":
            self.cursor.execute("INSERT INTO buttons_inline_msg (title,descraption,type) VALUES (?,?,?)", (state["label"],state['msg_u'],state['type']))
        else:
            self.cursor.execute("INSERT INTO buttons_inline_msg (title,descraption,type,hash_id) VALUES (?,?,?,?)", (state["label"],state['msg_u'],state['type'],state['hash_button']))
        self.conn.commit()
    def get_channels(self, datas=None):
        channels = self.cursor.execute("SELECT * FROM channels").fetchall()
        if datas:
            return [channel[1] for channel in channels]
        else:
            return channels

    def add_channel(self, name):
        self.cursor.execute("INSERT INTO channels (name) VALUES (?)", (name,))
        self.conn.commit()

    def get_buttons(self, place):
        return self.cursor.execute(f"SELECT * FROM Buttons WHERE place = '{place}'").fetchall()

    def get_detail_of_buttons(self, title):
        return self.cursor.execute(f"SELECT * FROM Buttons WHERE title = '{title}'").fetchone()
    def get_admins(self,user_id=None,user_id2=None,role=None,Role2=None):
        if role:
            return self.cursor.execute(f"SELECT * FROM users WHERE role = '{role}'").fetchall()
        elif user_id:
            return self.cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}' AND (role = 'owner' OR role = 'admin')").fetchone()
        elif user_id2:
            return self.cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id2}' AND role = '{Role2}'").fetchone()
        else:
            return self.cursor.execute(f"SELECT * FROM users WHERE role = 'owner' or role = 'admin'").fetchall()

    def add_expired_vip_signals(self,user_id,start_date, end_date, expired_date, status):
        self.cursor.execute("INSERT INTO expired_vipsignals (user_id, start_date, end_date, expired_date, status) VALUES (?, ?, ?, ?, ?)",
                            (user_id, start_date, end_date, expired_date, status))
        self.conn.commit()
    def get_expired_vip_signals(self,hash_id=None):
        if hash_id:
            return self.cursor.execute(f"SELECT * FROM expired_vipsignals WHERE user_id = {hash_id}").fetchone()
        else:
            return self.cursor.execute(f"SELECT * FROM expired_vipsignals").fetchall()
    def add_user(self, full_name, username, user_id, role, date):
        self.cursor.execute("INSERT INTO users (full_name, username, user_id, role, date) VALUES (?, ?, ?, ?, ?)",
                            (full_name, username, user_id, role, date))
        self.conn.commit()

    def add_user_to_vipsignals(self,user_id,start_date,end_date,type_offer,payment_method,price,status,hash_id,dolar):
        self.cursor.execute("INSERT INTO vip_signals (user_id, start_date,end_date, type_offer,status,payment_method,price,hash_id,dolar) VALUES (?, ?,?,?,?,?, ?, ?, ?)",
                            (user_id, start_date,end_date,type_offer, status,payment_method,price,hash_id,dolar))
        self.conn.commit()
    def get_vip_signals(self,hash_id=None,user_id=None):
        if hash_id:
            return self.cursor.execute(f"SELECT * FROM vip_signals WHERE hash_id = '{hash_id}'").fetchone()
        if user_id:
            return self.cursor.execute(f"SELECT * FROM vip_signals WHERE user_id = '{user_id}'").fetchone()
        else:
            return self.cursor.execute(f"SELECT * FROM vip_signals").fetchall()
    def add_user_to_affiliate(self, user_id):
        key = {str(i): str((i + 5) % 10) for i in range(10)}
        encrypted_number = ''.join(key[digit] for digit in str(user_id))
        self.cursor.execute("INSERT INTO affiliates (user_id, affiliate_code, key, date) VALUES (?, ?, ?, ?)",
                            (user_id, encrypted_number, str(key), datetime.now()))
        self.conn.commit()
    def get_detail_of_affiliate(self,user_id=None,code=None):
        if code:
            return self.cursor.execute(f"SELECT * FROM affiliates WHERE affiliate_code = '{code}'").fetchone()
        else:
            return self.cursor.execute(f"SELECT * FROM affiliates WHERE user_id = '{user_id}'").fetchone()
    def get_payment_methods(self,title=None):
        if title:
            return self.cursor.execute(f"SELECT * FROM payment_method WHERE title = '{title}'").fetchone()
        else:
            return self.cursor.execute(f"SELECT * FROM payment_method").fetchall()
    def add_payment_methods(self,data,photo=None):
        if photo:
            self.cursor.execute("INSERT INTO payment_method (title, descraption,photo) VALUES (?,?,?)",(data.get("title"), data.get("descraption"),data.get("photo")))
        else:
            self.cursor.execute("INSERT INTO payment_method (title, descraption) VALUES (?, ?)",(data.get("title"), data.get("descraption")))
        self.conn.commit()
    def get_faqs(self,msg=None,id=None):
        if msg:
            return self.cursor.execute(f"SELECT * FROM faq WHERE msg = '{msg}'").fetchone()
        elif id:
            return self.cursor.execute("SELECT * FROM faq WHERE inline_button LIKE '%to%'").fetchall()
        else:
            return self.cursor.execute(f"SELECT * FROM faq").fetchall()
    def get_challenges(self,title=None,inline=None):
        if title:
            return self.cursor.execute(f"SELECT * FROM challneges WHERE name = '{title}'").fetchone()
        elif inline:
            return self.cursor.execute(f"SELECT * FROM challneges WHERE inline_buttons = '{inline}'").fetchone()
        else:
            return self.cursor.execute(f"SELECT * FROM challneges").fetchall()
    def update_column(self,name_table,column_to_change,change_text,where,where_equal):
        self.cursor.execute(f"UPDATE {name_table} SET {column_to_change} = '{change_text}' WHERE {where} = '{where_equal}'")
        self.conn.commit()
    def delete_column(self,name_table,where,where_equal):
        self.cursor.execute(f"DELETE FROM {name_table} WHERE {where} = '{where_equal}'")
        self.conn.commit()
    async def add_affilite_coin(self,code,bot,user_id,point):
        check_user = self.cursor.execute('SELECT * FROM users WHERE user_id = ? AND affiliate IS NULL', (user_id,)).fetchone()
        if check_user:
            self.cursor.execute('SELECT user_id FROM affiliates WHERE affiliate_code = ?', (code,))
            result = self.cursor.fetchone()
            if result:
                referring_user_id = result[0]
                self.cursor.execute('UPDATE affiliates SET points = points + ? WHERE user_id = ?', (point,referring_user_id,))
                self.conn.commit()
                await bot.send_message(referring_user_id, f"{point} خاڵت بەدەست هێنا")
            else:
                await bot.send_message(user_id, "ببورە ئەو لینكەهەڵەیە")
        else:
            await bot.send_message(user_id,"ببورە تۆ ناتوانیت لە ڕێی لینكی ترەوە بەشداری بكەی ، پێشتر بەشداری بۆتت كردوە")
    def add_point(self,user_id,point):
        self.cursor.execute(f"UPDATE affiliates SET points = points + {point} WHERE affiliate_code = '{user_id}'")
        self.conn.commit()
    async def remove_channel(self, chat_id):
        try:
            self.cursor.execute("DELETE FROM channels WHERE name = ?", (chat_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error removing channel {chat_id}: {e}")

    async def is_bot_admin(self, chat_id, bot):
        try:
            administrators = await bot.get_chat_administrators(chat_id)
            return any(admin.user.id == bot.id for admin in administrators)
        except Exception as e:
            await self.remove_channel(chat_id)
            return False

    async def check_user_channels(self, user_id, bot):
        if self.get_channels():
            for channel in self.get_channels():
                try:
                    if await self.is_bot_admin(channel[1], bot=bot):
                        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
                        if chat_member.status in [
                            types.ChatMemberStatus.MEMBER, types.ChatMemberStatus.ADMINISTRATOR,
                            types.ChatMemberStatus.CREATOR
                        ]:
                            return True
                except Exception as e:
                    print(f"Error checking channel {channel[1]}: {e}")
            return False
        else:
            return True