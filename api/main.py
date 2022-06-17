import array
from sqlalchemy.orm import Session
from . import crud, schema

from typing import List
from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, Request, Response
import uvicorn


app = FastAPI(
    title="Pregnancy diagnostic",
    description="""
Pregnancy diagnostic API
## Users

You will be able to:

* **Read data**.
* **Create data** (_not implemented_).
* **Edit data** (_not implemented_).
* **Delete data** (_not implemented_).

""",
    version="V0.1",
    docs_url="/"
)


"""@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = database.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response"""
@app.get("/debug", tags=["debug"])
def debug():
    import pdb; pdb.set_trace()


@app.get("/data/pages/{page}", tags=["get"])
def get_by_page(page: int, columns_to_show: list[schema.List_cols] = Query(...), db: Session = Depends(crud.get_db)):
    return crud.get_by_page(page, columns_to_show, db)

@app.get("/data/filterMMA", tags=["get"])
def max_of(column_to_filter: schema.List_cols = Query(...), filter_value: schema.listMMA = Query(...),  db: Session = Depends(crud.get_db)):
    return crud.get_MMA_of(column_to_filter, filter_value, db)

@app.get("/data/multi_filter", tags=["get"])
def filter_with_value(columns_to_show: list[schema.List_cols] = Query(...), columns_to_filter: list[schema.List_cols] = Query(...),
filters_values: list[float] = Query(...), filters_symbols: tuple[schema.list_symbols] = Query(...), db: Session = Depends(crud.get_db)):  
    return crud.return_query(columns_to_show, columns_to_filter, filters_symbols, filters_values, db)

@app.get("data/range_filter", tags=["get"])
def filter_in_range(columns_to_show: list[schema.List_cols] = Query(...), columns_to_filter_by_range: list[schema.List_cols] = Query(...),
symbol1: tuple[schema.list_symbols] = Query(...), filters_values1: list[float] = Query(...), symbol2: tuple[schema.list_symbols] = Query(...),
filters_values2: list[float] = Query(...), num_results:int = Query(...), db: Session = Depends(crud.get_db)):
    return crud.return_query(columns_to_show, columns_to_filter_by_range, filters_values1, symbol1, db, num_results, columns_to_filter_by_range, filters_values2, symbol2)


if __name__ == '__main__':
    uvicorn.run(app, port = 3000, host='0.0.0.0')
