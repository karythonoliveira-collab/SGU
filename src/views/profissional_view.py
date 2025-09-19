from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from src.schemas import profissional_schema
from src.entities import profissional
from src.services import profissional_services
from src import api

# Lidar com todos os profissionais
class ProfissionalList(Resource):
    def get(self):
        profissionais = profissional_services.listar_profissionais()
        schema = profissional_schema.ProfissionalSchema(many=True)

        if not profissionais:
            return make_response(jsonify({'message': 'Não existe profissional'}), 404)

        return make_response(jsonify(schema.dump(profissionais)), 200)

    def post(self):
        schema = profissional_schema.ProfissionalSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            novo_profissional = profissional.Profissional(
                nome=dados['nome']
            )
            resultado = profissional_services.cadastrar_profissional(novo_profissional)
            return make_response(jsonify(schema.dump(resultado)), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(ProfissionalList, '/profissional')


# Lidar com um profissional específico
class ProfissionalResource(Resource):
    def get(self, id_profissional):
        profissional_encontrado = profissional_services.listar_profissional_id(id_profissional)
        schema = profissional_schema.ProfissionalSchema()

        if not profissional_encontrado:
            return make_response(jsonify({'message': 'Profissional não encontrado'}), 404)

        return make_response(jsonify(schema.dump(profissional_encontrado)), 200)

    def put(self, id_profissional):
        profissional_encontrado = profissional_services.listar_profissional_id(id_profissional)
        schema = profissional_schema.ProfissionalSchema()

        if not profissional_encontrado:
            return make_response(jsonify({'message': 'Profissional não encontrado'}), 404)

        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            resultado = profissional_services.editar_profissional(
                id_profissional,
                profissional.Profissional(nome=dados['nome'])
            )
            return make_response(jsonify(schema.dump(resultado)), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)

    def delete(self, id_profissional):
        profissional_encontrado = profissional_services.listar_profissional_id(id_profissional)

        if not profissional_encontrado:
            return make_response(jsonify({'message': 'Profissional não encontrado'}), 404)

        try:
            profissional_services.excluir_profissional(id_profissional)
            return make_response(jsonify({'message': 'Profissional excluído com sucesso'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(ProfissionalResource, '/profissional/<int:id_profissional>')  # /profissional/1
