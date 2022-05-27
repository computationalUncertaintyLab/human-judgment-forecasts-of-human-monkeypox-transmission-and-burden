#mcandrew

import sys
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import seaborn as sns

import matplotlib.gridspec as gridspec
from datetime import datetime

if __name__ == "__main__":

    def mm2inch(x):
        return x/25.4

    def plot_density(QID,d, ax, log=False, color="blue"):
        subset = d.loc[ d.qid==QID ]

        ax.plot( subset.interval,subset.densityValue, lw=1, color="black", alpha=0.75 )

        N = len(subset)
        ax.fill_between( subset.interval, [0]*N, subset.densityValue, alpha=0.60, color=color )

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

    def save(TXT):
        fig.set_tight_layout(True)

        w = mm2inch(183)
        fig.set_size_inches(w,w/1.5)

        plt.savefig("predictive_density__{:s}.pdf".format(TXT))
        plt.savefig("predictive_density__{:s}.png".format(TXT),dpi=300)
        plt.close()

    def stamp(ax,txt):
        ax.text(0.01,0.99,txt,weight="bold",va="top",ha="left",transform=ax.transAxes)

    d  = pd.read_csv("communitypredictions.csv")
    hp = pd.read_csv("historical_forecast_data.csv")

    hp["ts"] = [ datetime.fromtimestamp(x) for x in hp.time.values ]
    
    
    plt.style.use("fivethirtyeight")


    fig = plt.figure()
    gs = fig.add_gridspec(2,2)

    ax = fig.add_subplot(gs[1,:])
    
    subset_hp = hp.loc[hp.qid==10976]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    color1 = l[0].get_color()
    
    subset_hp = hp.loc[hp.qid==10982]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    color2 = l[0].get_color()
    
    ax.set_yscale("log")
    ax.tick_params(which="both", labelsize=8)

    #ax.set_xlabel("Time",fontsize=8)
    ax.set_ylabel("Predictive median, 25th, and\n75th percentile",fontsize=10)

    dtFmt = mdates.DateFormatter('%b-%d\n%H:%m') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)

    ax.set_yticks([10,10**2,10**3,10**4,10**5]) 
    ax.set_yticklabels(["10","100","1,000","10,000","100,000"], fontsize=8)
    
    
    stamp(ax,"C.")
 
    ax = fig.add_subplot(gs[0,0])
    plot_density(10976, d,ax, log=True, color=color1) # all 

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Num. of human monkeypox cases in 2022", fontsize=10)

    ax.set_xlim(10**0,10**9)

    ax.set_xticks([10**0,10**2,10**4,10**6,10**8])
    ax.set_xticklabels(["1","100","10,000","1M","10M"],fontsize=8)
    
    stamp(ax,"A.")
    
    ax = fig.add_subplot(gs[0,1])
    plot_density(10982, d,ax, log=True, color=color2) # all 

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Num. of deaths due to\n human monkeypox in 2022", fontsize=10)

    ax.set_xlim(10**0,10**9)

    ax.set_xticks([10**0,10**2,10**4,10**6,10**8])
    ax.set_xticklabels(["1","100","10,000","1M",r"10M"],fontsize=8)
    
    stamp(ax,"B.")

   
    save("global_cases_and_burden")
    
    #---------------------------------------------------------------------------------------
    fig = plt.figure()
    gs = fig.add_gridspec(2,3)

    ax = fig.add_subplot(gs[1,:])
    
    subset_hp = hp.loc[hp.qid==10979]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    color1 = l[0].get_color()
    
    subset_hp = hp.loc[hp.qid==11039]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    color2 = l[0].get_color()
    
    subset_hp = hp.loc[hp.qid==10978]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    color3 = l[0].get_color()

    ax.set_yscale("log")
    ax.tick_params(which="both", labelsize=8)

    ax.set_ylabel("Predictive median, 25th, and\n75th percentile",fontsize=10)
    
    stamp(ax,"D.")

    dtFmt = mdates.DateFormatter('%b-%d\n%H:%m') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)

    ax=fig.add_subplot(gs[0,0])
    plot_density(10979, d,ax, log=True,color=color1) # us

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Monkeypox cases reported\nin US on July 1, 2022", fontsize=10)

    ax.set_xlim(10**0,10**5)

    stamp(ax,"A.")

    ax=fig.add_subplot(gs[0,1])
    plot_density(11039, d, ax,log=True,color=color2) # canada

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Monkeypox cases reported\nin Canada on July 1, 2022", fontsize=10)

    ax.set_xlim(10**0,10**5)

    stamp(ax,"B.")

    ax=fig.add_subplot(gs[0,2])
    plot_density(10978, d, ax,log=True,color=color3) # europe

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Monkeypox cases reported\nin Europe on July 1, 2022", fontsize=10)

    ax.set_xlim(10**0,10**5)

    stamp(ax,"C.")
    
    save("Country_level_cases")

    #---------------------------------------------------------------------------------------

    fig = plt.figure()
    gs = fig.add_gridspec(2,2)

    ax = fig.add_subplot(gs[1,:])
    
    subset_hp = hp.loc[hp.qid==10975]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    color1 = l[0].get_color()
 
    subset_hp = hp.loc[hp.qid==10981]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    color2 = l[0].get_color()

    #ax.set_yscale("log")
    ax.tick_params(which="both", labelsize=8)

    ax.set_ylabel("Predictive median, 25th, and\n75th percentile",fontsize=10)

    dtFmt = mdates.DateFormatter('%b-%d\n%H:%m') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)
    
    stamp(ax,"C.")
    
    ax = fig.add_subplot(gs[0,0])
    plot_density(10975, d,ax, log=False,color=color1) # num of countries

    ax.set_ylabel("Probability density", fontsize=10)
    ax.set_xlabel("Num. of countries reporting\n at least one infection on July 31", fontsize=10)

    ax.axvline(19,color="black",ls="--",lw=1,alpha=0.50,label="Truth as of 2020-05-24")
    ax.legend(frameon=False,loc="upper right",fontsize=8)

    stamp(ax,"A.")

    ax = fig.add_subplot(gs[0,1])
    plot_density(10981, d,ax, log=False,color=color2)

    ax.axvline(3,color="black",ls="--",lw=1,alpha=0.50,label="Truth as of 2020-05-24")
    ax.legend(frameon=False,loc="upper right",fontsize=8)
    
    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Num. of US states reporting\n at least one infection on July 1", fontsize=10)

    stamp(ax,"B.")
    
    save("Country_and_state_level_spread")
 
