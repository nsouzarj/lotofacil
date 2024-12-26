def calcular_numero_destino(nome_completo):
    """Calcula o Número de Destino (Expressão) de um nome completo usando a tabela pitagórica.

    Args:
      nome_completo: O nome completo da pessoa (string).

    Returns:
      O Número de Destino (int), ou None se o nome for inválido.
    """

    tabela_pitagorica = {
        'a': 1, 'j': 1, 's': 1,
        'b': 2, 'k': 2, 't': 2,
        'c': 3, 'l': 3, 'u': 3,
        'd': 4, 'm': 4, 'v': 4,
        'e': 5, 'n': 5, 'w': 5,
        'f': 6, 'o': 6, 'x': 6,
        'g': 7, 'p': 7, 'y': 7,
        'h': 8, 'q': 8, 'z': 8,
        'i': 9, 'r': 9
    }

    nome_completo = nome_completo.lower()
    soma_total = 0

    for letra in nome_completo:
        if letra in tabela_pitagorica:
            soma_total += tabela_pitagorica[letra]
        elif letra == " ":
            continue
        else:
            return None  # Retorna None se encontrar caracteres inválidos

    while soma_total > 9 and soma_total not in [11, 22, 33]:
        soma_total = sum(int(digito) for digito in str(soma_total))

    return soma_total


def calcular_numero_caminho_vida(data_nascimento):
    """Calcula o Número do Caminho de Vida a partir da data de nascimento.

    Args:
      data_nascimento: A data de nascimento no formato DD/MM/AAAA (string).

    Returns:
      O Número do Caminho de Vida (int), ou None se a data for inválida.
    """
    try:
        dia, mes, ano = map(int, data_nascimento.split('/'))
        soma_total = dia + mes + ano

        while soma_total > 9:
            soma_total = sum(int(digito) for digito in str(soma_total))

        return soma_total
    except ValueError:
        return None  # Retorna None se a data for inválida

# Exemplo de uso:
nome = input("Digite seu nome completo: ")
data_nascimento = input("Digite sua data de nascimento no formato DD/MM/AAAA: ")

numero_destino = calcular_numero_destino(nome)
numero_caminho_vida = calcular_numero_caminho_vida(data_nascimento)

if numero_destino is not None and numero_caminho_vida is not None:
    print(f"O Número de Destino para {nome} é: {numero_destino}")
    print(f"O Número do Caminho de Vida para {data_nascimento} é: {numero_caminho_vida}")
elif numero_destino is None:
    print("Nome inválido. Utilize apenas letras e espaços.")
elif numero_caminho_vida is None:
    print("Data de nascimento inválida. Utilize o formato DD/MM/AAAA.")