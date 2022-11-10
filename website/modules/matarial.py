import random
import datetime as dt
from sqlalchemy import asc, desc, null, or_, and_
from sqlalchemy.sql import func

from .. import db
from .database.flask_sqlalchemy_model import Matarial, MatarialBuyingRecord, MatarialInStorehouse, MatarialRemainingAdjustmentRecord, MatarialSupplier, MatarialTransferRecord, MatarialUsingRecord, Project, Storehouse

class MatarialC:
    def __init__(self, matarial_id:str=None) -> None:
        if matarial_id:
            self.matarial_id = matarial_id

    def check_id(callback):
        def inner(self, *args, **kwargs):
            assert self.matarial_id, 'Please set the matarial_id first.'
            return callback(self, *args, **kwargs)
        return inner

    @check_id
    def get_info(self, storehouse_id: str=None):
        sub_query = db.session.query(
            MatarialInStorehouse.matarial_id,
            MatarialInStorehouse.storehouse_id,
            MatarialInStorehouse.date,
            MatarialInStorehouse.remaining
        ).filter(
            MatarialInStorehouse.matarial_id == self.matarial_id,
            MatarialInStorehouse.storehouse_id == storehouse_id
        ).order_by(
            desc(MatarialInStorehouse.sn)
        ).limit(1).subquery()

        matarial_query = db.session.query(
            Matarial.matarial_id,
            Matarial.matarial_name,
            Matarial.notes,
            Matarial.unit,
            sub_query.c.storehouse_id,
            sub_query.c.remaining
        ).outerjoin(
            sub_query,
            Matarial.matarial_id == sub_query.c.matarial_id
        ).filter(
            Matarial.matarial_id == self.matarial_id
        ).first()
        return matarial_query

    def create(self, matarial_name:str, unit: str, notes: str=''):
        def id_gen():
            a = oct(random.randint(8**9+1, 8**10))[2:] # 10
            b = hex(random.randint(16**5+1, 16**6))[2:] # 6
            c = str(random.randint(102, 999)) # 3
            d = oct(int(dt.date.today().strftime('%Y%m%d')))[2:]
            lef = d + b + c + a
            e = hex(random.randint(16**(32-len(lef)-1)+1, 16**(32 - len(lef))))[2:]
            return lef + e

        matarial_id = id_gen()

        db.session.add(
            Matarial(
                matarial_id = matarial_id,
                matarial_name = matarial_name,
                notes = notes if notes else None,
                unit = unit
            )
        )
        db.session.commit()
    
    @check_id
    def modify(self, matarial_name:str, unit: str, notes: str):
        query1 = db.session.query(
            Matarial
        ).filter(
            Matarial.matarial_id == self.matarial_id
        ).first()
        if query1.matarial_name != matarial_name:
            query1.matarial_name = matarial_name
        if query1.notes != notes:
            query1.notes = notes
        if query1.unit != unit:
            query1.unit = unit

        db.session.commit()
    @check_id
    def modify_remaining(self, **kwargs):
        storehouse_id = kwargs['storehouse_id']
        matarial_id = self.matarial_id
        remaining = float(kwargs['remaining'])

        query = db.session.query(
            MatarialInStorehouse
        ).filter(
            MatarialInStorehouse.storehouse_id == storehouse_id,
            MatarialInStorehouse.matarial_id == matarial_id
        ).order_by(
            desc(MatarialInStorehouse.sn)
        ).first()
        
        delta = remaining - query.remaining
        assert delta != 0, "detal = 0"

        db.session.add(
            MatarialRemainingAdjustmentRecord(
                storehouse_id=storehouse_id,
                matarial_id=matarial_id,
                quantity=delta,
                date=dt.date.today()
            )
        )
        buying_record = db.session.query(
            MatarialBuyingRecord
        ).filter(
            MatarialBuyingRecord.remaining != 0,
            MatarialBuyingRecord.matarial_id == matarial_id
        ).order_by(
            MatarialBuyingRecord.sn
        ).first()
        
        if (buying_record.quantity - buying_record.remaining) >= delta and buying_record.remaining + delta >= 0:
            buying_record.remaining += delta
        else:
            buying_records = db.session.query(
                MatarialBuyingRecord
            ).filter(
                or_(
                    and_(delta > 0, MatarialBuyingRecord.sn < buying_record.sn),
                    and_(delta < 0, MatarialBuyingRecord.sn > buying_record.sn)
                ), 
                MatarialBuyingRecord.matarial_id == matarial_id
            )
            if delta > 0:
                buying_records = buying_records.order_by(
                    desc(MatarialBuyingRecord.sn)
                ).all()
            else:
                buying_records = buying_records.order_by(
                    MatarialBuyingRecord.sn
                ).all()
            buying_records = [buying_record] + buying_records

            i = 0
            while delta != 0:
                if (buying_records[i].quantity - buying_records[i].remaining) >= delta and buying_records[i].remaining + delta >= 0:
                    buying_records[i].remaining += delta
                    break
                else:
                    if delta > 0:
                        delta -= buying_records[i].quantity - buying_records[i].remaining
                        buying_records[i].remaining = buying_records[i].quantity
                    else: # delta < 0
                        delta += buying_records[i].remaining
                        buying_records[i].remaining = 0
                i += 1
        
        db.session.add(
            MatarialInStorehouse(
                matarial_id = matarial_id,
                storehouse_id = storehouse_id,
                date = dt.date.today(),
                remaining = remaining,
                notes = 'adjust remaining'
            )
        )
        db.session.commit()
        return ''
    @check_id
    def delete(self):
        db.session.query(
            Matarial
        ).filter(
            Matarial.matarial_id == self.matarial_id
        ).delete()
        db.session.commit()

    @check_id
    def get_buying_record(self, storehouse_id: str, sn: int=None):
        query = db.session.query(
            MatarialBuyingRecord.sn,
            MatarialBuyingRecord.matarial_id,
            MatarialSupplier.matarial_supplier_name,
            MatarialBuyingRecord.matarial_supplier_id,
            MatarialBuyingRecord.storehouse_id,
            MatarialBuyingRecord.buying_date,
            MatarialBuyingRecord.quantity,
            MatarialBuyingRecord.price,
            MatarialBuyingRecord.remaining,
        ).filter(
            MatarialBuyingRecord.matarial_id == self.matarial_id,
            MatarialBuyingRecord.storehouse_id == storehouse_id,
            or_(
                sn == None,
                MatarialBuyingRecord.sn == sn
            )
        ).join(
            MatarialSupplier
        ).all()
        return query
    @check_id
    def modify_buying_record(self, sn, buying_date, matarial_supplier_id, quantity, price, storehouse_id):
        matarial_id = self.matarial_id
        sh_query = db.session.query(
            MatarialInStorehouse
        ).filter(
            MatarialInStorehouse.matarial_id == matarial_id,
            MatarialInStorehouse.storehouse_id == storehouse_id
        ).order_by(
            desc(MatarialInStorehouse.sn)
        ).first()

        if sn:
            query = db.session.query(
                MatarialBuyingRecord
            ).filter(
                MatarialBuyingRecord.sn == sn
            ).first()

            quantity_delta = quantity - query.quantity # 庫存變化量
            if quantity_delta != 0:
                remaining = sh_query.remaining + quantity_delta
                db.session.add(
                    MatarialInStorehouse(
                        matarial_id = matarial_id,
                        storehouse_id = storehouse_id,
                        date = dt.date.today(),
                        remaining = remaining,
                        notes = 'modify purchase'
                    )
                )
            
            query.buying_date = buying_date
            query.matarial_supplier_id = matarial_supplier_id
            query.quantity = quantity
            query.price = price
            query.remaining += quantity_delta # 由前端確認變化量是否超過餘額
        else:
            new_record = MatarialBuyingRecord(
                matarial_id = matarial_id,
                storehouse_id=storehouse_id,
                matarial_supplier_id=matarial_supplier_id,
                buying_date = buying_date,
                quantity = quantity,
                price = price,
                remaining = quantity
            )
            db.session.add(new_record)

            if sh_query:
                db.session.add(
                    MatarialInStorehouse(
                        matarial_id = matarial_id,
                        storehouse_id = storehouse_id,
                        date = dt.date.today(),
                        remaining = sh_query.remaining + quantity,
                        notes = 'purchase'
                    )
                )
            else:
                db.session.add(
                    MatarialInStorehouse(
                        matarial_id = matarial_id,
                        storehouse_id = storehouse_id,
                        date = dt.date.today(),
                        remaining = quantity,
                        notes = 'first purchase'
                    )
                )

        db.session.commit()
    @check_id
    def remove_buying_rocord(self, sn) -> bool:
        matarial_id = self.matarial_id

        sql = db.session.query(
            MatarialBuyingRecord
        ).filter(
            MatarialBuyingRecord.sn == sn,
            MatarialBuyingRecord.matarial_id == matarial_id
        )
        query = sql.first()
        if query.quantity == query.remaining:
            sh_query = db.session.query(
                MatarialInStorehouse
            ).filter(
                MatarialInStorehouse.matarial_id == matarial_id,
                MatarialInStorehouse.storehouse_id == query.storehouse_id
            ).order_by(
                desc(MatarialInStorehouse.sn)
            ).first()
            
            db.session.add(
                MatarialInStorehouse(
                    matarial_id = matarial_id,
                    storehouse_id = query.storehouse_id,
                    date = dt.date.today(),
                    remaining = sh_query.remaining - query.quantity,
                    notes = 'delete purchase'
                )
            )

            sql.delete()

            db.session.commit()
            return True
        else:
            return False


    # using
    @check_id
    def get_using_record(self, storehouse_id: str=None) -> tuple:
        matarial_id = self.matarial_id
        query = db.session.query(
            MatarialUsingRecord.sn,
            MatarialUsingRecord.matarial_id,
            MatarialUsingRecord.storehouse_id,
            MatarialUsingRecord.matarial_buying_sn,
            MatarialUsingRecord.date,
            MatarialUsingRecord.project_id,
            MatarialUsingRecord.quantity,
            MatarialUsingRecord.employee_id,
            Project.project_name
        ).filter(
            MatarialUsingRecord.matarial_id == matarial_id,
            or_(
                storehouse_id == None,
                MatarialUsingRecord.storehouse_id == storehouse_id
            )
        ).join(
            Project
        ).order_by(
            desc(MatarialUsingRecord.date)
        ).all()

        return query
    @check_id
    def modify_using_record(self, sn:str, using_date:str, quantity:float, project_id:str, storehouse_id: str, employee_id: str):
        matarial_id = self.matarial_id
        matarial_query = db.session.query(
            MatarialInStorehouse
        ).filter(
            MatarialInStorehouse.matarial_id == matarial_id,
            MatarialInStorehouse.storehouse_id == storehouse_id
        ).order_by(
            desc(MatarialInStorehouse.sn)
        ).first()
        def buying_and_using_record(quantity):
            buying_query = db.session.query(
                MatarialBuyingRecord
            ).filter(
                MatarialBuyingRecord.matarial_id == matarial_id,
                MatarialBuyingRecord.remaining != 0
            ).order_by(
                asc(MatarialBuyingRecord.buying_date)
            ).all()
            for buying_record in buying_query:
                if buying_record.remaining >= quantity:
                    new_using_record = MatarialUsingRecord(
                        matarial_id = matarial_id,
                        storehouse_id = storehouse_id,
                        matarial_buying_sn = buying_record.sn,
                        date = using_date,
                        project_id = project_id,
                        quantity = quantity,
                        employee_id = employee_id,
                    )
                    db.session.add(new_using_record)

                    buying_record.remaining -= quantity
                    break
                else:
                    new_using_record = MatarialUsingRecord(
                        matarial_id = matarial_id,
                        storehouse_id = storehouse_id,
                        matarial_buying_sn = buying_record.sn,
                        date = using_date,
                        project_id = project_id,
                        quantity = buying_record.remaining,
                        employee_id = employee_id,
                    )
                    db.session.add(new_using_record)
                    
                    quantity -= buying_record.remaining
                    buying_record.remaining = 0
        if sn:
            using_record_query = db.session.query(
                MatarialUsingRecord
            ).filter(
                MatarialUsingRecord.matarial_id == matarial_id,
                MatarialUsingRecord.sn == sn
            ).first()
            quantity_delta = quantity - using_record_query.quantity
            assert matarial_query.remaining >= quantity_delta, "餘額不足"
            
            if quantity_delta != 0:
                db.session.add(
                    MatarialInStorehouse(
                        matarial_id = matarial_id,
                        storehouse_id = storehouse_id,
                        date = using_date,
                        remaining = matarial_query.remaining - quantity_delta,
                        notes = 'modify used'
                    )
                )
                buying_record_remaining = using_record_query.MatarialBuyingRecord.remaining
                if buying_record_remaining <= quantity_delta:
                    if buying_record_remaining != 0:
                        using_record_query.MatarialBuyingRecord.remaining = 0
                        using_record_query.quantity += buying_record_remaining
                        quantity_delta -= buying_record_remaining
                    buying_and_using_record(quantity_delta)
                else:
                    # 還有餘額(buying record)可以扣
                    using_record_query.MatarialBuyingRecord.remaining -= quantity_delta
                    using_record_query.quantity = quantity
            
            using_record_query.date = using_date
            using_record_query.project_id = project_id
            db.session.commit()
        else:
            assert matarial_query.remaining >= quantity, f"餘額不足{matarial_query.remaining} > {quantity}"
            # total change
            db.session.add(
                MatarialInStorehouse(
                    matarial_id = matarial_id,
                    storehouse_id = storehouse_id,
                    date = using_date,
                    remaining = matarial_query.remaining - quantity,
                    notes = 'used'
                )
            )
            # buying record and using record change
            buying_and_using_record(quantity)
            db.session.commit()
    @check_id
    def remove_using_rocord(self, sn) -> bool:
        matarial_id = self.matarial_id

        sql = db.session.query(
            MatarialUsingRecord
        ).filter(
            MatarialUsingRecord.sn == sn,
            MatarialUsingRecord.matarial_id == matarial_id
        )
        using_record_query = sql.first()

        matarial_query = db.session.query(
            MatarialInStorehouse
        ).filter(
            MatarialInStorehouse.matarial_id == matarial_id,
            MatarialInStorehouse.storehouse_id == using_record_query.storehouse_id
        ).order_by(
            desc(MatarialInStorehouse.sn)
        ).first()
        
        db.session.add(
            MatarialInStorehouse(
                matarial_id = matarial_id,
                storehouse_id = using_record_query.storehouse_id,
                date = dt.date.today(),
                remaining = matarial_query.remaining + using_record_query.quantity, # total
                notes = 'delete used'
            )
        )

        using_record_query.MatarialBuyingRecord.remaining += using_record_query.quantity # buying record
        sql.delete()
        db.session.commit()
        return True
    @check_id
    def get_transfer_record(self):
        q1 = db.session.query(
            Storehouse
        ).subquery()
        q2 = db.session.query(
            Storehouse
        ).subquery()
        query = db.session.query(
            MatarialTransferRecord.date,
            MatarialTransferRecord.matarial_id,
            Matarial.matarial_name,
            MatarialTransferRecord.storehouse_id_from,
            q1.c.storehouse_name.label('storehouse_name_from'),
            MatarialTransferRecord.storehouse_id_to,
            q2.c.storehouse_name.label('storehouse_name_to'),
            MatarialTransferRecord.quantity
        ).join(
            Matarial
        ).join(
            q1,
            MatarialTransferRecord.storehouse_id_from == q1.c.storehouse_id
        ).join(
            q2,
            MatarialTransferRecord.storehouse_id_to == q2.c.storehouse_id
        ).filter(
            MatarialTransferRecord.matarial_id == self.matarial_id
        ).order_by(
            desc(MatarialTransferRecord.sn)
        ).all()
        return query

    @check_id
    def modify_transfer_record(self, **kwargs):
        kwargs['date'] = dt.date.today()
        kwargs['matarial_id'] = self.matarial_id
        db.session.add(
            MatarialTransferRecord(
                **kwargs
            )
        )
        fmatarial_query = db.session.query(
            MatarialInStorehouse
        ).filter(
            MatarialInStorehouse.matarial_id == self.matarial_id,
            MatarialInStorehouse.storehouse_id == kwargs['storehouse_id_from']
        ).order_by(
            desc(MatarialInStorehouse.sn)
        ).first()

        db.session.add(
            MatarialInStorehouse(
                matarial_id = self.matarial_id,
                storehouse_id = kwargs['storehouse_id_from'],
                date = dt.date.today(),
                remaining = fmatarial_query.remaining - kwargs['quantity'],
                notes = 'transfer o'
            )
        )

        tmatarial_query = db.session.query(
            MatarialInStorehouse
        ).filter(
            MatarialInStorehouse.matarial_id == self.matarial_id,
            MatarialInStorehouse.storehouse_id == kwargs['storehouse_id_to']
        ).order_by(
            desc(MatarialInStorehouse.sn)
        ).first()
        
        db.session.add(
            MatarialInStorehouse(
                matarial_id = self.matarial_id,
                storehouse_id = kwargs['storehouse_id_to'],
                date = dt.date.today(),
                remaining = tmatarial_query.remaining + kwargs['quantity'] if tmatarial_query else kwargs['quantity'],
                notes = 'transfer i'
            )
        )

        db.session.commit()

    # 
    def get_matarials(self, storehouse_id: str='') -> tuple:
        row_number_column = func.row_number().over(partition_by=(MatarialInStorehouse.matarial_id, MatarialInStorehouse.matarial_id), order_by=desc(MatarialInStorehouse.sn)).label('row_num')
        sub_query = db.session.query(
            MatarialInStorehouse.matarial_id,
            MatarialInStorehouse.storehouse_id,
            MatarialInStorehouse.date,
            MatarialInStorehouse.remaining,
        ).filter(
            or_(
                storehouse_id == '',
                MatarialInStorehouse.storehouse_id == storehouse_id
            )
        ).order_by(
            desc(MatarialInStorehouse.sn)
        )
        sub_query = sub_query.add_column(row_number_column)
        sub_query = sub_query.from_self().filter(row_number_column == 1).subquery()

        matarials_query = db.session.query(
            Matarial.matarial_id,
            Matarial.matarial_name,
            Matarial.notes,
            Matarial.unit,
            sub_query.c.matarial_in_storehouse_storehouse_id.label('storehouse_id'),
            sub_query.c.matarial_in_storehouse_remaining.label('remaining')
        ).outerjoin(
            sub_query
        ).order_by(
            Matarial.matarial_name
        ).all()
        return matarials_query