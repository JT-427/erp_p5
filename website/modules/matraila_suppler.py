import random
import datetime as dt
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .. import db
from .database.flask_sqlalchemy_model import MatarialSupplier

class MatarialSupplierC:
    def __init__(self, matarial_supplier_id:str=None) -> None:
        if matarial_supplier_id:
            self.matarial_supplier_id=matarial_supplier_id

    def get_suppliers(self, cooperating: bool=True) -> list:
        try:
            matarial_supplier_id = self.matarial_supplier_id
        except AttributeError:
            matarial_supplier_id = None
        query = db.session.query(
            MatarialSupplier
        ).filter(
            or_(
                matarial_supplier_id == None,
                MatarialSupplier.matarial_supplier_id == matarial_supplier_id
            ),
            or_(
                cooperating == False,
                MatarialSupplier.cooperating == cooperating
            )
        ).all()

        return query
    
    def create(self, **kwargs) -> None:
        new = MatarialSupplier(**kwargs)
        
        def id_gen():
            a = oct(random.randint(8**9+1, 8**10))[2:] # 10
            b = hex(random.randint(16**5+1, 16**6))[2:] # 6
            c = str(random.randint(102, 999)) # 3
            d = oct(int(dt.date.today().strftime('%Y%m%d')))[2:]
            lef = d + b + c + a
            e = hex(random.randint(16**(32-len(lef)-1)+1, 16**(32 - len(lef))))[2:]
            return lef + e
        new.matarial_supplier_id = id_gen()

        db.session.add(new)
        try:
            db.session.commit()
        except IntegrityError:
            new.matarial_supplier_id = id_gen()
            db.session.add(new)
            db.session.commit()
        
    def modify(self, **kwargs) -> None:
        matarial_supplier_id = self.matarial_supplier_id
        db.session.query(
            MatarialSupplier
        ).filter(
            MatarialSupplier.matarial_supplier_id == matarial_supplier_id
        ).update(kwargs)
        db.session.commit()

    def delete(self) -> None:
        matarial_supplier_id = self.matarial_supplier_id
        
        db.session.query(
            MatarialSupplier
        ).filter(
            MatarialSupplier.matarial_supplier_id == matarial_supplier_id
        ).delete()
        db.session.commit()