from mysql.connector import connect

#Importa decimal para float, pois estamos pegando dados do BD para fazer contas em python.
from decimal import Decimal

#Para pegar somente os que foi transferido para o BD na hora, para fazer o print dos dados bonitnho.
from datetime import datetime

#Printar em tabela 
from tabulate import tabulate

conexao_mysql = None

#Função para conectar no BD
def obter_dados_produto():
    cod_prod = input('Digite o código do produto: ')
    nome_prod = input('Digite o nome do produto: ')
    descri_prod = input('Digite a Descrição do produto: ')
    return cod_prod, nome_prod, descri_prod

def inserir_produto():
    try:
        cod_prod, nome_prod, descri_prod = obter_dados_produto()

        # Lógica para inserir o produto no banco de dados
        inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro)
        
        print("Produto inserido com sucesso!")
        
        # Pergunta se deseja incluir outro produto
        while True:
            resposta = input("\nDeseja incluir outro produto (S/N)? ").upper()
            if resposta == "S":
                break
            elif resposta == "N":
                return
            else:
                print("Resposta inválida! Por favor, digite 'S' para Sim ou 'N' para Não.")

    except ValueError as ve:
        print("Erro: Valor inválido. Certifique-se de inserir um número válido.")
    except Exception as e:
        print("Erro ao inserir produto:", e)

#Função para conectar no BD
def obtemConexaoComMySQL(servidor, usuario, senha, bd): 
    global conexao_mysql
    try:
        if conexao_mysql is None or not conexao_mysql.is_connected():
            conexao_mysql = connect(host=servidor, user=usuario, passwd=senha, database=bd)
        return conexao_mysql
    except Exception as e:
        print("Erro ao conectar ao MySQL:", e)
        return None
#Função para inserir valores no BD
def inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro):
    comando = "INSERT INTO PRODUTOS (cod_prod, nome_prod, descri_prod, custo_prod, custo_fixo, comissao_venda, imposto_venda, margem_lucro, data_insercao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())"
    valores = (cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro)
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
    cursor = conexao.cursor()
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

#Função para selecionar os valores no BD
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

#Função para listar itens do Banco de dados
def listar_produtos(produtos):
    try:
        conexao = connect(host="127.0.0.1", user="root", password="Cauekenzo071525.", database="puccamp")
        consulta_sql = "SELECT * FROM tbl_produtos"
        cursor = conexao.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()
        print("Número total de Registro retornados:", cursor.rowcount)
        print("\nMostrar os Produtos cadastrados")
        for linha in linhas:
            print("Id:", linha[0])
            print("Nome:", linha[1])
            print("Descrição:", linha[2], "\n")
    except Error as e:
        print("Erro ao acessar tabela MySQL:", e)
    finally:
        if conexao.is_connected():
            conexao.close()
            cursor.close()
            print("Conexão ao MySQL encerrada")

#Função para atualizar 
def atualizar_produto(produtos):
    if not produtos:
        print("Nenhum produto cadastrado para atualizar.")
    else:
        listar_produtos(produtos)
        escolha = int(input("Digite o número do produto que deseja atualizar: "))
        if escolha < 1 or escolha > len(produtos):
            print("Número de produto inválido.")
            return
        nome_novo = input("Digite o novo nome do produto: ")
        preco_novo = float(input("Digite o novo preço do produto: "))
        produtos[escolha - 1]["Nome"] = nome_novo
        produtos[escolha - 1]["Preço"] = preco_novo
        print("Produto atualizado com sucesso!")

menu = ['Incluir Produto', 'Listar Produtos', 'Atualizar Produto', 'Sair do Programa']

produtos = []  # Inicialização da lista de produtos

opcao = 0
while opcao != 4:
    opcao = int(opcaoEscolhida(menu))

    if opcao == 1:
        inserir_produto()
    elif opcao == 2:
        listar_produtos(produtos)
    elif opcao == 3:
        atualizar_produto(produtos)

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
    except Exception as e:
        print("Um erro ocorreu:", e)
    except ValueError:
        print("Somente unidades numéricas!")
        
    while True:
        resposta = input("\nDeseja continuar adicionando produtos (S/N)?").upper()
        if resposta not in ["S", "N"]:
            print("A resposta deve ser S ou N; tente novamente!")
        else:
            break
        
    if resposta == "N":
        break
