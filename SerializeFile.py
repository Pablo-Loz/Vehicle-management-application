
from Car import Car

# CSV

import pandas as pd


def save_car_csv(csv_filename, car):
    # Create a Pandas DataFrame from the Car object
    car_data = {
        "ID": [car.ID],
        "model": [car.model],
        "factory": [car.factory],
        "plate": [car.plate],
        "erased": [car.erased]
    }
    df = pd.DataFrame(car_data)

    # 'a' mode to append at the end of the file if it already exists
    df.to_csv(csv_filename, mode='a', index=False, header=not pd.io.common.file_exists(csv_filename))


def modify_car_csv(csv_filename, car):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Find the row that has the same ID as the car to be updated
    mask = df['ID'] == car.ID

    # If such a row is found, update the values of that row with the new values of the car
    df.loc[mask, ['ID', 'model', 'factory', 'plate']] = [car.ID, car.model, car.factory, car.plate]

    # Save the DataFrame back to the CSV file
    df.to_csv(csv_filename, index=False)


def read_car_csv(csv_filename):
    try:
        # Try to read the CSV file into a DataFrame
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        # Print an error message if the file is not found
        print(f"Error: The file {csv_filename} was not found.")
        return []

    if df is None or df.empty:
        # Print a warning if the DataFrame is empty
        print("Warning: The DataFrame is empty.")
        return []

    # List that will store the Car objects
    car_list: list[Car] = []

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # Only add to the list if 'erase' is False
        if row['erase'] == False:
            car_list.append(Car(row['ID'], row['model'], row['factory'], row['plate']))

    return car_list