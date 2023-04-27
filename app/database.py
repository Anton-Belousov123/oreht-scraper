from app.scraper import Item
from secrets import secret
import psycopg2
import dataclasses


@dataclasses.dataclass
class DBObj:
    s_article: str
    s_name: str
    s_url: str
    s_photo: str
    s_price: float
    t_name: str
    t_url: str
    t_photo: str
    t_price: float
    t_type: str
    stage: str
    t_article: int


class Database:
    def __init__(self):
        self.table_name = 'kamran'
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()

    def get_code(self):
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE stage=%s", ("Created",))
        record = self.cur.fetchone()
        if not record:
            return None
        return DBObj(
            record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8],
            record[9], record[10], record[11])

    def update_item(self, item: Item, article: str):
        self.cur.execute(f"UPDATE {self.table_name} SET s_name=%s, s_url=%s, s_photo=%s,"
                         f" s_price=%s, stage=%s t_type=%s WHERE s_article=%s", (item.name, item.url, item.photo, item.price, 'Source parsed', 'ozon', article))
        self.conn.commit()
