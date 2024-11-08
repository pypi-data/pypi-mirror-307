# ANOVA 
# Ryan Gosselin
# Version 2023

import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np
import pandas as pd



def get_index_positions(list_of_elems, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        #except ValueError as e:
        except:
            break
    return index_pos_list



def include_C(text):
    # OLS expects categorical variables in ANOVA
    # to do so, add C() aroun each variable

    # Find + 
    plus = get_index_positions(text, '+')
    plus = np.array(plus)[np.newaxis]
    # Find ~
    wave = get_index_positions(text, '~')
    wave = np.array(wave)[np.newaxis]
    # Find :
    dots = get_index_positions(text, ':')
    dots = np.array(dots)[np.newaxis]
    # How long is the text string
    length = len(text)
    length = np.array(length)[np.newaxis][np.newaxis]
    # Combine all these items
    parts = np.concatenate((plus, wave, dots, length),axis=1)
    parts = np.sort(parts)

    # Add C() around each variable
    formula = ''
    formula = formula + text[0:int(parts[0,0])+1]
    #print(formula)
    
    for i in range(parts.shape[1]-1):
        word = text[int(parts[0,i])+1:int(parts[0,i+1])]
        word = 'C('+word+')'
        #print(word)
        formula = formula + word
        #print(formula) 
        try:
            sign = text[int(parts[0,i+1])]
            formula = formula + sign
        except:
            break
    return formula


def exclude_C(text):
    # OLS expects categorical variables in ANOVA
    # to do so, add C() aroun each variable
    # After OLS, remove it to show in table

   # Find + 
    plus = get_index_positions(text, '+')
    plus = np.array(plus)[np.newaxis]
    # Find ~
    wave = get_index_positions(text, '~')
    wave = np.array(wave)[np.newaxis]
    # How long is the text string
    length = len(text)
    length = np.array(length)[np.newaxis][np.newaxis]
    # Combine all these items
    parts = np.concatenate((plus, wave, length),axis=1)
    parts = np.sort(parts)

    WORDS = []
    for i in range(parts.shape[1]-1):
        word = text[int(parts[0,i])+1:int(parts[0,i+1])]
        WORDS.append(word)
    return WORDS

def anova(data,text,general):
    
    '''
    ANOVA
    
    data: données dans un format pandas
    text: modèle ANOVA recherché
    general: 1 si un plan d'experience ANOVA à plusieurs niveaux (3 et +)
    '''
    
    # OLS expects categorical variables in ANOVA
    # to do so, add C() aroun each variable
    if general == 1:
        formula = include_C(text)
    else:
        formula = text
      
    model = ols(formula, data).fit()
    table = sm.stats.anova_lm(model, typ=2)
    
    MS = table['sum_sq']/table['df'] 
    table.insert(2, 'MS', MS)
    
    table.columns = ['SS', 'df', 'MS', 'F','p']
    
    WORDS = exclude_C(text)
    WORDS.append('Erreur')
    WORDS.append('Total')
    
    
    # Totals
    y_bar = np.mean(data.y)
    SST = np.sum((data.y - y_bar)**2)
    dfT = len(data.y)-1
    
    
    # Check for confounding
    # Summed within the table
    #SSsum = table['SS'].sum() 
    dfsum = table['df'].sum()
    
    
    # Include row for totals
    d_row = [SST,dfT,'-','-','-']
    table.loc[len(table)] = d_row
    
    table.index = WORDS
    
    # Get rid of NaN
    table.at['Erreur', 'F'] = ('-')
    table.at['Erreur', 'p'] = ('-')
    
    freedom = dfsum > dfT
    
    if freedom == 1:
        print('\n..........................................')
        print('ATTENTION!')
        print('Il manque %.0f degré de liberté.' %freedom)    
        print('Vérifier le patron de confusion.')
        print('..........................................')
        print('\n')
    if freedom > 1:
        print('\n..........................................')
        print('ATTENTION!')
        print('Il manque %.0f degrés de liberté.' %freedom)   
        print('Vérifier le patron de confusion.')
        print('..........................................')
        print('\n')
     
    return table