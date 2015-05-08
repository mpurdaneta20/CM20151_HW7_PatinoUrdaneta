all: ./data/time_series.csv ./fits/linear_fit.csv ./fits/gauss_fit.csv ./fits/step_fit.csv ./Graficas/*.png  ./fits/bestmodels.txt

./fits/bestmodels.txt: bestmodels.py ./fits/linear_fit.csv ./fits/gauss_fit.csv ./fits/step_fit.csv
	python bestmodels.py

./Graficas/*.png: bestmodels.py ./fits/linear_fit.csv ./fits/gauss_fit.csv ./fits/step_fit.csv 

./fits/step_fit.csv: step-fit.py
	python step-fit.py 

./fits/gauss_fit.csv: gauss-fit.py
	python gauss-fit.py

./fits/linear_fit.csv: linear-fit.py
	python linear-fit.py

./data/time_series.csv: Conversion_Fechas.R
	Rscript Conversion_Fechas.R

clean:
	cd Graficas; rm *.png
	cd ..
	cd fits; rm *.csv bestmodels.txt
	cd ..
	cd data; rm time_series.csv