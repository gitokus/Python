# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 11:24:23 2019

@author: Bieszczad
"""
import matplotlib.pyplot as plt
import numpy as np

#przykladowe 100 puntkow
wart_x = np.arange(100);
wart_y0 = 2 * wart_x;
wart_y1 = 4 * wart_x;

print( wart_y0 )
print( wart_y1 )
con = np.union1d(wart_y0, wart_y1)
print( con )

#rozmiar obrazka w calach = A4, rodzielczosc=100dpi
plt.figure( figsize=(8.27, 11.69), dpi=100 )

p1 = plt.subplot(411);
p1.set_title('Wykres laczony');
p1.plot(wart_x, wart_y0, color='b', marker='.', markersize=3, linestyle='none');
p1.plot(wart_x, wart_y1, color='y', marker=',', markersize=2, linestyle='none');

plt.legend(['y = 2x', 'y = 4x'], loc='upper left')

plt.show();

