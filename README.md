# Computer_vision--imageoverlay
This script merges Schlieren images and flame chemiluminescence images from a laser ignition and spark discharge ignition in a cavity-based supersonic combustor. The schlieren flow is non-reactive and does not show the flame that is captured in the chemiluminescence images. The goal of this program is to outline the flame in the chemiluminescence images and superimpose that contour onto the Schlieren images for analysis.  

First the flame images are processed in three steps: 
        1) splits image into RGB, 
        2) Resize the image to match the schlieren 
        3) transforms the flame image into the same perspective of the schlieren image'''
        
Takes the files from two folders and produces the outline of the flame superimposed onto the schlieren image
    Input: Filenames to be read of both folders
    Output: New folder with merged images'''
        '''Reads images from different folders given the path and file_names'''

![](Figures/Flame000200.PNG)  
![](Figures/schlieren000200.PNG)  
![](Figures/merged000200.PNG)  
