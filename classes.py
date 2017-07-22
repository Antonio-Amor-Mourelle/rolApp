import numpy as np
import copy as cp

################################################################################
class BasicPlayer:
    """docstring for BasicPlayer.
    """
    def __init__(self, name, owner=None, dSkills={}):
        self.name = name
        self.owner= owner
        self.dSkills=dSkills

    def __str__( self ):
        return "Name : " +self.name +" skills: "+ str(self.dSkills)

################################################################################
class Foundable:
    """docstring for Foundable.
    """
    def __init__(self, name,desc=None,fClass='Other'):
        self.name=name
        self.desc=desc
        self.fClass=fClass
        #Clase de los objetos, permite tener clases dinamicas de objetos
        #Vuelve innecesarias a las clases Plant, Animal y OtherObj
    def __str__(self):
        return self.desc+ self.fClass

################################################################################
class Plant(Foundable):
    """docstring for Plant.
    """
    def __init__(self, name, desc=None, fClass='Plant'):
        super(Plant, self).__init__(name, desc,fClass)

    def __str__(self):
        return self.desc

################################################################################
class Animal(Foundable):
    """docstring for Animal.
    """
    def __init__(self, name, desc=None,fClass='Animal'):
        super(Animal, self).__init__(name, desc,fClass)

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
        self.dicObj=cp.deepcopy(dicObj)
        #self.listPlants=sorted(cp.deepcopy(listPlants), reverse=True)#lista de tuplas (prob, obj, numObj)
        #self.listAnimals=sorted(cp.deepcopy(listAnimals), reverse=True)#lista de tuplas (prob, obj, numObj)
        #self.listOtherObj=sorted(cp.deepcopy(listOtherObj), reverse=True)#lista de tuplas (prob, obj, numObj)

    def __str__(self):
        return self.name +': ' + self.desc

    def applyDistro(self, num=1):
        """devuelve un numero aleatorio con probabilidad del Enviroment"""
        return self.probDistro(*self.paramsDistro,num)

    def addObj(self,obj, prob, num=1):
        self.dicObj[obj.fClass]=cp.deepcopy((prob,obj, num))
        sorted(self.dicObj[obj.fClass], reverse=True)

    def createObj(self, name, desc,fClass, prob,num=1):
        self.dicObj[fClass]=(prob,Foundable(name,owner,fClass),num)
        sorted(self.dicObj[obj.fClass], reverse=True)

    def rmObj(self,Obj):
        L=self.dicObj[Obj.fClass]
        for i in range(len(L)):
            if L[i][1]==obj:
                L.remove(L[i])
                break



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
    def search(self,env,pl,skill,nHoras=1,dice=0):
        '''busca en un enviroment (env) usando la skill (skill) de un BasicPlayer (pl)
           durante nHoras y puede tener en cuenta un dado.
           Una vez encontrado el objeto actualiza la lista
        '''
        ret=[]
        stat=pl.skills[skill]
        L=env.dicObj[skill]
        #formula prob
        #nHoras permite usar la distro con el param size
        probs=env.applyDistro(nHoras)+(stat/100)*1 + (dice/100)*1

        for p in probs:
            for j in range(len(L)):
                if p > L[j][0]:#probabilidad de la tupla numero j
                    ret.append(L[j][1])#anyadimos el elemento a la lista resultado
                    if L[j][2]-1 == 0:#restamos al numero de elementos que quedaban
                        L.pop(j) #si no quedan mas borramos el objeto
                    break
        return ret

#  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  #

    def createPlayer(self,name,owner,dSkills):
        '''crea un jugador en la partida.'''
        self.lPlayer.append(BasicPlayer(name, owner,dSkills))

    def createEnviroment(self,name,probDistro, paramsDistro,desc,dObj):
        '''crea un enviroment en la partida'''
        self.lEnv.append(Enviroment(name,probDistro, paramsDistro,desc,dObj))

    def addPlayers(self,lp):
        '''anyade una copia del jugador pasado por argumento'''
        for p in lp:
            self.lPlayer.append(cp.deepcopy(p))

    def rmPlayers(self, lp):
        '''elimina el jugador de la partida pasado por argumento'''
        for p in lp:
            self.lPlayer.remove(p)

    def addEnvs(self,le):
        '''anyade una copia del enviroment pasado por argumento'''
        for e in le:
            self.lEnv.append(cp.deepcopy(e))# deepcopy esnecesario

    def rmEnvs(self,e):
        '''elimina el enviroment de la partida pasado por argumento'''
        for e in le:
            self.lEnv.remove(e)

    def addSkills(self, ls,statDefault=0, objDefault=[]):
        '''anyade una skill al game, y tambien a los envs y player'''
        for s in ls:
            if s not in self.lskills:
                for p in self.lPlayer:
                    p.skills[s]=statDefault
                for e in self.lEnv:
                    e.dicObj[s]=cp.deepcopy(objDefault)
        self.lskills+= cp.deepcopy(ls)

    def rmSkills(self, ls):
        '''elimina una skill del game, y tambien de los envs y player'''
        for s in ls:
            for p in self.lPlayer:
                del p.skills[s]
            for e in self.lEnv:
                del e.dicObj[s]
            self.lskills.remove(s)

################################################################################
class App:

    def __init__(self):
        self.lGames=[]
        self.dObj={}
        self.lEnv=[]

    def readObj(self, cadObj):
        '''funcion de lectura de objetos de un fichero.
        Se llama cuando en la linea se ha leido un o;
        El objeto sigue el formato:
           'clave:[name,desc]'
        '''
        k , v =cadObj.split(':')# separamos la clave de los valores
        print(k)
        name,desc=v.split(';')
        self.dObj[k]=Foundable(name,desc,k)

    def readEnv(self, cadEnv):
        name,probDistro, paramsDistro,desc,dicObj= cadEnv.split(';')
        probDistro=eval(probDistro)#conseguimos la funcion numpy

        #transformamos la lista de parametros en numeros
        paramsDistro=paramsDistro[1:-1].split(',')
        lParams=[]
        for x in paramsDistro:
            print(x)
            lParams.append(float(x))
        #fin
        TODO hay problemas con el DICT
        self.lEnv.append(Enviroment(name,probDistro, lParams,desc,dicObj))



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
bp=BasicPlayer('ton','ton',dSkills=d)

#creamos un Game
g=Game('prueba', lskills=ls, lEnv=[pradera], lPlayer=[bp])

#creamos la App
app=App()
app.lGames.append(g)
app.readObj("Animal:prueba;esto es una prueba")
app.readEnv("'pradera';np.random.beta;[1,2.3]; 'una simple pradera';d")
print(app.lGames)
print(app.dObj)
print(app.lEnv[0].applyDistro())

'''
print('Game skills:'+ str(g.lskills))
g.lPlayer[0].skills['herb']=15
g.lPlayer[0].skills['hunt']=15
print(g.lPlayer[0].skills.keys(),g.lPlayer[0].skills['herb'],g.lPlayer[0].skills['hunt'])
g.lEnv[0].dicObj['herb']= listaPlantas
print(g.lEnv[0].dicObj.keys(),g.lEnv[0].dicObj['herb'],g.lEnv[0].dicObj['hunt'])
'''

'''realizamos busquedas
print('final prueba')
print(g.lEnv[0].dicObj['herb'])
L=g.search(g.lEnv[0],g.lPlayer[0], 'herb')
print('objeto:'+ str(L))
print(g.lEnv[0].dicObj['herb'])
'''

#anyadimos una nueva skill
'''
g.addSkills(['other'],10,[(0.5,cuchillo,2),(0.2,manzana,1)])
print('Game skills:'+ str(g.lskills))
print(g.lPlayer[0].skills.keys(),g.lPlayer[0].skills['herb'],g.lPlayer[0].skills['hunt'],g.lPlayer[0].skills['other'])
print(g.lEnv[0].dicObj.keys(),g.lEnv[0].dicObj['herb'],g.lEnv[0].dicObj['hunt'],g.lEnv[0].dicObj['other'])
'''
