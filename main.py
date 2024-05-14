from mysql.connector import connect
from tabulate import tabulate
conexao_mysql = None

def obtemConexaoComMySQL(servidor, usuario, senha, bd): 
    global conexao_mysql
    try:
        # Verifica se a conexão já foi estabelecida ou se ela está ativa
        if conexao_mysql is None or not conexao_mysql.is_connected():
            # Estabelece a conexão
            conexao_mysql = connect(host=servidor, user=usuario, passwd=senha, database=bd)
        return conexao_mysql
    except Exception as e:
        print("Erro ao conectar ao MySQL:", e)
        return None

#Insere uma linha de valores desejados na tabela
def inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro):
    comando = "INSERT INTO PRODUTOS (cod_prod, nome_prod, descri_prod, custo_prod, custo_fixo, comissao_venda, imposto_venda, margem_lucro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro)
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
    cursor = conexao.cursor()
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()
    valoresAtualizados()

def inserir_calculos(preco_venda, bruto, ValorCustoFixo, ValorComissaoVendas, ValorImpostoVenda, resto, rentabilidade):
    comando = "INSERT INTO CALCULANDO (preco_venda, bruto, ValorCustoFixo, ValorComissaoVendas, ValorImpostoVenda, resto, rentabilidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    valores = (preco_venda, bruto, ValorCustoFixo, ValorComissaoVendas, ValorImpostoVenda, resto, rentabilidade)
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "Cauekenzo071525.", "puccamp")
    cursor = conexao.cursor()
    cursor.execute(comando, valores)
    conexao.commit()
    cursor.close()
    conexao.close()
    valoresCalculados()

def retornoDados (): #Função que retorna os dados atualizados após alguma alteração
    comando = "select * from PRODUTOS"
    conexao=obtemConexaoComMySQL("127.0.0.1","root","Cauekenzo071525.","puccamp")
    cursor=conexao.cursor()
    cursor.execute(comando)
    return cursor.fetchall()

def valoresAtualizados (): #Printa a tabela com os dados atualizados
    novosValores = retornoDados()
    print(tabulate(novosValores, headers = col_nomes))

def retornoCalculos (): #Função que retorna os dados atualizados após alguma alteração
    comando = "select * from CALCULANDO"
    conexao=obtemConexaoComMySQL("127.0.0.1","root","Cauekenzo071525.","puccamp")
    cursor=conexao.cursor()
    cursor.execute(comando)
    return cursor.fetchall()

def valoresCalculados (): #Printa a tabela com os dados atualizados
    novosCalculos = retornoCalculos()
    print(tabulate(novosCalculos, headers = col_names))

#Introdução
print("Seja Bem-vindo ao PYEstoque\n")
print("Comece agora e simplifique sua vida empresarial.\n")

while True:
    try:
        col_nomes = ["Código do produto","Nome do produto ","Descrição do produto", "Custo do produto", "Custo fixo %", "Comissão de vendas %", "Imposto sobre as vendas %", "Margem de lucro %"]
        
        col_names = ["Preço de Venda R$", "Receita bruta R$", "Custo fixo/administrativo R$", "Comissão de vendas R$", "Impostos R$", "Rentabilidade R$"]
        
        cod_prod = input ('Digite o código do produto: ') #chave-primaria sql
        nome_prod = input ('Digite o nome do produto: ')
        descri_prod = input ('Digite a Descrição do produto: ')

        def verificar_negativo(num):  #função para testar número negativo
            if num < 0:
                raise ValueError("Erro: O número não pode ser negativo.")
            return num
                
        #Pegando as informcações de custo. imposto, comissão, custo fixo e margem de lucro do produto
    
        custo_produto = float(input("\nQual o custo do produto? ").replace(",","."))   #replace usado para alterar caso o usuaria coloque uma vírgua no lugar do ponto
        custo_produto= verificar_negativo(custo_produto) #Verifica se o numero é negativo
        custo_fixo = float(input("\nQual o custo fixo/administrativo? ").replace(",","."))
        custo_fixo= verificar_negativo(custo_fixo) #Verifica se o numero é negativo
        comissao_venda = float(input("\nQual a comissão de vendas(%)?").replace(",","."))
        comissao_venda= verificar_negativo(comissao_venda) #Verifica se o numero é negativo
        imposto_venda = float(input("\nQual é o imposto sobre a venda(%)? ").replace(",","."))
        imposto_venda= verificar_negativo(imposto_venda) #Verifica se o numero é negativo
        margem_lucro = float(input("\nQual a margem de lucro desejada(%)? ").replace(",","."))
        margem_lucro= verificar_negativo(margem_lucro) #Verifica se o numero é negativo
        
        preco_venda = custo_produto/(1-((custo_fixo+comissao_venda+imposto_venda+margem_lucro)/100))
        #Descrição
    
        #Preço de Venda(PV)
        print(f"\nO Preço de venda foi de R${round(preco_venda):.2f} que é igual a 100% do valor final")
            
        #Custo de Aquisição (Fornecedor)
        porcent = custo_produto * 100 / preco_venda
        print(f"\nO preço do produto pelo fornecedor foi igual a R${round(custo_produto):.2f} que é igual a {round(porcent)}% do valor final")
           
        #Receita Bruta (A-B)
        bruto = preco_venda - custo_produto
        porcent1 = (bruto * 100) / preco_venda
        print(f"\na receita bruta foi de R${round(bruto):.2F} que é igual a {round(porcent1)}% do valor final")
            
        #Custo Fixo/Administrativo
        ValorCustoFixo = preco_venda * custo_fixo / 100
        print(f"\no custo fixo foi de R${round(ValorCustoFixo):.2f} que é igual a {round(custo_fixo)}% do valor final")
            
         #Comissão de Vendas
        ValorComissaoVendas = preco_venda * comissao_venda / 100
        print(f"\na comissao foi de R${round(ValorComissaoVendas):.2f} que é igual a {round(comissao_venda)}% do valor final")
            
         #Impostos
        ValorImpostoVenda = preco_venda * imposto_venda / 100
        print(f"\no valor do imposto foi de R${round(ValorImpostoVenda):.2f} que é igual a {round(imposto_venda)}% do valor final")
            
        #Outros custos (D+E+F)
        resto = ValorCustoFixo + ValorComissaoVendas + ValorImpostoVenda
        porcent2 = custo_fixo + comissao_venda + imposto_venda
        print(f"\noutros custos R${round(resto):.2f} que é igual a {round(porcent2)}% do valor final")
            
        #Rentabilidade (C-G)
        rentabilidade = bruto - resto
        print(f"\na rentabilidade foi de R${round(rentabilidade):.2f} que é igual a {round(margem_lucro)}% do valor final\n")

        #Margem de lucro
        if rentabilidade >= 0.20 * preco_venda:
            print('sua classificação é de nivel alto\n')
              
        elif rentabilidade >= 0.10 * preco_venda and rentabilidade < 0.20 * preco_venda:
            print('sua classificação é de nivel médio\n')
              
        elif rentabilidade > 0 * 100 and rentabilidade < 0.10 * 100:
            print('sua classificação é de nivel baixo\n')
              
        elif rentabilidade == 0:
            print('sua classificação é de nivel equilibrado\n')
              
        else:
            rentabilidade < 0 * 100
            print('sua classificação é de prejuizo\n')
        
        inserirValores(cod_prod, nome_prod, descri_prod, custo_produto, custo_fixo, comissao_venda, imposto_venda, margem_lucro)
        todosValores = retornoDados()
        print(tabulate(todosValores, headers=col_nomes))

        inserir_calculos(preco_venda, bruto, ValorCustoFixo, ValorComissaoVendas, ValorImpostoVenda, resto, rentabilidade)
        novosCalculos = retornoCalculos()
        print(tabulate(novosCalculos, headers=col_names))
    #Erro caso seja negativo o número
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
        
    if resposta =="N":
        break