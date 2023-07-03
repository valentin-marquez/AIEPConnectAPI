@echo off

REM Verifica si existe la carpeta del entorno virtual (.venv) y si no, crea una nueva

if not exist .venv (
    python -m venv .venv
)

REM Activa el entorno virtual (en Windows)
call .venv\Scripts\activate

REM Instala las dependencias del proyecto (si es necesario)
REM pip install -r requirements.txt

REM Inicia el servidor FastAPI
python main.py
