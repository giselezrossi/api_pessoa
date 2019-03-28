from http import HTTPStatus
from app import app
from flask import jsonify, request, Response
from app.model import Pessoa
from app.service import PessoaService

@app.route("/")
def contexto_app():
    return "Bem vindo ao CRUD de pessoa", HTTPStatus.OK

# é possível colocar a documentação (swagger) em um arquivo separado, mas eu prefiro deixar no metodo pela facilidade de manutenção
# é possível também mandar renderizar o serializador no model ao inves de colocar todos os campos

#Coloquei as strings de retorno fixas no código, porem o ideal na produção, seria retornar uma chave para que o front faça um mapaamento das msg para fazer a internacionalização

@app.route("/pessoas", methods=['POST'])
def salvar():
    """
        Verbo responsável por salvar pessoa
        ---
        tags:
          - Pessoas
        parameters:
          - name: nome
            in: path
            type: string
            required: true
            description: Nome da pessoa
          - name: idade
            in: query
            type: integer
            description: idade da pessoa
         - email: cpf
            in: path
            type: string
            required: true
            description: Nome da pessoa
        responses:
          201:
            description: criado com sucesso
    """
    conteudo = request.json
    if conteudo is None:
        return "Json inválido",HTTPStatus.BAD_REQUEST
    try:
        pessoa_service = PessoaService()
        pessoa_service.salvar(conteudo)
        # o correto seria, alem de retornar status 201 (criado), colocar o cabeçalho um parâmetro chamado Location
        # com a url de acesso para acessar o recurso e Location_id com id do recurso salvo para elevar o nível de maturidade da API
        # porém não deu tempo de fazer
        return "Registro salvo com sucesso", HTTPStatus.CREATED
    except Exception as e:
        return str(e), HTTPStatus.OK

@app.route("/pessoas", methods=['GET'])
def listar_todos():
    """
        Verbo responsável por listar todas as pessoas
        ---
        tags:
            - Pessoas
        parameters:
            - name: nome
                in: path
                type: string
                required: true
                description: Nome da pessoa
            - name: size
                in: query
                type: integer
                description: size of awesomeness
            responses:
                200:
                    description: requesição efetuada com sucesso
    """
    cols = ['id','username', 'email']
    pessoas = PessoaService().obter_pessoas()
    return jsonify(resultado=Pessoa.serialize_list(pessoas), total=len(pessoas))

@app.route("/pessoas/<id>", methods=['GET'])
def listar_by_id(id):
    """
        Verbo responsável por editar pessoa
        ---
        tags:
            - Pessoas
        parameters:
            - name: nome
                in: path
                type: string
                required: true
                description: Nome da pessoa
            - name: size
                in: query
                type: integer
                description: size of awesomeness
            responses:
                200:
                description: requesição efetuada com sucesso
    """
    if id is None:
        return HTTPStatus.BAD_REQUEST

    pessoa_service = PessoaService()
    pessoa = pessoa_service.obter_pessoa_por_id(id)
    return jsonify(Pessoa.serialize(pessoa))

@app.route("/pessoas/<id>", methods=['DELETE'])
def excluir(id):
    """
        Verbo responsável por excluir pessoa
        ---
        tags:
            - Pessoas
        parameters:
            - name: nome
                in: path
                type: string
                required: true
                description: Nome da pessoa
            - name: size
                in: query
                type: integer
                description: size of awesomeness
            responses:
                200:
                    description: requesição efetuada com sucesso
    """
    if id is None:
        return "identificador não encontrado" ,HTTPStatus.BAD_REQUEST

    PessoaService().excluir(id)
    return "Registro excluido com sucesso", HTTPStatus.OK

@app.route("/pessoas/<id>", methods=['PUT'])
def editar(id):
    """
        Verbo responsável por editar pessoa
        ---
        tags:
            - Pessoas
        parameters:
            - name: nome
                in: path
                type: string
                required: true
                description: Nome da pessoa
              - name: size
                in: query
                type: integer
                description: size of awesomeness
            responses:
              200:
                description: requesição efetuada com sucesso
    """
    conteudo = request.json
    if conteudo is None or id is None:
        return "Conteúdo inválido", HTTPStatus.BAD_REQUEST
    try:
        pessoa_service = PessoaService()
        pessoa_service.editar(id, conteudo)
        return "Registro alterado com sucesso", HTTPStatus.OK
    except Exception as e:
        return str(e), HTTPStatus.OK



if __name__ == "__main__":
    app.run(debug=True)