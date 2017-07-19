import numpy as np

################################################################################
class BasicPlayer:
    """docstring for BasicPlayer.
    """
    def __init__(self, name, herb=0,owner=None):
        self.name = name
        self.herb = int(herb)
        self.owner= owner

    def __str__( self ):
        return "Name : " +self.name +" herb: "+ str(self.herb)

################################################################################
class Foundable:
    """docstring for Foundable.
    """
    def __init__(self, name,desc=None):
        self.name=name
        self.desc=desc

    def __str__(self):
        return self.desc

################################################################################
class Plant(Foundable):
    """docstring for Plant.
    """
    def __init__(self, name, desc=None):
        super(Plant, self).__init__(name, desc)

    def __str__(self):
        return self.desc

################################################################################
class Animal(Foundable):
    """docstring for Animal.
    """
    def __init__(self, name, desc=None):
        super(Animal, self).__init__(name, desc)

################################################################################
class OtherObj(Foundable):
    """docstring for OtherObj.
    """
    def __init__(self, name, desc=None):
        super(OtherObj, self).__init__(name, desc)

################################################################################
class Enviroment:
    """docstring for Enviroment.
       Actualmente el Enviroment solo dispone de lista de plantas.
    """
    def __init__(self, name,probDistro, paramsDistro=[],desc=None,listPlants=[],listAnimals=[],listOtherObj=[]):
        self.name=name
        self.probDistro=probDistro #https://en.wikipedia.org/wiki/List_of_probability_distributions
        self.paramsDistro=paramsDistro
        self.desc=desc
        self.listPlants=sorted(listPlants, reverse=True)#lista de tuplas (prob, obj, numObj)
        self.listAnimals=sorted(listAnimals, reverse=True)#lista de tuplas (prob, obj, numObj)
        self.listOtherObj=sorted(listOtherObj, reverse=True)#lista de tuplas (prob, obj, numObj)

    def __str__(self):
        return self.name +': ' + self.desc

    def applyDistro(self, num=1):
        """devuelve un numero aleatorio con probabilidad del Enviroment"""
        return self.probDistro(*self.paramsDistro,num)



#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
    def getPlants(self):
        return self.listPlants
    def getAnimals(self):
        return self.listAnimals
    def getOtherObj(self):
        return self.getOtherObj
    def getObj(self):
        return {'Plants':self.getPlants(),'Animals':self.getAnimals(),'Other':self.getOtherObj()}
#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #

################################################################################
class Game:
    """docstring for Game.
       Hay que hacer que la formula sea un parametro
    """
    def __init__(self, name, lPlayer=[],lEnv=[]):
        self.name=name
        self.lPlayer=lPlayer
        self.lEnv=lEnv

#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
    def addPlayer(self,p):
        self.lPlayer.append(p)

    def addEnv(self,e):
        self.lEnv.append(e)

    def rmPlayer(self, p):
        self.lPlayer.remove(p)

    def rmEnv(self,e):
        self.lEnv.remove(p)
#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
    def serchPlant(self,nHoras, pl, env, dice=0):
        L=[]
        plants=env.getPlants()
        #formula prob
        probs=env.applyDistro(nHoras)+(bp.herb/100)*1.5

        for p in probs:
            for j in range(len(plants)):
                if p > plants[j][0]:#probabilidad de la tupla numero i
                    L.append(plants[j][1])#anyadimos el elemento a la lista resultado
                    break
        return L

amapola=Plant('amapola', desc='Una simple amapola')
rosa=Plant('rosa',desc='una rosa roja')
bl=Plant('Black Lotus',desc='THE BLACK LOTUS')
perro=Animal('perro',desc='Un perro')
pradera=Enviroment('pradera',np.random.beta,paramsDistro=[1,2.3], \
                    desc='una simple pradera', \
                    listPlants=[(0.7,rosa,1),(0.5,amapola,1), (0.9,bl,1)], listAnimals=[perro])
bp=BasicPlayer('ton',herb=18)
g=Game('prueba', lEnv=[pradera])


L=g.serchPlant(10,bp,pradera,0)


print(pradera.getPlants())
print(len(L))
print(L.count(bl))
print(L.count(rosa))
print(L.count(amapola))
print(L)
