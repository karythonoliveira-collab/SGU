from src import ma
from marshmallow import fields, validate
from src.models import agendamento_model

class AgendamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = agendamento_model.AgendamentoModel
        fields = (
            'id',
            'dt_agendamento',
            'dt_atendimento',
            'id_user',
            'id_profissional',
            'id_servico',
            'status',
            'valor_total',
            'taxa_cancelamento'
        )
        load_instance = True  # Para desserializar direto para a entidade

    # Campos obrigatórios e validações
    dt_atendimento = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    id_user = fields.Integer(required=True)
    id_profissional = fields.Integer(required=True)
    id_servico = fields.Integer(required=True)
    status = fields.String(validate=validate.OneOf(
        ["agendado", "cancelado", "concluido"]), load_default="agendado")
    valor_total = fields.Float(required=True)
    taxa_cancelamento = fields.Float(load_default=0.00)
