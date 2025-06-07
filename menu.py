import os
import re  # Biblioteca para expressões regulares para validações de formato
import json
import oracledb
import requests

data_json = {
    "usuarios": {}
}

def get_conexao():
    return oracledb.connect(user="", password="",
                            dsn="oracle.fiap.com.br/orcl")

# Função para validar cada campo individualmente
def validar_campo(valor, tipo):
    if tipo == 'nome':
        # Validação para o nome: permite apenas letras e espaços
        if re.fullmatch(r'[A-Za-zÀ-ÿ ]+', valor):
            return True
        print("Erro: O nome deve conter apenas letras e espaços.")
    
    elif tipo == 'cpf':
        # Validação para o CPF: deve estar no formato "000.000.000-00"
        if re.fullmatch(r'\d{11}', valor):
            return True
        print("Erro: O CPF deve estar no formato 00000000000.")
    
    elif tipo == 'cargo':
        # Validação para o cargo: deve conter apenas letras e espaços
        if re.fullmatch(r'[A-Za-zÀ-ÿ ]+', valor):
            return True
        print("Erro: O cargo deve conter apenas letras.")
    
    elif tipo == 'email':
        # Validação para o email: permite letras e números antes do '@', e deve ter o formato básico
        if re.fullmatch(r'[A-Za-z0-9À-ÿ]+@[A-Za-z]+\.[A-Za-z]+', valor):
            return True
        print("Erro: O email deve ser válido e conter apenas letras e números antes do '@'.")
    
    elif tipo == 'senha':
        # Validação para a senha: pode incluir letras, números e alguns caracteres especiais
        if re.fullmatch(r'[A-Za-z0-9!@#$%^&*(),.?":{}|<>]+', valor):
            return True
        print("Erro: A senha pode conter letras, números e caracteres especiais.")

    elif tipo == 'acesso':
        # Validação para a permissao: valor numérico de um algarismo
        if re.fullmatch(r'\d{1}', valor):
            return True
        print("Erro: O acesso deve ser apenas um número de 0 a 3")
    
    return False  # Retorna False se a validação falhar


# Função para cadastrar um usuário
def consultar_usuarios():

    while True:
        sql =  """
            SELECT * FROM usuario
        """

        usuarios = []
        
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql)
                columns = [col[0].lower() for col in cur.description]
                usuarios = [dict(zip(columns, row)) for row in cur.fetchall()]
        
        for i in usuarios:
            print(f"id: {i['id_usuario']}, nome: {i['nome']}, cargo: {i['cargo']}")

        data_json['usuarios'] = usuarios
   
        # Opção de voltar ao menu principal
        voltar = input('Digite "V" para voltar ao menu principal: ').upper()
        if voltar == 'V':
            break  # Sai do laço e retorna ao menu principal

def consultar_usuario_id(id):

    while True:
        sql =  """
            SELECT * FROM usuario where id_usuario=:id
        """

        dados = {"id": id}
        
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, dados)
                usuario = cur.fetchone()
        
        if usuario != None:
            print("usuario encontrado!")
            print(usuario)
            return True
        
        else:
            print("usuário não existe! Selecione um ID válido")
            return False


def deletar_usuario(id):

    while True:
        sql =  """
            DELETE FROM usuario WHERE id_usuario=:id
        """

        parametros = {'id': id}
        
        
        with get_conexao() as con:
            with con.cursor() as cur:
                cur.execute(sql, parametros)
        

        print("usuario deletado com sucesso!")
    
        # Opção de voltar ao menu principal
        voltar = input('Digite "V" para voltar ao menu principal: ').upper()
        if voltar == 'V':
            break  # Sai do laço e retorna ao menu principal

def coletar_id_usuario():
    id = input("Digite o id do usuário a ser deletado")
    return id

def coletar_informacao_usuario():
    usuario = {}
    os.system('cls')  # função para limpar a tela
        
    # Solicita e valida cada campo individualmente
    while True:
        nome = input('Digite o nome do usuário: ')
        if validar_campo(nome, 'nome'):
            usuario.update({"nome": nome})
            break  # Sai do loop se o nome for válido
        
    while True:
        cpf = input('Digite o CPF do usuário: ')
        if validar_campo(cpf, 'cpf'):
            usuario.update({"cpf": cpf})
            break  # Sai do loop se o CPF for válido
        
    while True:
        cargo = input('Digite o cargo do usuário: ')
        if validar_campo(cargo, 'cargo'):
            usuario.update({"cargo": cargo})
            break  # Sai do loop se o cargo for válido
        
    while True:
        email = input('Digite o email do usuário: ')
        if validar_campo(email, 'email'):
            usuario.update({"email": email})
            break  # Sai do loop se o email for válido
        
    while True:
        senha = input('Digite a senha do usuário: ')
        if validar_campo(senha, 'senha'):
            usuario.update({"senha": senha})
            break  # Sai do loop se a senha for válida

    while True:
        acesso = input('Digite o nível de permissao do usuario, de 0 a 3: ')
        if validar_campo(acesso, 'acesso'):
            usuario.update({"acesso": acesso})
            break  # Sai do loop se a senha for válida

    usuario = {
        'nome': nome,
        'cpf': cpf,
        'cargo': cargo,
        'email': email,
        'senha': senha,
        'acesso': acesso
    }

    return usuario


# Função para cadastrar um usuário
def cadastrar_usuario(usuario):
        
    #criando sql concatenando strings
    sql = """
    INSERT INTO usuario (nome, cpf, cargo, email, senha, acesso)
    VALUES (:nome, :cpf, :cargo, :email, :senha, :acesso)
    """
        
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, usuario)
        con.commit()

# Função para cadastrar um usuário
def atualizar_usuario(usuario):

    #criando sql concatenando strings
    sql = """
    UPDATE usuario set nome =:nome, cpf =:cpf, cargo=:cargo, email=:email, senha=:senha, acesso=:acesso
    WHERE id_usuario =:id
    """
        
    with get_conexao() as con:
        with con.cursor() as cur:
                cur.execute(sql, usuario)
        con.commit()


# Função para sair do programa
def sair():
    os.system('cls')  
    try:
        with open ("dados.json", "w", encoding='utf-8') as file_json:
                json.dump(data_json, file_json, indent=4)
    except:
        print("Não foi possível escrever o arquivo de relatório")


    print('Você optou por sair do app. Obrigado por utilizar o CaTech!')

def menu_usuario():
    while True:

        os.system('cls')  
        print('Seja bem-vindo ao menu de gerenciamento de usuários')
        print('1 - Cadastrar usuário')
        print('2 - Consultar usuários existentes')
        print('3 - Atualizar cadastro de usuário')
        print('4 - Deletar usuário')
        print('5 - consultar usuario por id')
        print('6 - Sair')
        
        # Ler opção do usuário
        opcao = input('Digite o número da opção escolhida: ')
        
        # Redireciona para a função escolhida
        if opcao == '1':
            usuario = coletar_informacao_usuario()
            cadastrar_usuario()
        elif opcao == '2':
            consultar_usuarios()
        elif opcao == '3':
            usuario = coletar_informacao_usuario()
            atualizar_usuario(usuario)
        elif opcao == '4':
            id = coletar_id_usuario()
            deletar_usuario(id)
            break  # Sai do programa
        elif opcao == '5':
            id = coletar_id_usuario()
            consultar_usuario_id(id)
        elif opcao == '6':
            sair()
            break  # Sai do programa
        else:
            os.system('cls')
            print('Opção inválida, favor tente novamente!')

# Executa o menu principal
menu_usuario()