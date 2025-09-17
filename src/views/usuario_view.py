from flask_restful import Resource
from marshmallow import ValidationError
from src.schemas import usuario_schema
from src.entities import usuario
from flask import request, jsonify, make_response
from src.services import usuario_services
from src import api


# POST-GET-PUT-DELETE
# Lidar com todos os usuarios
class UsuarioList(Resource):
    def get(self):
        usuarios = usuario_services.listar_usuario()
        schema = usuario_schema.UsuarioSchema(many=True)

        if not usuarios:
            return {'success': False, 'data': [], 'message': 'Não existe usuários!'}, 200

        return {'success': True, 'data': schema.dump(usuarios), 'message': 'Lista de usuários'}, 200

    def post(self):
        schema = usuario_schema.UsuarioSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return {'success': False, 'data': err.messages, 'message': 'Erro de validação'}, 400
        
        if usuario_services.listar_usuario_email(dados['email']):
            return {'success': False, 'data': {}, 'message': 'Email já cadastrado'}, 400

        try:
            novo_usuario = usuario.Usuario(
                nome=dados['nome'],
                email=dados['email'],
                telefone=dados['telefone'],
                senha=dados['senha']
            )
            resultado = usuario_services.cadastrar_usuario(novo_usuario)
            return {'success': True, 'data': schema.dump(resultado), 'message': 'Usuário criado com sucesso'}, 201

        except Exception as e:
            return {'success': False, 'data': {}, 'message': str(e)}, 400

api.add_resource(UsuarioList, '/usuario')

class UsuarioResource(Resource):
    def get(self, id_usuario):
        usuario_encontrado = usuario_services.listar_usuario_id(id_usuario)
        if not usuario_encontrado:
            return {'success': False, 'data': {}, 'message': 'Usuário não encontrado'}, 404
        
        schema = usuario_schema.UsuarioSchema()
        return {'success': True, 'data': schema.dump(usuario_encontrado), 'message': 'Usuário encontrado'}, 200
    
    def put(self, id_usuario):
        usuario_encontrado = usuario_services.listar_usuario_id(id_usuario)
        if not usuario_encontrado:
            return {'success': False, 'data': {}, 'message': 'Usuário não encontrado'}, 404

        schema = usuario_schema.UsuarioSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return {'success': False, 'data': err.messages, 'message': 'Erro de validação'}, 400

        try:
            resultado = usuario_services.editar_usuario(id_usuario, dados)
            return {'success': True, 'data': schema.dump(resultado), 'message': 'Usuário atualizado com sucesso'}, 200
        except Exception as e:
            return {'success': False, 'data': {}, 'message': str(e)}, 400

    def delete(self, id_usuario):
        usuario_encontrado = usuario_services.listar_usuario_id(id_usuario)
        if not usuario_encontrado:
            return {'success': False, 'data': {}, 'message': 'Usuário não encontrado'}, 404
        try:
            usuario_services.excluir_usuario(id_usuario)
            return {'success': True, 'data': {}, 'message': 'Usuário excluído com sucesso'}, 200
        except Exception as e:
            return {'success': False, 'data': {}, 'message': str(e)}, 400


api.add_resource(UsuarioResource, '/usuario/<int:id_usuario>') # /usuario/1