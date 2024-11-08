# fct ternaire
# tracer un diagramme ternaire

import numpy as np
import matplotlib.pyplot as plt
from types import SimpleNamespace
import sherbystats as sherby


#%% Ternary plot functions

def tri2cartX(upper_apex, right_apex, left_apex):
    """ Converts ternary to Cartesian x coordinates."""
    return 0.5 * (upper_apex + 2 * right_apex) / (upper_apex + right_apex + left_apex)


def tri2cartY(upper_apex, right_apex, left_apex):
    """ Converts ternary to Cartesian y coordinates."""
    return (3**0.5 / 2) * upper_apex / (upper_apex + right_apex + left_apex)

def ternary(upper_label=None, left_label=None, right_label=None, **fig_kw):
    """ No-fuss ternary plot using matplotlib, meaning: A simple
    ternary diagram using matplolib with the minimum necessary
    elements. It requires no other dependencies than matplolib.
    Returns the figure and axe objects with which you can use the
    typical matplotlib functions such as plot(), scatter(), etc.
    Coordinates must be converted from ternary to Cartesian for use.
    See tri2cart() function.

    Parameters
    ----------
    upper_label : str, optional
        the label of the upper corner/apex
    right_label : str, optional
        the label of the right corner/apex
    left_label : str, optional
        the label of the left corner/apex
    """

    # set grid (each 0.2)
    slines = (
              # //CB
              SimpleNamespace(x1=tri2cartX(4/5, 0, 1/5), y1=tri2cartY(4/5, 0, 1/5),
                              x2=tri2cartX(4/5, 1/5, 0), y2=tri2cartY(4/5, 1/5, 0)),
              SimpleNamespace(x1=tri2cartX(3/5, 0, 2/5), y1=tri2cartY(3/5, 0, 2/5),
                              x2=tri2cartX(3/5, 2/5, 0), y2=tri2cartY(3/5, 2/5, 0)),
              SimpleNamespace(x1=tri2cartX(2/5, 0, 3/5), y1=tri2cartY(2/5, 0, 3/5),
                              x2=tri2cartX(2/5, 3/5, 0), y2=tri2cartY(2/5, 3/5, 0)),
              SimpleNamespace(x1=tri2cartX(1/5, 0, 4/5), y1=tri2cartY(1/5, 0, 4/5),
                              x2=tri2cartX(1/5, 4/5, 0), y2=tri2cartY(1/5, 4/5, 0)),
              # //AB
              SimpleNamespace(x1=tri2cartX(0, 1/5, 4/5), y1=tri2cartY(0, 1/5, 4/5),
                              x2=tri2cartX(1/5, 0, 4/5), y2=tri2cartY(1/5, 0, 4/5)),
              SimpleNamespace(x1=tri2cartX(0, 2/5, 3/5), y1=tri2cartY(0, 2/5, 3/5),
                              x2=tri2cartX(2/5, 0, 3/5), y2=tri2cartY(2/5, 0, 3/5)),
              SimpleNamespace(x1=tri2cartX(0, 3/5, 2/5), y1=tri2cartY(0, 3/5, 2/5),
                              x2=tri2cartX(3/5, 0, 2/5), y2=tri2cartY(3/5, 0, 2/5)),
              SimpleNamespace(x1=tri2cartX(0, 4/5, 1/5), y1=tri2cartY(0, 4/5, 1/5),
                              x2=tri2cartX(4/5, 0, 1/5), y2=tri2cartY(4/5, 0, 1/5)),
              # //AC
              SimpleNamespace(x1=tri2cartX(0, 4/5, 1/5), y1=tri2cartY(0, 4/5, 1/5),
                              x2=tri2cartX(1/5, 4/5, 0), y2=tri2cartY(1/5, 4/5, 0)),
              SimpleNamespace(x1=tri2cartX(0, 3/5, 2/5), y1=tri2cartY(0, 3/5, 2/5),
                              x2=tri2cartX(2/5, 3/5, 0), y2=tri2cartY(2/5, 3/5, 0)),
              SimpleNamespace(x1=tri2cartX(0, 2/5, 3/5), y1=tri2cartY(0, 2/5, 3/5),
                              x2=tri2cartX(3/5, 2/5, 0), y2=tri2cartY(3/5, 2/5, 0)),
              SimpleNamespace(x1=tri2cartX(0, 1/5, 4/5), y1=tri2cartY(0, 1/5, 4/5),
                              x2=tri2cartX(4/5, 1/5, 0), y2=tri2cartY(4/5, 1/5, 0))
              )

    # make plot
    fig, ax = plt.subplots(constrained_layout=True, **fig_kw)

    # draw master (triangle) lines
    ax.plot([0, 1], [0, 0], '-', color='black', linewidth=3, zorder=11)
    ax.plot([0, 0.5], [0, 0.8660254], '-', color='black', linewidth=3, zorder=11)
    ax.plot([0.5, 1], [0.8660254, 0], '-', color='black', linewidth=3, zorder=11)

    # draw grid lines
    for line in slines:
        ax.plot([line.x1, line.x2], [line.y1, line.y2], '-', color='grey', linewidth=1, zorder=1)

    if upper_label is not None:
        ax.text(x=0.5, y=0.91, s=upper_label, fontsize=14,
                horizontalalignment='center', verticalalignment='top', zorder=11)
        ax.text(x=1.05, y=-0.01, s=right_label, fontsize=14,
                horizontalalignment='center', verticalalignment='top', zorder=11)
        ax.text(x=-0.05, y=-0.01, s=left_label, fontsize=14,
                horizontalalignment='center', verticalalignment='top', zorder=11)

    # Prettify
    ax.set_axis_off()  # remove the box, ticks, etc.
    ax.axis('equal')  # ensure equal aspect ratio

    return fig, ax


def ternaire(a,b,c,beta,*args):

    # Cover all the space
    a = []
    b = []
    c = []
    for i in np.arange(0.015,1.1,0.015):
        for j in np.arange(0.015,1,0.015):
            for k in np.arange(0.015,1,0.015):
                ijk = i+j+k
                if np.abs(1-ijk) < 0.01:
                    a.append(i)
                    b.append(j)
                    c.append(k)
                
    a = np.array(a)[np.newaxis].T
    b = np.array(b)[np.newaxis].T
    c = np.array(c)[np.newaxis].T
    
    ab = a*b; ac = a*c; bc = b*c
    
    X = np.concatenate((a,b,c,ab,ac,bc),axis=1)
    
    # Elemnts of beta vector must be swapped between B and C
    # to put B on the right and C on the left
    beta_swap = np.array([beta[0],beta[2],beta[1],beta[4],beta[3],beta[5]]) 
    
    y = X@beta_swap
    
    a = np.squeeze(a)
    b = np.squeeze(b)
    c = np.squeeze(c)
    y = np.squeeze(y)
    
    # Plot
    #plt.figure()
    #plt.scatter(a,b,c=y)
    
    try : upper = args[0]
    except : upper = '$x_i$'
    
    try : left = args[1]
    except : left = '$x_j$'
    
    try : right = args[2]
    except : right = '$x_k$'   
    
    fig, ax = ternary(figsize=[8,5], upper_label=upper, left_label=left, right_label=right)
    cs = ax.scatter(tri2cartX(a,b,c),tri2cartY(a,b,c),c=y,s=130,marker='^',cmap=plt.cm.plasma)
    
    
    # set grid (each 0.2)
    slines = (
              # //CB
              SimpleNamespace(x1=tri2cartX(4/5, 0, 1/5), y1=tri2cartY(4/5, 0, 1/5),
                              x2=tri2cartX(4/5, 1/5, 0), y2=tri2cartY(4/5, 1/5, 0)),
              SimpleNamespace(x1=tri2cartX(3/5, 0, 2/5), y1=tri2cartY(3/5, 0, 2/5),
                              x2=tri2cartX(3/5, 2/5, 0), y2=tri2cartY(3/5, 2/5, 0)),
              SimpleNamespace(x1=tri2cartX(2/5, 0, 3/5), y1=tri2cartY(2/5, 0, 3/5),
                              x2=tri2cartX(2/5, 3/5, 0), y2=tri2cartY(2/5, 3/5, 0)),
              SimpleNamespace(x1=tri2cartX(1/5, 0, 4/5), y1=tri2cartY(1/5, 0, 4/5),
                              x2=tri2cartX(1/5, 4/5, 0), y2=tri2cartY(1/5, 4/5, 0)),
              # //AB
              SimpleNamespace(x1=tri2cartX(0, 1/5, 4/5), y1=tri2cartY(0, 1/5, 4/5),
                              x2=tri2cartX(1/5, 0, 4/5), y2=tri2cartY(1/5, 0, 4/5)),
              SimpleNamespace(x1=tri2cartX(0, 2/5, 3/5), y1=tri2cartY(0, 2/5, 3/5),
                              x2=tri2cartX(2/5, 0, 3/5), y2=tri2cartY(2/5, 0, 3/5)),
              SimpleNamespace(x1=tri2cartX(0, 3/5, 2/5), y1=tri2cartY(0, 3/5, 2/5),
                              x2=tri2cartX(3/5, 0, 2/5), y2=tri2cartY(3/5, 0, 2/5)),
              SimpleNamespace(x1=tri2cartX(0, 4/5, 1/5), y1=tri2cartY(0, 4/5, 1/5),
                              x2=tri2cartX(4/5, 0, 1/5), y2=tri2cartY(4/5, 0, 1/5)),
              # //AC
              SimpleNamespace(x1=tri2cartX(0, 4/5, 1/5), y1=tri2cartY(0, 4/5, 1/5),
                              x2=tri2cartX(1/5, 4/5, 0), y2=tri2cartY(1/5, 4/5, 0)),
              SimpleNamespace(x1=tri2cartX(0, 3/5, 2/5), y1=tri2cartY(0, 3/5, 2/5),
                              x2=tri2cartX(2/5, 3/5, 0), y2=tri2cartY(2/5, 3/5, 0)),
              SimpleNamespace(x1=tri2cartX(0, 2/5, 3/5), y1=tri2cartY(0, 2/5, 3/5),
                              x2=tri2cartX(3/5, 2/5, 0), y2=tri2cartY(3/5, 2/5, 0)),
              SimpleNamespace(x1=tri2cartX(0, 1/5, 4/5), y1=tri2cartY(0, 1/5, 4/5),
                              x2=tri2cartX(4/5, 1/5, 0), y2=tri2cartY(4/5, 1/5, 0))
              )
    
    # draw grid lines
    for line in slines:
        ax.plot([line.x1, line.x2], [line.y1, line.y2], '-', color='black', linewidth=1, zorder=1)

    
    plt.colorbar(cs)

    #ternary()  This creates an empty ternary plot
