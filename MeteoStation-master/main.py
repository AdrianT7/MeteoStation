import serial
import time
from os import system
import tkinter as tk

# Wartości skrajne(temperatura, wilgotność)

minTmp = "100"
maxTmp = "-100"

minHum = "100"
maxHum = "-100"


# Zapis temperatury do pliku
def saveTemp():
    with open("temp.txt", 'w') as f: # zamknięcie pliku odbędzie się autmatycznie
        f.write(minTmp)
        f.write('\n')
        f.write(maxTmp)


# Zapis temperatury do pliku
def saveHum():
    with open("hum.txt", 'w') as f: # zamknięcie pliku odbędzie się autmatycznie
        f.write(minHum)
        f.write('\n')
        f.write(maxHum)


# Odczyt temperatury z pliku
def readTemp():
    global minTmp, maxTmp
    with open("temp.txt", "r") as f:
        minTmp = f.readline()
        maxTmp = f.readline()

# Odczyt temperatury z pliku
def readHum():
    global minHum, maxHum
    with open("hum.txt", "r") as f:
        minHum = f.readline()
        maxHum = f.readline()


# Połączenie z urządzeniem
def connectToDevice():
    while True:
        port = input("Type com port number: ")
        port = str("com" + str(port))
        print("Connecting to: " + port)

        try:
            s = serial.Serial(port, baudrate=9600, timeout=0)
            return s

        except serial.SerialException:
            print("Not connected, try again..")            
            time.sleep(3)
            system('cls')


# Pobieranie danych z arduino
def SerialPrint():
    dane: str = ser.readline().decode('ascii')  # decode('ascii') pozwala wyświetlić dane bez prefix'a
    # dane = '+T25'
    if len(dane) > 0 and dane[0] == '+':

        dane = formatData(dane)

        print(dane)

        if dane[1] == 'T':
            dane = dane.replace('+T', '')
            compareTemp(dane)
            dane = '%s Celsius' % (dane)
            temperature.config(text = dane)

        if dane[1] == 'W':
            dane = dane.replace('+W', '')
            compareHum(dane)
            dane = '%s procent' % (dane)
            humidity.config(text = dane)

    dataFrame.after(5000, SerialPrint)

def formatData(data):
    for d in data:
        d.replace("\\n", "")
        d.replace("\\r", "")

    return data


# Wypisanie wartości
def printValues():
    dane: str = "Max temp: " + maxTmp + " Min temp: " + minTmp
    dbTemperature.config(text = dane)

    dane: str = "Max hum: " + maxHum + " Min hum: " + minHum
    dbHum.config(text = dane)

    dataFrame.after(500, printValues)


# Porównanie wartości temperatury
def compareTemp(value):
    global maxTmp, minTmp
    if (float(value) > float(maxTmp)): 
        maxTmp = value
        saveTemp()

    if (float(value) < float(minTmp)): 
        minTmp = value
        saveTemp()


# Porównanie wartości wilgotności
def compareHum(value):
    global minHum, maxHum
    if (int(value) > int(maxHum)): 
        maxHum = value
        saveHum()

    if (int(value) < int(minHum)): 
        minHum = value
        saveHum()

# Nawiązanie połączenia z arduino
ser = connectToDevice()

readTemp()
readHum()

# Tworzenie interfejsu graficznego
root = tk.Tk()
Width = 750
Height = 650
root.maxsize(900, 850)
root.minsize(650, 550)
canvas = tk.Canvas(root, width=Width, height=Height)
canvas.pack()

backgroundImg = tk.PhotoImage(file="img/arduinoBg2.png")
backgroundLabel = tk.Label(root, image=backgroundImg)
backgroundLabel.place(relwidth=1, relheight=1)

# Tytuł aplikacji
title = tk.Label(root, font='lato 32 bold', bg='#005c5f', fg='white', text='Meteo Station')
title.place(relx=0.5, rely=0.02, relwidth=0.75, relheight=0.1, anchor='n')


# Frame that contains data from arduino
dataFrame = tk.Frame(root, bg='#005c5f', bd=5)
dataFrame.place(relx=0.5, rely=0.125, relwidth=0.75, relheight=0.3, anchor='n')


# Frame for temperature
tempFrame = tk.Frame(dataFrame, bg='#00979d', bd=5)
tempFrame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.37, anchor='n')

# temperature info
tmp = tk.Label(tempFrame, bg='#00979d', fg='white', font='lato 16 bold', justify='center', text='Temp: ')
tmp.place(relx=0.001, relheight=1, relwidth=0.39)

# This label contains temperature data
temperature = tk.Label(tempFrame, font='lato 16', text='waiting for informations...')
temperature.place(relx=0.35, relheight=1, relwidth=0.65)


#Frame for humidity
humFrame = tk.Frame(dataFrame, bg='#00979d', bd=5)
humFrame.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.37)

# humidity info
hdt = tk.Label(humFrame, bg='#00979d', fg='white', font='lato 16 bold', justify='center', text='Humidity: ')
hdt.place(relx=0.001, relheight=1, relwidth=0.39)

# This label contains humidity data
humidity = tk.Label(humFrame, font='lato 16', text='waiting for informations...')
humidity.place(relx=0.35, relheight=1, relwidth=0.65)


# Dane maksymalne/ minimalne
dbFrame = tk.Frame(root, bg='#005c5f', bd=5)
dbFrame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.3, anchor='n')


# Frame for temperature
dbTempFrame = tk.Frame(dbFrame, bg='#00979d', bd=5)
dbTempFrame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.37, anchor='n')

# This label contains temperature data
dbTemperature = tk.Label(dbTempFrame, font='lato 16', text='waiting for informations...')
dbTemperature.place(relheight=1, relwidth=1)


# Frame for humidity
dbHumFrame = tk.Frame(dbFrame, bg='#00979d', bd=5)
dbHumFrame.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.37, anchor='n')

# This label contains humidity data
dbHum = tk.Label(dbHumFrame, font='lato 16', text='waiting for informations...')
dbHum.place(relheight=1, relwidth=1)

SerialPrint()
printValues()

root.mainloop()