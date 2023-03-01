from flask import Flask, request, json, Response, Blueprint, g
from marshmallow import ValidationError
from ..models.EmployersModel import EmployersModel, EmployersSchema,EmployersSchemaUpdate
from ..models.BeneficiaryModel import BeneficiaryModel, BeneficiarySchema, BeneficiarySchemaUpdate,BeneficiarySchemaQuery
from ..models.RolesModel import RolesModel
from ..models.StatusModel import EstatusUsuariosModel
from ..models import db
from ..services import returnCodes
from flask_restx import Api,fields,Resource
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Beneficiary_api = Blueprint("beneficiary_api", __name__)
beneficiary_schema = BeneficiarySchema()
beneficiary_schema_update = BeneficiarySchemaUpdate()
beneficiary_schema_query = BeneficiarySchemaQuery()
api = Api(Beneficiary_api)

nsBeneficiary = api.namespace("beneficiaries", description="API operations for beneficiary")

UsersModelApi = nsBeneficiary.model(
    "beneficiarios",
    {
     
        "nombre": fields.String(required=True, description="nombre"),
        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password"),
        "foto":fields.String( description="foto"),
        "rolId":fields.Integer(required=True, description="rolId"),
        "statusId":fields.Integer(required=True, description="statusId"),
        "fechaNacimiento":fields.String(required=True, description="fecha nacimiento"),
        "sexo":fields.String(required=True, description="genero"),
        "parentezco":fields.String(required=True, description="puesto")

    }
)

UsersModelQueryApi = nsBeneficiary.model(
    "beneficiariosquery",
    {
     
        "nombre": fields.String(required=True, description="nombre"),
        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password"),
        "foto":fields.String( description="foto"),
        "rolId":fields.Integer(required=True, description="rolId"),
        "statusId":fields.Integer(required=True, description="statusId"),
        "fechaNacimiento":fields.String(required=True, description="fecha nacimiento"),
        "sexo":fields.String(required=True, description="genero"),
        "parentezco":fields.String(required=True, description="puesto")
    }
)


UsersModelListApi = nsBeneficiary.model('usersList', {
    'beneficiarioslist': fields.List(fields.Nested(UsersModelApi)),
})

UsersPutApi = nsBeneficiary.model(
    "beneficiariosPut",
    {
        "id": fields.Integer(required=True, description="identificador"),
        "nombre": fields.String(required=True, description="nombre"),
        "username":fields.String(required=True, description="username"),
        "password":fields.String(required=True, description="password"),
        "foto":fields.String( description="foto"),
        "rolId":fields.Integer(required=True, description="rolId"),
        "statusId":fields.Integer(required=True, description="statusId"),
        "fechaNacimiento":fields.String(required=True, description="fecha nacimiento"),
        "sexo":fields.String(required=True, description="genero"),
        "parentezco":fields.String(required=True, description="puesto")
        
    }
)

def createUsers(req_data, listaObjetosCreados, listaErrores):
    data = None
    try:
        data = beneficiary_schema.load(req_data)
    except ValidationError as err:
     
        error = returnCodes.partial_response("TPM-2",str(err))
        listaErrores.append(error)
        return returnCodes.custom_response(None, 400, "TPM-2", str(err))

    # Aquí hacemos las validaciones para ver si el catalogo de negocio ya existe previamente

    employer_in_db = EmployersModel.get_one_emp(data.get("empleadoId"))
    if not employer_in_db:
        error = returnCodes.partial_response("TPM-5","",data.get("empleadoId"))
        listaErrores.append(error)
        return returnCodes.custom_response(None, 409, "TPM-5", "", data.get("empleadoId"))

    user_in_db = BeneficiaryModel.get_beneficiary_by_nombre(data.get("nombre"))
    if user_in_db:
        error = returnCodes.partial_response("TPM-5","",data.get("nombre"))
        listaErrores.append(error)
        return returnCodes.custom_response(None, 409, "TPM-5", "", data.get("nombre"))

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


    user = BeneficiaryModel(data)

    try:
        user.save()
    except Exception as err:
        error = returnCodes.custom_response(None, 500, "TPM-7", str(err)).json
        error = returnCodes.partial_response("TPM-7",str(err))
        listaErrores.append(error)
        db.session.rollback()
        return returnCodes.custom_response(None, 500, "TPM-7", str(err))
    
    serialized_user = beneficiary_schema.dump(user)
    listaObjetosCreados.append(serialized_user)
    return returnCodes.custom_response(serialized_user, 201, "TPM-1")


@nsBeneficiary.route("")
class UsersList(Resource):
    @nsBeneficiary.doc("lista de beneficiarios")
    def get(self):
        """List all status"""
        print('getting')
        users = BeneficiaryModel.get_all_ben()
        #return catalogos
        serialized_users = beneficiary_schema.dump(users, many=True)
        return returnCodes.custom_response(serialized_users, 200, "TPM-3")

    @nsBeneficiary.doc("Crear beneficiario")
    @nsBeneficiary.expect(UsersModelApi)
    @nsBeneficiary.response(201, "created")
    @nsBeneficiary.response(409, "conflicto")
    def post(self):
        if request.is_json is False:
            return returnCodes.custom_response(None, 400, "TPM-2")

        req_data = request.json
        if(not req_data):
            return returnCodes.custom_response(None, 400, "TPM-2")
        try:
            data = beneficiary_schema.load(req_data)
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
    
    @nsBeneficiary.doc("actualizar usuario")
    @nsBeneficiary.expect(UsersPutApi)
    def put(self):
        if request.is_json is False:
            return returnCodes.custom_response(None, 400, "TPM-2")
        req_data = request.json
        data = None
        if(not req_data):
            return returnCodes.custom_response(None, 400, "TPM-2")
        try:
            data = beneficiary_schema_update.load(req_data, partial=True)
        except ValidationError as err:
            return returnCodes.custom_response(None, 400, "TPM-2", str(err))

        user = BeneficiaryModel.get_one_ben(data.get("id"))
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
            
        if "empleadoId" in data:
            employer_in_db = EmployersModel.get_one_emp(data.get("empleadoId"))
            if not employer_in_db:
                return returnCodes.custom_response(None, 409, "TPM-4", "empleado no encontrado", data.get("empleadoId"))

        try:
            user.update(data)
        except Exception as err:
            return returnCodes.custom_response(None, 500, "TPM-7", str(err))

        serialized_status = beneficiary_schema.dump(user)
        return returnCodes.custom_response(serialized_status, 200, "TPM-6")

@nsBeneficiary.route("/<int:id>")
@nsBeneficiary.param("id", "The id identifier")
@nsBeneficiary.response(404, "usuario no encontrado")
class OneCatalogo(Resource):
    @nsBeneficiary.doc("obtener un usuario")
    def get(self, id):
       
        rol = BeneficiaryModel.get_one_ben(id)
        if not rol:
            return returnCodes.custom_response(None, 404, "TPM-4")

        serialized_user = beneficiary_schema.dump(rol)
        return returnCodes.custom_response(serialized_user, 200, "TPM-3")

@nsBeneficiary.route("/query")
@nsBeneficiary.response(404, "usuario no encontrado")
class UserQuery(Resource):
    
    @nsBeneficiary.doc("obtener varios beneficiarios")
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
            data = beneficiary_schema_query.load(req_data, partial=True)
        except ValidationError as err:
            return returnCodes.custom_response(None, 400, "TPM-2", str(err))

        users = BeneficiaryModel.get_beneficiary_by_query(data,offset,limit)
        if not users:
            return returnCodes.custom_response(None, 404, "TPM-4")

        serialized_device = beneficiary_schema.dump(users.items,many=True)
        return returnCodes.custom_response(serialized_device, 200, "TPM-3")