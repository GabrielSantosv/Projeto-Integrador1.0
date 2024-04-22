while True: 
    try: 
        cp = int(input("Qual o custo do produto?"))
        cf = int(input("Qual o custo fixo/administrativo?"))
        cv = int(input("Qual a comissão de vendas?"))
        iv = int(input("Qual é o imposto sobre a venda?"))
        ml = int(input("Qual a margem de lucro desejada?"))
        
        pv = cp/(1-((cf+cv+iv+ml)/100))
        
        print("O preço de venda do produto é",pv,"em reais!")
    
    except ValueError:
        print("Somente unidades numéricas!")
        
    while True:
        resposta = input("Deseja continuar cotanto o preço (S/N)?").upper()
        if resposta not in ["S", "N"]:
            print("A resposta deve ser S ou N; tente novamente!")
        else:
            break
        
    if resposta =="N":
        break