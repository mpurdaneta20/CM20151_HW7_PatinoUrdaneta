all: ./fits/linear_fit.csv ./fits/gauss_fit.csv ./fits/step_fit.csv ./Graficas/*.png  ./fits/bestmodels.txt

./fits/bestmodels.txt: bestmodels.py ./fits/linear_fit.csv ./fits/gauss_fit.csv ./fits/step_fit.csv
	python bestmodels.py

./Graficas/*.png: bestmodels.py ./fits/linear_fit.csv ./fits/gauss_fit.csv ./fits/step_fit.csv 

./fits/step_fit.csv: step-fit.py
	python step-fit.py 

./fits/gauss_fit.csv: gauss-fit.py
	python gauss-fit.py

./fits/linear_fit.csv: linear-fit.py
	python linear-fit.py

clean:
	cd Graficas; rm *.png
	cd ..
	cd fits; rm *.csv bestmodels.txt