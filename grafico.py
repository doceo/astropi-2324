import matplotlib.pyplot as plt
import csv
import os

def grafico(file):
    # Apri il file CSV
    with open(file, 'r') as csvfile:

        # Crea un lettore CSV
        reader = csv.reader(csvfile, delimiter=',')

        # Salta la prima riga, che contiene i nomi delle colonne
        next(reader, None)
        
        # Crea due liste per contenere i dati
        x_values = []
        y_values = []

        for row in reader:
            if (float((row[8]))<1):
                y_values.append(row[8])

        # Itera sulle righe del file CSV

            # Aggiungi i valori alla lista x_values
            #x_values.append()

            # Aggiungi i valori alla lista y_values
        
        x_values = list(range(len(y_values)))
        # Crea il grafico a dispersione
        plt.plot(y_values)

        # Imposta le etichette degli assi
        plt.xlabel('x')
        plt.ylabel('y')

        # Salva il grafico come immagine jpg
        name = file + ".jpg"
        plt.show()
        #print(y_values)

grafico("data-2.csv")
