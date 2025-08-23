import sqlite3
from datetime import datetime, timedelta

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
                                multiplier REAL,
                                FOREIGN KEY (user_id) REFERENCES users(user_id)
                                )""")
            
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS rates(
                                rate_id INT PRIMARY KEY,
                                name TEXT,
                                description TEXT,
                                first_event_name TEXT,
                                second_event_name TEXT,
                                first_event_chance REAL,
                                second_event_chance REAL
                                )""")
            
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users_rates(
                                user_id INT,
                                rate_id INT,
                                bet BIGINT,
                                selected_event BOOL,
                                FOREIGN KEY (rate_id) REFERENCES rates(rate_id),
                                FOREIGN KEY (user_id) REFERENCES users(user_id)
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
        return result[0]

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
    
    def get_rate_id(self, rate_id: int):
        result =  self.cursor.execute("SELECT rate_id FROM rates WHERE rate_id = ?", (rate_id,)).fetchone()
        return result[0] if result else None
    
    def get_rate_name(self, rate_id: int):
        result =  self.cursor.execute("SELECT name FROM rates WHERE rate_id = ?", (rate_id,)).fetchone()
        return result[0]
    
    def get_rate_description(self, rate_id: int):
        result =  self.cursor.execute("SELECT description FROM rates WHERE rate_id = ?", (rate_id,)).fetchone()
        return result[0]
    
    def get_rate_first_event_name(self, rate_id: int):
        result =  self.cursor.execute("SELECT first_event_name FROM rates WHERE rate_id = ?", (rate_id,)).fetchone()
        return result[0]
    
    def get_rate_second_event_name(self, rate_id: int):
        result =  self.cursor.execute("SELECT second_event_name FROM rates WHERE rate_id = ?", (rate_id,)).fetchone()
        return result[0]
    
    def get_rate_first_event_chance(self, rate_id: int):
        result =  self.cursor.execute("SELECT first_event_chance FROM rates WHERE rate_id = ?", (rate_id,)).fetchone()
        return result[0]
    
    def get_rate_second_event_chance(self, rate_id: int):
        result =  self.cursor.execute("SELECT second_event_chance FROM rates WHERE rate_id = ?", (rate_id,)).fetchone()
        return result[0]
    
    def get_user_rate_user_id(self, member_id: int):
        result =  self.cursor.execute("SELECT user_id FROM users_rates WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]
    
    def get_user_rate_rate_id(self, member_id: int):
        result =  self.cursor.execute("SELECT rate_id FROM users_rates WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]
    
    def get_user_rate_bet(self, member_id: int):
        result =  self.cursor.execute("SELECT bet FROM users_rates WHERE user_id = ?", (member_id,)).fetchone()
        return result[0]
    
    def get_user_rate_selected_event(self, member_id: int):
        result =  self.cursor.execute("SELECT selected_event FROM users_rates WHERE user_id = ?", (member_id,)).fetchone()
        if result:
            return True
        else:
            return False



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
    
    def set_rates_name(self, name: str, rate_id: int):
        self.cursor.execute("UPDATE rates SET name = ? WHERE rate_id = ?", (name, rate_id))
        self.connection.commit()
        return
    
    def set_rates_description(self, description: str, rate_id: int):
        self.cursor.execute("UPDATE rates SET description = ? WHERE rate_id = ?", (description, rate_id))
        self.connection.commit()
        return
    
    def set_rates_first_event_name(self, name: str, rate_id: int):
        self.cursor.execute("UPDATE rates SET first_event_name = ? WHERE rate_id = ?", (name, rate_id))
        self.connection.commit()
        return
    
    def set_rates_second_event_name(self, name: str, rate_id: int):
        self.cursor.execute("UPDATE rates SET second_event_name = ? WHERE rate_id = ?", (name, rate_id))
        self.connection.commit()
        return
    
    def set_rates_first_event_chance(self, chance: float, rate_id: int):
        self.cursor.execute("UPDATE rates SET first_event_chance = ? WHERE rate_id = ?", (chance, rate_id))
        self.connection.commit()
        return
    
    def set_rates_second_event_chance(self, chance: float, rate_id: int):
        self.cursor.execute("UPDATE rates SET second_event_chance = ? WHERE rate_id = ?", (chance, rate_id))
        self.connection.commit()
        return
    
    def set_user_rate_bet(self, bet: int, member_id: int):
        self.cursor.execute("UPDATE users_rates SET bet = ? WHERE user_id = ?", (bet, member_id))
        self.connection.commit()
        return
    
    def set_user_rate_selected_event(self, event: bool, usemember_idr_id: int):
        self.cursor.execute("UPDATE users_rates SET selected_event = ? WHERE user_id = ?", (event, member_id))
        self.connection.commit()
        return
    


    # update методы
    def update_member_cash(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET cash = cash + ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_level(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET level = level + ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_level_xp(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET level_xp = level_xp + ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_total_wins(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET total_wins = total_wins + ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_member_total_lose(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users SET total_lose = total_lose + ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_role_cost(self, amount: int, role_id: int):
        self.cursor.execute("UPDATE shop SET cost = cost + ? WHERE role_id = ?", (amount, role_id))
        self.connection.commit()
        return
    
    def update_bank_end_date(self, date: timedelta, member_id: int):
        self.cursor.execute("UPDATE bank SET end_date = end_date + ? WHERE user_id = ?", (date, member_id))
        self.connection.commit()
        return
    
    def update_bank_deposit(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE bank SET deposit = deposit + ? WHERE user_id = ?", (amount, member_id))
        self.connection.commit()
        return
    
    def update_user_rate_bet(self, amount: int, member_id: int):
        self.cursor.execute("UPDATE users_rates SET bet = bet + ? WHERE user_id = ?", (amount, member_id))
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
    
    def delete_rate(self, rate_id: int):
        self.cursor.execute("DELETE FROM rates WHERE rate_id = ?", (rate_id,))
        self.connection.commit()
        return
    
    def delete_user_rate(self, member_id: int):
        self.cursor.execute("DELETE FROM users_rates WHERE user_id = ?", (member_id,))
        self.connection.commit()
        return
    


    def level_xp_update(self, member_id: int, xp_gain: int):
        level_up = 50 - xp_gain
        self.cursor.execute("UPDATE users SET level_xp = level_xp + ? WHERE user_id = ?", (xp_gain, member_id))
        if self.get_member_level_xp(member_id) > 49:
            self.cursor.execute("UPDATE users SET level_xp = level_xp - 50 WHERE user_id = ?", (member_id,))
            self.cursor.execute("UPDATE users SET level = level + 1 WHERE user_id = ?", (member_id,))

        self.connection.commit()
        return