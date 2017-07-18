import numpy as np

class BasicPlayer:
    """docstring for BasicPlayer.
    """
    def __init__(self, name, herb=0,owner=None):
        self.name = name
        self.herb = herb
        self.owner= owner

    def __str__( self ):
        return "Name : " +self.name +" herb: "+ str(self.herb)


class Foundable:
    """docstring for Foundable.
    """
    def __init__(self, name,desc=None):
        self.name=name
        self.desc=desc

    def __str__(self):
        return self.desc


class Plant(Foundable):
    """docstring for Plant.
    """
    def __init__(self, name, desc=None):
        super(Plant, self).__init__(name, desc)


class Animal(Foundable):
    """docstring for Animal.
    """
    def __init__(self, name, desc=None):
        super(Animal, self).__init__(name, desc)


class OtherObj(Foundable):
    """docstring for OtherObj.
    """
    def __init__(self, name, desc=None):
        super(OtherObj, self).__init__(name, desc)


class Enviroment:
    """docstring for Enviroment.
       Actualmente el Enviroment solo dispone de lista de plantas.
    """
    def __init__(self, name,probDistro, paramsDistro=[],desc=None,listPlants=[],listAnimals=[],listOtherObj=[]):
        self.name=name
        self.probDistro=probDistro
        self.paramsDistro=paramsDistro
        self.desc=desc
        self.listPlants=listPlants
        self.listAnimals=listAnimals
        self.listOtherObj=listOtherObj

    def applyDistro(self):
        """devuelve un numero aleatorio con probabilidad del Enviroment"""
        return self.probDistro(*self.paramsDistro)

    def __str__(self):
        return self.name +': ' + self.desc
################################################################################
    def getPlants(self):
        return self.listPlants
    def getAnimals(self):
        return self.listAnimals
    def getOtherObj(self):
        return self.getOtherObj
    def getObj(self):
        return {'Plants':self.getPlants(),'Animals':self.getAnimals(),'Other':self.getOtherObj()}
################################################################################




amapola=Plant('amapola', desc='Una simple amapola')
pradera=Enviroment('pradera',np.random.exponential,paramsDistro=[],desc='una simple pradera', listPlants=[amapola])
print(pradera.applyDistro())

print(pradera.getPlants())
