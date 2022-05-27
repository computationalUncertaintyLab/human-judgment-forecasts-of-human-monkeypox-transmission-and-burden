#mcandrew

import sys
from metaculus_client import metaculus_client
from interfaceForServer import interfaceForServer

import numpy as np
import pandas as pd

if __name__ == "__main__":
    interface = interfaceForServer()
    
    metac = metaculus_client("../../../metaculusloginInfoFlu.text")
    metac.sendRequest2Server() # ping the server
   
    questions = [10976, 10978, 10979, 10975, 10981, 10977, 11039, 10982]

    metadata = {"question_text":[]
                ,"qid":[]
                ,"page_url":[]
                ,"title":[]
                ,"numOfForecasts":[]
                ,"numOfOforecasters":[]
                ,"lower_bound":[]
                ,"upper_bond":[]
                ,"created_time":[]
                ,"publish_time":[]
                ,"resolve_time":[]}

    historical_forecast_data = {"qid":[]
                                ,"time":[]
                                ,"min":[]
                                ,"max":[]
                                ,"deriv_ratio":[]
                                ,"q1":[]
                                ,"q2":[]
                                ,"q3":[]
    }
    
    for q in questions:
        sys.stdout.write('Downloading data from Q {:04d}\n'.format(q))
        sys.stdout.flush()

        metac.collectQdata(q) # collect json data for this specific question
        if metac.data["type"]=="discussion":
            continue

        if metac.hasMetacDist() == True: 
            metac.constructPDF(comm=0)  # construct Metaculus prediction
            comm=0
        elif metac.hasCommDist() == True:
            metac.constructPDF(comm=1)
            comm=1
        else:
            continue
        interface.extractCommunityPrediction(metac, comm)

        # store historical predictions

        def scaleup(x,minvalue,maxvalue,deriv_ratio):
            if deriv_ratio==1:
                b = (maxvalue-minvalue)
                return minvalue + b*x
            else:
                exponent = np.log(deriv_ratio)
                b = (maxvalue-minvalue)/(deriv_ratio-1.)
                return minvalue + b* np.exp( exponent*x)

        history = metac.data['metaculus_prediction']['history']

        for info in history:
            time = info['t']

            try:
                q1 = scaleup(info['x']['q1'], metac.minvalue, metac.maxvalue, metac.deriv_ratio)
                q2 = scaleup(info['x']['q2'], metac.minvalue, metac.maxvalue, metac.deriv_ratio)
                q3 = scaleup(info['x']['q3'], metac.minvalue, metac.maxvalue, metac.deriv_ratio)
                
            except TypeError: #binary prediction
                q1=np.nan
                q2=info['x']
                q3=np.nan
                
            historical_forecast_data["qid"].append(q)
            historical_forecast_data["time"].append(time)
            historical_forecast_data["min"].append( metac.minvalue )
            historical_forecast_data["max"].append( metac.maxvalue)
            historical_forecast_data["deriv_ratio"].append(metac.deriv_ratio)

            
            historical_forecast_data["q1"].append(q1)
            historical_forecast_data["q2"].append(q2)
            historical_forecast_data["q3"].append(q3)


        nu = metac.data['community_prediction']['history'][-1]['nu']
            
        # META DATA FILE
        metadata["question_text"].append( metac.data["description"]  )
        metadata["qid"].append( metac.data["id"] )
        metadata["page_url"].append( metac.data["url"]   )
        metadata["title"].append( metac.data["title"] )
        metadata["numOfForecasts"].append( metac.data["number_of_predictions"] )
        metadata["numOfOforecasters"].append( nu )
        metadata["created_time"].append(metac.data["created_time"] )
        metadata["publish_time"].append(metac.data["publish_time"] )
        metadata["resolve_time"].append(metac.data["resolve_time"] )

        try:
            metadata["lower_bound"].append(metac.data["possibilities"]["scale"]["min"] )
            metadata["upper_bond"].append(metac.data["possibilities"]["scale"]["max"]  )
        except KeyError: # Yes/No question
            metadata["lower_bound"].append(0)
            metadata["upper_bond"].append(1)

    # Write meta data
    metadata = pd.DataFrame(metadata)
    metadata.to_csv("metadata.csv")

    # write historical predictions
    historical_forecast_data = pd.DataFrame(historical_forecast_data)
    historical_forecast_data.to_csv("historical_forecast_data.csv")
    
     # compute and store prob dens functions
    interface.communityPredictions2DF()
    interface.out()

    # remove the binary question
    interface.predictions = interface.predictions.loc[ interface.predictions.qid!=10977,:  ]

    # compute quantiles
    interface.computeAllQuantiles()
    interface.mergeQuantilesAndPredictions()
    interface.out(quants=True)
