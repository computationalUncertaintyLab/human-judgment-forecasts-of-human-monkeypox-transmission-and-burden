#mcandrew

import sys
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import seaborn as sns

from datetime import datetime

if __name__ == "__main__":

    def stamp(ax,txt):
        ax.text(0.01,0.99,txt,weight="bold",va="top",ha="left",transform=ax.transAxes)

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

    def save(QID):
        fig.set_tight_layout(True)

        w = mm2inch(183)
        fig.set_size_inches(w,w/1.5)

        plt.savefig("predictive_density__{:d}.pdf".format(QID))
        plt.savefig("predictive_density__{:d}.png".format(QID),dpi=300)
        plt.close()

    d = pd.read_csv("communitypredictions.csv")
    
    plt.style.use("fivethirtyeight")
    
    fig,ax = plt.subplots()
    plot_density(10976, d,ax, log=True) # all 

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Num. of monkeypox infections in 2022", fontsize=10)

    save(10976)

    fig,ax = plt.subplots()
    plot_density(10982, d,ax, log=True) # all 

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Num. of deaths due to human monkeypox in 2022", fontsize=10)

    save(10982)
    
    
    fig,ax = plt.subplots() 
    plot_density(10979, d,ax, log=True) # us

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Human monkeypox cases reported\nin US as of July 1, 2022", fontsize=10)

    save(10979)
 
    fig,ax = plt.subplots()
    plot_density(10978, d, ax,log=True) # europe

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Human monkeypox cases reported\nin Europe on July 1, 2022", fontsize=10)

    save(10978)
 
    fig,ax = plt.subplots()
    plot_density(10975, d,ax, log=False) # num of countries

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Num. of countries reporting\n at least one infection as of July 31", fontsize=10)

    save(10975)
 
    fig,ax = plt.subplots()
    plot_density(10981, d,ax, log=False)

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Num. of US states reporting\n at least one infection as of July 1", fontsize=10)

    save(10981)

    fig,ax = plt.subplots()
    plot_density(11039, d,ax, log=True)

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Human monkeypox cases reported\nin Canada as of July 1, 2022", fontsize=10)

    save(11039)
 
 
    fig,ax = plt.subplots()

    subset = d.loc[d.qid==10977]

    # def cdf(x,dens):
    #     x = np.sort(x)
    #     prob = np.cumsum(dens)/sum(dens)
    #     return x,prob
    # x,px = cdf(subset.interval.values, subset.densityValue.values)

    # n = len(x)
    # a = 0.05
    # epsilon = ( (1/(2*n)) * np.log(2/a) )**0.5

    # L = np.array([ max(x,0) for x in px-epsilon])
    # U = np.array([ min(x,1) for x in px+epsilon])

    # ax = axs[0]
    # l = ax.plot(x,1.-px)
    # ax.fill_between(x,1.-L,1.-U, color = l[0].get_color() , alpha=0.50)
    
    # ax.set_ylabel("Prob. the crowd assigns\nto the value x or greater ", fontsize=10)
    # ax.set_xlabel("Prob. the WHO will declare monkeypox a PHEIC before 2023", fontsize=10)

    # ax.set_yticks(np.arange(0,1+0.1,0.1))
    
    # ax.tick_params(labelsize=8)

    # stamp(ax,"A.")
    

    hp = pd.read_csv("historical_forecast_data.csv")
    hp["ts"] = [ datetime.fromtimestamp(x) for x in hp.time.values ]
    
    subset_hp = hp.loc[hp.qid==10977]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    ax.set_yticks(np.arange(0,1+0.1,0.1))
    ax.tick_params(which="both", labelsize=8)

    ax.set_ylabel("Predictive median",fontsize=10)

    dtFmt = mdates.DateFormatter('%b-%d\n%H:%m') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)

#    stamp(ax,"B.")
    
    save(10977)

    #NEED TO ADD CANADA
