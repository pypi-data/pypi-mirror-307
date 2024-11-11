# Colorspectra: plot X spectra with colorcode defined by y

import numpy as np
import matplotlib.pyplot as plt

def colorspectra(X,y,wavelength="",x_label='wavelength',y_label='intensity',colorbar_label='% w/w'):
    '''
    
    Colorspectra: plot X spectra with a colorcode defined by y
    colorspectra(X,y,x_label,y_label,colorbar_label)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    Y [n x 1] <numpy.ndarray> 
        spectra
    wavelength [k]
        optional input
        wavelength values, x-axis positions
    x_label, y_label, colorbar_label [] <str> 
        optional inputs
        labels of x-axis, y-axis and colorbar
    
    OUTPUT
    none        
    
    '''

    if (len(wavelength)==0):
        wavelength = np.arange(0,len(X.T))

    # Plot - color by lines
    [s0,s1]=X.shape
    # Add column listing the original order of y
    
    
    order = np.arange(0,s0,1)
    order = (order[np.newaxis]).T
    
    unique, counts = np.unique(y, return_counts=True)
    su = len(unique)
    
    color = plt.cm.inferno(np.linspace(0,0.9,su))
    ycolor = np.repeat(color,counts, axis=0)
    
    # Order X
    X = X[np.squeeze(np.argsort(y,axis=0)),:]
    
    # Using contourf to provide my colorbar info, then clearing the figure
    plt.figure()
    mymap = plt.cm.inferno
    Z = [[0,0],[0,0]]
    ymin, ymax = (np.floor(np.min(y)), np.ceil(np.max(y)))
    ymin = int(ymin)
    ymax = int(ymax+1) 
    levels = np.arange(ymin,ymax,(ymax-ymin)/100)
    CS3 = plt.contourf(Z, levels,cmap=mymap)
    plt.close()

    plt.figure()
    for i in range(len(y)):
        x = X[i,:]
        plt.plot(wavelength, x.T, color=ycolor[i])
    cbar = plt.colorbar(CS3)
    cbar.set_label(colorbar_label, rotation=270, labelpad=10)
    plt.xlabel(x_label,fontsize=14)
    plt.ylabel(y_label,fontsize=14)
    # plt.title(title,fontsize=18)
    # plt.title(title)
    plt.show()
    count = int(np.round(1000*np.random.rand(1),0))
    plt.tight_layout()
    #name = 'plot colors'+str(count)+'.png'
    #name = str(name)
    #print(name)
    #fig.savefig('plot colors'+str(count)+'.png',dpi=200)