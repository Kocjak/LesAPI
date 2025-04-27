from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from hdfs import InsecureClient

def load_weather_data(file_path):
    df = pd.read_csv(file_path)
    return df


def extract_temperature_data(weather_data):
    temperature_data = []
    for city, data in weather_data.groupby('Location'):
        temperature = data['Temperature_C'].mean()
        temperature_data.append((city, temperature))
    return temperature_data


def plot_temperature_change(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='City', y='Temperature', marker='o')
    plt.title('Temperature Change in Different Cities')
    plt.xlabel('Cities')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('temp_change.png')
    plt.show()


def plot_temperature_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Temperature'], bins=5, kde=True)
    plt.title('Temperature Distribution')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('temp_distribution.png')
    plt.show()


data_path = Path("kaggle_wqather.csv")
weather_data = load_weather_data(data_path)
temperature_data = extract_temperature_data(weather_data)
df = pd.DataFrame(temperature_data, columns=['City', 'Temperature'])

plot_temperature_change(df)
plot_temperature_distribution(df)

client = InsecureClient('http://172.18.0.4:50070/')

# Сохранение изображений в HDFS
client = pa.hdfs.connect()
with open('temp_change.png', 'rb') as file:
    with client.open('temp_change_new.png', 'wb') as output_file:
        output_file.write(file.read())

with open('temp_distribution.png', 'rb') as file:
    with client.open('temp_distribution_new.png', 'wb') as output_file:
        output_file.write(file.read())