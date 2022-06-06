import numpy as np
import cv2
from math import sqrt
from os import path

# Calculando o valor da correção gamma
def __calc_gamma_correction(f, c, y):
    return pow((f/255), 1/y)*255

def __do_gamma_correction(f, f_name):

    # Niveis de gamma utilizados
    gamma_range = (
        0.04, 
        0.10, 
        0.20,
        0.40,
        0.67,
        1.0,
        1.5,
        2.5,
        5.0,
        10.0,
        25.0,
    )

    s = f.shape
    imgs = [] # Array que vai guardar as correções
    imgs_index = 0

    for g in gamma_range:
        imgs.append(np.array([])) # Adiciona um NP array que sera a imagem corrigida para cada nivel de gamma
        print(f'Aplicando correção com gama = {g}...')
        for i in range(s[0]):
            for j in range(s[1]):
                imgs[imgs_index] = np.append(imgs[imgs_index], __calc_gamma_correction(f[i][j], 1, g))
        
        aux = imgs[imgs_index]
        aux = np.reshape(aux, f.shape)

        cv2.imwrite(path.join('output', f'{f_name}_{g}.jpg'), aux)
        imgs_index = imgs_index + 1
    
    print('\nImagens salvas em: output/')

def run():
    __do_gamma_correction(cv2.imread(path.join('images', 'polem.bmp'), cv2.IMREAD_GRAYSCALE), 'polem')