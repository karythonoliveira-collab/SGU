from ..models.profissional_model import ProfissionalModel
from ..entities.profissional import Profissional
from src import db


def cadastrar_profissional(profissional_entity):
    profissional_db = ProfissionalModel(
        nome=profissional_entity.nome
    )
    db.session.add(profissional_db)
    db.session.commit()
    return profissional_db  # retorna model para ser serializado no schema


def listar_profissionais():
    profissionais_db = ProfissionalModel.query.all()
    profissionais = [
        Profissional(p.nome) for p in profissionais_db
    ]
    return profissionais


def listar_profissional_id(id):
    try:
        profissional_db = ProfissionalModel.query.get(id)
        if profissional_db:
            return Profissional(
                profissional_db.nome,
                profissional_db.id
            )
        return None
    except Exception as e:
        print(f"Erro ao buscar profissional por id: {e}")
        return None


def editar_profissional(id, profissional_entity):
    profissional_db = ProfissionalModel.query.get(id)

    if not profissional_db:
        return None

    profissional_db.nome = profissional_entity.nome
    db.session.commit()

    return Profissional(
        profissional_db.nome,
        profissional_db.id
    )


def excluir_profissional(id):
    profissional_db = ProfissionalModel.query.get(id)

    if profissional_db:
        db.session.delete(profissional_db)
        db.session.commit()
        return True
    
    return False
