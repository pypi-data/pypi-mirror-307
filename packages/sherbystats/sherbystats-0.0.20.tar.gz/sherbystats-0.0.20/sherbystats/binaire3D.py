# Binary surface plot 3D
import numpy as np
import matplotlib.pyplot as plt

def binaire3D(i,j,beta,*args): # creates a model with beta coefficients : [i,j,ij,i2,j2]

    # Make mesh grid
    ii = np.arange(min(i),max(i),(max(i)-min(i))/100)
    jj = np.arange(min(j),max(j),(max(j)-min(j))/100)
    ii, jj = np.meshgrid(ii, jj) 
    ij2 = ii*jj
    ii2 = ii*ii
    jj2 = jj*jj
    
    yy = beta[0]*np.ones((ii.shape)) + beta[1]*ii + beta[2]*jj + \
    beta[3]*ij2 + beta[4]*ii2 + beta[5]*jj2
        
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(ii, jj, yy, cmap=plt.cm.plasma,linewidth=0, antialiased=False, alpha = 0.5)
    # ax.set_xlabel('a', fontsize=16)
    # ax.set_ylabel('b', fontsize=20)
    # ax.set_zlabel('y', fontsize=20)
    
    try : ax.set_xlabel(args[0],fontsize=16)
    except : ax.set_xlabel('$x_i$', fontsize=16)
    try : ax.set_ylabel(args[1],fontsize=16)
    except : ax.set_ylabel('$x_j$', fontsize=16)
    try : ax.set_zlabel(args[2], fontsize=16) 
    except : ax.set_zlabel('$y$', fontsize=16)    
        
    plt.show()

