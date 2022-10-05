import random
import datetime as dt
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .. import db
from .database.flask_sqlalchemy_model import Outsourcer

class OutsourcerC:
    def __init__(self, outsourcer_id:str=None) -> None:
        if outsourcer_id:
            self.outsourcer_id=outsourcer_id

    def get_outsourcers(self) -> list:
        try:
            outersourcer_id = self.outersourcer_id
        except AttributeError:
            outersourcer_id = None
        outsourcers_query = db.session.query(
            Outsourcer
        ).filter(
            or_(
                outersourcer_id == None,
                Outsourcer.outsourcer_id == outersourcer_id
            )
        ).all()
        return outsourcers_query

    def modify(self, **kwargs) -> None:
        outsourcer_id = self.outsourcer_id
        db.session.query(
            Outsourcer
        ).filter(
            Outsourcer.outsourcer_id == outsourcer_id
        ).update(kwargs)
        db.session.commit()
    
    def create(self, **kwargs) -> None:
        new = Outsourcer(**kwargs)
        
        def id_gen():
            a = oct(random.randint(8**9+1, 8**10))[2:] # 10
            b = hex(random.randint(16**5+1, 16**6))[2:] # 6
            c = str(random.randint(102, 999)) # 3
            d = oct(int(dt.date.today().strftime('%Y%m%d')))[2:]
            lef = d + b + c + a
            e = hex(random.randint(16**(32-len(lef)-1)+1, 16**(32 - len(lef))))[2:]
            return lef + e
        new.outsourcer_id = id_gen()

        db.session.add(new)
        try:
            db.session.commit()
        except IntegrityError:
            new.outsourcer_id = id_gen()
            db.session.add(new)
            db.session.commit()
        return new.outsourcer_id
    def delete(self) -> None:
        outsourcer_id = self.outsourcer_id
        db.session.query(
            Outsourcer
        ).filter(
            Outsourcer.outsourcer_id == outsourcer_id
        ).delete()
        db.session.commit()