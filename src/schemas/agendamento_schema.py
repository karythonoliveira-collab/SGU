from src import ma
from marshmallow import fields, validate, post_load
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
        load_instance = False  # Mudamos para False para não tentar instanciar automaticamente
        
    # Campos obrigatórios e validações
    dt_atendimento = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    id_user = fields.Integer(required=True)
    id_profissional = fields.Integer(required=True)
    id_servico = fields.Integer(required=True)
    status = fields.String(validate=validate.OneOf(
        ["agendado", "cancelado", "concluido"]), 
        load_default="agendado", dump_default="agendado")
    valor_total = fields.Float(load_default=0.00)
    taxa_cancelamento = fields.Float(load_default=0.00)
    
    # Campos calculados automaticamente (não enviados pelo cliente)
    dt_agendamento = fields.DateTime(dump_only=True)
    id = fields.Integer(dump_only=True)