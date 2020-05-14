import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import operator
import math
import sys

from functools import reduce
from PIL import Image



# gaussian kerner
def gaussian_filter(size, sigma):
    op = lambda i , j :( 1/(sigma * np.sqrt(2 * np.pi))) * np.exp( - (i**2 + j**2) / (2 * sigma**2) )

    if size%2 == 0:
        print("err:filter size sould be add number")
        return sys.eixt()
    else:
        kerner = np.array([[op(j, i)
                            for j in range(-size//2+1, size//2+1)]
                            for i in range(-size//2+1, size//2+1)])
    return kerner
    # return kerner


def blur(octaves):
    size = 5
    pd = size//2
    blur_octaves = list(range(4))

    # make padding
    for i, octave in enumerate(octaves):
        row = octave.shape[0]
        col = octave.shape[1]
        octave_pd = np.zeros((row + pd*2, col + pd*2))
        octave_pd[pd:-pd, pd:-pd] = octave[:,:]
        octaves[i] = octave_pd

    #blur   
    for k, octave in enumerate(octaves):
        row = octave.shape[0]
        col = octave.shape[1]
        blur_img_1 = np.zeros((row-size+1, col-size+1))
        blur_img_2 = np.zeros((row-size+1, col-size+1))
        blur_img_3 = np.zeros((row-size+1, col-size+1))
        blur_img_4 = np.zeros((row-size+1, col-size+1))
        blur_img_5 = np.zeros((row-size+1, col-size+1))
        kerner_1 = gaussian_filter(size, 2**(-1/2)*(1/2)*(k+1))
        kerner_2 = gaussian_filter(size, 2**(-1/2)*(k+1))
        kerner_3 = gaussian_filter(size, 1*(k+1))
        kerner_4 = gaussian_filter(size, 2**(1/2)*(k+1))
        kerner_5 = gaussian_filter(size, 2*(k+1))

        op_mul = lambda x,y : operator.mul(x,y)
        for i in range(pd, row-pd):
            for j in range(pd, col-pd):
                blur_img_1[i-pd][j-pd] = np.sum(op_mul(octave[i-pd:i+1+pd,j-pd:j+1+pd], kerner_1))
                blur_img_2[i-pd][j-pd] = np.sum(op_mul(octave[i-pd:i+1+pd,j-pd:j+1+pd], kerner_2))
                blur_img_3[i-pd][j-pd] = np.sum(op_mul(octave[i-pd:i+1+pd,j-pd:j+1+pd], kerner_3))
                blur_img_4[i-pd][j-pd] = np.sum(op_mul(octave[i-pd:i+1+pd,j-pd:j+1+pd], kerner_4))
                blur_img_5[i-pd][j-pd] = np.sum(op_mul(octave[i-pd:i+1+pd,j-pd:j+1+pd], kerner_5))

        print(k/len(octaves))

        blur_octaves[k] = [blur_img_1//1,
                            blur_img_2//1,
                            blur_img_3//1,
                            blur_img_4//1,
                            blur_img_5//1]

    return blur_octaves

# 1. scale space 만들기
def make_space(img_path):

    # image load
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    width, height = img.shape

    # image resize    
    octave_1 = np.array(cv.resize(img, (height*2, width*2)))
    octave_2 = np.array(img)
    octave_3 = np.array(cv.resize(img, (height//2, width//2)))
    octave_4 = np.array(cv.resize(img, (height//4, width//4)))

    octaves = [octave_1, octave_2, octave_3, octave_4]

    # make blur img
    blur_octaves = blur(octaves)

    # saving
    for i, blur_octave in enumerate(blur_octaves):
        for j, img in enumerate(blur_octave):
            
            plt.imshow(img, cmap='gray',)
            plt.savefig('blur_result/{}-{}.png'.format(i,j))
    
    blur_octaves = np.array(blur_octaves)
    np.save('blur_result/blur_image_array', blur_octaves)
    
    return blur_octaves

# if __name__ == "__main__":
#     img_path ='imgs/img1.ppm'
#     octaves = make_space(img_path)
