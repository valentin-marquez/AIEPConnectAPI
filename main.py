from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

load_dotenv()

app = FastAPI(
    title="AIEP API",
    description="API para obtener datos de AIEP",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,

)

# origins = [
#     "chrome-extension://bjpnoafcpgdhpfdniojakbpbonfehoci",
#     "http://localhost:8000",  # Agrega cualquier otro origen permitido si es necesario
#     "https://aiep-connect-api.vercel.app"
# ]

# # middlewares 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# Rutas de la API
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
