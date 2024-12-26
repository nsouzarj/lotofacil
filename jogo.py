import random
import pandas as pd


def carregar_dados(caminho_arquivo):
    """Carrega os dados de um arquivo CSV e seleciona as colunas de números."""
    try:
        df = pd.read_csv(caminho_arquivo)
        # Seleciona as colunas das bolas (colunas de índice 2 a 16)
        df_numeros = df.iloc[:, 2:17]
        # Força a conversão para int
        df_numeros = df_numeros.apply(pd.to_numeric, errors='coerce')

        return df_numeros
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
        return None


def calcular_frequencia_numeros(df):
    """Calcula a frequência de cada número."""
    todos_numeros = df.values.flatten()
    frequencia = pd.Series(todos_numeros).value_counts().sort_index()
    return frequencia


def gerar_combinacao_mais_frequentes(frequencia, quantidade=15):
    """Gera combinação com os números mais frequentes."""
    mais_frequentes = frequencia.nlargest(quantidade).index.tolist()
    return sorted(random.sample(mais_frequentes, 15))


def gerar_combinacao_menos_frequentes(frequencia, quantidade=15):
    """Gera combinação com os números menos frequentes."""
    menos_frequentes = frequencia.nsmallest(25).index.tolist()  # Lista com os 25 números menos frequentes
    if len(menos_frequentes) < 15:
        numeros_faltando = 15 - len(menos_frequentes)
        numeros_aleatorios = [num for num in range(1, 26) if num not in menos_frequentes]
        menos_frequentes.extend(random.sample(numeros_aleatorios, numeros_faltando))
    return sorted(random.sample(menos_frequentes, 15))


def gerar_combinacao_mix_frequencias(frequencia, quantidade_mais=7, quantidade_menos=8):
    """Gera combinação com mix de números mais e menos frequentes."""
    mais_frequentes = frequencia.nlargest(quantidade_mais).index.tolist()
    menos_frequentes = frequencia.nsmallest(quantidade_menos).index.tolist()
    combinacao = random.sample(mais_frequentes, quantidade_mais) + random.sample(menos_frequentes, quantidade_menos)
    return sorted(random.sample(combinacao, 15))


def calcular_somas_sorteios(df):
    """Calcula a soma dos números em cada sorteio."""
    return df.sum(axis=1)


def gerar_combinacao_por_soma(df, faixa_soma_min, faixa_soma_max):
    """Gera combinação com soma dentro de uma faixa."""
    while True:
        combinacao = sorted(random.sample(range(1, 26), 15))
        soma_combinacao = sum(combinacao)
        if faixa_soma_min <= soma_combinacao <= faixa_soma_max:
            return combinacao


def calcular_pares_impares(df):
    """ Calcula quantidade de pares e impares por sorteio."""
    pares_impares = []
    for index, row in df.iterrows():
        pares = 0
        impares = 0
        for num in row:
            try:
                num = int(num)  # Tenta converter para inteiro
                if num % 2 == 0:
                    pares += 1
                else:
                    impares += 1
            except ValueError:
                result_series = row.index[row == num]
                if not result_series.empty:
                    print(f"Erro: Valor não numérico encontrado: {num} na linha {index}, coluna {result_series[0]}")
                else:
                    print(f"Erro: Valor não numérico encontrado: {num} na linha {index}, sem coluna definida")
        pares_impares.append({'pares': pares, 'impares': impares})
    return pares_impares


def gerar_combinacao_por_pares_impares(pares_impares_analise, mais_pares=True):
    """Gera uma combinação baseada no padrão de pares e impares"""
    pares = 0
    impares = 0
    if mais_pares:
        while pares <= 6:
            combinacao = sorted(random.sample(range(1, 26), 15))
            pares = 0
            impares = 0
            for num in combinacao:
                if num % 2 == 0:
                    pares += 1
                else:
                    impares += 1
        return combinacao
    else:
        while impares <= 6:
            combinacao = sorted(random.sample(range(1, 26), 15))
            pares = 0
            impares = 0
            for num in combinacao:
                if num % 2 == 0:
                    pares += 1
                else:
                    impares += 1
        return combinacao


def analisar_distribuicao_por_linha_coluna(df):
    """Analisa a distribuição dos números por linha e coluna no volante da Lotofácil."""
    distribuicao = {'linhas': [], 'colunas': []}

    for _, row in df.iterrows():
        linhas = [0] * 5
        colunas = [0] * 10
        for num in row:
            try:
                num = int(num)
                linha = (num - 1) // 5  # Identifica a linha (0 a 4)
                coluna = (num - 1) % 10  # Identifica a coluna (0 a 9)
                linhas[linha] += 1
                colunas[coluna] += 1
            except ValueError:
                result_series = row.index[row == num]
                if not result_series.empty:
                    print(f"Erro: Valor não numérico encontrado: {num} na linha {row.name}, coluna {result_series[0]}")
                else:
                    print(f"Erro: Valor não numérico encontrado: {num} na linha {row.name}, sem coluna definida")
        distribuicao['linhas'].append(linhas)
        distribuicao['colunas'].append(colunas)

    return distribuicao


def gerar_combinacao_por_distribuicao(distribuicao_analise, linhas_escolhidas, colunas_escolhidas):
    """Gera combinação baseada na distribuição por linha e coluna."""
    combinacao = []
    linhas_usadas = []
    for l in linhas_escolhidas:
        numeros_linha = [num for num in range(1, 26) if (num - 1) // 5 == l]
        linha = random.sample(numeros_linha, linhas_escolhidas[l])
        combinacao.extend(linha)
        linhas_usadas.extend(linha)

    colunas_disponiveis = set(colunas_escolhidas)  # Usando set para eficiência

    # Calcula quantos números faltam
    numeros_faltando = 15 - len(combinacao)

    # Gera os números restantes de uma vez
    numeros_restantes = []
    todos_numeros = list(range(1, 26))
    random.shuffle(todos_numeros)

    combinacao_set = set(combinacao)

    for num in todos_numeros:
        if len(numeros_restantes) == numeros_faltando:
            break
        coluna = (num - 1) % 10
        if coluna in colunas_disponiveis and num not in combinacao_set:
            numeros_restantes.append(num)
            combinacao_set.add(num)

    combinacao.extend(numeros_restantes)
    return sorted(combinacao)


def main():
    caminho_arquivo = '/home/nelson/pagina/lotofacil.csv'  # Substitua pelo caminho do seu arquivo
    df = carregar_dados(caminho_arquivo)

    if df is None:
        return

    # Calcular a frequência dos números nos últimos 6 jogos
    df_ultimos_6 = df.tail(6)
    frequencia_ultimos_6 = calcular_frequencia_numeros(df_ultimos_6)

    # Obter os números mais e menos frequentes
    mais_frequentes_ultimos_6 = frequencia_ultimos_6.nlargest(15).index.tolist()
    menos_frequentes_ultimos_6 = frequencia_ultimos_6.nsmallest(15).index.tolist()

    # Exibir os resultados
    print("Números Mais Frequentes nos Últimos 6 Jogos:", mais_frequentes_ultimos_6)
    print("Números Menos Frequentes nos Últimos 6 Jogos:", menos_frequentes_ultimos_6)

    frequencia_numeros = calcular_frequencia_numeros(df)
    somas_sorteios = calcular_somas_sorteios(df)
    pares_impares_sorteios = calcular_pares_impares(df)
    distribuicao_analise = analisar_distribuicao_por_linha_coluna(df)

    # Exemplos de geração de combinações
    print("Combinação Mais Frequentes:", gerar_combinacao_mais_frequentes(frequencia_numeros))
    print("Combinação Menos Frequentes:", gerar_combinacao_menos_frequentes(frequencia_numeros))
    print("Combinação Mix Frequências:", gerar_combinacao_mix_frequencias(frequencia_numeros))
    print("Combinação Por Soma (180-220):", gerar_combinacao_por_soma(df, 180, 220))
    print("Combinação Mais Pares:", gerar_combinacao_por_pares_impares(pares_impares_sorteios, mais_pares=True))
    print("Combinação Mais Impares:", gerar_combinacao_por_pares_impares(pares_impares_sorteios, mais_pares=False))

    # Escolhendo 2 números na linha 0 e 3 números na linha 2
    linhas_escolhidas = {0: 2, 2: 3}
    # Escolhendo a coluna 1 e 4
    colunas_escolhidas = [1, 4]
    print("Combinação por Linhas e Colunas",
          gerar_combinacao_por_distribuicao(distribuicao_analise, linhas_escolhidas, colunas_escolhidas))


if __name__ == "__main__":
    main()