from . import database, crud

from fastapi import Depends, FastAPI, Request, Response
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
def debug(db: database.Session = Depends(crud.get_db)):
    import pdb; pdb.set_trace()




if __name__ == '__main__':
    uvicorn.run(app, port = 3000, host='0.0.0.0')
