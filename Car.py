class Car:
    # Class variables for table headings and field labels
    headings = ['ID', 'Model', 'Factory Address', 'Plate']
    fields = {
        '-ID-': 'Car ID:',
        '-Model-': 'Car Model:',
        '-Factory-': 'Factory Address:',
        '-Plate-': 'Plate:'
    }

    def __init__(self, ID, model, factory, plate):
        # Instance variables for car details
        self.ID = ID
        self.model = model
        self.factory = factory
        self.plate = plate
        self.erased = False

    def __eq__(self, other_car):
        # Overriding the equality operator to compare cars based on their ID
        return other_car.ID == self.ID

    def __str__(self):
        # Overriding the string representation of the car object
        return str(self.ID) + str(self.model) + str(self.factory) + str(self.plate)

    def set_car(self, name, factory, plate):
        # Method to update car details
        self.name = name
        self.factory = factory
        self.plate = plate