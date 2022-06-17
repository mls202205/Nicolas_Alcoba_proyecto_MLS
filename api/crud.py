from sqlalchemy.orm import Session
from sqlalchemy import func, literal_column
from fastapi import HTTPException
from . import schema, database

def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


def get_columns_picked(columns: list[schema.List_cols]):
    #converts a list of columns names to a str
    cant_col = len(columns)
    print(cant_col)
    final_cols:str = ""
    while cant_col > 0:
        aux = columns.pop(0)
        final_cols = final_cols + "models.fetal_health.{}, ".format(aux)
        cant_col -= 1
    final_cols[:-2]
    return final_cols

def get_filter_with_values(columns: list[schema.List_cols], values: list[float], symbols: list[schema.list_symbols]):
    #converts a list of columns names and a list of values to a single str
    cant_names = len(columns)
    cant_values = len(values)
    cant_symbols = len(symbols)
    if cant_names != cant_values != cant_symbols: raise HTTPException(status_code=400, detail="The amount of filter names, values and symbols must be the same")
    filters:str = ""
    while cant_values > 0:
        auxCol = columns.pop(0)
        auxVal = values.pop(0)
        auxSymb = symbols.pop(0)
        filters = filters + "models.fetal_health.{} {} {}, ".format(auxCol, auxSymb, auxVal)
        cant_values -= 1
    filters[:-2]
    return filters


def return_query(columns_show: list[schema.List_cols], columns_filter: list[schema.List_cols], values: list[float], symbols: list[schema.list_symbols], db: Session, cant: int = 20, columns_filter2: list[schema.List_cols] = None, values2: list[float] = None, symbols2: list[schema.list_symbols] = None):
    show = get_columns_picked(columns_show)
    filters = get_filter_with_values(columns_filter, values, symbols)
    if columns_filter2 != None: #if more values are given, add them
        filters2 = get_filter_with_values(columns_filter2, values2, symbols2)
        filters = filters + ", " + filters2
    return db.query(literal_column(show)).filter(literal_column(filters)).offset(0).limit(cant).all()

def get_by_page(page: int, filters: list[schema.List_cols], db: Session):
    #give data without filter, 10 per page
    skip = 10 * page
    limit = skip + 10
    show = get_columns_picked(filters)
    return db.query(literal_column(show)).offset(skip).limit(limit).all()

def get_MMA_of(column: list[schema.List_cols], filter: schema.listMMA, db: Session):
    #give max, min, avg
    fix = "func." + filter + "(models.fetal_health." + column + ")"
    return db.query(fix).offset(0).limit(20).all()