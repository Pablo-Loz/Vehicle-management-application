import pickle
def saveCar(f,oC):
    f.seek(0, 2)
    oC.posFile=f.tell()
    pickle.dump(oC, f)


def modifyCar(f,oC):
    f.seek(oC.posFile,0)
    pickle.dump(oC, f)

def readCar(fCar,lC):
    fCar.seek(0,0)
    while True:
        try:
            lC.append(pickle.load(fCar))
        except EOFError:
            break
