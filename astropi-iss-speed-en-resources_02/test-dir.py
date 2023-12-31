from utils import *

import glob

def main_functions():

    row = []
    base_folder = path.dirname(__file__)

    # Initialise the CSV file
    data_file = path.join(base_folder, "data.csv")
    create_csv(data_file)

    # Ottieni la lista di tutti i file jpg nella cartella img
    jpg_files = glob.glob('img/*.jpg')
    print(len(jpg_files))
    # Per ogni coppia di file jpg
    for i in range(len(jpg_files)):
        for j in range(i + 1, len(jpg_files)):
            # Stampa la coppia di file
            
            row.append(jpg_files[i])
            row.append(jpg_files[j])
            image_1 = jpg_files[i]
            image_2 = jpg_files[j]
                    
            crop_image_1 = Crop_image(cv2.imread(image_1), 0.333)
            crop_image_2 = Crop_image(cv2.imread(image_2), 0.333)
            #prima viene richiamata la funzione get_image, il suo output viene stampato a monitor
            #Crea dei file con le immagini jpg
            #cv2.imwrite("cropped_image_1.jpg", crop_image_1)
            #cv2.imwrite("cropped_image_2.jpg", crop_image_2)
            
            print(get_time(image_1))
            row.append(get_time(image_1))
            print(get_time(image_2))
            row.append(get_time(image_2))
            
            time_difference = get_time_difference(image_1, image_2) # Get time difference between images
            print("differenza tra le foto in secondi: ", time_difference)
            row.append(time_difference)
            
            #image_1_cv, image_2_cv = convert_to_cv(crop_image_1, crop_image_2) # Create OpenCV image objects
            #keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) # Get keypoints and descriptors
            keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(crop_image_1, crop_image_2, 1000)
            matches = calculate_matches(descriptors_1, descriptors_2) # Match descriptors
            #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
            if len(matches)!= 0: 
                display_matches(crop_image_1, keypoints_1, crop_image_2, keypoints_2, matches) # Display matches
                coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
                print('le coordinate sono',coordinates_1[0], coordinates_2[0])
                row.append(coordinates_1[0])
                row.append(coordinates_2[0])
                
                average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2) 
                print("La distanza media rilevata è: ", average_feature_distance)
                row.append(average_feature_distance)
                
                speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
                print("La velocità media calcolata è: ",speed, "km/sec")
                row.append(speed)
                add_csv_data(data_file, row)
                row = []

                    

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
                    
                    row.append(str(files[index]))
                    row.append(str(files[index+1]))
                    
                    
                    print(image_1)
                    print(image_2)
                    crop_image_1 = Crop_image(cv2.imread(image_1), 0.333)
                    crop_image_2 = Crop_image(cv2.imread(image_2), 0.333)
                    #prima viene richiamata la funzione get_image, il suo output viene stampato a monitor
                    #Crea dei file con le immagini jpg
                    #cv2.imwrite("cropped_image_1.jpg", crop_image_1)
                    #cv2.imwrite("cropped_image_2.jpg", crop_image_2)
                    
                    print(get_time(image_1))
                    row.append(get_time(image_1))
                    print(get_time(image_2))
                    row.append(get_time(image_2))
                    
                    time_difference = get_time_difference(image_1, image_2) # Get time difference between images
                    print("differenza tra le foto in secondi: ", time_difference)
                    row.append(time_difference)
                    
                    #image_1_cv, image_2_cv = convert_to_cv(crop_image_1, crop_image_2) # Create OpenCV image objects
                    #keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) # Get keypoints and descriptors
                    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(crop_image_1, crop_image_2, 1000)
                    matches = calculate_matches(descriptors_1, descriptors_2) # Match descriptors
                    #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
                    if len(matches)!= 0: 
                        display_matches(crop_image_1, keypoints_1, crop_image_2, keypoints_2, matches) # Display matches
                        coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
                        print('le coordinate sono',coordinates_1[0], coordinates_2[0])
                        row.append(coordinates_1[0])
                        row.append(coordinates_2[0])
                        
                        average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2) 
                        print("La distanza media rilevata è: ", average_feature_distance)
                        row.append(average_feature_distance)
                        
                        speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
                        print("La velocità media calcolata è: ",speed, "km/sec")
                        row.append(speed)
                        add_csv_data(data_file, row)

                    


'''

# Main code
if __name__ == "__main__":
    print("main.py - AstroPI 2023/2024")

    main_functions()
