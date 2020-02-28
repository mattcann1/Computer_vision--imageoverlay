# -----------------------------------------------------------#
# (C) 2020 Matthew Cann
# Released under MIT Public License (MIT)
# email mcann@uwaterloo.ca
# -----------------------------------------------------------
#IMPORTS.......................................................................
import cv2
import numpy as np
import glob
import os 
import matplotlib.pyplot as plt

#FUNCTIONS.....................................................................
def get_img(Directory_name, file_name):
    '''Reads images from different folders given the path and file_names'''
    os.chdir(Directory_name) #Chanegs the directory to the given path
    img_flame = cv2.imread(file_name,1) #Reads the image given the filename and returns the RGB image
    return img_flame

def flame_img_proc(image, sch_img_size):
    '''Processes the flame image in three steps: 
        1) splits image into RGB, 
        2) Resize the image to match the schlieren 
        3) transforms the flame image into the same perspective of the schlieren image'''
    
    b,g,r = cv2.split(image) # Splits the images into the RGB layers, b is taken for the largest intensity range to provide the best picture
    
    b = cv2.resize(b,sch_img_size) #Resize Image to the schlieren image size
    
    #Perspective transform points
    pts1 = np.float32([[156,221],[129,288],[644,315],[727,244]])
    pts2 = np.float32([[192,223],[193,296],[649,315],[731,241]])
    
    M = cv2.getPerspectiveTransform(pts1,pts2) #Gets the perspective transform
    dst = cv2.warpPerspective(b,M,sch_img_size) #Transformed image

    return dst

def image_overlay(files_flame,files_schlieren):
    '''Takes the files from two folders and produces the outline of the flame superimposed onto the schlieren image
    Input: Filenames to be read of both folders
    Output: New folder with merged images'''
    
    for file_flame, file_schlieren in zip(files_flame,files_schlieren):
        img_flame = get_img(Directory_flame,file_flame) #Gets RGB images of flame
        img_schlieren = get_img(Directory_schlieren,file_schlieren) #Gets RGB images of schlieren
        schlieren_size = (img_schlieren.shape[1],img_schlieren.shape[0]) # Determines the resolution size of schlieren images
        #flame_size = (img_flame.shape[1], img_flame.shape[0])
        
        flame_img = flame_img_proc(img_flame, schlieren_size) #Processes the flame image to match the schlieren image. 
        
        Height = flame_img.shape[1]
        Width =flame_img.shape[0] 
        Pix_number = Height*Width
        
        image_train = flame_img.reshape(Pix_number) #Vectorizes the images
        y = np.where(image_train < 25,0,1) #If the intensity is greater than 25, that pixel is considered as a flame (1).
        y = y.reshape(Width,Height) #Reshapes back into image. 
        
        #plt.imshow(flame_img)
        #plt.contour(y, colors = "blue")
        #plt.show()
        
        plt.imshow(img_schlieren) # Show and save orginal image.
        plt.contour(y, colors = "white") #Prints flame contour onto image
        os.chdir(Directory_storage) #New folder for images
        plt.savefig( "merged"+ file_schlieren[9:-4]) # Saves figure with time code
        plt.show()
    return

def make_video(Image_directory, image_type,video_name ):
    os.chdir(Image_directory)
    filenames = glob.glob("*."+str(image_type))
    img_array = []
    
    for filename in filenames:
        print(filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter(str(video_name)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    return
#%% MAIN.......................................................................  

Directory_storage = 'E:\Documents\Waterloo-Masters\Image_feature_extraction\Images\schlieren_merged'
if not os.path.exists(Directory_storage):
    os.makedirs(Directory_storage)

#Gets file names from the two folders
Directory_schlieren = 'E:\Documents\Waterloo-Masters\Image_feature_extraction\Images\schlieren' # Main Directory Working in
os.chdir(Directory_schlieren)
filenames_schlieren = glob.glob("*.tif")

Directory_flame = 'E:\Documents\Waterloo-Masters\Image_feature_extraction\Images\_flame' # Main Directory Working in
os.chdir(Directory_flame)
filenames_flame = glob.glob("*.tif")

image_overlay(filenames_flame,filenames_schlieren) #Merges the images
#%%MAKES VIDEO..................................................................

Directory = 'E:\Documents\Waterloo-Masters\Image_feature_extraction\Images\schlieren_merged' # Main Directory Working in

make_video(Directory, "png", "Merged")




