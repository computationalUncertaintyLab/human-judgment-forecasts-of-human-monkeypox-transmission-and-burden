#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":

    def mm2inch(x):
        return x/25.4

    def plot_density(QID,d, ax, log=False):
        subset = d.loc[ d.qid==QID ]

        ax.plot( subset.interval,subset.densityValue, lw=1, color="black", alpha=0.75 )

        N = len(subset)
        ax.fill_between( subset.interval, [0]*N, subset.densityValue, alpha=0.60 )

        ax.tick_params(labelsize=8)
        
        if log:
            ax.set_xscale('log')

            l,u = ax.get_xlim()
            ax.set_xlim(l*0.8,u)

    def plot_bars(QID,d,ax):
        subset = d.loc[ d.qid==QID ]

        w=  subset.interval.values[1]-subset.interval.values[0]
        ax.bar( subset.interval, subset.densityValue,width=w)
        ax.tick_params(labelsize=8)
            
        
    d = pd.read_csv("communitypredictions.csv")
    
    plt.style.use("fivethirtyeight")
    fig,axs = plt.subplots(2,3)
    
    ax = axs[0,0]
    plot_density(10976, d,ax, log=True) # all 

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Num. of estimated Monkeypox\ninfections in 2022", fontsize=10)
    
    ax = axs[0,1]
    plot_density(10979, d,ax, log=True) # us

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Monkeypox cases reported\nin US on July 1, 2022", fontsize=10)
 

    ax = axs[0,2]
    plot_density(10978, d, ax,log=True) # europe

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Monkeypox cases reported\nin Europe on July 1, 2022", fontsize=10)
 

    ax = axs[1,0]
    plot_density(10975, d,ax, log=False) # num of countries

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Num. of countries reporting\n at least one infection on July 31", fontsize=10)
 

    ax = axs[1,1]
    plot_density(10981, d,ax, log=False)

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Num. of US states reporting\n at least one infection on July 1", fontsize=10)
 
    ax = axs[1,2]
    plot_bars(10977,d,ax)
    
    ax.set_ylabel("Frequency", fontsize=10)
    ax.set_xlabel("Prob. the WHO will declare\n monkeypox a PHEIC\nbefore 2023", fontsize=10)

    
    fig.set_tight_layout(True)

    w = mm2inch(183)
    fig.set_size_inches(w,w/1.5)

    plt.savefig("predictive_densities.pdf")
    plt.savefig("predictive_densities.png",dpi=300)
    plt.close()
