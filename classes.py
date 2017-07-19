import numpy as np
import copy as cp

################################################################################
class BasicPlayer:
    """docstring for BasicPlayer.
    """
    def __init__(self, name, owner=None, skills={}):
        self.name = name
        self.owner= owner
        self.skills=skills

    def __str__( self ):
        return "Name : " +self.name +" skills: "+ str(self.skills)

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
    def __init__(self, name,probDistro, paramsDistro=[],desc=None,dicObj={}):
        self.name=name
        self.probDistro=probDistro #https://en.wikipedia.org/wiki/List_of_probability_distributions
        self.paramsDistro=paramsDistro
        self.desc=desc
        self.dicObj=dicObj
        #self.listPlants=sorted(cp.deepcopy(listPlants), reverse=True)#lista de tuplas (prob, obj, numObj)
        #self.listAnimals=sorted(cp.deepcopy(listAnimals), reverse=True)#lista de tuplas (prob, obj, numObj)
        #self.listOtherObj=sorted(cp.deepcopy(listOtherObj), reverse=True)#lista de tuplas (prob, obj, numObj)

    def __str__(self):
        return self.name +': ' + self.desc

    def applyDistro(self, num=1):
        """devuelve un numero aleatorio con probabilidad del Enviroment"""
        return self.probDistro(*self.paramsDistro,num)


################################################################################
class Game:
    """docstring for Game.
       Hay que hacer que la formula sea un parametro
    """
    def __init__(self, name, lskills=[],lPlayer=[],lEnv=[]):
        self.name=name
        self.lPlayer=cp.deepcopy(lPlayer)
        self.lEnv=cp.deepcopy(lEnv)
        self.lskills=cp.deepcopy(lskills)

#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
    def addPlayers(self,lp):
        for p in lp:
            self.lPlayer.append(cp.deepcopy(p))

    def rmPlayers(self, lp):
        for p in lp:
            self.lPlayer.remove(p)

    def addEnvs(self,le):
        for e in le:
            self.lEnv.append(cp.deepcopy(e))# deepcopy esnecesario

    def rmEnvs(self,e):
        for e in le:
            self.lEnv.remove(e)

    def addSkills(self, ls,statDefault=0, objDefault=[]):
        for s in ls:
            if s not in self.lskills:
                for p in self.lPlayer:
                    p.skills[s]=statDefault
                for e in self.lEnv:
                    e.dicObj[s]=cp.deepcopy(objDefault)

        self.lskills+= cp.deepcopy(ls)
#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #
    def search(self,env,pl,skill,nHoras=1,dice=0):
        ret=[]
        stat=pl.skills[skill]
        L=env.dicObj[skill]
        #formula prob
        probs=env.applyDistro(nHoras)+(stat/100)*1 + (dice/100)*1

        for p in probs:
            for j in range(len(L)):
                if p > L[j][0]:#probabilidad de la tupla numero i
                    ret.append(L[j][1])#anyadimos el elemento a la lista resultado
                    break
        return ret
#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #


#
#
#
#
#
#
#
#
#


# creamos Plantas
amapola=Plant('amapola', desc='Una simple amapola')
rosa=Plant('rosa',desc='una rosa roja')
bl=Plant('Black Lotus',desc='THE BLACK LOTUS')

#creamos lista plantas con prob
listaPlantas=[(0.7,rosa,1),(0.5,amapola,1), (0.9,bl,1)]

#creamos Animales
perro=Animal('perro',desc='Un perro')

#creamos objetos tipo Other
cuchillo=OtherObj('cuchillo', desc='cuchillito cuchillito')
manzana=OtherObj('manzana', desc='una manzana caida de un arbol')

#creamos lista de skills
ls=['herb', 'hunt']

#creamos dic generico
d=dict(zip(ls,[None for _ in range(len(ls))]))

#creamos Enviroment
pradera=Enviroment('pradera',np.random.beta,paramsDistro=[1,2.3], \
                    desc='una simple pradera', \
                    dicObj=d)


#creamos player
bp=BasicPlayer('ton','ton',skills=d)

g=Game('prueba', lskills=ls, lEnv=[pradera], lPlayer=[bp])

print('Game skills:'+ str(g.lskills))
g.lPlayer[0].skills['herb']=15
g.lPlayer[0].skills['hunt']=15
print(g.lPlayer[0].skills.keys(),g.lPlayer[0].skills['herb'],g.lPlayer[0].skills['hunt'])
g.lEnv[0].dicObj['herb']= listaPlantas
print(g.lEnv[0].dicObj.keys(),g.lEnv[0].dicObj['herb'],g.lEnv[0].dicObj['hunt'])

'''realizamos busquedas
L=g.search(g.lEnv[0],g.lPlayer[0], 'herb')
print(L)
'''

#anyadimos una nueva skill

g.addSkills(['other'],10,[(0.5,cuchillo,2),(0.2,manzana,1)])
print('Game skills:'+ str(g.lskills))
print(g.lPlayer[0].skills.keys(),g.lPlayer[0].skills['herb'],g.lPlayer[0].skills['hunt'],g.lPlayer[0].skills['other'])
print(g.lEnv[0].dicObj.keys(),g.lEnv[0].dicObj['herb'],g.lEnv[0].dicObj['hunt'],g.lEnv[0].dicObj['other'])
