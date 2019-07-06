from __future__ import print_function

import time
import sys
import os.path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

def read_img(file_name):
    if not os.path.isfile(file_name):
        print("cannot find file '{}'!\nskipping...".format(file_name))
        return None
    print("reading '{}'".format(file_name), end='')
    pic = plt.imread(file_name)
    print(" of size {}".format(pic.shape))
    if pic.ndim == 3:
        pic = matplotlib.colors.rgb_to_hsv(pic)
        pic = pic[:,:,-1]
    return pic

def read_imgs(file_names):
    valid_file_names = []
    pics = []
    for file_name in file_names:
        pic = read_img(file_name)
        if pic is not None:
            pics.append(pic)
            valid_file_names.append(file_name)
    return pics, valid_file_names
    
def crop_arrays(pics):
    min_w, min_h = sys.maxsize, sys.maxsize
    for pic in pics:
        h, w = pic.shape
        min_w = min(min_w, w)
        min_h = min(min_h, h)
    return [ pic[:min_h,:min_w] for pic in pics ], min_h, min_w


class ICA():

    def __init__(self):
        self.npics = 0
        self.pics = []
        self.fig = plt.figure( figsize=(30,30) )
        self.fig.set_tight_layout(True)
        
    def read_sources(self, file_names):
        print("reading images")
        self.pics, self.file_names = read_imgs(file_names)
        self.npics = len(self.pics)
        if self.npics < 2:
            sys.exit("less than 2 pictures...") 
        self.inverted = [False]*self.npics
        print("cropping images")
        self.pics, common_h, common_w = crop_arrays(self.pics)
        self.pic_size = [ common_h, common_w ]
        
    def plot(self):
        scaler = MinMaxScaler(feature_range=(0, 255))
        
        # plot original sources
        for i, pic in enumerate(self.pics):
            graph = self.fig.add_subplot(3,self.npics,1+i)
            graph.axis('off')
            graph.imshow(pic, cmap='gray')
        
        # plot mixed source
        for i in range(self.npics):
            x = self.X[:,i]
            x = scaler.fit_transform(x.reshape(-1,1))
            graph = self.fig.add_subplot(3,self.npics,self.npics+1+i)
            graph.axis('off')
            graph.imshow( np.reshape(x, self.pic_size), cmap='gray' )
            
        # show sources
        self.graphs = []
        for i in range(self.npics):
            graph = self.fig.add_subplot(3,self.npics,2*self.npics+1+i)
            s = self.S_[:,i]
            s = scaler.fit_transform(s.reshape( (-1, 1) ) )
            graph.axis('off')
            graph.imshow( np.reshape(s, self.pic_size), cmap='gray' )
            self.graphs.append(graph)
            
        plt.pause(0.1)
        print("plotting done")
        
    def run(self):
        # print out shape of all images
        print("Image size: {}".format(self.pic_size))
        print("Image total size: {}".format(np.prod(self.pic_size)))
        
        # stack the images into column vectors to make the source
        S = []
        for i, pic in enumerate(self.pics):
            s = np.ravel(pic)
            S.append(s)
            print("range of value for '{}': {} -> {}" \
                  .format(self.file_names[i], np.min(s), np.max(s)) )
        self.S = np.asarray(S).T
        print("Shape of the source matrix: {}".format(self.S.shape))
        
        # mixing matrix
        self.A = np.random.randn(self.npics,self.npics)
        print("mixing matrix = \n{}".format(self.A))
        
        # mixed data
        self.X = np.dot(self.S, self.A.T)
        
        # normalize mixed data
        self.X_standard_scaler = StandardScaler()
        self.X = self.X_standard_scaler.fit_transform(self.X)
        
        # compute ICA
        print("starting ICA")
        
        start_time = time.time()
        ica = FastICA(n_components=self.npics, random_state=1)
        self.S_ = ica.fit_transform(self.X)  # estimated sources
        self.A_ = ica.mixing_  # estimated mixing matrix
        print("Estimated mixing matrix:\n{}".format(self.A_))
        
        print("ICA done in %fs." % (time.time()-start_time))
    
    def inverseFig(self, i):
        self.inverted[i] = not self.inverted[i]
        cmap='gray'
        if self.inverted[i]:
            cmap += "_r"
        
        scaler = MinMaxScaler(feature_range=(0, 255))
        graph = self.graphs[i]
        graph.clear()
        s = self.S_[:,i]
        s = scaler.fit_transform(s.reshape( (-1, 1) ) )
        graph.axis('off')
        graph.imshow( np.reshape(s, self.pic_size), cmap=cmap )
        
        plt.pause(0.1)
