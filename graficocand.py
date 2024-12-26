import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle


# Função para gerar dados simulados (mantido como antes)
def generate_candlestick_data(num_points=100):
    dates = pd.date_range("2024-01-01", periods=num_points, freq="H")
    open_prices = np.random.rand(num_points) * 50 + 100  # Preços de abertura base
    high_prices = open_prices + np.random.rand(num_points) * 10  # Preços máximos
    low_prices = open_prices - np.random.rand(num_points) * 10  # Preços mínimos
    close_prices = open_prices + np.random.randn(num_points) * 5  # Preços de fechamento variam mais

    # Ajuste para garantir que os preços de máximos e mínimos estejam corretos
    high_prices = np.maximum(high_prices, np.maximum(open_prices, close_prices))
    low_prices = np.minimum(low_prices, np.minimum(open_prices, close_prices))

    df = pd.DataFrame(
        {
            "Date": dates,
            "Open": open_prices,
            "High": high_prices,
            "Low": low_prices,
            "Close": close_prices,
        }
    )
    return df


# Criar os dados
df = generate_candlestick_data(100)

# Calcular a Média Móvel Simples (SMA) de 20 períodos
period = 20
df['SMA'] = df['Close'].rolling(window=period).mean()

# Criar o gráfico
fig, ax = plt.subplots(figsize=(12, 6))

# Definir a cor de fundo do gráfico para preto
ax.set_facecolor('black')

# Largura do candle ajustada
width = 4 / len(df)

# Iterar sobre os dados para criar cada candlestick
for i in range(len(df)):
    date = mdates.date2num(df["Date"][i])
    open_price = df["Open"][i]
    high_price = df["High"][i]
    low_price = df["Low"][i]
    close_price = df["Close"][i]

    # Desenhar o corpo do candle
    if close_price > open_price:
        color = "blue"
        rect = Rectangle((date - width / 2, open_price), width, close_price - open_price, facecolor=color,
                         edgecolor="white")
    else:
        color = "red"
        rect = Rectangle((date - width / 2, close_price), width, open_price - close_price, facecolor=color,
                         edgecolor="white")

    ax.add_patch(rect)

    # Desenhar as sombras (máximo e mínimo)
    ax.plot([date, date], [low_price, high_price], color="white", linewidth=1)

# Plotar a linha da SMA
ax.plot(df['Date'], df['SMA'], color='blue', label=f'SMA ({period})', linewidth=1.5)
ax.legend(facecolor='black', labelcolor='white')

# Formatar o eixo X para datas
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
plt.xticks(rotation=45, ha="right", color='white')

# Adicionar títulos e rótulos
ax.set_title("Gráfico de Candlestick com SMA", color='white')
ax.set_xlabel("Data", color='white')
ax.set_ylabel("Preço", color='white')
ax.grid(True, color='gray')
ax.tick_params(axis='y', colors='white')

plt.tight_layout()
plt.show()