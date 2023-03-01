from flask import Flask, request, json, Response, Blueprint, g
from marshmallow import ValidationError
from ..models.EmployersModel import EmployersModel, EmployersSchema,EmployersSchemaUpdate,EmployersLoginSchema,EmployersLoginUpdateSchema, EmployersSchemaQuery
from ..models.RolesModel import RolesModel
from ..models.StatusModel import EstatusUsuariosModel
from ..models import db
from ..services import returnCodes
from flask_restx import Api,fields,Resource
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Employer_api = Blueprint("employers_api", __name__)
employers_schema = EmployersSchema()
employers_schema_update = EmployersSchemaUpdate()
user_auth = EmployersLoginSchema()
user_pass_update = EmployersLoginUpdateSchema()
employers_schema_query = EmployersSchemaQuery()
api = Api(Employer_api)

nsEmployers = api.namespace("employers", description="API operations for employers")

UsersModelApi = nsEmployers.model(
    "empleados",
    {
     
        "nombre": fields.String(required=True, description="nombre"),
        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password"),
        "foto":fields.String( description="foto"),
        "rolId":fields.Integer(required=True, description="rolId"),
        "statusId":fields.Integer(required=True, description="statusId"),
        "fechaContratacion":fields.String(required=True, description="fecha nacimiento"),
        "sexo":fields.String(required=True, description="genero"),
        "puesto":fields.String(required=True, description="puesto"),
        "salario":fields.Integer(required=True, description="salario")

    }
)

UsersModelQueryApi = nsEmployers.model(
    "empleadosquery",
    {
     
        "nombre": fields.String(required=True, description="nombre"),
        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password"),
        "foto":fields.String( description="foto"),
        "rolId":fields.Integer(required=True, description="rolId"),
        "statusId":fields.Integer(required=True, description="statusId"),
        "fechaContratacion":fields.String(required=True, description="fecha nacimiento"),
        "sexo":fields.String(required=True, description="genero"),
        "puesto":fields.String(required=True, description="puesto"),
        "salario":fields.Integer(required=True, description="salario")
    }
)

UsersModelLoginApi = nsEmployers.model(
    "empleadosLogin",
    {

        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password"),

    }
)

UsersModelLoginpassUpdateApi = nsEmployers.model(
    "empleadosUpdatePass",
    {
     
       "id": fields.Integer(required=True, description="identificador"),
        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password")
        
    }
)

UsersModelListApi = nsEmployers.model('usersList', {
    'empleadoslist': fields.List(fields.Nested(UsersModelApi)),
})

UsersPutApi = nsEmployers.model(
    "empleadosPut",
    {
        "id": fields.Integer(required=True, description="identificador"),
        "nombre": fields.String(required=True, description="nombre"),
        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password"),
        "foto":fields.String( description="foto"),
        "rolId":fields.Integer(required=True, description="rolId"),
        "statusId":fields.Integer(required=True, description="statusId"),
        "fechaContratacion":fields.String(required=True, description="fecha nacimiento"),
        "sexo":fields.String(required=True, description="genero"),
        "puesto":fields.String(required=True, description="puesto"),
        "salario":fields.Integer(required=True, description="salario")
        
    }
)

def createUsers(req_data, listaObjetosCreados, listaErrores):
    data = None
    try:
        data = employers_schema.load(req_data)
    except ValidationError as err:
     
        error = returnCodes.partial_response("TPM-2",str(err))
        listaErrores.append(error)
        return returnCodes.custom_response(None, 400, "TPM-2", str(err))

    # Aquí hacemos las validaciones para ver si el catalogo de negocio ya existe previamente
    user_in_db = EmployersModel.get_employers_by_username(data.get("username"))
    if user_in_db:
        error = returnCodes.partial_response("TPM-5","",data.get("username"))
        listaErrores.append(error)
        return returnCodes.custom_response(None, 409, "TPM-5", "", data.get("username"))

    rol_in_db = RolesModel.get_one_rol(data.get("rolId"))
    if not rol_in_db:
        error = returnCodes.partial_response("TPM-4","",data.get("rolId"))
        listaErrores.append(error)
        return returnCodes.custom_response(None, 409, "TPM-4", "", data.get("rolId"))

    status_in_db = EstatusUsuariosModel.get_one_status(data.get("statusId"))
    if not status_in_db:
        error = returnCodes.partial_response("TPM-4","",data.get("statusId"))
        listaErrores.append(error)
        return returnCodes.custom_response(None, 409, "TPM-4", "", data.get("statusId"))

    data['password'] = generate_password_hash(data['password'])

    user = EmployersModel(data)

    try:
        user.save()
    except Exception as err:
        error = returnCodes.custom_response(None, 500, "TPM-7", str(err)).json
        error = returnCodes.partial_response("TPM-7",str(err))
        #error="Error al intentar dar de alta el registro "+data.get("nombre")+", "+error["message"]
        listaErrores.append(error)
        db.session.rollback()
        return returnCodes.custom_response(None, 500, "TPM-7", str(err))
    
    serialized_user = employers_schema.dump(user)
    listaObjetosCreados.append(serialized_user)
    return returnCodes.custom_response(serialized_user, 201, "TPM-1")



@nsEmployers.route("/login")
class UsersLogin(Resource):
    @nsEmployers.doc("login usuario")
    @nsEmployers.expect(UsersModelLoginApi)
    @nsEmployers.response(201, "auth")
    def post(self):
        if request.is_json is False:
            return returnCodes.custom_response(None, 400, "TPM-2")

        req_data = request.json
        if(not req_data):
            return returnCodes.custom_response(None, 400, "TPM-2")
        try:
            data = user_auth.load(req_data)
        except ValidationError as err:    
            return returnCodes.custom_response(None, 400, "TPM-2", str(err))

        user = EmployersModel.get_employers_by_username(data.get("username"))
        if not user:
            
            return returnCodes.custom_response(None, 404, "TPM-4","Usuario no encontrado")

        if user.statusId==3:
            return returnCodes.custom_response(None, 409, "TPM-19","Usuario dado de baja")


        if check_password_hash(user.password,data['password'])==False:
            return returnCodes.custom_response(None, 401, "TPM-10","acceso no autorizado, usuario y/o contraseña incorrecto")
        serialized_user = employers_schema.dump(user)
        return returnCodes.custom_response(serialized_user, 201, "TPM-18")


@nsEmployers.route("/pass")
class Usersupdatepass(Resource):
    @nsEmployers.doc("cambiar password")
    @nsEmployers.expect(UsersModelLoginpassUpdateApi)
    @nsEmployers.response(200, "success")
    def put(self):
        if request.is_json is False:
            return returnCodes.custom_response(None, 400, "TPM-2")

        req_data = request.json
        if(not req_data):
            return returnCodes.custom_response(None, 400, "TPM-2")
        try:
            data = user_pass_update.load(req_data)
        except ValidationError as err:    
            return returnCodes.custom_response(None, 400, "TPM-2", str(err))

        user = EmployersModel.get_all_emp(data.get("id"))
        if not user:
            
            return returnCodes.custom_response(None, 404, "TPM-4","empleado no encontrado")

        data['password'] = generate_password_hash(data['password'])

        try:
            user.update(data)
        except Exception as err:
            return returnCodes.custom_response(None, 500, "TPM-7", str(err))

        
        serialized_user = employers_schema.dump(user)
        return returnCodes.custom_response(serialized_user, 201, "TPM-6")


@nsEmployers.route("")
class UsersList(Resource):
    @nsEmployers.doc("lista de  empleados")
    def get(self):
        """List all status"""
        print('getting')
        users = EmployersModel.get_all_users_ok()
        #return catalogos
        serialized_users = employers_schema.dump(users, many=True)
        return returnCodes.custom_response(serialized_users, 200, "TPM-3")

    @nsEmployers.doc("Crear usuario")
    @nsEmployers.expect(UsersModelApi)
    @nsEmployers.response(201, "created")
    def post(self):
        if request.is_json is False:
            return returnCodes.custom_response(None, 400, "TPM-2")

        req_data = request.json
        if(not req_data):
            return returnCodes.custom_response(None, 400, "TPM-2")
        try:
            data = employers_schema.load(req_data)
        except ValidationError as err:    
            return returnCodes.custom_response(None, 400, "TPM-2", str(err))
        
        listaObjetosCreados = list()
        listaErrores = list()
        
       
        createUsers(data, listaObjetosCreados, listaErrores)
        
        if(len(listaObjetosCreados)>0):
            if(len(listaErrores)==0):
                return returnCodes.custom_response(listaObjetosCreados, 201, "TPM-8")
            else:
                return returnCodes.custom_response(listaObjetosCreados, 201, "TPM-16", "",listaErrores)
        else:
            return returnCodes.custom_response(None, 409, "TPM-16","", listaErrores)
    
    @nsEmployers.doc("actualizar usuario")
    @nsEmployers.expect(UsersPutApi)
    def put(self):
        if request.is_json is False:
            return returnCodes.custom_response(None, 400, "TPM-2")
        req_data = request.json
        data = None
        if(not req_data):
            return returnCodes.custom_response(None, 400, "TPM-2")
        try:
            data = employers_schema_update.load(req_data, partial=True)
        except ValidationError as err:
            return returnCodes.custom_response(None, 400, "TPM-2", str(err))

        user = EmployersModel.get_one_emp(data.get("id"))
        if not user:
            
            return returnCodes.custom_response(None, 404, "TPM-4")
        if "rolId" in data:
            rol_in_db = RolesModel.get_one_rol(data.get("rolId"))
            if not rol_in_db:
    
                
                return returnCodes.custom_response(None, 409, "TPM-4", "", data.get("rolId"))

        if "statusId" in data:
            status_in_db = EstatusUsuariosModel.get_one_status(data.get("statusId"))
            if not status_in_db:
       
                
                return returnCodes.custom_response(None, 409, "TPM-4", "", data.get("statusId"))

        try:
            user.update(data)
        except Exception as err:
            return returnCodes.custom_response(None, 500, "TPM-7", str(err))

        serialized_status = employers_schema.dump(user)
        return returnCodes.custom_response(serialized_status, 200, "TPM-6")

@nsEmployers.route("/<int:id>")
@nsEmployers.param("id", "The id identifier")
@nsEmployers.response(404, "usuario no encontrado")
class OneCatalogo(Resource):
    @nsEmployers.doc("obtener un usuario")
    def get(self, id):
       
        rol = EmployersModel.get_one_emp(id)
        if not rol:
            return returnCodes.custom_response(None, 404, "TPM-4")

        serialized_user = employers_schema.dump(rol)
        return returnCodes.custom_response(serialized_user, 200, "TPM-3")

@nsEmployers.route("/query")

@nsEmployers.response(404, "usuario no encontrado")
class UserQuery(Resource):
    
    @nsEmployers.doc("obtener varios usuarios")
    @api.expect(UsersModelQueryApi)
    def post(self):
        print(request.args)
        offset = 1
        limit = 100

        if request.is_json is False:
            return returnCodes.custom_response(None, 400, "TPM-2")

        if "offset" in request.args:
            offset = request.args.get('offset',default = 1, type = int)

        if "limit" in request.args:
            limit = request.args.get('limit',default = 10, type = int)

        req_data = request.json
        data = None
        if(not req_data):
            return returnCodes.custom_response(None, 400, "TPM-2")
        try:
            data = employers_schema_query.load(req_data, partial=True)
        except ValidationError as err:
            return returnCodes.custom_response(None, 400, "TPM-2", str(err))

        users = EmployersModel.get_employers_by_query(data,offset,limit)
        if not users:
            return returnCodes.custom_response(None, 404, "TPM-4")

        serialized_device = employers_schema.dump(users.items,many=True)
        return returnCodes.custom_response(serialized_device, 200, "TPM-3")