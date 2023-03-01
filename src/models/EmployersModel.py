# app/src/models/CatalogoModel.py
from pkgutil import ModuleInfo
from marshmallow import fields, Schema, validate
import datetime
from .StatusModel import EstatusUsuariosModel, EstatusUsuariosSchema
from .RolesModel import RolesSchema,RolesModel
from sqlalchemy import desc
import sqlalchemy
from . import db
from sqlalchemy import Date,cast
from sqlalchemy import or_
class EmployersModel(db.Model):
    """
    Catalogo Model
    """
    __tablename__ = 'invEmpleados'

    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.Text)
    nombre = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.Text)
    Puesto = db.Column(db.String(100))
    salario = db.Column(db.Integer)
    statusId= db.Column(
        db.Integer,db.ForeignKey("invStatusUsuarios.id"),nullable=False
    )
    fechaAlta = db.Column(db.Date)
    fechaUltimaModificacion = db.Column(db.DateTime)
    fechaContratacion = db.Column(db.Date)
    sexo = db.Column(db.String(100))

    status=db.relationship(
        "EstatusUsuariosModel",backref=db.backref("invStatusUsuarios",lazy=True)
    )
    rolId = db.Column(
        db.Integer,db.ForeignKey("invRoles.id"),nullable=False
    )

    rol=db.relationship(
        "RolesModel",backref=db.backref("invRoles",lazy=True)
    )



    def __init__(self, data):
        """
        Class constructor
        """
        self.nombre = data.get("codigo")
        self.foto = data.get("foto")
        self.sexo = data.get("sexo")
        self.statusId = data.get("statusId")
        username = data.get("username")
        password = data.get("password")
        puesto = data.get("puesto")
        salario = data.get("salario")
        fechaContratacion = data.get("fechaContratacion")
        rolId = data.get("rolId")
        self.fechaAlta = datetime.datetime.utcnow()
        self.fechaUltimaModificacion = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.fechaUltimaModificacion = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_ben(offset=1,limit=10):
        return EmployersModel.query.order_by(EmployersModel.id).paginate(offset,limit,error_out=False) 


    @staticmethod
    def get_one_ben(id):
        return EmployersModel.query.get(id)

    @staticmethod
    def get_devices_by_nombre(value):
        return EmployersModel.query.filter_by(nombre=value).first()

    @staticmethod
    def get_devices_by_sexo(value):
        return EmployersModel.query.filter_by(sexo=value).first()
    
    @staticmethod
    def get_device_by_nombre_like(value,offset,limit):
        return EmployersModel.query.filter(EmployersModel.nombre.ilike(f'%{value}%') ).order_by(EmployersModel.id).paginate(offset,limit,error_out=False)





    @staticmethod
    def get_devices_by_query(jsonFiltros,offset=1,limit=100):
        #return DispositivosModel.query.filter_by(**jsonFiltros).paginate(offset,limit,error_out=False)
        return EmployersModel.query.filter_by(**jsonFiltros).order_by(EmployersModel.id).paginate(offset,limit,error_out=False) 


        

    def __repr(self):
        return '<id {}>'.format(self.id)

class BeneficiarySchema(Schema):
    """
    Catalogo Schema
    """
    id = fields.Int()
    nombre = fields.Str(required=True, validate=[validate.Length(max=100)])
    foto = fields.Str()
    parentezco = fields.Str(required=True, validate=[validate.Length(max=100)])
    sexo = fields.Str(required=True, validate=[validate.Length(max=100)])
    statusId = costo = fields.Integer()
    fechaNacimiento = fechaAlta = fields.Date()
    fechaAlta = fechaAlta = fields.DateTime()
    fechaUltimaModificacion = fechaAlta = fields.DateTime()
    status = fields.Nested(EstatusUsuariosSchema)
    rolId = fields.Integer(required=True)
    rol=fields.Nested(RolesSchema)
    

class BeneficiarySchemaSomeFields(Schema):
    """
    Catalogo Schema
    """
    id = fields.Int()
    nombre = fields.Str(required=True, validate=[validate.Length(max=100)])
    foto = fields.Str()
    parentezco = fields.Str(required=True, validate=[validate.Length(max=100)])
    sexo = fields.Str(required=True, validate=[validate.Length(max=100)])
    statusId = costo = fields.Integer()
    fechaNacimiento = fechaAlta = fields.Date()
    fechaAlta = fechaAlta = fields.DateTime()
    fechaUltimaModificacion = fechaAlta = fields.DateTime()
    status = fields.Nested(EstatusUsuariosSchema)
    rolId = fields.Integer(required=True)
    rol=fields.Nested(RolesSchema)

class BeneficiarySchemaUpdate(Schema):
    """
    Catalogo Schema
    """
    id = fields.Int()
    nombre = fields.Str(required=True, validate=[validate.Length(max=100)])
    foto = fields.Str()
    parentezco = fields.Str(required=True, validate=[validate.Length(max=100)])
    sexo = fields.Str(required=True, validate=[validate.Length(max=100)])
    statusId = costo = fields.Integer()
    fechaNacimiento = fechaAlta = fields.Date()
    fechaAlta = fechaAlta = fields.DateTime()
    fechaUltimaModificacion = fechaAlta = fields.DateTime()
    status = fields.Nested(EstatusUsuariosSchema)
    rolId = fields.Integer(required=True)
    rol=fields.Nested(RolesSchema)


class BeneficiarySchemaQuery(Schema):
    """
    Catalogo Schema
    """
    id = fields.Int()
    nombre = fields.Str(required=True, validate=[validate.Length(max=100)])
    foto = fields.Str()
    parentezco = fields.Str(required=True, validate=[validate.Length(max=100)])
    sexo = fields.Str(required=True, validate=[validate.Length(max=100)])
    statusId = costo = fields.Integer()
    fechaNacimiento = fechaAlta = fields.Date()
    fechaAlta = fechaAlta = fields.DateTime()
    fechaUltimaModificacion = fechaAlta = fields.DateTime()
    status = fields.Nested(EstatusUsuariosSchema)
    rolId = fields.Integer(required=True)
    rol=fields.Nested(RolesSchema)
