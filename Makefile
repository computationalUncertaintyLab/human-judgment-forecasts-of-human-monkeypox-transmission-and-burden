#mcandrew;

PYTHON:=python3 -W ignore

COMMITprefix:=Forecasts generated for LUcompUncertLab monkeypox model on
COMMITsuffix:=$(shell date +"%Y-%m-%d")

COMMIT:=$(COMMITprefix) $(COMMITsuffix)

runall: collectAndFormatData plotIndividualForecasts plotGroups plotSummaryQuantiles
.PHONY: runall

collectAndFormatData:
	$(PYTHON) download_predictions.py && echo "data collected"

plotIndividualForecasts:
	$(PYTHON) plot_individual_densities.py

plotGroups:
	$(PYTHON) plot_grouped_predictive_densities.py

plotSummaryQuantiles:
	$(PYTHON) plot_summary_boxplots.py
