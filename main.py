#Introdução
print("Seja Bem-vindo ao PYEstoque\n")
print("Comece agora e simplifique sua vida empresarial.\n")

cod_prod = input('Digite o código do produto: ') #chave-primaria sql
nome_prod = input('Digite o nome do produto: ')
descri_prod = input('Digite a Descrição do produto: ')

def verificar_negativo(num):  #função para testar número negativo
    if num < 0:
        raise ValueError("Erro: O número não pode ser negativo.")
    return num

while True: 
    try: 
        cp = int(input("\nQual o custo do produto?"))
        cp= verificar_negativo(cp) #Verifica se o numero é interio
        cf = int(input("\nQual o custo fixo/administrativo?"))
        cf= verificar_negativo(cf) #Verifica se o numero é interio
        cv = int(input("\nQual a comissão de vendas(%)?"))
        cv= verificar_negativo(cv) #Verifica se o numero é interio
        iv = int(input("\nQual é o imposto sobre a venda(%)?"))
        iv= verificar_negativo(iv) #Verifica se o numero é interio
        ml = int(input("\nQual a margem de lucro desejada(%)?"))
        ml= verificar_negativo(ml) #Verifica se o numero é interio
        
        pv = cp/(1-((cf+cv+iv+ml)/100))
        #Descrição
    
        #Preço de Venda(PV)
        print('\nO Preço de venda foi de ', round(pv), 'que é igual a 100% do valor final')
            
        #Custo de Aquisição (Fornecedor)
        porcent = cp * 100 / pv
        print("\nO preço do produto pelo fornecedor foi igual a R$", round(cp),' que é igual a', round(porcent),'%' 'do valor final')
           
        #Receita Bruta (A-B)
        bruto = pv - cp
        porcent1 = (bruto * 100) / pv
        print('\na receita bruta foi de ', round(bruto), 'que é igual a', round(porcent1),'% do valor final')
            
        #Custo Fixo/Administrativo
        valorCF = pv * cf / 100
        print('\no custo fixo foi de ', round(valorCF), 'que é igual a', round(cf),'% do valor final')
            
         #Comissão de Vendas
        valorCV = pv * cv / 100
        print('\na comissao foi de ', round(valorCV), 'que é igual a', round(cv),'% do valor final')
            
         #Impostos
        valorIV = pv * iv / 100
        print('\no valor do imposto foi de ', round(valorIV), 'que é igual a', round(iv),'% do valor final')
            
        #Outros custos (D+E+F)
        resto = valorCF + valorCV + valorIV
        porcent2 = cf + cv + iv
        print('\noutros custos ', round(resto), 'que é igual a', round(porcent2),'% do valor final')
            
        #Rentabilidade (C-G)
        rentabilidade = bruto - resto
        print('\na rentabilidade foi de', round(rentabilidade), 'que é igual a', round(ml), '% do valor final')

        #Margem de lucro
        if rentabilidade >= 0.20 * pv:
            print('sua classificação é de nivel alto')
              
        elif rentabilidade >= 0.10 * pv < 0.20 * pv:
            print('sua classificação é de nivel médio')
              
        elif rentabilidade > 0 * 100 < 0.10 * 100:
            print('sua classificação é de nivel baixo')
              
        elif rentabilidade == 0:
            print('sua classificação é de nivel equilibrado')
              
        else:
            rentabilidade < 0 * 100
            print('sua classificação é de prejuizo')
    #Erro caso seja negativo o número
    except ValueError as e:
        print(e)
    except Exception as e:
        print("Um erro ocorreu:", e)
    except ValueError:
        print("Somente unidades numéricas!")
        
    while True:
        resposta = input("\nDeseja continuar cotanto o preço (S/N)?").upper()
        if resposta not in ["S", "N"]:
            print("A resposta deve ser S ou N; tente novamente!")
        else:
            break
        
    if resposta =="N":
        break