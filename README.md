migrations to sql server

Activar - el entorno virtual con:
``` 
#para windows
    venv2\Scripts\activate
#para linux
    source venv/bin/activate
pip install -r requirements.txt

#para windows
    set FLASK_APP=app/main.py
#para linux
    export FLASK_APP=app/main.py
    
#Para llevar un control de las migraciones, para nuestro ambiente local usaremos:
flask db init --directory migrationsLocal
flask db migrate --directory migrationsLocal
flask db upgrade --directory migrationsLocal