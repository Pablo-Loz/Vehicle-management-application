class Car:
    headings = ['ID', 'Model', 'Factory Address', 'Plate']
    fields = {
        '-ID-': 'Car ID:',
        '-Model-': 'Car Model:',
        '-Factory-': 'Factory Address:',
        '-Plate-': 'Plate:'
    }

    def __init__(self, ID, model, bill, Plate):
        self.ID = ID
        self.model = model
        self.factory = bill
        self.plate = Plate
        self.erased = False

    def __eq__(self, oC):
        return oC.ID == self.ID

    def __str__(self):
        return str(self.ID) + str(self.model) + str(self.factory) + str(self.plate)

    def setCar(self, name, bill, plate):
        self.name = name
        self.factory = bill
        self.plate = plate