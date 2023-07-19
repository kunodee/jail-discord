
import core

class database:

    def __init__(self):

        self.conn = core.sqlite3.connect('database.db')
        self.cur  = self.conn.cursor()

    def get_user(self, user_id: int = 0):
        self.cur.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        result = self.cur.fetchone()
        return result if not None else False
    
    def jail(self, user_id, roles, admin, reason, date):
        self.cur.execute("""
                INSERT INTO users (user_id, roles, admin, reason, date)
                VALUES (?, ?, ?, ?, ?)
            """, (str(user_id), ','.join(roles), admin, reason, date))
        self._commit()

    def unjail(self, user_id):
        self.cur.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")
        self._commit()
    
    def _close(self):
        self.conn.close()

    def _commit(self):
        self.conn.commit()