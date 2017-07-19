import numpy as np
import copy as cp

################################################################################
class BasicPlayer:
    """docstring for BasicPlayer.
    """
    def __init__(self, name, owner=None, herb=0,hunt=0):
        self.name = name
        self.owner= owner
        self.herb = int(herb)
        self.hunt = int(hunt)

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
    """
    def __init__(self, name,probDistro, paramsDistro=[],desc=None,listPlants=[],listAnimals=[],listOtherObj=[]):
        self.name=name
        self.probDistro=probDistro #https://en.wikipedia.org/wiki/List_of_probability_distributions
        self.paramsDistro=paramsDistro
        self.desc=desc
        self.listPlants=sorted(cp.deepcopy(listPlants), reverse=True)#lista de tuplas (prob, obj, numObj)
        self.listAnimals=sorted(cp.deepcopy(listAnimals), reverse=True)#lista de tuplas (prob, obj, numObj)
        self.listOtherObj=sorted(cp.deepcopy(listOtherObj), reverse=True)#lista de tuplas (prob, obj, numObj)

    def __str__(self):
        return self.name +': ' + self.desc

    def applyDistro(self, num=1):
        """devuelve un numero aleatorio con probabilidad del Enviroment"""
        return self.probDistro(*self.paramsDistro,num)

    def getObj(self):
        return {'Plants':self.listPlants,'Animals':self.listAnimals,'Other':self.listOtherObj}

################################################################################
class Game:
    """docstring for Game.
       Hay que hacer que la formula sea un parametro
    """
    def __init__(self, name, lPlayer=[],lEnv=[]):
        self.name=name
        self.lPlayer=cp.deepcopy(lPlayer)
        self.lEnv=cp.deepcopy(lEnv)

#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
    def addPlayers(self,lp):
        for p in lp:
            self.lPlayer.append(cp.deepcopy(p))

    def addEnvs(self,le):
        for e in le:
            self.lEnv.append(cp.deepcopy(e))# deepcopy esnecesario

    def rmPlayers(self, lp):
        for p in lp:
            self.lPlayer.remove(p)

    def rmEnvs(self,e):
        for e in le:
            self.lEnv.remove(e)
#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
    def serchPlant(self,nHoras, pl, env, dice=0):
        L=[]
        plants=env.listPlants
        #formula prob
        probs=env.applyDistro(nHoras)+(bp.herb/100)*1.5

        for p in probs:
            for j in range(len(plants)):
                if p > plants[j][0]:#probabilidad de la tupla numero i
                    L.append(plants[j][1])#anyadimos el elemento a la lista resultado
                    break
        return L
#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #


amapola=Plant('amapola', desc='Una simple amapola')
rosa=Plant('rosa',desc='una rosa roja')
bl=Plant('Black Lotus',desc='THE BLACK LOTUS')
perro=Animal('perro',desc='Un perro')
pradera=Enviroment('pradera',np.random.beta,paramsDistro=[1,2.3], \
                    desc='una simple pradera', \
                    listPlants=[(0.7,rosa,1),(0.5,amapola,1), (0.9,bl,1)], listAnimals=[perro])
bp=BasicPlayer('ton',herb=18, hunt=5)
g=Game('prueba', lEnv=[pradera])


print('cambio cad\n'+ str(pradera))
g.lEnv[0].desc='hola'
print(pradera)
print(g.lEnv[0])

''' pruebas PROBABILIDADES
L=g.serchPlant(10,bp,pradera,0)
print(pradera.listPlants)
print(len(L))
print(L.count(bl))
print(L.count(rosa))
print(L.count(amapola))
print(L)
'''
