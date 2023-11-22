#https://apuntes.de/python/expresiones-regulares-y-busqueda-de-patrones-en-python-poder-y-flexibilidad/#gsc.tab=0
#https://rico-schmidt.name/pymotw-3/pickle/index.html
#https://stackoverflow.com/questions/55809976/seek-on-pickled-data
#https://www.reddit.com/r/learnpython/comments/pgfj63/sorting_a_table_with_pysimplegui/
#https://www.geeksforgeeks.org/python-sorted-function/
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Element_Header_or_Cell_Clicks.py
#https://github.com/PySimpleGUI/PySimpleGUI/issues/5646
#https://docs.python.org/3/howto/sorting.html
import Car
from SerializeFile import *
from Car import *
import PySimpleGUI as sg
import re
import operator


fCar = open('Car.txt', 'rb+')
car_list=[]
"""pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"""""
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"


def add_car(car_list, t_CarInterfaz, oCar):
    car_list.append(oCar)
    saveCar(fCar, oCar)
    t_CarInterfaz.append([oCar.ID, oCar.model, oCar.factory, oCar.plate, oCar.posFile])
    pass

def delCar(car_list, t_CarInterfaz, posinTable):
    posinFile=t_CarInterfaz[posinTable][-1]
    cdel=None
    for o in car_list:
        if (o.carInpos(posinFile)):
            cdel=o
            break
    if (cdel is not None):
        car_list.remove(cdel)
        t_CarInterfaz.remove(t_CarInterfaz[posinTable])
        cdel.erased=True
        modifyCar(fCar, cdel)
    pass

def updateCar(car_list, t_row_CarInterfaz, posinFile):
    cdel=None
    for o in car_list:
        if (o.carInpos(posinFile)):
            cdel=o
            break
    if (cdel is not None):
        cdel.setCar(t_row_CarInterfaz[1],t_row_CarInterfaz[2],t_row_CarInterfaz[3])
        modifyCar(fCar, cdel)
    pass

def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table



def interfaz():
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.set_options(font=font1)
    table_data=[]
    rowToUpdate = []

    readCar(fCar, car_list)
    for o in car_list:
        if (not o.erased):
            table_data.append([o.ID, o.model, o.factory, o.plate, o.posFile])

    layout = [
        [sg.Push(), sg.Text('Car CRUD'), sg.Push()]] + [
        [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Car.fields.items()] + [
        [sg.Push()] +
        [sg.Button(button) for button in ('Add', 'Delete','Modify','Clear')] +
        [sg.Push()],
        [sg.Table(values=table_data, headings=Car.headings, max_col_width=50, num_rows=10,
            display_row_numbers=False, justification='center', enable_events=True, enable_click_events=True,
            vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            expand_x=True,bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Push(),sg.Button('Sort File')],
    ]
    sg.theme('DarkBlue2')
    window = sg.Window('Car Management with Files', layout,finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
          break
        if event == 'Add':
            valida=False
            if re.match(pattern_ID, values['-ID-']):
                if re.match(pattern_phone, values['-Plate-']):
                    valida=True
            if (valida):
                add_car(car_list, table_data, Car(values['-ID-'], values['-Model-'], values['-Factory-'], values['-Plate-'], -1))
                window['-Table-'].update(table_data)
        if event == 'Delete':
            if(len(values['-Table-'])>0):
                delCar(car_list, table_data, values['-Table-'][0])
                window['-Table-'].update(table_data)

        if (event == '-Table- Double'):
            print(event)
            print(values)
            print(len(values['-Table-']))
            if len(values['-Table-']) > 0:
                row=values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Model-'].update(str(table_data[row][1]))
                window['-Factory-'].update(str(table_data[row][2]))
                window['-Plate-'].update(str(table_data[row][3]))
                window['-PosFile-'].update(str(table_data[row][4]))
            pass
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Model-'].update('')
            window['-Factory-'].update('')
            window['-Plate-'].update('')
            window['-PosFile-'].update('')

        if event == 'Modify':
            valida=False
            if re.match(pattern_ID, values['-ID-']):
                if re.match(pattern_phone, values['-Plate-']):
                        valida=True
            if valida:
                for t in table_data:
                    if t[-1] == int(values['-PosFile-']):
                        rowToUpdate=t
                        t[1], t[2], t[3] = values['-Model-'], values['-Factory-'], values['-Plate-']
                        break
                updateCar(car_list, rowToUpdate, int(values['-PosFile-']))
                window['-Table-'].update(table_data)
                window['-ID-'].update(disabled=False)
                
        if isinstance(event, tuple):
            print(event)
            print(values)
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
        # You can also call Table.get_last_clicked_position to get the cell clicked
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

        """if event == 'Purge': EVENTO DE PULSAR EL BOTON PURGE
                    purgeCar(fCar, car_list)
                    table_data.clear()
                    window['-Table-'].update(table_data)"""

    window.close()

interfaz()
fCar.close()

