from src import ma
from src.models import servicos_model
from marshmallow import fields

class ServicoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = servicos_model.ServicoModel
        fields = ('id', 'descricao', 'valor', 'horario_duracao')

    descricao = fields.String(required=True)
    valor = fields.Float(required=True)
    horario_duracao = fields.Float(required=True)
