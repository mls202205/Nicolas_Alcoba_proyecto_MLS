from sqlalchemy import MetaData, inspect
from crud import crud
from database import database
from schema import schema
from models import models

from typing import List, Tuple
from sqlalchemy.orm import Session
from fastapi import Body, Depends, FastAPI, HTTPException, Query, Request, Response
import uvicorn


app = FastAPI(
    title="Pregnancy diagnostic",
    description="""
Pregnancy diagnostic API
## Users

You will be able to:

* **Read data**.
* **Create data**
* **Edit data**
* **Delete data**

""",
    version="V0.2",
    docs_url="/"
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = database.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.get("/debug", tags=["debug"])
def debug():
    import pdb; pdb.set_trace()


@app.get("/data/pages/{page}", tags=["get"])
def get_by_page(page: int, columns_to_show: List[schema.List_cols] = Query(description = "Select the columns you want to see"), db: Session = Depends(crud.get_db)):
    return crud.get_by_page(page, columns_to_show, db)

@app.get("/data/filterMMA", tags=["get"])
def max_of(column_to_filter: schema.List_cols = Query(...), filter_value: schema.listMMA = Query(...),  db: Session = Depends(crud.get_db)):
    return crud.get_MMA_of(column_to_filter, filter_value, db)

@app.get("/data/multi_filter", tags=["get"])
def filter_with_value(columns_to_show: List[schema.List_cols] = Query(...), columns_to_filter: List[schema.List_cols] = Query(...),
filters_values: List[float] = Query(...), filters_symbols: Tuple[schema.list_symbols] = Query(...), db: Session = Depends(crud.get_db)):  
    return crud.return_query(columns_to_show, columns_to_filter, filters_symbols, filters_values, db)

@app.get("/data/range_filter", tags=["get"])
def filter_in_range(columns_to_show: List[schema.List_cols] = Query(...), columns_to_filter_by_range: List[schema.List_cols] = Query(...),
symbol1: Tuple[schema.list_symbols] = Query(...), filters_values1: List[float] = Query(...), symbol2: Tuple[schema.list_symbols] = Query(...),
filters_values2: List[float] = Query(...), num_results:int = Query(...), db: Session = Depends(crud.get_db)):
    return crud.return_query(columns_to_show, columns_to_filter_by_range, filters_values1, symbol1, db, num_results, columns_to_filter_by_range, filters_values2, symbol2)

@app.post("/data/new_study", tags=["post"])
def new_study(data: schema.DataCreate = Body(...), db: Session = Depends(crud.get_db)):
    return crud.new_data(data, db)

@app.patch("/data/edit", tags=["edit"])
def edit_study(study_id: int, cols_to_update: List[schema.List_cols] = Query(...), data: List[float] = Query(...), db: Session = Depends(crud.get_db)):
    return crud.modify_data(study_id, cols_to_update, data, db)

@app.delete("/data/delete", tags=["delete"])
def delete_study(study_id: int, db: Session = Depends(crud.get_db)):
    return crud.delete_data(study_id, db)

@app.get("/create_table", include_in_schema=True)
def create_table(db: Session = Depends(crud.get_db)):
    ins =  inspect(database.engine).has_table("fetal_health")
    if ins == "fetal_health": return "Already exists"
    database.Base.metadata.create_all(database.engine, models.fetal_health)
    return "Ready!"

@app.post("/predict", tags=["get"])
def get_prediction(data: schema.DataBase = Body(...)):
    pred = crud.get_pred(data)
    if pred==2: return 'Prediction: Pathological'
    if pred==1: return 'Prediction: Suspicious'
    return 'Prediction: Normal'