from src import ma
from src.models import profissional_model
from marshmallow import fields

class ProfissionalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = profissional_model.ProfissionalModel
        fields = ('id', 'nome')

    nome = fields.String(required=True)
