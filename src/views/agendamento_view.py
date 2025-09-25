from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, jsonify, make_response
from src.schemas import agendamento_schema
from src.models.agendamento_model import AgendamentoModel
from src.services import agendamento_services
from src import api
import traceback

# Lidar com todos os agendamentos
class AgendamentoList(Resource):
    def get(self):
        """Lista agendamentos com filtros opcionais"""
        try:
            # Parâmetros opcionais
            user_id = request.args.get('user_id', type=int)
            status = request.args.get('status')
            
            if user_id:
                # Listar agendamentos de um usuário específico
                agendamentos = agendamento_services.listar_agendamentos_usuario(user_id, status)
            else:
                # Listar todos os agendamentos
                agendamentos = agendamento_services.listar_agendamentos()
                
                # Aplicar filtro de status se fornecido
                if status:
                    agendamentos = [ag for ag in agendamentos if ag.status == status]
            
            schema = agendamento_schema.AgendamentoSchema(many=True)
            
            if not agendamentos:
                return make_response(jsonify({
                    'message': 'Nenhum agendamento encontrado',
                    'data': []
                }), 200)
            
            return make_response(jsonify({
                'message': 'Agendamentos encontrados',
                'data': schema.dump(agendamentos),
                'total': len(agendamentos)
            }), 200)
            
        except Exception as e:
            print(f"ERRO GET agendamentos: {str(e)}")
            print(traceback.format_exc())
            return make_response(jsonify({
                'message': 'Erro interno do servidor',
                'error': str(e)
            }), 500)

    def post(self):
        """Cria um novo agendamento"""
        schema = agendamento_schema.AgendamentoSchema()
        
        try:
            # Debug: imprimir dados recebidos
            print(f"DEBUG - Dados recebidos: {request.json}")
            
            # Carregar e validar dados sem instanciar a model automaticamente
            dados = schema.load(request.json)
            print(f"DEBUG - Dados após schema.load: {dados}")
            
        except ValidationError as err:
            print(f"ERRO ValidationError: {err.messages}")
            return make_response(jsonify({
                'message': 'Dados inválidos',
                'errors': err.messages
            }), 400)
        except Exception as e:
            print(f"ERRO no schema.load: {str(e)}")
            print(traceback.format_exc())
            return make_response(jsonify({
                'message': 'Erro ao validar dados',
                'error': str(e)
            }), 400)

        try:
            print(f"DEBUG - Criando AgendamentoModel com dados: {dados}")
            
            # Criar objeto de agendamento manualmente
            novo_agendamento = AgendamentoModel(
                dt_atendimento=dados['dt_atendimento'],
                id_user=dados['id_user'],
                id_profissional=dados['id_profissional'],
                id_servico=dados['id_servico'],
                valor_total=dados.get('valor_total', 0.00)
            )
            
            print(f"DEBUG - AgendamentoModel criado: {novo_agendamento.__dict__}")
            
            # Usar a service para validar e criar
            resultado = agendamento_services.cadastrar_agendamento(novo_agendamento)
            print(f"DEBUG - Resultado da service: {resultado}")
            
            return make_response(jsonify({
                'message': 'Agendamento criado com sucesso',
                'data': schema.dump(resultado)
            }), 201)
            
        except Exception as e:
            print(f"ERRO na criação do agendamento: {str(e)}")
            print(traceback.format_exc())
            return make_response(jsonify({
                'message': 'Erro ao criar agendamento',
                'error': str(e)
            }), 400)


# Lidar com um agendamento específico
class AgendamentoResource(Resource):
    def get(self, id_agendamento):
        """Busca um agendamento específico"""
        try:
            agendamento_encontrado = agendamento_services.listar_agendamento_id(id_agendamento)
            schema = agendamento_schema.AgendamentoSchema()

            if not agendamento_encontrado:
                return make_response(jsonify({
                    'message': 'Agendamento não encontrado'
                }), 404)

            return make_response(jsonify({
                'message': 'Agendamento encontrado',
                'data': schema.dump(agendamento_encontrado)
            }), 200)
            
        except Exception as e:
            print(f"ERRO GET agendamento por ID: {str(e)}")
            return make_response(jsonify({
                'message': 'Erro interno do servidor',
                'error': str(e)
            }), 500)

    def put(self, id_agendamento):
        """Atualiza um agendamento específico"""
        try:
            agendamento_encontrado = agendamento_services.listar_agendamento_id(id_agendamento)
            
            if not agendamento_encontrado:
                return make_response(jsonify({
                    'message': 'Agendamento não encontrado'
                }), 404)

            schema = agendamento_schema.AgendamentoSchema()
            
            try:
                dados = schema.load(request.json)
            except ValidationError as err:
                return make_response(jsonify({
                    'message': 'Dados inválidos',
                    'errors': err.messages
                }), 400)

            # Criar objeto com os novos dados
            dados_atualizados = AgendamentoModel(
                dt_atendimento=dados['dt_atendimento'],
                id_user=dados['id_user'],
                id_profissional=dados['id_profissional'],
                id_servico=dados['id_servico'],
                valor_total=dados.get('valor_total', 0.00)
            )
            
            # Usar a service para validar e atualizar
            resultado = agendamento_services.editar_agendamento(id_agendamento, dados_atualizados)
            
            return make_response(jsonify({
                'message': 'Agendamento atualizado com sucesso',
                'data': schema.dump(resultado)
            }), 200)
            
        except Exception as e:
            print(f"ERRO PUT agendamento: {str(e)}")
            return make_response(jsonify({
                'message': 'Erro ao atualizar agendamento',
                'error': str(e)
            }), 400)

    def delete(self, id_agendamento):
        """Cancela um agendamento específico"""
        try:
            agendamento_encontrado = agendamento_services.listar_agendamento_id(id_agendamento)

            if not agendamento_encontrado:
                return make_response(jsonify({
                    'message': 'Agendamento não encontrado'
                }), 404)

            # Usar a service para cancelar (que calcula taxa se necessário)
            agendamento_services.excluir_agendamento(id_agendamento)
            
            return make_response(jsonify({
                'message': 'Agendamento cancelado com sucesso'
            }), 200)
            
        except Exception as e:
            print(f"ERRO DELETE agendamento: {str(e)}")
            return make_response(jsonify({
                'message': 'Erro ao cancelar agendamento',
                'error': str(e)
            }), 400)


# Registrar recursos na API
api.add_resource(AgendamentoList, '/agendamento')
api.add_resource(AgendamentoResource, '/agendamento/<int:id_agendamento>')