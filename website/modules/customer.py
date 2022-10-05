import random
import datetime as dt
from sqlalchemy.exc import IntegrityError

from .. import db
from .database.flask_sqlalchemy_model import Customer

class CustomerC:
    def __init__(self, customer_id:str=None) -> None:
        if customer_id:
            self.customer_id = customer_id
    
    def get_customer_info(self) -> list:
        customer_query = db.session.query(
            Customer
        ).filter(
            Customer.customer_id == self.customer_id
        ).first()
        return customer_query

    def get_all_customer(self) -> list:
        customers_query = db.session.query(
            Customer
        ).all()
        return customers_query

    def modify(self, **kwargs) -> None:
        customer_id = self.customer_id
        db.session.query(
            Customer
        ).filter(
            Customer.customer_id == customer_id
        ).update(kwargs)
        db.session.commit()
    
    def create(self, **kwargs) -> None:
        new = Customer(**kwargs)
        
        def id_gen():
            a = oct(random.randint(8**9+1, 8**10))[2:] # 10
            b = hex(random.randint(16**5+1, 16**6))[2:] # 6
            c = str(random.randint(102, 999)) # 3
            d = oct(int(dt.date.today().strftime('%Y%m%d')))[2:]
            lef = d + b + c + a
            e = hex(random.randint(16**(32-len(lef)-1)+1, 16**(32 - len(lef))))[2:]
            return lef + e
        new.customer_id = id_gen()

        db.session.add(new)
        try:
            db.session.commit()
        except IntegrityError:
            new.customer_id = id_gen()
            db.session.add(new)
            db.session.commit()
    def delete(self) -> None:
        customer_id = self.customer_id
        db.session.query(
            Customer
        ).filter(
            Customer.customer_id == customer_id
        ).delete()
        db.session.commit()

            