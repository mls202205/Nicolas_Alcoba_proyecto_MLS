from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func, literal_column
from fastapi import HTTPException
from schema import schema
from models import models
from database import database
import torch
import numpy as np

def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


def get_columns_picked(columns: List[schema.List_cols]):
    #converts a list of columns names to a str
    cant_col = len(columns)
    final_cols:str = ""
    while cant_col > 0:
        aux = columns.pop(0)
        final_cols = final_cols + "models.fetal_health.{}, ".format(aux)
        cant_col -= 1
    final_cols[:-2]
    return final_cols

def get_filter_with_values(columns: List[schema.List_cols], values: list, symbols: List[schema.list_symbols]):
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


def return_query(columns_show: List[schema.List_cols], columns_filter: List[schema.List_cols], values: list, symbols: List[schema.list_symbols], db: Session, cant: int = 20, columns_filter2: List[schema.List_cols] = None, values2: list = None, symbols2: List[schema.list_symbols] = None):
    show = get_columns_picked(columns_show)
    filters = get_filter_with_values(columns_filter, values, symbols)
    if columns_filter2 != None: #if more values are given, add them
        filters2 = get_filter_with_values(columns_filter2, values2, symbols2)
        filters = filters + ", " + filters2
    return db.query(literal_column(show)).filter(literal_column(filters)).offset(0).limit(cant).all()

def get_by_page(page: int, filters: List[schema.List_cols], db: Session):
    #give data without filter, 10 per page
    skip = 10 * page
    limit = skip + 10
    show = get_columns_picked(filters)
    return db.query(literal_column(show)).offset(skip).limit(limit).all()

def get_MMA_of(column: List[schema.List_cols], filter: schema.listMMA, db: Session):
    #give max, min, avg
    fix = "func." + filter + "(models.fetal_health." + column + ")"
    return db.query(fix).offset(0).limit(20).all()

def modify_data(study_id: int, col_modify: List[schema.List_cols], modify_to: list, db: Session):
    aux = ""
    for i in modify_to:
        aux = aux + '"' + col_modify[i] + '": ' + modify_to[i] + ', '
    aux[:-2]
    db.query(models.fetal_health).filter(study_id == models.fetal_health.id).update({aux})
    db.commit()
    return "Ready!"



def delete_data(study_id: int, db: Session):
    aux: schema.Data = db.query(models.fetal_health).filter(study_id == models.fetal_health.id).first()
    aux.delete()
    db.commit()
    return aux

def new_data(data: schema.DataCreate, db: Session):
    db_data = models.fetal_health(baseline_value = data.baseline_value,
    accelerations = data.accelerations,
    fetal_movement = data.fetal_movement,
    uterine_contractions = data.uterine_contractions,
    light_decelerations = data.light_decelerations,
    severe_decelerations = data.severe_decelerations,
    prolongued_decelerations = data.prolongued_decelerations,
    abnormal_short_term_variability = data.abnormal_short_term_variability,
    mean_value_of_short_term_variability = data.mean_value_of_short_term_variability,
    percentage_of_time_with_abnormal_long_term_variability = data.percentage_of_time_with_abnormal_long_term_variability,
    mean_value_of_long_term_variability = data.mean_value_of_long_term_variability,
    histogram_width = data.histogram_width,
    histogram_min = data.histogram_min,
    histogram_max = data.histogram_max,
    histogram_number_of_peaks = data.histogram_number_of_peaks,
    histogram_number_of_zeroes = data.histogram_number_of_zeroes,
    histogram_mode = data.histogram_mode,
    histogram_mean = data.histogram_mean,
    histogram_median = data.histogram_median,
    histogram_variance = data.histogram_variance,
    histogram_tendency = data.histogram_tendency,
    fetal_health = data.fetal_health)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def load_model():
    model = schema.LR()
    model.load_state_dict(torch.load('./Model.pth'))
    return model

def get_pred(data: schema.DataBase, model = load_model()):
    aux = []
    for i in data:
        aux.append(i[1])
    aux = torch.tensor(aux, dtype=torch.float32)
    with torch.no_grad():
        pred = model(aux)
        pred = np.argmax(pred)
    return pred
