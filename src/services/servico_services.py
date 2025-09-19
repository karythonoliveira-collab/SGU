from ..models.servicos_model import ServicoModel
from ..entities.servico import Servico
from src import db


def cadastrar_servico(servico_entity):
    servico_db = ServicoModel(
        descricao=servico_entity.descricao,
        valor=servico_entity.valor,
        horario_duracao=servico_entity.horario_duracao
    )
    db.session.add(servico_db)
    db.session.commit()
    return servico_db  # retorna o model para ser serializado pelo schema


def listar_servicos():
    servicos_db = ServicoModel.query.all()
    servicos = [
        Servico(s.descricao, s.valor, s.horario_duracao) for s in servicos_db
    ]
    return servicos


def listar_servico_id(id):
    try:
        servico_db = ServicoModel.query.get(id)
        if servico_db:
            return Servico(
                servico_db.descricao,
                servico_db.valor,
                servico_db.horario_duracao,
                servico_db.id
            )
        return None
    except Exception as e:
        print(f"Erro ao buscar serviço por id: {e}")
        return None


def editar_servico(id, servico_entity):
    servico_db = ServicoModel.query.get(id)

    if not servico_db:
        return None

    servico_db.descricao = servico_entity.descricao
    servico_db.valor = servico_entity.valor
    servico_db.horario_duracao = servico_entity.horario_duracao

    db.session.commit()

    return Servico(
        servico_db.descricao,
        servico_db.valor,
        servico_db.horario_duracao,
        servico_db.id
    )


def excluir_servico(id):
    servico_db = ServicoModel.query.get(id)

    if servico_db:
        db.session.delete(servico_db)
        db.session.commit()
        return True
    
    return False
