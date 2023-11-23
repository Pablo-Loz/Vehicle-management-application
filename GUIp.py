# Importaciones de módulos necesarios
import Car
from SerializeFile import *
import PySimpleGUI as sg
import re
import operator
import pandas as pd


# Lista que almacenará los objetos Car leídos desde el archivo CSV
car_list2 = []

# Definición de patrones de expresiones regulares para validación
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"



# Función para agregar un nuevo automóvil a la lista y guardar los datos en un archivo CSV
def add_car(car_list, t_CarInterfaz, oCar):
    saveCarCSV('Car.csv', oCar)
    car_list.append(oCar)  # Agrega el objeto Car a la lista
    t_CarInterfaz.append([oCar.ID, oCar.model, oCar.factory, oCar.plate])


# Función para eliminar un automóvil de la lista y actualizar la interfaz y el archivo CSV
def delCar(car_list, t_CarInterfaz, posinTable):
    # Leer el archivo CSV y almacenar los datos en un DataFrame
    df = pd.read_csv('Car.csv')

    # Buscar la fila que tenga el mismo ID que el coche que se quiere eliminar
    mask = df['ID'] == t_CarInterfaz[posinTable][0]

    # Si se encuentra tal fila, cambiar el valor de 'erase' a True
    df.loc[mask, 'erase'] = True

    # Guardar el DataFrame de nuevo en el archivo CSV
    df.to_csv('Car.csv', index=False)

    # Actualizar la lista de coches en memoria
    for o in car_list:
        if o.ID == t_CarInterfaz[posinTable][0]:
            o.erased = True
            break

    # Eliminar el coche de la lista de la interfaz
    t_CarInterfaz.remove(t_CarInterfaz[posinTable])


# Función para actualizar un automóvil en la lista y el archivo CSV
def updateCar(car_list, t_row_CarInterfaz):
    # Leer el archivo CSV y almacenar los datos en un DataFrame
    df = pd.read_csv('Car.csv')

    # Convertir el ID a string antes de hacer la comparación
    car_id = str(t_row_CarInterfaz[0])
    df['ID'] = df['ID'].astype(str)

    # Buscar la fila que tenga el mismo ID que el coche que se quiere actualizar
    mask = df['ID'] == car_id

    # Si se encuentra tal fila, actualizar los valores de esa fila con los nuevos valores del coche
    if df.loc[mask].shape[0] > 0:
        df.loc[mask, 'model'] = t_row_CarInterfaz[1]
        df.loc[mask, 'factory'] = t_row_CarInterfaz[2]
        df.loc[mask, 'plate'] = t_row_CarInterfaz[3]
        #df.loc[mask, 'erased'] = False  # Asegurarse de que el estado 'erased' se establece en False

        # Guardar el DataFrame de nuevo en el archivo CSV
        df.to_csv('Car.csv', index=False)

        # Actualizar la lista de coches en memoria
        for o in car_list:
            if o.ID == car_id:
                o.setCar(t_row_CarInterfaz[1], t_row_CarInterfaz[2], t_row_CarInterfaz[3])
                o.erased = False  # Asegurarse de que el estado 'erased' se establece en False
                break
    else:
        print("Error: No se encontró un coche con el ID proporcionado.")

def handle_add_event(event, values, car_list2, table_data, window):
    valida = False
    if re.match(pattern_ID, values['-ID-']):
        if re.match(pattern_phone, values['-Plate-']):
            valida = True
    if valida:
        add_car(car_list2, table_data, Car(values['-ID-'], values['-Model-'], values['-Factory-'],values['-Plate-']))
        window['-Table-'].update(table_data)

def handle_delete_event(event, values, car_list2, table_data, window):
    if len(values['-Table-']) > 0:
        delCar(car_list2, table_data, values['-Table-'][0])
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

# Función para ordenar la tabla por múltiples columnas
def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


# Función principal que define la interfaz gráfica y maneja eventos
def interfaz():
    # Definición de fuentes para la interfaz
    font1, font2 = ('Arial', 14), ('Arial', 16)

    # Configuración de la apariencia de PySimpleGUI
    sg.theme('Reddit')
    sg.set_options(font=font1)

    # Lista que almacenará los datos para la tabla en la interfaz
    table_data = []

    # Lista que se utilizará para actualizar un automóvil existente
    rowToUpdate = []

    # Lectura de datos desde el archivo CSV
    car_list2 = readCarCSV('Car.csv')

    # Llenado de la lista de datos para la tabla
    for o in car_list2:
        table_data.append([o.ID, o.model, o.factory, o.plate])

    # Definición de la disposición de la interfaz
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
    # Creación de la ventana de PySimpleGUI
    window = sg.Window('Car Management with CSV', layout, finalize=True)

    window['-Table-'].bind("<Double-Button-1>", " Double")

    # Bucle principal para manejar eventos de la interfaz
    while True:
        event, values = window.read()

        # Manejo del evento de cerrar la ventana
        if event == sg.WIN_CLOSED:
            break

        # Manejo del evento de agregar un automóvil
        if event == 'Add':
            handle_add_event(event, values, car_list2, table_data, window)

        # Manejo del evento de eliminar un automóvil
        if event == 'Delete':
            handle_delete_event(event, values, car_list2, table_data, window)

        # Manejo del evento de doble clic en la tabla
        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Model-'].update(str(table_data[row][1]))
                window['-Factory-'].update(str(table_data[row][2]))
                window['-Plate-'].update(str(table_data[row][3]))

        # Manejo del evento de limpiar campos
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Model-'].update('')
            window['-Factory-'].update('')
            window['-Plate-'].update('')

        # Manejo del evento de modificar un automóvil
        if event == 'Modify':
            handle_modify_event(event, values, car_list2, table_data, window)

        # Manejo del evento de clic en la tabla para ordenar
        if isinstance(event, tuple):
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    # Cierre de la ventana al salir del bucle
    window.close()


# Llamada a la función principal
interfaz()

# Cierre del archivo al finalizar el programa
