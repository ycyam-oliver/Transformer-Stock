# Transformer-Stock

> The transformer-based models were modified from the official repo of Informer (https://github.com/zhouhaoyi/Informer2020) and NS-Tranformer (https://github.com/thuml/Nonstationary_Transformers) for predicting stock data. 

***Input feature(s)*** (e.g. Open, High, Low, Close, Volume) can be specfied manually in the `args.auxil_features` variable (in the `.ipynb` files) to predict any intended ***target(s)*** (e.g. Close) indicated by the `args.target` variable.

The details of stock data of SPY (SPDR S&P 500 ETF Trust) used in the models can be found in the data exploration file `data_prep_and_exploration.ipynb`. 

(1) How to use the codes
========================================
The way to run the codes for the transformer-based models and the relevant results can be found in the `.ipynb` files:

- Informer model for Stock Price -> `informer_price.ipynb`  <br>
- Informer model for Daily % Change of Stock Price  -> `informer_price.ipynb` <br>

- NS-Transformer model for Stock Price -> `nstransformer_price.ipynb` <br>
- NS-Informer model for Stock Price -> `ns_Informer_price.ipynb` <br>

(2) Baseline model
========================================
The simple ARIMA model is used as a baseline model to evaluate the transformer-based model performance. Its relevant code and results can be found in `arima_percent_change.ipynb`

