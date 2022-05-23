#mcandrew

import sys
from metaculus_client import metaculus_client
from interfaceForServer import interfaceForServer

if __name__ == "__main__":
    interface = interfaceForServer()
    
    metac = metaculus_client("../../../metaculusloginInfoFlu.text")
    metac.sendRequest2Server() # ping the server
   
    questions = [10976, 10978, 10979, 10975, 10981, 10977, 11039, 10982]
    
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
        
     # compute and store prob dens functions
    interface.communityPredictions2DF()
    interface.out()

    # remove the binary question
    interface.predictions = interface.predictions.loc[ interface.predictions.qid!=10977,:  ]

    # compute quantiles
    interface.computeAllQuantiles()
    interface.mergeQuantilesAndPredictions()
    interface.out(quants=True)
