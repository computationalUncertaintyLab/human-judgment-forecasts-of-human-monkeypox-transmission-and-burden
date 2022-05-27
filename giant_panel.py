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
    GS_left  = fig.add_gridspec(nrows=4, ncols=2, left=0.08, right=0.48,wspace=0.05, hspace=0.20, top=0.99)
    GS_right = fig.add_gridspec(nrows=3, ncols=3, left=0.55, right=0.98,wspace=0.05, hspace=0.20, top=0.99)
    
    fig = plt.figure() 

    ax = fig.add_subplot(GS_left[1,:])
    
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
    ax.set_ylabel("Predictive median, 25th, and\n75th percentile",fontsize=8)

    dtFmt = mdates.DateFormatter('%b-%d') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)

    ax.set_yticks([10,10**2,10**3,10**4,10**5]) 
    ax.set_yticklabels(["10","100","1k","10k","100k"], fontsize=8)
    
    stamp(ax,"C.")
 
    ax = fig.add_subplot(GS_left[0,0])
    plot_density(10976, d,ax, log=True, color=color1) # all 

    ax.set_ylabel("Probability density", fontsize=8)
    ax.set_xlabel("Num. of human monkeypox\n cases in 2022", fontsize=8)

    ax.set_xlim(10**0,10**9)

    ax.set_xticks([10**0,10**2,10**4,10**6,10**8])
    ax.set_xticklabels(["1","100","10k","1M","10M"],fontsize=8)
    
    stamp(ax,"A.")
    
    ax = fig.add_subplot(GS_left[0,1])
    plot_density(10982, d,ax, log=True, color=color2) # all 

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Num. of deaths due to\n human monkeypox in 2022", fontsize=8)

    ax.set_xlim(10**0,10**9)

    ax.set_xticks([10**0,10**2,10**4,10**6,10**8])
    ax.set_xticklabels(["1","100","10k","1M",r"10M"],fontsize=8)
    
    stamp(ax,"B.")


    #---------------Country and state
    ax = fig.add_subplot(GS_left[3,:])
    
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

    ax.set_ylabel("Predictive median, 25th, and\n75th percentile",fontsize=8)

    dtFmt = mdates.DateFormatter('%b-%d') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)
    
    stamp(ax,"F.")
    
    ax = fig.add_subplot(GS_left[2,0])
    plot_density(10975, d,ax, log=False,color=color1) # num of countries

    ax.set_ylabel("Probability density", fontsize=8)
    ax.set_xlabel("Num. of countries reporting at\n least one infection on July 31", fontsize=8)

    ax.axvline(19,color="black",ls="--",lw=1,alpha=0.50,label="Truth as of 2020-05-24")
    ax.legend(frameon=False,loc="upper right",fontsize=8)

    ax.set_yticklabels([])

    stamp(ax,"D.")

    ax = fig.add_subplot(GS_left[2,1])
    plot_density(10981, d,ax, log=False,color=color2)

    ax.axvline(3,color="black",ls="--",lw=1,alpha=0.50,label="Truth as of 2020-05-24")
    ax.legend(frameon=False,loc="upper right",fontsize=8)
    
    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Num. of US states reporting at\n least one infection on July 1", fontsize=8)

    ax.set_yticklabels([])

    stamp(ax,"E.")

    #RIGHT SIDE
    #CASEE---------------------
    ax = fig.add_subplot(GS_right[1,:])
    
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

    ax.set_ylabel("Predictive median, 25th, and\n75th percentile",fontsize=8)
    ax.set_yticks([10**2,10**3,10**4])
    ax.set_yticklabels(["100","1k","10k"],fontsize=8)
    

    
    stamp(ax,"J.")

    dtFmt = mdates.DateFormatter('%b-%d') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)

    ax=fig.add_subplot(GS_right[0,0])
    plot_density(10979, d,ax, log=True,color=color1) # us

    ax.set_ylabel("Probability density", fontsize=8)
    ax.set_xlabel("Monkeypox cases reported\nin US on July 1, 2022", fontsize=8)

    ax.set_xlim(10**0,10**5)
    ax.set_xticks([1,100,10000])
    ax.set_xticklabels(["1","100","10k"],fontsize=9)

    ax.set_ylim(0,5)
    ax.set_yticks(np.arange(0,5+1))
    ax.set_yticklabels([])

    stamp(ax,"G.")

    ax=fig.add_subplot(GS_right[0,1])
    plot_density(11039, d, ax,log=True,color=color2) # canada

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Monkeypox cases reported\nin Canada on July 1, 2022", fontsize=8)

    ax.set_xlim(10**0,10**5)

    ax.set_xticks([1,100,10000])
    ax.set_xticklabels(["1","100","10k"],fontsize=9)

    ax.set_ylim(0,5)
    ax.set_yticks(np.arange(0,5+1))
    ax.set_yticklabels([])


    stamp(ax,"H.")

    ax=fig.add_subplot(GS_right[0,2])
    plot_density(10978, d, ax,log=True,color=color3) # europe

    ax.set_ylabel("", fontsize=10)
    ax.set_xlabel("Monkeypox cases reported\nin Europe on July 1, 2022", fontsize=8)

    ax.set_xlim(10**0,10**5)
    ax.set_xticks([1,100,10000])
    ax.set_xticklabels(["1","100","10k"],fontsize=9)
    
    ax.set_ylim(0,5)
    ax.set_yticks(np.arange(0,5+1))
    ax.set_yticklabels([])

    stamp(ax,"I.")



    #PHEIC
    subset = d.loc[d.qid==10977]
   

    ax=fig.add_subplot(GS_right[2,:])
  
    hp = pd.read_csv("historical_forecast_data.csv")
    hp["ts"] = [ datetime.fromtimestamp(x) for x in hp.time.values ]
    
    subset_hp = hp.loc[hp.qid==10977]
    ax.fill_between( subset_hp.ts, subset_hp.q1, subset_hp.q3, alpha=0.50 )
    l = ax.plot( subset_hp.ts, subset_hp.q2)

    ax.set_yticks(np.arange(0,1+0.1,0.1))
    ax.tick_params(which="both", labelsize=8)

    ax.set_ylabel("Predictive median",fontsize=8)

    dtFmt = mdates.DateFormatter('%b-%d') # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)


    stamp(ax,"K.")
   
    fig.set_tight_layout(True)

    w = mm2inch(183)
    fig.set_size_inches(1.6*w,w)

    plt.savefig("giant_panel.pdf")
    plt.savefig("giant_panel.png",dpi=300)
    plt.close()


