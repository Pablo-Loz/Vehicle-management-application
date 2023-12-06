# Importaciones de módulos necesarios
import Car
from SerializeFile import *
import PySimpleGUI as sg
import re
import operator
import pandas as pd

# List that will store the Car objects read from the CSV file
car_list2 = []

# Definition of regular expression patterns for validation
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"


def purgeCars(car_list, t_CarInterfaz):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('Car.csv')

    # Delete rows that have 'erase' set to True
    df = df[df['erase'] != True]

    # Save the DataFrame back to the CSV file
    df.to_csv('Car.csv', index=False)


# Function to add a new car to the list and save the data in a CSV file.
def add_car(car_list, t_CarInterfaz, oCar):
    save_car_csv('Car.csv', oCar)
    car_list.append(oCar)  # Add the Car object to the list
    t_CarInterfaz.append([oCar.ID, oCar.model, oCar.factory, oCar.plate])


# Function to remove a car from the list and update the interface and the CSV file.
def delCar(car_list, t_CarInterfaz, posinTable):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('Car.csv')

    # Search for the row that has the same ID as the car to be deleted
    car_id = t_CarInterfaz[posinTable][0]
    mask = df['ID'] == car_id

    # If such row is found, set the 'erase' value to True
    df.loc[mask, 'erase'] = True

    # Save the DataFrame back to the CSV file
    df.to_csv('Car.csv', index=False)

    # Search for the car in the list and delete it
    for o in car_list:
        if o.ID == car_id:
            o.erased = True
            break

    # Delete the car from the interface list
    for i, car in enumerate(t_CarInterfaz):
        if car[0] == car_id:
            del t_CarInterfaz[i]
            break


def check_id_exists(csv_filename, id_to_check):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Convert the ID column to string
    df['ID'] = df['ID'].astype(str)

    # Check if the ID exists in the ID column
    if str(id_to_check) in df['ID'].values:
        return True
    else:
        return False


# Function to update a car in the list and update the interface and the CSV file.
def updateCar(car_list, t_row_CarInterfaz):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('Car.csv')

    # Get the ID of the car to be updated
    car_id = str(t_row_CarInterfaz[0])
    df['ID'] = df['ID'].astype(str)

    # Search for the row that has the same ID as the car to be updated
    mask = df['ID'] == car_id

    #   If such row is found, update the values of the columns
    if df.loc[mask].shape[0] > 0:
        df.loc[mask, 'model'] = t_row_CarInterfaz[1]
        df.loc[mask, 'factory'] = t_row_CarInterfaz[2]
        df.loc[mask, 'plate'] = t_row_CarInterfaz[3]

        # Save the DataFrame back to the CSV file
        df.to_csv('Car.csv', index=False)

        # Search for the car in the list and update it
        for o in car_list:
            if o.ID == car_id:
                o.setCar(t_row_CarInterfaz[1], t_row_CarInterfaz[2], t_row_CarInterfaz[3])
                o.erased = False  # Set the 'erased' value to False
                break
    else:
        print("Error: No se encontró un coche con el ID proporcionado.")


def handle_add_event(event, values, car_list2, table_data, window):
    # Check if all fields have been filled
    if (check_id_exists('Car.csv', values['-ID-'])):
        sg.popup_error('El ID ya existe')
        return
    else:

        if all([values['-ID-'], values['-Model-'], values['-Factory-'], values['-Plate-']]):
            valida = False
            if re.match(pattern_ID, values['-ID-']):
                if re.match(pattern_phone, values['-Plate-']):
                    valida = True
            if valida:
                # Check if the ID already exists

                # Add the new car to the list and update the interface
                add_car(car_list2, table_data,
                        Car(values['-ID-'], values['-Model-'], values['-Factory-'], values['-Plate-']))
                window['-Table-'].update(table_data)
        else:
            # Show an error message if any of the fields is empty
            sg.popup_error('Todos los campos deben estar rellenados')


def handle_delete_event(event, values, car_list2, table_data, window):
    if len(values['-Table-']) > 0:
        delCar(car_list2, table_data, values['-Table-'][0])

        # Update the table in the GUI
        table_data.clear()
        for o in car_list2:
            if not o.erased:
                table_data.append([o.ID, o.model, o.factory, o.plate])

        # Update the table in the GUI
        window['-Table-'].update(table_data)


def handle_modify_event(event, values, car_list2, table_data, window):
    valida = False
    if re.match(pattern_ID, values['-ID-']):
        if re.match(pattern_phone, values['-Plate-']):
            valida = True
    if valida:
        rowToUpdate = None
        for t in table_data:
            if str(t[0]) == values['-ID-']:
                rowToUpdate = t
                t[1], t[2], t[3] = values['-Model-'], values['-Factory-'], values['-Plate-']
                break
        if rowToUpdate is None:
            print("Error: No se encontró un coche con el ID proporcionado EN EL EVENTO.")
            return
        updateCar(car_list2, rowToUpdate)
        window['-Table-'].update(table_data)
        window['-ID-'].update(disabled=False)


# Function to read the data from the CSV file and store it in a list of Car objects.
def interfaz():
    # Definición de fuentes para la interfaz
    font1, font2 = ('Arial', 14), ('Arial', 16)

    # Configure the PySimpleGUI theme
    sg.theme('Reddit')
    sg.set_options(font=font1)

    # List that will store the data to be displayed in the table
    table_data = []

    # List that will store the data of the row to be updated
    rowToUpdate = []

    # Read the CSV file and store the data in a list of Car objects
    car_list2 = read_car_csv('Car.csv')

    # Store the data of the Car objects in the list to be displayed in the table
    for o in car_list2:
        table_data.append([o.ID, o.model, o.factory, o.plate])

    # Definition of the layout of the GUI
    layout = [
                 [sg.Push(), sg.Text('Car CRUD'), sg.Push()]] + [
                 [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Car.fields.items()] + [
                 [sg.Push()] +
                 [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
                 [sg.Push()],
                 [sg.Table(values=table_data, headings=Car.headings, max_col_width=50, num_rows=10,
                           display_row_numbers=False, justification='center', enable_events=True,
                           enable_click_events=True, vertical_scroll_only=False,
                           select_mode=sg.TABLE_SELECT_MODE_BROWSE, expand_x=True, bind_return_key=True,
                           key='-Table-')],
                 [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')],
             ]
    sg.theme('Topanga')
    # Create the window
    window = sg.Window('Car Management with CSV', layout, finalize=True)

    window['-Table-'].bind("<Double-Button-1>", " Double")

    # Event loop. Read buttons, make callbacks
    while True:
        event, values = window.read()

        # Manage the window closing event
        if event == sg.WIN_CLOSED:
            break

        # Manage the event of adding a new car
        if event == 'Add':
            handle_add_event(event, values, car_list2, table_data, window)

        # Manage the event of deleting a car
        if event == 'Delete':
            handle_delete_event(event, values, car_list2, table_data, window)

        # Manage the event of double clicking on a row in the table
        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Model-'].update(str(table_data[row][1]))
                window['-Factory-'].update(str(table_data[row][2]))
                window['-Plate-'].update(str(table_data[row][3]))

        # Manage the event of clearing the fields
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Model-'].update('')
            window['-Factory-'].update('')
            window['-Plate-'].update('')

        # Manage the event of modifying a car
        if event == 'Modify':
            handle_modify_event(event, values, car_list2, table_data, window)

        # Manage the event of sorting the file
        if event == 'Sort File':
            # New window to select the value to sort by
            layout = ([[sg.Text('Select a value to sort by')],
                       [sg.Combo(['ID', 'model', 'factory', 'plate'], key='-COMBO-', default_value='plate')],
                       [sg.Button('OK')]])
            sort_window = sg.Window('Sort File', layout)

            while True:  # Event Loop
                sort_event, sort_values = sort_window.read()
                if sort_event == 'OK':
                    sort_window.close()

                    df = pd.read_csv('Car.csv')

                    # Order the DataFrame by the selected value
                    df.sort_values(by=sort_values['-COMBO-'], inplace=True)

                    # Write the sorted DataFrame back to the CSV file
                    df.to_csv('Car.csv', index=False)
                    break
                elif sort_event == sg.WIN_CLOSED:
                    break
                else:
                    break

        # Manage the event of purging the file
        if event == 'Purge':
            purgeCars(car_list2, table_data)
            window['-Table-'].update(table_data)

    # close the window
    window.close()


# call the function
interfaz()

# End of GUIp.py
