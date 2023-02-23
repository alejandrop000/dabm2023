import csv
from datetime import datetime

class Sensor:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def registrar_lecturas(self, paciente, valor):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{paciente.nombre}.csv", mode="a", newline="") as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow([valor, fecha_hora_actual])

class Paciente:
    def __init__(self, nombre, patologia, sensores):
        self.nombre = nombre
        self.patologia = patologia
        self.sensores = sensores
    
    def registrar_lecturas(self):
        for sensor in self.sensores:
            valor = input(f"Ingrese el valor del sensor {sensor.nombre} para el paciente {self.nombre}: ")
            sensor.registrar_lecturas(self, valor)
    
    def reporte_lecturas(self):
        print(f"Reporte de lecturas del paciente {self.nombre}:")
        with open(f"{self.nombre}.csv", mode="r") as archivo:
            lector_csv = csv.reader(archivo)
            for fila in lector_csv:
                print(f"Fecha/hora: {fila[1]} - Sensor: {self.sensores[0].nombre} - Valor: {fila[0]}")
                
# Ejemplo de uso
sensor1 = Sensor("Sensor 1")
sensor2 = Sensor("Sensor 2")
paciente1 = Paciente("Juan Perez", "Hipertensión", [sensor1, sensor2])
paciente1.registrar_lecturas()
paciente1.reporte_lecturas()