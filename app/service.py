from app import db
from app.model import Pessoa, Endereco
from validate_email import validate_email

class PessoaService():

    def obter_pessoas(self):
        return Pessoa.query.all()

    def salvar(self, dict_data):
        pessoa = self.parse_pessoa(dict_data, Pessoa())
        self.validar_campos_obrigatorios(pessoa)
        self.valida_email(pessoa.email)
        pessoa.endereco = self.parse_endereco(dict_data, Endereco())
        db.session.add(pessoa)
        db.session.commit()

    def editar(self, pessoa_id, dict_data):
        pessoa = self.obter_pessoa_por_id(pessoa_id)
        if (pessoa is None):
            raise Exception("Pessoa não encotranda para edição")

        pessoa = self.parse_pessoa(dict_data, pessoa)
        pessoa.endereco = self.parse_endereco(dict_data, pessoa.endereco)
        db.session.add(pessoa)
        db.session.commit()

    def parse_pessoa(self, dict_pessoa, pessoa):
        """ Método responsável por efetuar o transformar um dict em um objeto Pessoa"""
        pessoa.nome = dict_pessoa.get("nome")
        pessoa.idade = dict_pessoa.get("idade")
        pessoa.cpf = dict_pessoa.get("cpf")
        pessoa.email = dict_pessoa.get("email")
        return pessoa

    def parse_endereco(self, dict_endereco, endereco):
        endereco.uf = dict_endereco.get("uf")
        endereco.cidade = dict_endereco.get("cidade")
        endereco.bairro = dict_endereco.get("bairro")
        endereco.rua = dict_endereco.get("rua")
        return endereco

    def obter_pessoa_por_id(self, pessoa_id):
        return Pessoa.query.filter_by(id=pessoa_id).first()

    def excluir(self, pessoa_id):
        pessoa = self.obter_pessoa_por_id(pessoa_id)
        if pessoa is not None:
            # pessoa.delete()
            Pessoa.query.filter(Pessoa.id == pessoa_id).delete()
            db.session.add(pessoa)
            db.session.commit()

    def validar_campos_obrigatorios(self, pessoa):
        if self.is_blank(pessoa.nome):
            raise Exception("nome é obrigatorio")
        if self.is_blank(pessoa.cpf):
            raise Exception("cpf é obrigatorio")
        if self.is_blank(pessoa.email):
            raise Exception("email é obrigatorio")

    def is_blank(self, string):
        return not (string and string.strip())

    def valida_email(self, email):
        is_valid = validate_email('example@example.com', check_mx=True)
        if not is_valid:
            raise Exception("email inválido")