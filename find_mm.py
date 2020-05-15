import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import math
import sys


def check_mm(img_1, img_2, img_3):
    row, col = img_1.shape[0], img_1.shape[1]
    mm_check_img = np.ones((row-2, col-2)) * 255
    for i in range(1, row-1):
        for j in range(1, col-1):
            center = img_2[i][j]
            p_s = np.array([img_1[i-1:i+2, j-1:j+2],
                                    img_2[i-1:i+2, j-1:j+2],
                                    img_3[i-1:i+2, j-1:j+2]])

            if center >= p_s.max():
                mm_check_img[i-1][j-1] = 0
            elif center <= p_s.min():
                mm_check_img[i-1][j-1] = 0
            
    return mm_check_img

def find_mm(octaves):
    mm_octaves = []
    for octave in octaves:
        mm_octave = []
        for img_num in range(2, len(octave)):

            img = check_mm(octave[img_num-2], octave[img_num-1], octave[img_num])
            mm_octave.append(img)

        mm_octaves.append(mm_octave)
    
    for i, mm_octave in enumerate(mm_octaves):
        for j, img in enumerate(mm_octave):
            
            plt.imshow(img, cmap='gray',)
            plt.savefig('mm_check_img/{}-{}.png'.format(i,j))
    
    mm_octaves = np.array(mm_octaves)
    np.save('mm_check_img/mm_check_imgs', mm_octaves)
    
    return np.array(mm_octaves)
        