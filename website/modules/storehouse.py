import random
import datetime as dt
from sqlalchemy import desc, null, or_, and_

from .. import db
from ..modules.database.flask_sqlalchemy_model import Storehouse

class StorehouseC:
    def __init__(self, storehouse_id: str=None) -> None:
        if storehouse_id:
            self.storehouse_id = storehouse_id
    
    def get_storehouse(self):
        query = db.session.query(
            Storehouse
        ).filter(
            Storehouse.storehouse_id == self.storehouse_id
        ).first()
        return query

    def create(self, **kwargs):
        def id_gen():
            a = oct(random.randint(8**9+1, 8**10))[2:] # 10
            b = hex(random.randint(16**6+1, 16**7))[2:] # 7
            d = oct(int(dt.datetime.strptime(kwargs["create_date"], '%Y-%m-%d').date().strftime('%Y%m%d')))[2:]
            lef = a + b + d
            e = hex(random.randint(16**(32-len(lef)-1)+1, 16**(32 - len(lef))))[2:]
            return lef + e
        
        new = Storehouse(**kwargs)
        new.storehouse_id = id_gen()
        db.session.add(new)
        db.session.commit()
        return True
    def modify(self, **kwargs):
        db.session.query(
            Storehouse
        ).filter(
            Storehouse.storehouse_id == self.storehouse_id
        ).update(
            kwargs
        )
        db.session.commit()
    def delete(self):
        db.session.query(
            Storehouse
        ).filter(
            Storehouse.storehouse_id == self.storehouse_id
        ).delete()
        db.session.commit()
    
    def get_all_storehouse(self, date: str=''):
        query = db.session.query(
            Storehouse
        ).filter(
            or_(
                date == '',
                and_(
                    Storehouse.create_date <= date,
                    or_(
                        Storehouse.quit_date == null(),
                        Storehouse.quit_date > date
                    )
                )
            )
        ).all()
        return query
