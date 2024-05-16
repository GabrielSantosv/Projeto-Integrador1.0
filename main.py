from mysql.connector import connect

#Importa decimal para float, pois estamos pegando dados do BD para fazer contas em python.
from decimal import Decimal

#Para pegar somente os que foi transferido para o BD na hora, para fazer o print dos dados bonitnho.
from datetime import datetime

conexao_mysql = None
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

print("Seja Bem-vindo ao PYEstoque\n")
print("Comece agora e simplifique sua vida empresarial.\n")

while True:
    try:
        cod_prod = input('Digite o código do produto: ')
        nome_prod = input('Digite o nome do produto: ')
        descri_prod = input('Digite a Descrição do produto: ')

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
            
            #Calculando preço de venda
            preco_venda = custo_produto / (1 - ((custo_fixo + comissao_venda + imposto_venda + margem_lucro) / 100))
        
            #Custo de aquisição (Fornecedor)
            porcent_custo = custo_produto * 100 / preco_venda
            
            #Receita bruta (A-B)
            bruto = preco_venda - custo_produto
            porcent_receita = (bruto * 100) / preco_venda
            
            #Custo fixo/administrativo
            ValorCustoFixo = preco_venda * custo_fixo / 100
            
            #Comissão de venda 
            ValorComissaoVendas = preco_venda * comissao_venda / 100
            
            #Imposto
            ValorImpostoVenda = preco_venda * imposto_venda / 100
            
            #Outros custos (D+E+F)
            resto = ValorCustoFixo + ValorComissaoVendas + ValorImpostoVenda
            porcent_outros = custo_fixo + comissao_venda + imposto_venda
            
            #Rentabilidade (C-G)
            rentabilidade = bruto - resto
                    
            print(f"\nProduto: {nome_prod}\n")
            print(f"Preço de venda: R${round(preco_venda):.2f} 100% do valor final\n")
            print(f"Preço do custo de aquisição: R${round(custo_produto):.2f} - {round(porcent_custo):.2f}%\n")
            print(f"Receita bruta: R${round(bruto):.2f} - {round(porcent_receita):.2f}%\n")
            print(f"Valor do custo fixo/administrativo: R${round(ValorCustoFixo):.2f} - {round(custo_fixo):.2f}%\n")
            print(f"Valor da comissão de vendas: R${round(ValorComissaoVendas):.2f} - {round(comissao_venda):.2f}%\n")
            print(f"Valor do imposto sobre a venda: R${round(ValorImpostoVenda):.2f} - {round(imposto_venda):.2f}%\n")
            print(f"Valor de outros custos: R${round(resto):.2f} - {round(porcent_outros):.2f}%\n")
            print(f"Rentabilidade: R${round(rentabilidade):.2f} - {round(margem_lucro):.2f}%\n")

            #Margem de lucro 
            if rentabilidade >= 0.20 * preco_venda:
                print('Sua classificação é de nível alto')
            elif 0.10 * preco_venda <= rentabilidade < 0.20 * preco_venda:
                print('Sua classificação é de nível médio')
            elif 0 <= rentabilidade < 0.10 * preco_venda:
                print('Sua classificação é de nível baixo')
            elif rentabilidade == 0:
                print('Sua classificação é de nível equilibrado')
            else:
                print('Você está com prejuízo')

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