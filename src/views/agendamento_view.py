from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from src.schemas import agendamento_schema
from src.entities import agendamento
from src.services import agendamento_services
from src import api

# Lidar com todos os agendamentos
class AgendamentoList(Resource):
    def get(self):
        agendamentos = agendamento_services.listar_agendamentos()
        schema = agendamento_schema.AgendamentoSchema(many=True)

        if not agendamentos:
            return make_response(jsonify({'message': 'Não existe agendamento'}), 404)

        return make_response(jsonify(schema.dump(agendamentos)), 200)

    def post(self):
        schema = agendamento_schema.AgendamentoSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            novo_agendamento = agendamento.Agendamento(
                dt_atendimento=dados['dt_atendimento'],
                id_user=dados['id_user'],
                id_profissional=dados['id_profissional'],
                id_servico=dados['id_servico'],
                valor_total=dados.get('valor_total', 0.00)
            )
            resultado = agendamento_services.cadastrar_agendamento(novo_agendamento)
            return make_response(jsonify(schema.dump(resultado)), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(AgendamentoList, '/agendamento')


# Lidar com um agendamento específico
class AgendamentoResource(Resource):
    def get(self, id_agendamento):
        agendamento_encontrado = agendamento_services.listar_agendamento_id(id_agendamento)
        schema = agendamento_schema.AgendamentoSchema()

        if not agendamento_encontrado:
            return make_response(jsonify({'message': 'Agendamento não encontrado'}), 404)

        return make_response(jsonify(schema.dump(agendamento_encontrado)), 200)

    def put(self, id_agendamento):
        agendamento_encontrado = agendamento_services.listar_agendamento_id(id_agendamento)
        schema = agendamento_schema.AgendamentoSchema()

        if not agendamento_encontrado:
            return make_response(jsonify({'message': 'Agendamento não encontrado'}), 404)

        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            resultado = agendamento_services.editar_agendamento(
                id_agendamento,
                agendamento.Agendamento(
                    dt_atendimento=dados['dt_atendimento'],
                    id_user=dados['id_user'],
                    id_profissional=dados['id_profissional'],
                    id_servico=dados['id_servico'],
                    valor_total=dados.get('valor_total', 0.00)
                )
            )
            return make_response(jsonify(schema.dump(resultado)), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)

    def delete(self, id_agendamento):
        agendamento_encontrado = agendamento_services.listar_agendamento_id(id_agendamento)

        if not agendamento_encontrado:
            return make_response(jsonify({'message': 'Agendamento não encontrado'}), 404)

        try:
            agendamento_services.excluir_agendamento(id_agendamento)
            return make_response(jsonify({'message': 'Agendamento excluído com sucesso'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(AgendamentoResource, '/agendamento/<int:id_agendamento>')  # /agendamento/1
