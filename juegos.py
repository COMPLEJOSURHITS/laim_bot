import pickle,random,math

masobj=pickle.load(open("bot/maso.pk","rb"))
cartas=pickle.load(open("bot/cartas.pk","rb"))
valores={
    "A":[11,1],
    "K":[10],
    "Q":[10],
    "J":[10],
    "10":[10],
    "1":[10],
    "9":[9],
    "8":[8],
    "7":[7],
    "6":[6],
    "5":[5],
    "4":[4],
    "3":[3],
    "2":[2],
}

class Repartidor:
    def __init__(self,maso):
        self.__maso=[el for el in maso]
        
    def repartir(self,ncartas=2):
        if len(self.__maso)<ncartas:
            return False
        rp=[]
        for el in range(ncartas):
            c=random.choice(self.__maso)
            self.__maso.remove(c)
            rp.append(c)
        return rp

    def cuantashay(self):
        return len(self.__maso)

class BlackjackGame:
    def __init__(self,nmasos=6):
        self.repartidor = Repartidor(masobj*nmasos)

    def makeround(nplayers=1):
        rpp=rp.repartir(2)
        jugador={"cartas":[a.split(" ")[1] for a in rpp],"fichas":monedas}
        jugador["valores"]=[x+y for x in [int(a) for a in rpp[0].split(" ")[0].split(",")]
            for y in [int(a) for a in rpp[1].split(" ")[0].split(",")]]

def bjrepartir(cartas):
    jugador={"cartas":[a.split(" ")[1] for a in cartas]}
    jugador["valores"]=[x+y for x in [int(a) for a in cartas[0].split(" ")[0].split(",")]
        for y in [int(a) for a in cartas[1].split(" ")[0].split(",")]]
    return jugador

def bjpedir(jugador,repartidor):
    jugador = jugador
    carta=repartidor.repartir(1)[0]
    jugador["cartas"].append(carta)
    jugador["valores"]=[x+y for x in jugador["valores"] for y in valores[carta[0]]]
    return jugador

def bjvalor(jugador):
    jvalor = list(filter(lambda x:x<=21,jugador["valores"])) 
    if jvalor:
        return max(jvalor)
    else:
        return min(jugador["valores"])

def regresarFichas(fichas):
    fic = []
    fichas = fichas
    while fichas:
        div=10**math.floor(math.log10(fichas))
        fic.append(div)
        fichas-=div
    return fic


