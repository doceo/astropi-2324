from exif import Image  # modulo utile all'uso delle informazioni nascoste nei file immagini
from datetime import datetime # modulo utile alla manipolazione di date e orari
import cv2 # modulo necessario per la computer vision
import math # libreria di funzioni matematiche
import os

import csv

def Crop_image(image, percent):
    width = image.shape[1]
    height = image.shape[0]

    # Calcola le dimensioni del ritaglio.
    crop_width = int(width * (percent))
    crop_height = int(height * (percent))
    # Ritaglia l'immagine.
    crop_image = image[crop_height:-crop_height, crop_width:-crop_width]  
    return crop_image
# get_time(image) preleva dai dati exif della singola foto la sua data di creazione
def get_time(image):
    with open(image, 'rb') as image_file:   #apre in lettura un oggetto di tipo "image" e lo rinomina "image_file" 
        img = Image(image_file) #salva in img tutte le informazioni contenute nel file
        
        # questo ciclo stampa a monitor tutte le informazioni a disposizione nei dati exif
        #for data in img.list_all():
        #    print(data)
        
        time_str = img.get("datetime_original") #estrapola da img il valore associato all'etichetta 
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S') #salva in time la data e l'ora formattata in un determinato modo
        return time #restituisce il valore di data e ora del file  
#questa funzione prende in input due immagini ed associa a due variabili le loro date di creazione. Dopo li sottrae
def get_time_difference(crop_image_1, crop_image_2):
    time_1 = get_time(crop_image_1)
    time_2 = get_time(crop_image_2)
    time_difference = time_2 - time_1
    
    #time difference è un oggetto che ha tutte le cifre: ora, minuti e secondi.
    print("la differenza temporale tra le due immagini e'", time_difference)
    #possiamo decidere di restiruire alla funzione chiamante solo i secondi, attraverso il metodo ".seconds"
    #dell'oggetto di tipo TIME.
    return time_difference.seconds
'''
OPEN CV2
questa funzione converte oggetti immagini in oggetti CV2
Gli oggetti OpenCV restituiti possono ora essere utilizzati da altre classi e metodi nel pacchetto OpenCV.
Per questo progetto è possibile utilizzare l'algoritmo Oriented FAST e Rotated BRIEF (ORB).
Questo algoritmo rileverà i punti chiave in un'immagine o in più immagini.
Se le immagini sono simili, dovrebbero essere rilevati gli stessi punti chiave in ciascuna immagine,
anche se alcune funzionalità sono state spostate o modificate.
ORB può anche assegnare descrittori ai punti chiave. Questi conterranno informazioni sul punto chiave,
come posizione, dimensione, rotazione e luminosità. Confrontando i descrittori tra i punti chiave,
è possibile calcolare i cambiamenti da un'immagine all'altra.
'''
def convert_to_cv(crop_image_1, crop_image_2):
    image_1_cv = cv2.imread(crop_image_1, 0)
    image_2_cv = cv2.imread(crop_image_2, 0)
    return image_1_cv, image_2_cv
'''
CALCULATE_FEATURES
è una funzione per trovare i punti chiave e i descrittori delle due immagini.
Ci vorranno tre argomenti: i primi due sono gli oggetti immagine OpenCV e l'ultimo è il numero massimo
di funzionalità che desideri cercare.
'''
def calculate_features(crop_image_1, crop_image_2, feature_number):
    orb = cv2.ORB_create(nfeatures = feature_number)
    #Associa a keapoint il punto chiave di image_cv ed a description la sua descrizione
    keypoints_1, descriptors_1 = orb.detectAndCompute(crop_image_1, None) 
    keypoints_2, descriptors_2 = orb.detectAndCompute(crop_image_2, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2
'''
Ora hai i punti chiave e i descrittori dei punti chiave, devono essere abbinati tra le due immagini.
Questo ti dirà se un punto chiave nella prima immagine è lo stesso punto chiave nella seconda immagine.
Il modo più semplice per farlo è usare la "forza bruta".
Un algoritmo di "brute force" significa che il computer proverà ogni possibile combinazione.
È come provare a sbloccare un telefono protetto da PIN iniziando con il PIN 0000, quindi passando a 0001 e
continuando finché non si sblocca o arrivi a 9999.
brute force, in questo contesto, significa prendere un descrittore dalla prima immagine e provare ad abbinarlo
a tutti i descrittori nella seconda immagine. Una corrispondenza verrà trovata oppure no.
Quindi prendi il secondo descrittore dalla prima immagine e ripeti il ​​processo,
quindi continui a ripetere questo processo finché non hai confrontato tutti i descrittori della prima immagine
con quelli della seconda immagine.
'''
# CALCULATE_MATCHES applica l'algoritmo bruce force ai descrittori delle due immagini
def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    try:
        matches = brute_force.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key=lambda x: x.distance)
    except:
        matches = []
    return matches #restituisce una lista (anche molto lunga) di match.
'''
DISPLAY_MATCHES
PRENDE come argomenti i due oggetti immagine OpenCV, i punti chiave e le corrispondenze.
'''
def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    
    # traccia delle linee tra i punti chiave in cui i descrittori corrispondono.
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
    
    # Le immagini possono ora essere ridimensionate e visualizzate, una accanto all'altra,
    # sullo schermo, con le linee tracciate tra le partite.
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
#    cv2.imshow('matches', resize)
    
    # Per completare la funzione, lo script deve attendere finché non viene premuto un tasto, quindi chiudere l'immagine.
#    cv2.waitKey(0)
 #   cv2.destroyWindow('matches')
    
'''
FIND_MATCHING_COORDINATES
accetta i due insiemi di punti chiave e l'elenco delle corrispondenze come argomenti.
'''
    
def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    # due elenchi vuoti per memorizzare le coordinate di ciascuna caratteristica corrispondente in ciascuna delle immagini.
    coordinates_1 = []
    coordinates_2 = []
    # L'elenco delle corrispondenze contiene molti oggetti di corrispondenza OpenCV.
    # Puoi scorrere l'elenco per trovare le coordinate di ciascuna corrispondenza su ciascuna immagine.
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt
        # tali coordinate possono essere aggiunte ai due elenchi di coordinate
        # e i due elenchi possono essere restituiti.
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
    return coordinates_1, coordinates_2
    
    
'''
CALCULATE_MEAN_DISTANCE
calcola la distanza media tra le coordinate corrispondenti. Sono necessari due argomenti, che costituiranno i due elenchi di coordinate.
'''
def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    
    # Per vedere cosa è successo qui, puoi aggiungere alcuni inviti alla stampa per vedere i dettagli degli elenchi.
    #print(coordinates_1[0])
    #print(coordinates_2[0])
    #print(merged_coordinates[0])
    
    #aggiungiamo un ciclo for per scorrere le merged_coordinates e calcolare le differenze tra le coordinate xey in ciascuna immagine.
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]

        # # La distanza tra i punti A e B è la lunghezza della linea c. Questa è chiamata ipotenusa del triangolo ABC.
        # Usando il pacchetto math per calcolare il suo valore (hypot)
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance

        # Restituisce la distanza media tra gli elementi dividendo all_distances per il
        # di corrispondenze di elementi, che è la lunghezza dell'elenco merged_coordinates.
        return all_distances / len(merged_coordinates)

'''
CALCULATE_SPEED_IN_KMPS
calcola la velocità della ISS. Dovrebbe prendere feature_distance, un fattore GSD e time_difference come argomenti.
È possibile utilizzare https://www.3dflow.net/ground-sampling-distance-calculator/ per calcolare il fattore di scala
tra la distanza in pixel e la distanza sulla Terra. La distanza del campione dal suolo (GSD) è espressa in centimetri
'''
def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    
    # Calcola la distanza moltiplicando la distanza della caratteristica in pixel per il GSD e poi dividi il tutto per 100.000.
    distance = feature_distance * GSD / 100000 
    # The speed can then be calculated by dividing by the time_difference between the two images, and the speed returned.
    speed = distance / time_difference
    return speed
'''
ALGORITMO PRINCIPALE
dopo aver implementato tutte le funzioni si può implementare l'algoritmo principale che le userà secondo
il flusso di lavoro scelto
'''

# scelgo le fotografie
#image_1 = ('photo_01931.JPG')
#image_2 = ('photo_01932.JPG')
for cartella, sottocartella, files in os.walk(os.getcwd()):
    print("\n"*3)
    for file in files:
        if file.endswith(".jpg"):
            index = files.index(file)
            if index <= (len(files) -2):            
                image_1 = str(cartella) + "\\" + str(files[index])
                image_2 = str(cartella) + "\\" + str(files[index+1])
                print(image_1)
                print(image_2)
                crop_image_1 = Crop_image(cv2.imread(image_1), 0.333)
                crop_image_2 = Crop_image(cv2.imread(image_2), 0.333)
                #prima viene richiamata la funzione get_image, il suo output viene stampato a monitor
                #Crea dei file con le immagini jpg
                #cv2.imwrite("cropped_image_1.jpg", crop_image_1)
                #cv2.imwrite("cropped_image_2.jpg", crop_image_2)
                print(get_time(image_1))
                print(get_time(image_2))
                time_difference = get_time_difference(image_1, image_2) # Get time difference between images
                print("differenza tra le foto in secondi: ", time_difference)
                #image_1_cv, image_2_cv = convert_to_cv(crop_image_1, crop_image_2) # Create OpenCV image objects
                #keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) # Get keypoints and descriptors
                keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(crop_image_1, crop_image_2, 1000)
                matches = calculate_matches(descriptors_1, descriptors_2) # Match descriptors
                #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
                if len(matches)!= 0: 
                    display_matches(crop_image_1, keypoints_1, crop_image_2, keypoints_2, matches) # Display matches
                    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
                    print('le coordinate sono',coordinates_1[0], coordinates_2[0])
                    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2) 
                    print("La distanza media rilevata è: ", average_feature_distance)
                    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
                    print("La velocità media calcolata è: ",speed, "km/sec")
            else:
                pass
        else:
            pass






