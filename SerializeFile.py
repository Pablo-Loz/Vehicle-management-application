
from Car import Car

# CSV

import pandas as pd


def saveCarCSV(csv_filename, car):
    # Crear un DataFrame de Pandas a partir del objeto Car
    car_data = {
        "ID": [car.ID],
        "model": [car.model],
        "factory": [car.factory],
        "plate": [car.plate],
        "erased": [car.erased]
    }
    df = pd.DataFrame(car_data)

    # Modo 'a' para agregar al final del archivo si ya existe
    df.to_csv(csv_filename, mode='a', index=False, header=not pd.io.common.file_exists(csv_filename))


def modifyCarCSV(csv_filename, car):
    df = pd.read_csv(csv_filename)
    mask = df['ID'] == car.ID
    df.loc[mask, ['ID', 'model', 'factory', 'plate']] = [car.ID, car.model, car.factory, car.plate]
    df.to_csv(csv_filename, index=False)

def readCarCSV(csv_filename):
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: El archivo {csv_filename} no fue encontrado.")
        return []

    if df is None or df.empty:
        print("Advertencia: El DataFrame está vacío.")
        return []

    car_list: list[Car] = []
    for index, row in df.iterrows():
        if row['erase'] == False:  # Solo añadir a la lista si 'erase' es False
            car_list.append(Car(row['ID'], row['model'], row['factory'], row['plate']))

    return car_list
