from dotenv import load_dotenv
from fastapi import FastAPI
from api.routes import router


load_dotenv()

app = FastAPI(
    title="AIEP API",
    description="API para obtener datos de AIEP",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,

)

# Rutas de la API
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
