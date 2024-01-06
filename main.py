from utils import *

import itertools

import glob
from os import path
def main_functions():
    row = []
    base_folder = path.dirname(__file__)

    # Initialise the CSV file
    data_file = path.join(base_folder, "data-test.csv")
    create_csv(data_file) # da aggiornare

    # Ottieni la lista di tutti i file jpg nella cartella img
    jpg_files = glob.glob('img-2/*.jpg')
    print(len(jpg_files))
    
    crop = input ("Inserisci la porzione di immagine da selezionare (valore compreso tra 0 ed 1): ")
    keyPoints = input("inserisci il numero di punti da verificare: ")
    lista = []
    for i in jpg_files:
        lista.append(i)
        
    count = 0
    saveImg = 0
        
    for jpg_f in itertools.combinations(lista, 2):
        print("iterazione ", count)
        print("salvataggi ", saveImg)


        row.append(jpg_f[0][5:])
        row.append(jpg_f[1][5:])
        image_1 = jpg_f[0]
        image_2 = jpg_f[1]
                
        crop_image_1 = Crop_image(cv2.imread(image_1), float(crop))
        crop_image_2 = Crop_image(cv2.imread(image_2), float(crop))
        #prima viene richiamata la funzione get_image, il suo output viene stampato a monitor
        #Crea dei file con le immagini jpg
        #cv2.imwrite("cropped_image_1.jpg", crop_image_1)
        #cv2.imwrite("cropped_image_2.jpg", crop_image_2)
        row.append(get_time(image_1))
        row.append(get_time(image_2))    
 
        if (date_equal(get_time(image_1), get_time(image_2))):
            time_difference = get_time_difference(image_1, image_2) # Get time difference between images
            #print("differenza tra le foto in secondi: ", time_difference)
            row.append(time_difference)
            
            #image_1_cv, image_2_cv = convert_to_cv(crop_image_1, crop_image_2) # Create OpenCV image objects
            #keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) # Get keypoints and descriptors
            keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(crop_image_1, crop_image_2, int(keyPoints))
            matches = calculate_matches(descriptors_1, descriptors_2) # Match descriptors
            #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
            if len(matches)!= 0:
                
        
                name = jpg_f[0][12:-4] + "-" + jpg_f[1][12:-4] 
                print(name)
                
                display_matches(crop_image_1, keypoints_1, crop_image_2, keypoints_2, matches, name) # Display matches
                coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
                #print('le coordinate sono',coordinates_1[0], coordinates_2[0])
                if (len(coordinates_1)>100):
                    row.append(coordinates_1[0])
                    row.append(coordinates_2[0])
                
                    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2) 
                #print("La distanza media rilevata è: ", average_feature_distance)
                    row.append(average_feature_distance)
                
                    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
                #print("La velocità media calcolata è: ",speed, "km/sec")
                    row.append(speed)
                    add_csv_data(data_file, row)
                    saveImg += 1
        count += 1
        row = []
        

# Main code
if __name__ == "__main__":
    print("main.py - AstroPI 2023/2024")

    main_functions()
