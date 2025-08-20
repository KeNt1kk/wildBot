import sqlite3
from datetime import datetime, date, timedelta

class Database:
    def __init__(self, client):
        self.connection = sqlite3.connect('server.db')
        self.cursor = self.connection.cursor()
        self.client = client
        
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id INT PRIMARY KEY,
                    name TEXT,
                    cash BIGINT DEFAULT 1000,
                    level INT DEFAULT 1,
                    level_xp INT DEFAULT 0,
                    total_wins INT DEFAULT 0,
                    total_lose INT DEFAULT 0
                    )""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS shop(
                        role_id INT PRIMARY KEY,
                        cost BIGINT
                        )""")
            
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS bank(
                                user_id INT,
                                end_date TIMESTAMP,
                                deposit BIGINT,
                                multiplier REAL
                                )""")
            
            self.connection.commit()


            for guild in client.guilds:
                for member in guild.members:
                    if not member.bot:
                        self.cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (member.id,))
                        if not self.cursor.fetchone():
                            member_name = str(member.name)
                            self.cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (member.id, member_name))
                            self.connection.commit()
        except Exception as e:
            print(f'Ошибка при инициализации базы данных: {e}')
        else:
            print('База данных успешно создана')

    
    # get методы
    def get_member_id(self, member_id: int):
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (member_id,)).fetchone()
        return result[0] if result else None

    def get_member_name(self, member_id: int):
        result =  self.cursor.execute("SELECT name FROM users WHERE user_id = ?", (member_id,)).fetchone()
        return result[0] if result else None

    def get_member_cash(self, member_id: int):
        result =  self.cursor.execute("SELECT cash FROM users WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]

    def get_member_level(self, member_id: int):
        result =  self.cursor.execute("SELECT level FROM users WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]

    def get_member_level_xp(self, member_id: int):
        result =  self.cursor.execute("SELECT level_xp FROM users WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]

    def get_member_total_wins(self, member_id: int):
        result =  self.cursor.execute("SELECT total_wins FROM users WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]

    def get_member_total_lose(self, member_id: int):
        result =  self.cursor.execute("SELECT total_lose FROM users WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]
    
    def get_role_id(self, role_id: int):
        result = self.cursor.execute("SELECT role_id FROM shop WHERE role_id = ?", (role_id,)).fetchone()
        return result[0]

    def get_role_cost(self, role_id: int):
        result =  self.cursor.execute("SELECT cost FROM shop WHERE role_id = ?", (role_id,)).fetchone()
        return result[0]
    
    def get_bank_id(self, member_id: int):
        result = self.cursor.execute("SELECT user_id FROM bank WHERE user_id = ?", (member_id,)).fetchone()
        return result[0] if result else None
    
    def get_bank_end_date(self, member_id: int) -> datetime:
        result = self.cursor.execute("SELECT end_date FROM bank WHERE user_id = ?", (member_id,)).fetchone()
        return datetime.fromisoformat(result[0])
    
    def get_bank_deposit(self, member_id: int) -> int:
        result = self.cursor.execute("SELECT deposit FROM bank WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]
    
    def get_bank_multiplier(self, member_id: int) -> float:
        result = self.cursor.execute("SELECT multiplier FROM bank WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]



    # set методы
    def set_member_cash(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET cash = ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return

    def set_member_level(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return

    def set_member_level_xp(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET level_xp = ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return

    def set_member_total_wins(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET total_wins = ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return

    def set_member_total_lose(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET total_lose = ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return

    def set_role_cost(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE shop SET cost = ? WHERE role_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def set_bank_end_date(self, date: datetime, member_id: int):
        self.cursor.execute("UPDATE bank SET end_date = ? WHERE user_id = ?", (date, member_id))
        self.connection.commit()
        return
    
    def set_bank_deposit(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE bank SET deposit = ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def set_bank_multiplier(self, multi: float, member_id: int):
        self.cursor.execute("UPDATE bank SET multiplier = ? WHERE user_id = ?", (multi, member_id))
        self.connection.commit()
        return
    


    # update методы
    def update_member_cash(self, amount: int, sign: str, member_id: int):
        self.cursor.execute(f"UPDATE users SET cash = cash {sign} ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_level(self, amount: int, sign: str, member_id: int):
        self.cursor.execute(f"UPDATE users SET level = level {sign} ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_level_xp(self, amount: int, sign: str, member_id: int):
        self.cursor.execute(f"UPDATE users SET level_xp = level_xp {sign} ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_total_wins(self, amount: int, sign: str, member_id: int):
        self.cursor.execute(f"UPDATE users SET total_wins = total_wins {sign} ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_total_lose(self, amount: int, sign: str, member_id: int):
        self.cursor.execute(f"UPDATE users SET total_lose = total_lose {sign} ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_role_cost(self, amount: int, sign: str, role_id: int):
        self.cursor.execute(f"UPDATE shop SET cost = cost {sign} ? WHERE role_id = ?", (amount, role_id))
        self.connection.commit()
        return
    


    # delete методы
    def delete_member(self, member_id: int):
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (member_id, ))
        self.connection.commit()
        return
    
    def delete_role(self, role_id: int):
        self.cursor.execute("DELETE FROM shop WHERE role_id = ?", (role_id, ))
        self.connection.commit()
        return
    
    def delete_bank(self, member_id: int):
        self.cursor.execute("DELETE FROM bank WHERE user_id = ?", (member_id,))
        self.connection.commit()
        return
    


    def check_bank_deposit(self, member_id):
        if self.cursor.execute("SELECT 1 FROM bank WHERE user_id = ?", (member_id,)).fetchone():
            return True
        else:
            return False

    def level_xp_update(self, member_id: int, xp_gain: int):
        level_up = 50 - xp_gain
        self.cursor.execute("UPDATE users SET level_xp = level_xp + ? WHERE user_id = ?", (xp_gain, member_id))
        if self.get_member_level_xp(member_id) > 49:
            self.cursor.execute("UPDATE users SET level_xp = level_xp - 50 WHERE user_id = ?", (member_id,))
            self.cursor.execute("UPDATE users SET level = level + 1 WHERE user_id = ?", (member_id,))

        self.connection.commit()
        return