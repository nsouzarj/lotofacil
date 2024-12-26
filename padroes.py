import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt


def carregar_dados(caminho_arquivo):
    """Carrega os dados de um arquivo CSV."""
    try:
        df = pd.read_csv(caminho_arquivo)
        df_numeros = df.iloc[:, 2:17]
        df_numeros = df_numeros.apply(pd.to_numeric, errors='coerce')
        return df_numeros
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
        return None


def analisar_repeticoes(df):
    """Analisa padrões de repetição de números nos sorteios."""
    resultados = df.values.tolist()
    analise = {
        'repeticao_imediata': defaultdict(int),
        'repeticao_2_sorteios': defaultdict(int),
        'repeticao_3_sorteios': defaultdict(int),
        'repeticao_geral': defaultdict(int)
    }

    for i in range(len(resultados)):
        for num in resultados[i]:
            analise['repeticao_geral'][num] += 1

    for i in range(len(resultados) - 1):
        proximo_sorteio = resultados[i + 1]
        for num in resultados[i]:
            if num in proximo_sorteio:
                analise['repeticao_imediata'][num] += 1

    for i in range(len(resultados) - 2):
        segundo_sorteio = resultados[i + 2]
        for num in resultados[i]:
            if num in segundo_sorteio:
                analise['repeticao_2_sorteios'][num] += 1

    for i in range(len(resultados) - 3):
        terceiro_sorteio = resultados[i + 3]
        for num in resultados[i]:
            if num in terceiro_sorteio:
                analise['repeticao_3_sorteios'][num] += 1

    return analise


def analisar_sequencias_repetidas(df):
    """ Analisa sequencias de números repetidas entre os sorteios"""
    resultados = df.values.tolist()
    sequencias = defaultdict(int)
    for i in range(len(resultados) - 1):
        sorteio_atual = resultados[i]
        proximo_sorteio = resultados[i + 1]

        for j in range(len(sorteio_atual) - 2):
            sequencia_atual = tuple(sorted(sorteio_atual[j:j + 3]))
            if sequencia_atual in [tuple(sorted(proximo_sorteio[k:k + 3])) for k in range(len(proximo_sorteio) - 2)]:
                sequencias[sequencia_atual] += 1
    return sequencias


def gerar_grafico_repeticao(repeticoes, titulo, tipo='bar'):
    """Gera um gráfico de barras ou pizza para as repetições."""
    numeros = list(repeticoes.keys())
    frequencias = list(repeticoes.values())

    plt.figure(figsize=(12, 6))
    if tipo == 'bar':
        plt.bar(numeros, frequencias, color='skyblue')
    elif tipo == 'pie':
        plt.pie(frequencias, labels=numeros, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(titulo)
    plt.xlabel("Número")
    plt.ylabel("Frequência")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


def gerar_grafico_sequencias(sequencias, titulo, top_n=40):
    """Gera um gráfico de barras para as sequências."""

    sequencias_ordenadas = sorted(sequencias.items(), key=lambda item: item[1], reverse=False)[:top_n]
    sequencias = [str(list(seq)) for seq, _ in sequencias_ordenadas]
    frequencias = [freq for _, freq in sequencias_ordenadas]

    plt.figure(figsize=(12, 6))
    plt.bar(sequencias, frequencias, color='lightcoral')
    plt.title(titulo)
    plt.xlabel("Sequência")
    plt.ylabel("Frequência")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()


def main():
    caminho_arquivo = '/home/nelson/pagina/lotofacil.csv'
    df = carregar_dados(caminho_arquivo)

    if df is None:
        return

    analise_repeticao = analisar_repeticoes(df)
    print("Análise de Repetição de Números:\n")
    print("Repetição Imediata:", analise_repeticao['repeticao_imediata'])
    print("Repetição em 2 Sorteios:", analise_repeticao['repeticao_2_sorteios'])
    print("Repetição em 3 Sorteios:", analise_repeticao['repeticao_3_sorteios'])
    print("Repetição Geral:", analise_repeticao['repeticao_geral'])

    # Gera gráficos
    gerar_grafico_repeticao(analise_repeticao['repeticao_imediata'], "Repetição Imediata (Barras)")
    gerar_grafico_repeticao(analise_repeticao['repeticao_2_sorteios'], "Repetição em 2 Sorteios (Barras)")
    gerar_grafico_repeticao(analise_repeticao['repeticao_3_sorteios'], "Repetição em 3 Sorteios (Barras)")
    gerar_grafico_repeticao(analise_repeticao['repeticao_geral'], "Repetição Geral (Barras)")

    analise_sequencias = analisar_sequencias_repetidas(df)
    print("\nAnálise de Sequências Repetidas (3 Números):\n")
    for seq, freq in sorted(analise_sequencias.items(), key=lambda item: item[1], reverse=False):
        print(f"Sequência:{freq} {list(seq)} - Frequência: {freq}")
    gerar_grafico_sequencias(analise_sequencias, "Sequências Mais Repetidas", top_n=153)


if __name__ == "__main__":
    main()