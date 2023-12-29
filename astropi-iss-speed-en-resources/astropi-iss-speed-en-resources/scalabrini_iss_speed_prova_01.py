from exif import Image
from datetime import datetime
import cv2
import math #importo nel file le proprietà delle diverse estensioni

def get_time(image):#funzione generica applicabile a tutte le immagini
    with open(image, 'rb') as image_file: 
        img = Image(image_file) #apriamo le immagini e convertiamole
        time_str = img.get("datetime_original")#salviamo i dati riferiti al tempo
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')#convertiamo i dati per potervi eseguire dei calcoli 
    return time

def get_time_difference(image_1, image_2): #creiamo la funzione che calcola la differenza di tempo, che ha come argomento le immagini interessate
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)#calcoliamo il tempo delle immagini, richiamando la funzione get_time
    time_difference = time_2 - time_1
    return time_difference #calcoliamo la differenza del tempo e restituiamola come risultato della funzione

def convert_to_cv(image_1, image_2): #creo una funzione che converta le immagini in elementi cv, per potervi eseguire le operazioni
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)#converto le immagini in cv con il metoso imread che vuole come argomento
                                       #il nome del file e il flag = il modo in cui deve essere letto il file, 0 = scala di grigi
    return image_1_cv, image_2_cv

def calculate_features(image_1, image_2, feature_number):#creiamo la funzione che calcola i punti chiave
                                                         #e i descrittori delle immagini, utilizzando la orb class reference
    orb_object = cv2.ORB_create(nfeatures = feature_number)#rendiamo il numero di punti chiave un oggetto di tipo orb
    keypoints_1, descriptors_1 = orb_object.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb_object.detectAndCompute(image_2_cv, None)#calcoliamo i valori dei punti chiave e dei descrittori e assegnamoli a delle variabili,
                                                                              #tramite un metodo che chiede come argomento la foto a cui c riferiamo e la maschera = ciò che vogliamo non considerare, in questo caso nulla
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

time_difference = get_time_difference('photo_00154.jpg','photo_00155.jpg') #associo il risultato della funzione ad una variabile esterna ad essa,
print('giorni:',time_difference.days)#così da poter calcolare le differenze di giorni, ore, minuti, secondi e microsecondi 
print('secondi:',time_difference.seconds)
print('microsecondi:', time_difference.microseconds)#ore e minuti non sono presenti tra gli attributi dei dati del tempo
image_1_cv, image_2_cv = convert_to_cv('photo_00154.jpg','photo_00155.jpg')
#cv2.imshow('immagine 1',image_1_cv)#mostra l'immagine
#cv2.waitKey(0)#mostra l'immagine