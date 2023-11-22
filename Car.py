class Car:
    headings = ['ID', 'Model', 'Factory Address', 'Plate', 'Pos']
    fields = {
        '-ID-': 'Car ID:',
        '-Model-': 'Car Model:',
        '-Factory-': 'Factory Address:',
        '-Plate-': 'Plate:',
        '-PosFile-': 'Position into File'
    }

    # El método __init__ es llamado al crear el objeto
    def __init__(self, ID, model, bill, Plate, posFile):
        # Atributos de instancia
        self.ID = ID
        self.model = model
        self.factory = bill
        self.plate = Plate
        self.posFile = posFile
        self.erased = False

    def __eq__(self, oC):
        return oC.posFile == self.posFile

    def __str__(self):
        return str(self.ID) + str(self.name) + str(self.bill) + str(self.plate) + str(self.posFile)

    """def customerinPos(self, pos):
        return self.posFile == pos"""


    def carInpos(self, pos):
        return self.posFile == pos

    def setCar(self, name, bill, plate):
        self.name = name
        self.bill = bill
        self.plate = plate
        """self.email = email"""
