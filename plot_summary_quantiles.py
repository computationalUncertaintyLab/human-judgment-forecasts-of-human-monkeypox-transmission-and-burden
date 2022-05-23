#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":

    def mm2inch(x):
        return x/25.4
    
    def save():
        fig.set_tight_layout(True)

        w = mm2inch(183)
        fig.set_size_inches(w,w/1.5)

        plt.savefig("predictive_density__tree.pdf")
        plt.savefig("predictive_density__tree.png",dpi=350)
        plt.close()

    d = pd.read_csv("communityquantiles.csv")
    

    plt.style.use("fivethirtyeight")
    fig,ax = plt.subplots()

    for n,qid in enumerate([10976, 10982, 10979, 11039, 10978, 10975, 10981]): # need to add canadan
        subset = d.loc[d.qid==qid]
            
        _10th, _90th = subset.loc[ subset["quantile"]==0.10, "value"], subset.loc[ subset["quantile"]==0.90, "value"], 
        median= subset.loc[ subset["quantile"]==0.50, "value"]

        ypos = 6-n
        handle = ax.plot( [_10th, _90th ], [ypos]*2, lw=2 )
        ax.scatter( [median], [ypos]*1 ,s=20 )

        clr = handle[0].get_color()
        
        if n in [0,1,4,5]:
            ax.text( median, ypos+0.01, "{:,.0f}".format( float(median)), va="bottom", ha="center", fontsize=10, color=clr, weight="bold" )
            ax.text( _10th , ypos+0.01, "{:,.0f}".format( float(_10th)) , va="bottom", ha="right", fontsize=10, color=clr, weight="bold" )
            ax.text( _90th , ypos+0.01, "{:,.0f}".format( float(_90th)) , va="bottom", ha="left"  , fontsize=10, color=clr, weight="bold" )
        else:
            ax.text( median, ypos+0.01, "{:,.0f}".format( float(median)), va="bottom", ha="center", fontsize=10, color=clr, weight="bold" )
            ax.text( _10th , ypos+0.01, "{:,.0f}".format( float(_10th)) , va="bottom", ha="center", fontsize=10, color=clr, weight="bold" )
            ax.text( _90th , ypos+0.01, "{:,.0f}".format( float(_90th)) , va="bottom", ha="center", fontsize=10, color=clr, weight="bold" )
            
        if n ==2:
            ax.text( median, ypos-0.05, "median".format( float(median)), va="top", ha="center", fontsize=10 , color=clr, weight="bold" )
            ax.text( _10th , ypos-0.05, "10th".format( float(_10th)) , va="top", ha="center"  , fontsize=10 , color=clr, weight="bold" )
            ax.text( _90th , ypos-0.05, "90th".format( float(_90th)) , va="top", ha="center"  , fontsize=10 , color=clr, weight="bold" )
            

    ax.set_xscale("log")
    ax.set_xticks([10**x for x in np.arange(1,6)])
    
    
    ax.set_yticks(np.arange(0,7))
    ax.set_yticklabels(["Num. of estimated monkeypox\ninfections in 2022"
                        ,"Num. of deaths due\n to human monkeypox in 2022"
                    ,"Human monkeypox cases reported\nin US as of July 1, 2022"
                    ,"Human monkeypox cases reported\nin Canada as of July 1, 2022"    
                    ,"Human monkeypox cases reported\nin Europe as of July 1, 2022"
                    ,"Num. of countries reporting\n at least one infection on July 31"
                    ,"Num. of US states reporting\n at least one infection on July 1"][::-1])

    ax.set_xlabel("Predicted values", fontsize=8)
    
    save()
        
        
    
