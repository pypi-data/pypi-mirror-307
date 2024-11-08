# Binary surface plot
import numpy as np
import matplotlib.pyplot as plt

def binaire(i,j,beta,*args): # creates a model with beta coefficients : [i,j,ij,i2,j2]

    # Use this model to cover all the space
    I = []
    J = []
    
    for ii in np.arange(min(i),max(i),(max(i)-min(i))/100):
        for jj in np.arange(min(j),max(j),(max(j)-min(j))/100):
            I.append(ii)
            J.append(jj)
         
    I = np.array(I)[np.newaxis].T
    J = np.array(J)[np.newaxis].T
    
    IJ = I*J
    I2 = I*I
    J2 = J*J
    onez = np.ones((len(I),1))
    X = np.concatenate((onez,I,J,IJ,I2,J2),axis=1)

    yhat = X@beta
 
    plt.figure()
    plt.scatter(I,J,marker='s',c=yhat,cmap=plt.cm.plasma)
    try : plt.xlabel(args[0],fontsize=16)
    except : plt.xlabel('$x_i$',fontsize=16)
    try : plt.ylabel(args[1],fontsize=16)
    except : plt.ylabel('$x_j$',fontsize=16)  
    plt.grid('on',c='black')    
    plt.xlim(min(i),max(i))
    plt.ylim(min(j),max(j))
    plt.colorbar()
    plt.tight_layout()

