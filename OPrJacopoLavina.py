conda install seaborn
import streamlit as st
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.sidebar.title('Option Pricing Model')
st.sidebar.subheader('Created by:')

st.sidebar.link_button(':link: :blue[Lavina Jacopo Linkedin Profile]', "http://www.linkedin.com/in/jacopo-lavina")

current_asset_price = st.sidebar.number_input('Current Asset Price', value=100.00, step=0.01, format="%.2f", key='CurrentAssetPrice')
strike_price = st.sidebar.number_input('Strike Price', value=100.00, step=0.01, format="%.2f", key='StrikePrice')
time_to_maturity = st.sidebar.number_input('Time to Maturity (Years)', value=1.00, step=0.01, format="%.2f", key='TimetoMaturity')
volatility = st.sidebar.number_input('Volatility (σ)', value=0.20, step=0.01, format="%.2f", key='Volatility')
risk_free_rate = st.sidebar.number_input('Risk-Free Interest Rate', value=0.05, step=0.01, format="%.2f", key='RiskFree')

st.sidebar.write("---") 

st.sidebar.subheader(':orange-background[Heat Map Parameters]')

min_spot_price = st.sidebar.number_input('Min Spot Price', 0.00, 10000.00, 60.00, step=0.01)
max_spot_price = st.sidebar.number_input('Max Spot Price', 0.00, 10000.00, 90.00, step=.001)
min_volatility = st.sidebar.slider('Min Volatility for Heatmap', 0.01, 1.00, 0.18, step=0.01)
max_volatility = st.sidebar.slider('Max Volatility for Heatmap', 0.01, 1.00, 0.30, step=0.01)

st.title('Black-Sholes Option Pricing Model')    

S = current_asset_price # Underling price
K =  strike_price # Strike price
T = time_to_maturity # Time to Expiration (year)
r = volatility # Risk-free ratio
vol =  risk_free_rate # volatility (sigma) (standard deviation of the stock prices)

d1 = (np.log(S/K) + (r + 0.5 * vol**2) * T) / (vol * math.sqrt(T))

d2 = d1 - (vol * math.sqrt(T))

call_value = S * math.norm.cdf(d1) - K * math.exp(-r * T) * math.norm.cdf(d2)
put_value = K * math.exp(-r * T) * math.norm.cdf(-d2) - S * math.norm.cdf(-d1)

st.markdown(f"""
<style>
    .table-container {{
        margin: auto;
        margin-top: 15px;
        width: 100%;
        border-collapse: collapse;
    }}
    .table-container th, .table-container td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }}
    .table-container th {{
        padding-top: 12px;
        padding-bottom: 12px;
        background-color: #47B4FB;
        color: black;
    }}
    .table-container td {{
        font-size: 18px;
    }}
</style>

<table class="table-container">
    <tr>
        <th>Current Asset Price</th>
        <th>Strike Price</th>
        <th>Time to Maturity (Years)</th>
        <th>Volatility (σ)</th>
        <th>Risk-Free Interest Rate</th>
    </tr>
    <tr>
        <td>{current_asset_price:.2f}</td>
        <td>{strike_price:.2f}</td>
        <td>{time_to_maturity:.2f}</td>
        <td>{volatility:.2f}</td>
        <td>{risk_free_rate:.2f}</td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="display: flex; justify-content: space-around; margin-top: 15px; margin-bottom:15px">
    <div style="background-color: #57E657; padding: 20px; border-radius: 20px; width: 35%; text-align: center;">
        <h3>CALL Value</h3>
        <p style="font-size: 24px; font-weight: bold;">${call_value:.2f}</p>
    </div>
    <div style="background-color: #F33914; padding: 20px; border-radius: 20px; width: 35%; text-align: center;">
        <h3>PUT Value</h3>
        <p style="font-size: 24px; font-weight: bold;">${put_value:.2f}</p>
    </div>
</div>
""", unsafe_allow_html=True)

def black_scholes(S, K, T, r, vol):
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * math.sqrt(T))
    d2 = d1 - vol * math.sqrt(T)
    call_value = S * math.norm.cdf(d1) - K * math.exp(-r * T) * math.norm.cdf(d2)
    put_value = K * math.exp(-r * T) * math.norm.cdf(-d2) - S * math.norm.cdf(-d1)
    return call_value, put_value

st.header("Heatmap Call and Put Options Prices")
st.subheader(r"$\textsf{\scriptsize Interactive heatmap useful to explore how option prices fluctuate with varying 'Spot Prices and Volatility', maintaining a constant 'Strike Price'.}$")

# Genera i dati per la heatmap
spot_prices = np.linspace(min_spot_price, max_spot_price, 10)
volatilities = np.linspace(min_volatility, max_volatility, 10)
call_data = np.zeros((10, 10))
put_data = np.zeros((10, 10))

# Calcola i valori delle opzioni call e put
for i, S in enumerate(spot_prices):
    for j, vol in enumerate(volatilities):
        call_value, put_value = black_scholes(S, strike_price, time_to_maturity, risk_free_rate, vol)
        call_data[j, i] = call_value
        put_data[j, i] = put_value

# Crea i DataFrame
call_df = pd.DataFrame(call_data, index=[f'{v:.2f}' for v in volatilities], columns=[f'{s:.2f}' for s in spot_prices])
put_df = pd.DataFrame(put_data, index=[f'{v:.2f}' for v in volatilities], columns=[f'{s:.2f}' for s in spot_prices])


# Crea le heatmap
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

sns.heatmap(call_df, annot=True, fmt=".2f", ax=ax[0], cmap="magma")
ax[0].set_title('Call Price Heatmap')
ax[0].set_xlabel('Spot Price')
ax[0].set_ylabel('Volatility (σ)')

sns.heatmap(put_df, annot=True, fmt=".2f", ax=ax[1], cmap="magma")
ax[1].set_title('Put Price Heatmap')
ax[1].set_xlabel('Spot Price')
ax[1].set_ylabel('Volatility (σ)')

st.pyplot(fig)
