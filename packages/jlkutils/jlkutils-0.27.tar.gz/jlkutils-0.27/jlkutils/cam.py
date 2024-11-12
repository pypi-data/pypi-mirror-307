import cv2


# initialize the camera 
# If you have multiple camera connected with  
# current device, assign a value in cam_port  
# variable according to that 
cam_port = 0
cam = cv2.VideoCapture(cam_port) 
  
def photo(name):
    result, image = cam.read() 
    
    # If image will detected without any error,  
    # show result 
    if result: 

        # saving image in local storage 
        cv2.imwrite(name, image) 
        print("Foto Gemacht!")
    else: 
        print("No image detected. Please! try again") 



