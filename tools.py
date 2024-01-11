import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from sklearn import metrics

def adf_val(data):
    adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(data)
    values=[adf, pvalue, usedlag, nobs, critical_values, icbest]
    
    print('pvalue=',pvalue)
    print('adf=',adf)
    print('critical_values=',critical_values)
    
    return adf, pvalue, critical_values

def checkout_data(data, data_title='data'):
    adf_val(data)
    
    plt.figure(figsize=(11,8))
    
    plt.subplot(2,2,1)
    data.plot()
    plt.xlabel('date')
    plt.title(data_title)
    plt.xticks(rotation=70)

    plt.subplot(2,2,2)
    data.rolling(30).std().plot()
    plt.xlabel('date')
    plt.ylabel('Std. Dev.')
    plt.xticks(rotation=70)

    axes = plt.subplot(2,2,3)
    plot_pacf(data,axes,lags=60)
    plt.xlabel('date')
    plt.ylabel('Correlation')

    axes = plt.subplot(2,2,4)
    plot_acf(data,axes,lags=60)
    plt.xlabel('date')
    plt.ylabel('Correlation')
    
    plt.tight_layout()
    plt.show()
    
    return

def simulate_price(data, preds, buy_threshold=0.5, date_labels=None):
    # preds: predicted price at different time points for the test portion of the data
    # data: ground truth of prices at different time points for the entire period (train+val+test)
    
    # if forecast the price increase/ decrease by 0.5%, then buy/sell it
    # (where the buy_threshold can be varied)
    Ntest = len(preds)
    dates = date_labels.copy()
    
    stake=1000 # how much money we buy everytime

    true, pred, balances = [],[],[]

    buy_price = 0 # cost of the asset if holding any
    buy_points, sell_points = [],[]
    balance = 0

    start_index = len(data) - len(preds)

    for i in range(len(preds)):

        if i+start_index-1 < 0 :
            Ntest-=1
            del dates[0]
            continue

        last_close = data[i+start_index-1]
        current_close = data[i+start_index]

        true.append(current_close)

        pred.append(preds[i])

        predicted_pct_change=(preds[i]-last_close)/last_close*100

        if  predicted_pct_change > buy_threshold and buy_price ==0:
            buy_price=last_close
            buy_points.append(i)
        elif predicted_pct_change < -buy_threshold and not buy_price == 0:
            unit=stake/buy_price
            profit=(last_close-buy_price)*unit
            balance += profit
            buy_price = 0
            sell_points.append(i)

        balances.append(balance)

    true=np.array(true)
    pred=np.array(pred)

    plt.figure(figsize=(11,4.5))
    plt.subplot(1,2,1)
    plt.plot(pred,label='Model fitted',linewidth=0.5,c='red')
    plt.plot(true,label='Ground Truth',linewidth=1,linestyle=':',c='k')
    plt.ylabel('$')
    if dates is not None:
        plt.xticks(ticks=np.linspace(0,Ntest-1,5,dtype=np.int32()),
                   labels=[dates[dd] for dd in np.linspace(0,Ntest-1,5,dtype=np.int32())])
    plt.xlabel('Day')
    plt.title('Price')
    plt.legend()
    
    plt.subplot(1,2,2)
    plt.plot(balances)
    plt.ylabel('$')
    if dates is not None:
        plt.xticks(ticks=np.linspace(0,Ntest-1,5,dtype=np.int32()),
                   labels=[dates[dd] for dd in np.linspace(0,Ntest-1,5,dtype=np.int32())])
    plt.xlabel('Day')
    plt.title('Profit')
    plt.tight_layout()
    plt.show()

    print('MSE: %.2f'%metrics.mean_squared_error(true,pred))
    balance_df=pd.DataFrame(balances)

    pct_ret = balance_df.diff()/stake
    pct_ret = pct_ret[pct_ret!=0].dropna()

    prev=None
    ret_rate=[]
    for bal in balances:
        if prev and bal!=prev:
            ret_rate.append((bal-prev)/stake)
        prev=bal
    print('mean return per sell: %.4f'%(np.mean(ret_rate)))
    print('std of return per sell: %.4f'%(np.std(ret_rate)))
    
    return

def simulate_pct_change(data, preds, buy_threshold=0.5, date_labels=None):
    # preds: predicted % change of price at different time points
    # data: ground truth of prices at different time points for the entire period (train+val+test)
    
    # if forecast the price increase/ decrease by 0.5%, then buy/sell it
    # (where the buy_threshold can be varied)
    Ntest = len(preds)
    dates = date_labels.copy()
    
    stake=1000 # how much money we buy everytime

    true, pred, balances = [],[],[]

    buy_price = 0 
    buy_points, sell_points = [],[]
    balance = 0

    start_index = len(data) - len(preds)

    for i in range(len(preds)):

        if i+start_index-1 < 0 :
            Ntest-=1
            del dates[0]
            continue
        
        current_close = data[i+start_index]
        true.append(current_close)

        last_close = data[i+start_index-1]
        pred.append(last_close*(1+preds[i]/100))

        if preds[i] > buy_threshold and buy_price ==0:
            buy_price=last_close
            buy_points.append(i)
        elif preds[i] < -buy_threshold and not buy_price == 0:
            unit=stake/buy_price
            profit=(last_close-buy_price)*unit
            balance += profit
            buy_price = 0
            sell_points.append(i)

        balances.append(balance)

    true=np.array(true)
    pred=np.array(pred)

    plt.figure(figsize=(11,4.5))
    plt.subplot(1,2,1)
    plt.plot(pred,label='Model fitted',linewidth=0.5,c='red')
    plt.plot(true,label='Ground Truth',linewidth=1,linestyle=':',c='k')
    plt.ylabel('$')
    if dates is not None:
        plt.xticks(ticks=np.linspace(0,Ntest-1,5,dtype=np.int32()),
                   labels=[dates[dd] for dd in np.linspace(0,Ntest-1,5,dtype=np.int32())])
    plt.xlabel('Day')
    plt.title('Price')
    plt.legend()
    
    plt.subplot(1,2,2)
    plt.plot(balances)
    plt.ylabel('$')
    if dates is not None:
        plt.xticks(ticks=np.linspace(0,Ntest-1,5,dtype=np.int32()),
                   labels=[dates[dd] for dd in np.linspace(0,Ntest-1,5,dtype=np.int32())])
    plt.xlabel('Day')
    plt.title('Profit')
    plt.tight_layout()
    plt.show()

    print('MSE: %.2f'%metrics.mean_squared_error(true,pred))
    balance_df=pd.DataFrame(balances)

    pct_ret = balance_df.diff()/stake
    pct_ret = pct_ret[pct_ret!=0].dropna()

    prev=None
    ret_rate=[]
    for bal in balances:
        if prev and bal!=prev:
            ret_rate.append((bal-prev)/stake)
        prev=bal
    print('mean return per sell: %.4f'%(np.mean(ret_rate)))
    print('std of return per sell: %.4f'%(np.std(ret_rate)))
    
    return