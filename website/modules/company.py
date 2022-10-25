import random
import datetime as dt
from sqlalchemy import and_, or_, null
from sqlalchemy.exc import IntegrityError

from .. import db
from .database.flask_sqlalchemy_model import Company

class CompanyC:
    def __init__(self, company_id:str=None) -> None:
        if company_id:
            self.company_id = company_id
    def get_all_company(self, date: str='') -> list:
        query = db.session.query(
            Company
        ).filter(
            or_(date=='', Company.create_date <= date),
            or_(
                date=='', 
                    or_(
                    Company.end_date == null(),
                    Company.end_date > date
                )
            )
        ).all()
        return query

    def create(self, **kwargs):
        def id_gen():
            a = oct(random.randint(8**9+1, 8**10))[2:] # 10
            b = hex(random.randint(16**5+1, 16**6))[2:] # 6
            c = str(random.randint(102, 999)) # 3
            d = oct(int(dt.date.today().strftime('%Y%m%d')))[2:]
            lef = d + b + c + a
            e = hex(random.randint(16**(32-len(lef)-1)+1, 16**(32 - len(lef))))[2:]
            return lef + e
        new = Company(**kwargs)
        new.company_id = id_gen()
        db.session.add(new)
        try:
            db.session.commit()
        except IntegrityError:
            new.company_id = id_gen()
            db.session.add(new)
            db.session.commit()

    def modify(self, **kwargs):
        company_id = self.company_id
        db.session.query(
            Company
        ).filter(
            Company.company_id == company_id
        ).update(kwargs)
        db.session.commit()

    def delete(self) -> None:
        company_id = self.company_id
        db.session.query(
            Company
        ).filter(
            Company.company_id == company_id
        ).delete()
        db.session.commit()
