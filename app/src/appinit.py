import imp
import random
from flask import Flask, current_app, render_template
from flask_cors import CORS
#from .config import app_config
from .models import db
from flask_migrate import Migrate
from .services import returnCodes
#from .views.LugaresView import lugares_api as lugares_blueprint
#from views.LugaresView import nsLugares as nsLugares


from .controllers.BeneficiaryController import nsBeneficiary
from .controllers.EmployersController import nsEmployers
from .controllers.RolesController import nsRoles
from .controllers.StatusController import nsStatusUser

from flask_restx import Api, fields, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import datetime
def create_app(env_name):
    """
    Create app
    """
    # app initiliazation
    app = Flask(__name__)
    # cors
    cors = CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://forrerunner97:Asterisco97@inventarioavs1.database.windows.net/avsInventory'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://master:peacesells2100@DESKTOP-FGFDBVD\\TEW_SQLEXPRESS/crud_manager'
    
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # La clave secreta que se utilizará para firmar los tokens JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 10
    jwt = JWTManager(app)

    db.init_app(app)

    migrate = Migrate(app, db)
    api = Api(app,title="Inventory API", version="1.1", description="A simple inventory API",)


   
    api.add_namespace(ns=nsEmployers,path="/api/v1/empleados")
    api.add_namespace(ns=nsBeneficiary,path="/api/v1/beneficiarios")
    api.add_namespace(ns=nsRoles,path="/api/v1/roles")
    api.add_namespace(ns=nsStatusUser,path="/api/v1/status")

    
    @app.errorhandler(404) 
    def not_found(e):
        return returnCodes.custom_response(None, 404, 4041, "TPM-4")

    @app.errorhandler(400)
    def bad_request(e):
        return returnCodes.custom_response(None, 400, 4001, "TPM-2")
    
    @app.errorhandler(401)
    def unauthorized(e):
        return returnCodes.custom_response(None, 409, 4001, "TPM-2","No autorizado, token invalido")



    return app