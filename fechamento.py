import random
from itertools import combinations

def gerar_fechamento(grupo_principal, grupo_a, grupo_b, grupo_c):
    """Gera um fechamento combinatório para Lotofácil."""

    combinacoes = []
    # Aposta 1
    combinacao1 = grupo_principal + random.sample(grupo_a, 5)
    combinacoes.append(sorted(combinacao1))

    # Aposta 2
    combinacao2 = grupo_principal + random.sample(grupo_b, 5)
    combinacoes.append(sorted(combinacao2))

    # Aposta 3
    combinacao3 = grupo_principal + random.sample(grupo_c, 5)
    combinacoes.append(sorted(combinacao3))

    # Aposta 4
    combinacao4 = grupo_principal + random.sample(grupo_a+grupo_b+grupo_c,5)
    combinacoes.append(sorted(combinacao4))

    return combinacoes

def main():
    # Entrada Manual das 10 Dezenas
    while True:
        try:
            grupo_principal_str = input("Digite as 10 dezenas do grupo principal separadas por vírgula (ex: 2,4,6,7,8,10,12,15,16,17): ")
            grupo_principal = [int(num) for num in grupo_principal_str.split(',')]
            if len(grupo_principal) != 10 or any(num < 1 or num > 25 for num in grupo_principal):
                print("Por favor, insira 10 dezenas válidas entre 1 e 25.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira apenas números inteiros separados por vírgula.")

    # Gerar Grupos A, B e C Automaticamente
    todos_numeros = list(range(1, 26))
    grupo_a_b_c = [num for num in todos_numeros if num not in grupo_principal]
    random.shuffle(grupo_a_b_c)
    grupo_a = grupo_a_b_c[:5]
    grupo_b = grupo_a_b_c[5:10]
    grupo_c = grupo_a_b_c[10:15]

    apostas = gerar_fechamento(grupo_principal, grupo_a, grupo_b, grupo_c)

    print("\nApostas geradas:")
    for i, aposta in enumerate(apostas):
        print(f"Aposta {i + 1}: {aposta}")


if __name__ == "__main__":
    main()