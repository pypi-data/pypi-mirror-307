# PCR regression

import numpy as np
import sherbystats as sherby



def pcr(y,X,nbPC):
    
    T,P,SSX = sherby.pca(X,nbPC)
    alpha,alpha_int,R2,F,p = sherby.mlr(y,T)
    beta = P@alpha

    yhat = X@beta
    ssy = np.sum(y**2)
    ssyhat = np.sum(yhat**2)
    SSY = ssyhat / ssy  
            
    Xhat = T@P.T
    ssX = np.sum(X**2)
    ssXhat = np.sum(Xhat**2)
    SSX = ssXhat / ssX 

    return beta, SSX, SSY


