import cv2

def Crop_image(image, percent):
  width = image.shape[1]
  height = image.shape[0]

  # Calcola le dimensioni del ritaglio.
  crop_width = int(width * (percent))
  crop_height = int(height * (percent))
 # Ritaglia l'immagine.
  crop_image = image[crop_height:-crop_height, crop_width:-crop_width]  
  return crop_image

# Carica l'immagine.
image = cv2.imread("photo_0675.jpg")

# Ritaglia l'immagine del 30%.
crop_image = Crop_image(image, 0.333)
#Verifica i pixel delle due immagini
#a = image.shape
#b = crop_image.shape
#print(a,b)

# Mostra l'immagine ritagliata.
cv2.imshow("Image", crop_image)
cv2.waitKey(0)
