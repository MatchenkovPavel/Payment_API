from fastapi import FastAPI, Depends, HTTPException

from tables import Activities, ActivityLegs, Accounts, Principals, Instruments
from schema import FinOperationGet
from databases import SessionLocal
from models import FinPut

from sqlalchemy.orm import Session

from typing import List
from loguru import logger
from datetime import date


app = FastAPI()


def db_connect():
    with SessionLocal() as dxcore:
        return dxcore


@app.get('/fin/all', response_model=List[FinOperationGet])
def get_fin_all(act_types: FinPut,
                limit: int=10,
                date_from: str='2023-03-01',
                date_to: str=str(date.today()),
                dxcore: Session=Depends(db_connect)
                ) -> FinOperationGet:
    logger.info(act_types.activity_type)
    result = (
        dxcore.query(
            Accounts.account_id,
            Activities.activity_type,
            Activities.created_time,
            Principals.up,
            Activities.description,
            Instruments.symbol,
            ActivityLegs.quantity
        )
        .order_by(Activities.created_time)
        .filter(Activities.created_time.between(date_from, date_to))
        .filter(Accounts.clearing_code == 'LIVE')
        .filter(Activities.description.notilike('test_%'))
        .filter(Activities.description.notilike('demo%'))
        .filter(Activities.activity_type.in_(tuple(act_types.activity_type)))
        .limit(limit)
        .all()
    )
    logger.info(result)
    return result


@app.get('/fin/{user_id}')  # валидировать вывод
def get_fin_by_user(user_id: str, dxcore: Session=Depends(db_connect)):
    result = (
        dxcore.query(
            Principals.up,
            Accounts.account_id,
            Activities.activity_type,
            Activities.created_time,
            Activities.description,
            Instruments.symbol,
            ActivityLegs.quantity
        )
        .filter(Principals.up == user_id)
        .filter(Accounts.clearing_code == 'LIVE')
        #.filter((~(Activities.description.contains('demo|Demo|test|Test'))))
        .order_by(Activities.created_time.desc())
        .limit(5)
        .all()
    )
    logger.info(result)
    return result

