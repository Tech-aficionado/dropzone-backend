from fastapi import APIRouter, FastAPI

from Routes.routes import Productsroute, Usersroute, defualtroute

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Allow cookies and other credentials
    allow_methods=["*"],  # Allow all HTTP methods (or specify)
    allow_headers=["*"],  # Allow all headers (or specify)
)


app.include_router(Usersroute)
app.include_router(defualtroute)
app.include_router(Productsroute)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
