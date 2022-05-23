#mcandrew

import sys
from metaculus_client import metaculus_client
from interfaceForServer import interfaceForServer
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
                ,"lower_bound":[]
                ,"upper_bond":[]
                ,"created_time":[]
                ,"publish_time":[]
                ,"resolve_time":[]}
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


        # META DATA FILE
        metadata["question_text"].append( metac.data["description"]  )
        metadata["qid"].append( metac.data["id"] )
        metadata["page_url"].append( metac.data["page_url"]   )
        metadata["title"].append( metac.data["title"] )
        metadata["numOfForecasts"].append( metac.data["number_of_predictions"] )
        metadata["created_time"].append(metac.data["created_time"] )
        metadata["publish_time"].append(metac.data["publish_time"] )
        metadata["resolve_time"].append(metac.data["resolve_time"] )

        try:
            metadata["lower_bound"].append(metac.data["possibilities"]["scale"]["min"] )
            metadata["upper_bond"].append(metac.data["possibilities"]["scale"]["max"]  )
        except KeyError: # Yes/No question
            metadata["lower_bound"].append(0)
            metadata["upper_bond"].append(1)

    metadata = pd.DataFrame(metadata)
    metadata.to_csv("metadata.csv")
            
     # compute and store prob dens functions
    interface.communityPredictions2DF()
    interface.out()

    # remove the binary question
    interface.predictions = interface.predictions.loc[ interface.predictions.qid!=10977,:  ]

    # compute quantiles
    interface.computeAllQuantiles()
    interface.mergeQuantilesAndPredictions()
    interface.out(quants=True)
