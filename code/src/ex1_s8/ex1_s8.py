from turtle import right
import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt
from math import floor
from numba import njit
######################################################################################################

@njit
def __calcNormalizedHistogram(img):
    l = np.amax(img) # Encontra o nível de cinza mais alto
    qtd_pixels = img.shape[0] * img.shape[1]
    
    hist = []

    # Criando a tabela base do histograma
    for i in range(l+1):
        hist.insert(i, [i, 0.0])

    # Preenchendo tabela base
    for i in img:
        for j in i:
            hist[j][1] = hist[j][1] + 1
    
    #print(hist)

    # Normalizando histograma
    for i in range(l+1):
        hist[i][1] = float(hist[i][1]/qtd_pixels)

    return hist

@njit
def __doOtsu(img):
    hist = __calcNormalizedHistogram(img)
    l = np.amax(img) + 1 # Definindo quantidade de níveis de cinza
    total_pixels = img.shape[0] * img.shape[1]

    v_max = -1
    all_k = []

    for k1 in range(0, l):
        print(f'Processing.... {k1}/{l-1}')
        w0 = 0.0
        for w0a in range(0, k1):
            w0 = w0 + hist[w0a][1]

        if w0 < 1.e-6:
            continue

        u0 = 0
        for u0a in range(0, k1):
            u0 = u0 + (u0a * hist[u0a][1])/w0

        # k2
        for k2 in range(k1 + 1, l):
            w1 = 0
            for w1a in range(k1, k2):
                w1 = w1 + hist[w1a][1]

            if w1 < 1.e-6:
                continue

            u1 = 0
            for u1a in range(k1, k2):
                u1 = u1 + (u1a * hist[u1a][1])/w1

            # k3
            for k3 in range(k2 + 1, l):
                w2 = 0
                for w2a in range(k2, k3):
                    w2 = w2 + hist[w2a][1]

                if w2 < 1.e-6:
                    continue

                u2 = 0
                for u2a in range(k2, k3):
                    u2 = u2 + (u2a * hist[u2a][1])/w2

                # k4
                for k4 in range(k3 + 1, l):
                    w3 = 0
                    for w3a in range(k3, k4):
                        w3 = w3 + hist[w3a][1]

                    if w3 < 1.e-6:
                        continue

                    u3 = 0
                    for u3a in range(k3, k4):
                        u3 = u3 + (u3a * hist[u3a][1])/w3

                    w4 = 0
                    for w4a in range(k4, l):
                        w4 = w4 + hist[w4a][1]
                    
                    if w4 < 1.e-6:
                        continue

                    u4 = 0
                    for u4a in range(k4, l):
                        u4 = u4 + (u4a * hist[u4a][1])/w4

                    u = (w0 * u0) + (w1 * u1) + (w2 * u2) + (w3 * u3) + (w4 * u4)
                    
                    v = (w0*((u-u0)**2)) + (w1*((u-u1)**2)) + (w2*((u-u2)**2)) + (w3*((u-u3)**2)) + (w4*((u-u4)**2))

                    if v > v_max:
                        v_max = v
                        if len(all_k) == 0:
                            all_k.append(k1)
                            all_k.append(k2)
                            all_k.append(k3)
                            all_k.append(k4)
                        
                        else:
                            all_k[0] = k1
                            all_k[1] = k2
                            all_k[2] = k3
                            all_k[3] = k4

    print(all_k, v_max)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > all_k[3]:
                img[i][j] = 255
            elif img[i][j] <= all_k[0] :
                img[i][j] = 0
            elif img[i][j] > all_k[0]  and img[i][j] <= all_k[1] :
                img[i][j] = 60
            elif img[i][j] > all_k[1]  and img[i][j] <= all_k[2] :
                img[i][j] = 130
            elif img[i][j] > all_k[2]  and img[i][j] <= all_k[3] :
                img[i][j] = 180

    return img
    
if __name__ == '__main__':
    
    img = cv2.imread(path.join('src', 'images', 'img_seg.jpg'), cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(path.join('src', 'output', f'output_colored.png'), cv2.applyColorMap(__doOtsu(img), cv2.COLORMAP_JET) )
    #cv2.imwrite(path.join('src', 'output', f'a_plz.png'), __doOtsu(img) )
    #imgs = __doOtsu(img)
    #cv2.imwrite(path.join('src', 'output', f'1.png'), imgs[0])
    #cv2.imwrite(path.join('src', 'output', f'2.png'), imgs[1])
    #cv2.imwrite(path.join('src', 'output', f'3.png'), imgs[2])
    #cv2.imwrite(path.join('src', 'output', f'4.png'), imgs[3])