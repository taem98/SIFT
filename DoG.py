import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv


def DoG(octaves):
    sub_octaves = []
    print(octaves.shape)
    for octave in octaves:
        sub_img = []
        for img_num in range(len(octave)-1):
            sub_img.append(octave[img_num] - octave[img_num+1])
        sub_octaves.append(sub_img)
    

    for i, sub_octave in enumerate(sub_octaves):
        for j, img in enumerate(sub_octave):
            plt.imshow(img, cmap='gray',)
            plt.savefig('DoG_result/{}-{}.png'.format(i,j))
    
    sub_octaves = np.array(sub_octaves)
    np.save('DoG_result/DoG_result_array', sub_octaves)

    return np.array(sub_octaves)
