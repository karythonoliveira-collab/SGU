from flask_restful import Resource
from marshmallow import ValidationError
from src.schemas import servico_schema
from src.entities import servico
from flask import request, jsonify, make_response
from src.services import servico_services
from src import api


# POST-GET-PUT-DELETE
# Lidar com todos os serviços
class ServicoList(Resource):
    def get(self):
        servicos = servico_services.listar_servicos()
        schema = servico_schema.ServicoSchema(many=True)

        if not servicos:
            return make_response(jsonify({'message': 'Não existe serviço'}), 404)

        return make_response(jsonify(schema.dump(servicos)), 200)

    def post(self):
        schema = servico_schema.ServicoSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            novo_servico = servico.Servico(
                descricao=dados['descricao'],
                valor=dados['valor'],
                horario_duracao=dados['horario_duracao']
            )
            resultado = servico_services.cadastrar_servico(novo_servico)
            return make_response(jsonify(schema.dump(resultado)), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(ServicoList, '/servico')


class ServicoResource(Resource):
    def get(self, id_servico):
        servico_encontrado = servico_services.listar_servico_id(id_servico)
        schema = servico_schema.ServicoSchema()

        if not servico_encontrado:
            return make_response(jsonify({'message': 'Serviço não encontrado'}), 404)

        return make_response(jsonify(schema.dump(servico_encontrado)), 200)
    
    def put(self, id_servico):
        servico_encontrado = servico_services.listar_servico_id(id_servico)
        schema = servico_schema.ServicoSchema()

        if not servico_encontrado:
            return make_response(jsonify({'message': 'Serviço não encontrado'}), 404)

        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            resultado = servico_services.editar_servico(id_servico, servico.Servico(
                descricao=dados['descricao'],
                valor=dados['valor'],
                horario_duracao=dados['horario_duracao']
            ))
            return make_response(jsonify(schema.dump(resultado)), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)

    def delete(self, id_servico):
        servico_encontrado = servico_services.listar_servico_id(id_servico)

        if not servico_encontrado:
            return make_response(jsonify({'message': 'Serviço não encontrado'}), 404)

        try:
            servico_services.excluir_servico(id_servico)
            return make_response(jsonify({'message': 'Serviço excluído com sucesso'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(ServicoResource, '/servico/<int:id_servico>')  # /servico/1
