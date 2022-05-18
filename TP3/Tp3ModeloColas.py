import numpy as np
import matplotlib.pyplot as plt

Q_LIMIT = 50  # Limite de longitud de la cola
BUSY = 1  # Servidor ocupado
IDLE = 0  # Servidor libre
INFINITE = 10**50 # Simular numero arbitrariamente grande para este caso
MAX_CUSTOMERS = 1000 # Maximo de clientes atendidos

class ModeloColas:
    def __init__(self, n, arrivalRate, serviceRate, queueLimit, arrivalMean):
        self.maxCustomers= MAX_CUSTOMERS
        self.arrivalRate = arrivalRate
        self.serviceRate = serviceRate
        self.runs = n
        self.queueLimit = queueLimit
        self.arrivalMean = arrivalMean
        self.parameterLambda = self.arrivalRate
        self.parameterMu = self.serviceRate
        self.totalCustomersInSystem = []
        self.totalCustomersInQueue = []
        self.totalTimeInSystem = []
        self.totalTimeInQueue = []
        self.totalAreaServerStatus = []
        self.totalCustomersPerAmountInQueue = []
        self.totalDenegationProbability = []
        self.totalSimulationTime = []

        for _ in range(self.runs):
            # Variables de estado (rutina de inicializacion)
            self.initializationRoutine()
            self.main()

        self.showFinalData()

    def initializationRoutine(self):
        self.clock = 0
        self.status = IDLE

        self.lastEventTime = 0
        self.nextEventType = 0 # 0: arrival, 1: departure
        self.customersInQueue = 0
        self.customersDelayed = 0
        self.delays = 0
        self.areaCustomersInQueue = 0
        self.areaServerStatus = 0
        self.amountArrivals = 0
        self.amountRejected = 0
        self.queueTimesPerCustomers = [0] * (self.queueLimit + 1)

        self.arrivalsTime = [0] * (Q_LIMIT + 1)
        self.nextEventTime = [0,0]
        self.nextEventTime[0] = self.clock + np.random.exponential(self.arrivalRate)
        self.nextEventTime[1] = INFINITE #Numero arbitrariamente grande

    def timingRoutine(self):
        self.clock = min(self.nextEventTime)
        self.nextEventType = np.argmin(self.nextEventTime)

    def eventRoutine(self):
        # ARRIVAL
        if self.nextEventType == 0:
            self.amountArrivals += 1
            # Valida si el servidor esta ocupado
            if self.status == BUSY:
                # El servidor esta ocupado, se incrementa el nro de clientes en cola
                self.customersInQueue += 1
                if self.customersInQueue > Q_LIMIT:
                    self.customersInQueue -= 1
                    # El limite de la cola es mayor que la cantidad de clientes, se rechaza al ultimo
                    self.amountRejected += 1
                else:
                    # Todavía hay lugar en la cola, se guarda el tiempo de arrivo del cliente que llega en el final de arrivalsTime
                    self.arrivalsTime[self.customersInQueue-1] = self.clock
            else:
                # El servidor pasa a estar ocupado
                self.status = BUSY
                self.customersDelayed += 1
                # Asigna un tiempo de partida para fin de servicio
                self.departure()
            self.arrival()
        # DEPARTURE
        else:
            if self.customersInQueue == 0:
                # La cola esta vacía, se pone el servidor como ocioso y se deja de considerar el evento de partida
                self.status = IDLE
                self.nextEventTime[1] = INFINITE
            else:
                # La cola no esta vacía, se decrementa el numero de clientes en cola
                self.customersInQueue -= 1
                # Se calcula y acumula el delay del cliente que empezó el servicio
                self.delays += self.clock - self.arrivalsTime[0]
                # Incrementa el numero de clientes demorado y se programa la partida
                self.customersDelayed += 1
                self.departure()
                # Mueve a cada cliente en cola una posición para arriba
                del self.arrivalsTime[0]
                self.arrivalsTime.append(0)

    def arrival(self):
        self.nextEventTime[0] = self.clock + np.random.exponential(1/self.arrivalRate)

    def departure(self):
        self.nextEventTime[1] = self.clock + np.random.exponential(1/self.serviceRate)

    def timeAndAverageStadistics(self):
        # Calcula el tiempo desde el último evento y actualiza el marcador del ultimo evento
        self.timeSincelastEvent = self.clock - self.lastEventTime
        self.lastEventTime = self.clock

        # Actualiza tiempo en cola segun cantidad de clientes
        # FALTA HACER ESTO
        #self.queueTimesPerCustomers[self.customersInQueue] += self.customersInQueue * self.timeSincelastEvent
        # Actualiza el area debajo de la función cantidad de clientes en cola
        self.areaCustomersInQueue += self.customersInQueue * self.timeSincelastEvent
        # Actualiza el area debajo de la función Servidor ocupado
        self.areaServerStatus += self.status * self.timeSincelastEvent

    def saveData(self):
        self.totalCustomersInQueue.append(self.areaCustomersInQueue / self.clock)
        self.totalCustomersInSystem.append(self.areaCustomersInQueue / self.clock + self.parameterLambda / self.parameterMu )
        self.totalTimeInQueue.append(self.delays / self.customersDelayed)
        self.totalTimeInSystem.append(self.delays / self.customersDelayed + 1 / self.parameterMu)
        self.totalAreaServerStatus.append(self.areaServerStatus / self.clock)
        #self.totalCustomersPerAmountInQueue.append(self.queueTimesPerCustomers)
        self.totalDenegationProbability.append(self.amountRejected / self.amountArrivals)
        self.totalSimulationTime.append(self.clock)
        
    def showFinalData(self):
        # Calcula y muestra los estimados de las medidas de performance
        print("--------------------------------------------------------------------")
        print(f"Limite de cola: {self.queueLimit}, Tasa de arribo: {self.arrivalMean}","\n")
        print("Promedio de tiempo en cola en minutos:        ", np.mean(self.totalTimeInQueue))
        print("Promedio de tiempo en sistema en minutos:     ", np.mean(self.totalTimeInSystem))
        print("Cantidad promedio de clientes en cola:        ", np.mean(self.totalCustomersInQueue))
        print("Cantidad promedio de clientes en el sistema:  ", np.mean(self.totalCustomersInSystem))
        #print("Probabilidad de n clientes en cola:          ", self.totalCustomersPerAmountInQueue)
        print("Utilizacion del Servidor:                     ", np.mean(self.totalAreaServerStatus))
        print("Probabilidad de ser denegado el servicio:     ", np.mean(self.totalDenegationProbability))
        print(f"La simulacion termino en promedio en {np.mean(self.totalSimulationTime)} minutos")
        
        self.plot(self.totalTimeInQueue, "Tiempo en cola", "Tiempo (m)",
        self.totalTimeInSystem, "Tiempo en sistemas","Tiempo (m)",
        self.totalCustomersInQueue, "Clientes en cola", "Clientes (cantidad)",
        self.totalCustomersInSystem, "Clientes en el sistema", "Clientes (cantidad)",
        self.totalAreaServerStatus, "Utilizacion del Servidor", "Utilizacion (%)",
        self.totalDenegationProbability, "Denegacion del Servicio", "Probabilidad (%)",
        f"Limite de cola: {self.queueLimit}, Tasa de arribo: {self.arrivalMean}, Tasa de servicio: {self.serviceRate}"
        )

    def plot(self, a1, t1, l1, a2, t2, l2, a3, t3, l3, a4, t4, l4, a5, t5, l5, a6, t6, l6, titulo):
        fig, axs = plt.subplots(3, 2, constrained_layout=True)

        axs[0, 0].set_title(t1)
        axs[0, 0].set_xlabel("Cantidad de Corridas")
        axs[0, 0].set_ylabel(l1)
        axs[0, 0].grid(True)
        axs[0, 0].plot(a1)

        axs[1, 0].set_title(t2)
        axs[1, 0].set_xlabel("Cantidad de Corridas")
        axs[1, 0].set_ylabel(l2)
        axs[1, 0].grid(True)
        axs[1, 0].plot(a2)
        
        axs[2, 0].set_title(t3)
        axs[2, 0].set_xlabel("Cantidad de Corridas")
        axs[2, 0].set_ylabel(l3)
        axs[2, 0].grid(True)
        axs[2, 0].plot(a3)

        axs[0, 1].set_title(t4)
        axs[0, 1].set_xlabel("Cantidad de Corridas")
        axs[0, 1].set_ylabel(l4)
        axs[0, 1].grid(True)
        axs[0, 1].plot(a4)

        axs[1, 1].set_title(t5)
        axs[1, 1].set_xlabel("Cantidad de Corridas")
        axs[1, 1].set_ylabel(l5)
        axs[1, 1].grid(True)
        axs[1, 1].plot(a5)

        axs[2, 1].set_title(t6)
        axs[2, 1].set_xlabel("Cantidad de Corridas")
        axs[2, 1].set_ylabel(l6)
        axs[2, 1].grid(True)
        axs[2, 1].plot(a6)
        fig.suptitle(titulo)
        #plt.savefig(f'Graficos/tableroMM1-cola-{self.queueLimit}-arribo-{self.arrivalRate}.png')
        #plt.show()

    def main(self):
        while self.customersDelayed < self.maxCustomers:
            # Determinar el siguiente evento.
            self.timingRoutine()
            # Actualizar estadisticos
            self.timeAndAverageStadistics()
            # Ejecutar el evento que corresponda
            self.eventRoutine()
        self.saveData()


if __name__ == '__main__':
    tasaServicio = 2
    tasasDeArribo = [0.25, 0.50, 0.75, 1, 1.25]
    tasasDeArribo = [t*tasaServicio for t in tasasDeArribo]
    limitesCola = [0, 2, 5, 10, 50]
    corridas = 20

    for limiteCola in limitesCola:
        listaIndividual = []
        Q_LIMIT = limiteCola
        for mediaArrival in tasasDeArribo:
            ModeloColas(corridas, mediaArrival, 2, limiteCola, mediaArrival)
              
            




   
    