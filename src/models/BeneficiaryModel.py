# app/src/models/CatalogoModel.py
from pkgutil import ModuleInfo
from marshmallow import fields, Schema, validate
import datetime
from .StatusModel import EstatusUsuariosModel, EstatusUsuariosSchema
from .EmployersModel import EmployersModel
from sqlalchemy import desc
import sqlalchemy
from . import db
from sqlalchemy import Date,cast
from sqlalchemy import or_
class BeneficiaryModel(db.Model):
    """
    Catalogo Model
    """
    __tablename__ = 'invBeneficiarios'

    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.Text)
    nombre = db.Column(db.String(100))
    parentezco = db.Column(db.String(100))
    statusId= db.Column(
        db.Integer,db.ForeignKey("invStatusUsuarios.id"),nullable=False
    )
    empleadoId= db.Column(
        db.Integer,db.ForeignKey("invEmpleados.id"),nullable=False
    )
    fechaAlta = db.Column(db.Date)
    fechaUltimaModificacion = db.Column(db.DateTime)
    fechaNacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(100))

    status=db.relationship(
        "EstatusUsuariosModel",backref=db.backref("invStatusUsuarios",lazy=True)
    )
    empleado=db.relationship(
        "EmployersModel",backref=db.backref("invEmpleados",lazy=True)
    )



    def __init__(self, data):
        """
        Class constructor
        """
        self.nombre = data.get("codigo")
        self.foto = data.get("foto")
        self.parentezco = data.get("parentezco")
        self.sexo = data.get("sexo")
        self.statusId = data.get("statusId")
        self.fechaNacimiento = data.get("fechaNacimiento")
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
        return BeneficiaryModel.query.order_by(BeneficiaryModel.id).paginate(offset,limit,error_out=False) 


    @staticmethod
    def get_one_ben(id):
        return BeneficiaryModel.query.get(id)

    @staticmethod
    def get_devices_by_nombre(value):
        return BeneficiaryModel.query.filter_by(nombre=value).first()

    @staticmethod
    def get_devices_by_sexo(value):
        return BeneficiaryModel.query.filter_by(sexo=value).first()
    
    @staticmethod
    def get_device_by_nombre_like(value,offset,limit):
        return BeneficiaryModel.query.filter(BeneficiaryModel.nombre.ilike(f'%{value}%') ).order_by(BeneficiaryModel.id).paginate(offset,limit,error_out=False)





    @staticmethod
    def get_devices_by_query(jsonFiltros,offset=1,limit=100):
        #return DispositivosModel.query.filter_by(**jsonFiltros).paginate(offset,limit,error_out=False)
        return BeneficiaryModel.query.filter_by(**jsonFiltros).order_by(BeneficiaryModel.id).paginate(offset,limit,error_out=False) 


        

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
