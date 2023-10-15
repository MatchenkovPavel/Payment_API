from pydantic import BaseModel


class FinPut(BaseModel):
    """
    данные, которые можно передать в body, что получить фин операции
    """
    activity_type: list = ['DEPOSIT', 'ADJUSTMENT', 'WITHDRAWAL', 'FINANCING']


