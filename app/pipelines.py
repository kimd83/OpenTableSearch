from sqlalchemy.orm import sessionmaker
from models import Restaurant, Alerts, db_connect, create_table

class FindTablePipleline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def save_alert(self, item):

        session = self.Session()
        alert = Alerts(**item)

        try:
            session.add(alert)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

