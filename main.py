from mysql.connector import connect
<<<<<<< HEAD

from decimal import Decimal

=======
from decimal import Decimal
>>>>>>> release
from datetime import datetime
from tabulate import tabulate
import bcrypt

<<<<<<< HEAD
from tabulate import tabulate

conexao_mysql = None

# Função para conectar ao BD
def obtemConexaoComMySQL(servidor, usuario, senha, bd): 
=======
conexao_mysql = None

# Função para conectar ao BD
def obtemConexaoComMySQL(servidor, usuario, senha, bd):
>>>>>>> release
    global conexao_mysql
    try:
        if conexao_mysql is None or not conexao_mysql.is_connected():
            conexao_mysql = connect(host=servidor, user=usuario, passwd=senha, database=bd)
        return conexao_mysql
    except Exception as e:
        print("Erro ao conectar ao MySQL:", e)
        return None

<<<<<<< HEAD
# Função para obter dados do produto
def obter_dados_produto():
    cod_prod = input('Digite o código do produto: ')
    nome_prod = input('Digite o nome do produto: ')
    descri_prod = input('Digite a Descrição do produto: ')
    return cod_prod, nome_prod, descri_prod

# Função para inserir valores no BD
def inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro):
    comando = "INSERT INTO PRODUTOS (cod_prod, nome_prod, descri_prod, custo_prod, custo_fixo, comissao_venda, imposto_venda, margem_lucro, data_insercao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())"
    valores = (cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro)
=======
def cadastrar_usuario(username, senha):
>>>>>>> release
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
    if conexao is None:
        print("Falha ao conectar ao banco de dados. Não foi possível cadastrar o usuário.")
        return

<<<<<<< HEAD
# Função para retornar dados do BD
def retornoDados():
    comando = "SELECT * FROM PRODUTOS WHERE data_insercao >= %s"
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
    cursor = conexao.cursor()
    cursor.execute(comando, (data_atual,))
    dadosSelecionados = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    # Converter os valores Decimal para float
    dados_convertidos = []
    for produto in dadosSelecionados:
        produto_convertido = list(produto)
        for i, valor in enumerate(produto):
            if isinstance(valor, Decimal):
                produto_convertido[i] = float(valor)
        dados_convertidos.append(produto_convertido)
    
    return dados_convertidos

# Função para listar produtos
# Função para listar produtos e calcular detalhes
def listar_produtos():
    try:
        conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
        cursor = conexao.cursor()
        cod_produto = input("Digite o código do produto que deseja listar: ")
        consulta_sql = "SELECT * FROM PRODUTOS WHERE cod_prod = %s"
        cursor.execute(consulta_sql, (cod_produto,))
        linhas = cursor.fetchall()
        print("\nMostrar os Produtos cadastrados")
        
        for linha in linhas:
            print("\nCódigo do produto:", linha[0])
            print("\nNome:", linha[1])
            print("\nDescrição:", linha[2])
            print("\nCusto do produto:", linha[3])
            print("\nCusto fixo/administrativo:", linha[4])
            print("\nComissão de vendas:", linha[5])
            print("\nImposto sobre a venda:", linha[6])
            print("\nMargem de lucro:", linha[7])
            print("\nData de inserção:", linha[8], "\n")
            
            # Converter os valores para float
            linha = tuple(float(valor) if isinstance(valor, Decimal) else valor for valor in linha)
            calcular_detalhes_produto(linha)

    except Exception as e:
        print("Erro ao acessar tabela MySQL:", e)
    finally:
        if conexao.is_connected():
            conexao.close()
            cursor.close()
            print("Conexão ao MySQL encerrada")

# Função para verificar valores negativos
=======
    hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    comando = "INSERT INTO USUARIOS (username, senha) VALUES (%s, %s)"
    valores = (username, hashed.decode('utf-8'))
    
    try:
        cursor = conexao.cursor()
        cursor.execute(comando, valores)
        conexao.commit()
        cursor.close()
        conexao.close()
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        print("Erro ao cadastrar o usuário:", e)

def verificar_usuario(username, senha):
    comando = "SELECT id, senha FROM USUARIOS WHERE username = %s"
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
    if conexao is None:
        print("Falha ao conectar ao banco de dados. Não foi possível verificar o usuário.")
        return None

    try:
        cursor = conexao.cursor()
        cursor.execute(comando, (username,))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[1].encode('utf-8')):
            print("Login bem-sucedido!")
            return resultado[0]  # Retorna o id do usuário
        else:
            print("Nome de usuário ou senha incorretos.")
            return None
    except Exception as e:
        print("Erro ao verificar o usuário:", e)
        return None

def sistema_login():
    while True:
        opcao = input("\nEscolha uma opção: \n1. Registrar\n2. Login\n3. Sair\nOpção: ")

        if opcao == "1":
            username = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")
            cadastrar_usuario(username, senha)

        elif opcao == "2":
            username = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")
            user_id = verificar_usuario(username, senha)
            if user_id:
                return user_id  # Retorna o id do usuário após login bem-sucedido
            else:
                print("Falha na autenticação. Tente novamente.")

        elif opcao == "3":
            return None  # Indica que o usuário escolheu sair

        else:
            print("Opção inválida. Por favor, escolha uma opção válida de 1 a 3.")

def inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro, user_id):
    comando = "INSERT INTO PRODUTOS (cod_prod, nome_prod, descri_prod, custo_prod, custo_fixo, comissao_venda, imposto_venda, margem_lucro, data_insercao, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)"
    valores = (cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro, user_id)
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
    if conexao is None:
        print("Falha ao conectar ao banco de dados. Não foi possível inserir os valores.")
        return

    try:
        cursor = conexao.cursor()
        cod_produto = input("Digite o código do produto que deseja listar: ")
        consulta_sql = "SELECT * FROM PRODUTOS WHERE cod_prod = %s"
        cursor.execute(consulta_sql, (cod_produto,))
        linhas = cursor.fetchall()
        print("\nMostrar os Produtos cadastrados")
        
        for linha in linhas:
            print("\nCódigo do produto:", linha[0])
            print("\nNome:", linha[1])
            print("\nDescrição:", linha[2])
            print("\nCusto do produto:", linha[3])
            print("\nCusto fixo/administrativo:", linha[4])
            print("\nComissão de vendas:", linha[5])
            print("\nImposto sobre a venda:", linha[6])
            print("\nMargem de lucro:", linha[7])
            print("\nData de inserção:", linha[8], "\n")
            
            # Converter os valores para float
            linha = tuple(float(valor) if isinstance(valor, Decimal) else valor for valor in linha)
            calcular_detalhes_produto(linha)

<<<<<<< HEAD
        def verificar_negativo(num):
            if num < 0:
                raise ValueError("Erro: O número não pode ser negativo.")
            return num
        
        custo_produto = float(input("\nQual o custo do produto? ").replace(",","."))
        custo_produto = verificar_negativo(custo_produto)
        
        custo_fixo = float(input("\nQual o custo fixo/administrativo? ").replace(",","."))
        custo_fixo = verificar_negativo(custo_fixo)
        
        comissao_venda = float(input("\nQual a comissão de vendas(%)?").replace(",","."))
        comissao_venda = verificar_negativo(comissao_venda)
        
        imposto_venda = float(input("\nQual é o imposto sobre a venda(%)? ").replace(",","."))
        imposto_venda = verificar_negativo(imposto_venda)
        
        margem_lucro = float(input("\nQual a margem de lucro desejada(%)? ").replace(",","."))
        margem_lucro = verificar_negativo(margem_lucro)
        
        #Inseri valores no BD
        inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro)
        
        #Recebe os valores do BD e printa
        dados_produtos = retornoDados()
        print("\nDados inseridos na tabela PRODUTOS:\n")
        print(dados_produtos)
        
        #Pega os valores do bando de dados para usar nas contas
        for produto in dados_produtos:
            cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro, data_insercao = produto
            
            preco_venda = custo_produto / (1 - ((custo_fixo + comissao_venda + imposto_venda + margem_lucro) / 100))
        
            porcent_custo = custo_produto * 100 / preco_venda
            
            bruto = preco_venda - custo_produto
            porcent_receita = (bruto * 100) / preco_venda
            
            ValorCustoFixo = preco_venda * custo_fixo / 100
            
            ValorComissaoVendas = preco_venda * comissao_venda / 100
            
            ValorImpostoVenda = preco_venda * imposto_venda / 100
            
            resto = ValorCustoFixo + ValorComissaoVendas + ValorImpostoVenda
            porcent_outros = custo_fixo + comissao_venda + imposto_venda
            
            rentabilidade = bruto - resto
                    
            tabela_dados = [
            ["Preço de venda", f"R${preco_venda}", "100%"],
            ["Preço do custo de aquisição", f"R${round(custo_produto):.2f}", f"{round(porcent_custo):.2f}%"],
            ["Receita bruta", f"R${round(bruto):.2f}", f"{round(porcent_receita):.2f}%"],
            ["Valor do custo fixo/administrativo", f"R${round(ValorCustoFixo):.2f}", f"{round(custo_fixo):.2f}%"],
            ["Valor da comissão de vendas", f"R${round(ValorComissaoVendas):.2f}", f"{round(comissao_venda):.2f}%"],
            ["Valor do imposto sobre a venda", f"R${round(ValorImpostoVenda):.2f}", f"{round(imposto_venda):.2f}%"],
            ["Valor de outros custos", f"R${round(resto):.2f}", f"{round(porcent_outros):.2f}%"],
            ["Rentabilidade", f"R${rentabilidade:.2f}", f"{round(margem_lucro):.2f}%"],
            ]
            print(f"\nProduto: {nome_prod}\n")
            # Use a função tabulate para formatar os dados em uma tabela
            print(tabulate(tabela_dados, headers=["Descrição", "Valor", "Porcentagem"]))

            if rentabilidade >= 0.20 * preco_venda:
                print('\nSua classificação é de nível alto')
            elif 0.10 * preco_venda <= rentabilidade < 0.20 * preco_venda:
                print('\nSua classificação é de nível médio')
            elif 0 <= rentabilidade < 0.10 * preco_venda:
                print('\nSua classificação é de nível baixo')
            elif rentabilidade == 0:
                print('\nSua classificação é de nível equilibrado')
            else:
                print('\nVocê está com prejuízo')

    except ValueError as e:
        print(e)
=======
>>>>>>> develop
    except Exception as e:
        print("Erro ao inserir os valores:", e)

def obter_dados_produto():
    cod_prod = input('Digite o código do produto: ')
    nome_prod = input('Digite o nome do produto: ')
    descri_prod = input('Digite a Descrição do produto: ')
    return cod_prod, nome_prod, descri_prod

>>>>>>> release
def verificar_negativo(num):
    if num < 0:
        raise ValueError("Erro: O número não pode ser negativo.")
    return num

<<<<<<< HEAD
# Função para calcular e exibir os detalhes do produto
def calcular_detalhes_produto(produto):
    cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro, data_insercao = produto

    preco_venda = custo_produto / (1 - ((custo_fixo + comissao_venda + imposto_venda + margem_lucro) / 100))
    
    porcent_custo = custo_produto * 100 / preco_venda
    
    bruto = preco_venda - custo_produto    
    porcent_receita = (bruto * 100) / preco_venda
    
    ValorCustoFixo = preco_venda * custo_fixo / 100
    
    ValorComissaoVendas = preco_venda * comissao_venda / 100
    
    ValorImpostoVenda = preco_venda * imposto_venda / 100
    
    resto = ValorCustoFixo + ValorComissaoVendas + ValorImpostoVenda
    porcent_outros = custo_fixo + comissao_venda + imposto_venda
    
=======
def calcular_detalhes_produto(produto):
    cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro, data_insercao, user_id = produto

    preco_venda = custo_produto / (1 - ((custo_fixo + comissao_venda + imposto_venda + margem_lucro) / 100))

    porcent_custo = custo_produto * 100 / preco_venda

    bruto = preco_venda - custo_produto
    porcent_receita = (bruto * 100) / preco_venda

    ValorCustoFixo = preco_venda * custo_fixo / 100

    ValorComissaoVendas = preco_venda * comissao_venda / 100

    ValorImpostoVenda = preco_venda * imposto_venda / 100

    resto = ValorCustoFixo + ValorComissaoVendas + ValorImpostoVenda
    porcent_outros = custo_fixo + comissao_venda + imposto_venda

>>>>>>> release
    rentabilidade = bruto - resto

    tabela_dados = [
        ["Preço de venda", f"R${preco_venda:.2f}", "100%"],
        ["Preço do custo de aquisição", f"R${custo_produto:.2f}", f"{porcent_custo:.2f}%"],
        ["Receita bruta", f"R${bruto:.2f}", f"{porcent_receita:.2f}%"],
        ["Valor do custo fixo/administrativo", f"R${ValorCustoFixo:.2f}", f"{custo_fixo:.2f}%"],
        ["Valor da comissão de vendas", f"R${ValorComissaoVendas:.2f}", f"{comissao_venda:.2f}%"],
        ["Valor do imposto sobre a venda", f"R${ValorImpostoVenda:.2f}", f"{imposto_venda:.2f}%"],
        ["Valor de outros custos", f"R${resto:.2f}", f"{porcent_outros:.2f}%"],
        ["Rentabilidade", f"R${rentabilidade:.2f}", f"{margem_lucro:.2f}%"],
    ]
    print(f"\nProduto: {nome_prod}\n")
    print(tabulate(tabela_dados, headers=["Descrição", "Valor", "Porcentagem"]))

    if rentabilidade >= 0.20 * preco_venda:
        print('\nSua classificação é de nível alto')
    elif 0.10 * preco_venda <= rentabilidade < 0.20 * preco_venda:
        print('\nSua classificação é de nível médio')
    elif 0 <= rentabilidade < 0.10 * preco_venda:
        print('\nSua classificação é de nível baixo')
    elif rentabilidade == 0:
        print('\nSua classificação é de nível equilibrado')
    else:
        print('\nVocê está com prejuízo')

<<<<<<< HEAD
# Função principal para inserir e calcular produtos
def main():
    while True:
        try:
            opcao = input("\nEscolha uma opção: \n1. Inserir produto\n2. Procurar produto\n3. Sair\nOpção: ")

            if opcao == "1":
                cod_prod, nome_prod, descri_prod = obter_dados_produto()
                
                custo_produto = float(input("\nQual o custo do produto? ").replace(",", "."))
                custo_produto = verificar_negativo(custo_produto)
                
                custo_fixo = float(input("\nQual o custo fixo/administrativo? ").replace(",", "."))
                custo_fixo = verificar_negativo(custo_fixo)
                
                comissao_venda = float(input("\nQual a comissão de vendas(%)? ").replace(",", "."))
                comissao_venda = verificar_negativo(comissao_venda)
                
                imposto_venda = float(input("\nQual é o imposto sobre a venda(%)? ").replace(",", "."))
                imposto_venda = verificar_negativo(imposto_venda)
                
                margem_lucro = float(input("\nQual a margem de lucro desejada(%)? ").replace(",", "."))
                margem_lucro = verificar_negativo(margem_lucro)
                
                # Inserir valores no BD
                inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro)
                print("Produto inserido com sucesso!")

            elif opcao == "2":
                listar_produtos()

            elif opcao == "3":
                break

            else:
                print("Opção inválida. Por favor, escolha uma opção válida de 1-3.")
                
        except ValueError as e:
            print(e)
        except Exception as e:
            print("Um erro ocorreu:", e)
=======
def listar_produtos(user_id):
    try:
        conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
        if conexao is None:
            print("Falha ao conectar ao banco de dados. Não foi possível listar os produtos.")
            return

        cursor = conexao.cursor()
        comando = "SELECT cod_prod, nome_prod, descri_prod, custo_prod, custo_fixo, comissao_venda, imposto_venda, margem_lucro, data_insercao, user_id FROM PRODUTOS WHERE user_id = %s"
        cursor.execute(comando, (user_id,))
        resultado = cursor.fetchall()

        for linha in resultado:
            print("\nCódigo do produto:", linha[0])
            print("\nNome do produto:", linha[1])
            print("\nDescrição:", linha[2])
            print("\nCusto do produto:", linha[3])
            print("\nCusto fixo administrativo:", linha[4])
            print("\nComissão de vendas:", linha[5])
            print("\nImposto de vendas:", linha[6])
            print("\nMargem de lucro:", linha[7])
            print("\nData de inserção:", linha[8])
            print("\n--------------------------")

            # Converter os valores para float
            linha = tuple(float(valor) if isinstance(valor, Decimal) else valor for valor in linha)
            calcular_detalhes_produto(linha)
            
        cursor.close()
        conexao.close()
    except Exception as e:
        print("Erro ao listar os produtos:", e)

def main():
    user_id = sistema_login()
    if user_id:
        while True:
            opcao = input("Digite 1 para cadastrar um produto\nDigite 2 para listar todos os produtos cadastrados\nDigite 3 para sair: ")

            if opcao == "1":
                try:
                    cod_prod, nome_prod, descri_prod = obter_dados_produto()
                    custo_produto = verificar_negativo(Decimal(input('Digite o custo de aquisição do produto: ')))
                    custo_fixo = verificar_negativo(Decimal(input('Digite o custo fixo/administrativo: ')))
                    comissao_venda = verificar_negativo(Decimal(input('Digite a comissão de vendas: ')))
                    imposto_venda = verificar_negativo(Decimal(input('Digite o imposto sobre a venda: ')))
                    margem_lucro = verificar_negativo(Decimal(input('Digite a margem de lucro: ')))

                    inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro, user_id)
                    print("Produto cadastrado com sucesso!")
                except ValueError as ve:
                    print(ve)
                except Exception as e:
                    print("Erro ao inserir produto:", e)

            elif opcao == "2":
                listar_produtos(user_id)

            elif opcao == "3":
                print("Saindo do sistema. Até a próxima!")
                break

            else:
                print("Opção inválida. Por favor, escolha uma opção válida de 1 a 3.")
>>>>>>> release

if __name__ == "__main__":
    main()
