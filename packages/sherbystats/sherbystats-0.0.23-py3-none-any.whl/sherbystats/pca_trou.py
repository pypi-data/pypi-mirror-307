# PCA trous

import numpy as np

def pca_trou(X, nbPC):

    s0, s1 = X.shape
    T = np.zeros((s0, nbPC))
    P = np.zeros((s1, nbPC))
        
    for k in range(0,nbPC):
        error = 1
        t_temp = np.ones((s0, 1))
        t = np.ones((s0, 1))
        
        while error > 1E-6:
            
            # The next few lines do: 
            # p = (X.T@t)/(t.T@t)
            # p = p/np.linalg.norm(p,2)
            num = np.zeros((1,X.shape[1]))
            denom = np.zeros((1,X.shape[1]))
            for i in range(X.shape[0]):
                Xt = X[i,:]*t[i]
                Xt[np.isnan(Xt)] = 0 # Replace NaNs by 0
                num = num + Xt
                tt = t[i]**2
                denom = denom + tt 
            p = (num / denom).T
            p = p/np.linalg.norm(p,2)
            # np.linalg.norm(p,2) = np.max(np.sqrt(p.T @ p))
    
            # The next few lines do: 
            # t = (X@p)/(p.T@p)
            num = np.zeros((1,X.shape[0]))
            denom = np.zeros((1,X.shape[0]))
            
            for j in range(X.shape[1]):
                Xp = X[:,j]*p[j]
                Xp[np.isnan(Xp)] = 0 # Replace NaNs by 0
                num = num + Xp
                
                pp = p[j]**2
                denom = denom + pp
            t = (num / denom).T
    
            # Check t convergence --------------------
            error = sum(np.power((t-t_temp),2),0) # Squared error
            t_temp = t
            # ----------------------------------------     
        P[:,k] = np.squeeze(p)
        T[:,k] = np.squeeze(t)
        X = X - t@p.T
    
    return T,P        