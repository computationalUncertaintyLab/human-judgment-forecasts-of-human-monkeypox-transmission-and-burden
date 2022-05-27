#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from interpolator import interpolator


def prob_btw_2_values(v1,v2,qid,d,linear=False):

    import numpy as np
    eps = np.finfo(float).eps 
    
    subset = d.loc[d.qid==qid]

    xvalues = np.linspace(0,1,201) 
    yvalues = subset.densityValue.values

    b, exponent = subset.iloc[0]["b"], subset.iloc[0]["exponent"] 

    minvalue = pd.read_csv("metadata.csv")
    minvalue = float(minvalue.loc[minvalue.qid==qid,"lower_bound"])
    
    if not linear:
        v1 = np.log( (v1-minvalue) / b) / exponent 
        v2 = np.log( (v2-minvalue) / b) / exponent

    if linear:
        xvalues = subset.interval.values
    
    f = interpolator(xvalues,yvalues)

    def computeCumualtive(mn,f,x):
        from scipy.integrate import quad
        y,err = quad(f,mn,x)
        return y

    if linear:
        pass
    else:
        xvalues[0] = 0
        mnx = xvalues[0]
    pieces = []
    for x0,x1 in zip(xvalues[:-1],xvalues[1:]):
        pieces.append( computeCumualtive(x0,f,x1) )
    ttl = sum(pieces) # total area under curve
    cdf = np.cumsum(pieces)/ttl

    g = interpolator(xvalues,[0]+list(cdf))

    return g(v2-eps) - g(v1+eps)


if __name__ == "__main__":

    #-----
    d = pd.read_csv("communitypredictions.csv")
    g = prob_btw_2_values(400,1000, 10976, d)

    g = prob_btw_2_values(1000,10000, 10976, d)
    g = 1 - prob_btw_2_values(400,10000, 10976, d)
    

    subset = d.loc[d.qid==10982]
    g = prob_btw_2_values(2,10, 10982, d)
    g = prob_btw_2_values(10,100, 10982, d)
    g = prob_btw_2_values(2,1000, 10982, d)
 

    subset = d.loc[d.qid==10979]
    g = prob_btw_2_values(2,10, 10979, d)
    g = prob_btw_2_values(10,100, 10979, d)
    g = prob_btw_2_values(100,1000, 10979, d)
    g = prob_btw_2_values(2,1000, 10979, d)
 

    subset = d.loc[d.qid==11039]
    g = prob_btw_2_values(44,100, 11039, d)
    g = prob_btw_2_values(100,1000, 11039, d)
    g = prob_btw_2_values(44,1000, 11039, d)
 
    subset = d.loc[d.qid==10978]
    g = prob_btw_2_values(150,500, 10978, d)
    g = prob_btw_2_values(500,1000, 10978, d)
    g = prob_btw_2_values(1000,2000, 10978, d)
    g = prob_btw_2_values(150,2000, 10978, d)
    
    
    subset = d.loc[d.qid==10975]
    g = prob_btw_2_values(7,30  , 10975 , d, linear=True)
    g = prob_btw_2_values(30,100, 10975 , d, linear=True )
    g = prob_btw_2_values(7,100 , 10975 , d, linear=True)

 
    subset = d.loc[d.qid==10981]
    g = prob_btw_2_values(1.1,10  , 10981 , d, linear=True)
    g = prob_btw_2_values(10,20, 10981 , d, linear=True )
    g = prob_btw_2_values(20,30 , 10981 , d, linear=True)
    g = prob_btw_2_values(1.1,30 , 10981 , d, linear=True)


    #for binary question

    subset = d.loc[d.qid==10977]
    def cdf(x,dens):
        x = np.sort(x)
        prob = np.cumsum(dens)/sum(dens)
        return x,prob
    x,px = cdf(subset.interval.values, subset.densityValue.values)

    q = 0.5
    px[np.argmin( abs(x-q))]
    






    

    
