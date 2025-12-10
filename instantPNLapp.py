import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Option Portfolio Instant P&L",
    page_icon="📈",
    layout="wide")

st.title("Option P&L Dashboard ")

EPS=1e-12

class MarketData:
    def __init__(self,rate,varying_spot,volatility,spot):
        self.rate=rate
        self.varying_spot=varying_spot
        self.volatility=volatility
        self.spot=spot

class Options:
    def __init__(self,strike,maturity,type,quantity):
        self.strike=strike
        self.maturity=maturity
        self.type=type
        self.quantity=quantity
    def __price__(self,MarketData):
        return self.quantity*bsm_price(
            d1=bsm_d1(
                MarketData.varying_spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            d2=bsm_d2(
                MarketData.varying_spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            type=self.type,
            spot=MarketData.varying_spot,
            strike=self.strike,
            rate=MarketData.rate,
            maturity=self.maturity)
    def __base_price__(self,MarketData):
        return self.quantity*bsm_price(
            d1=bsm_d1(
                MarketData.spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            d2=bsm_d2(
                MarketData.spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            type=self.type,
            spot=MarketData.spot,
            strike=self.strike,
            rate=MarketData.rate,
            maturity=self.maturity)
    def __delta__(self,MarketData):
        return bsm_delta(
            d1=bsm_d1(
                MarketData.varying_spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            type=self.type,
            quantity=self.quantity)
    def __gamma__(self,MarketData):
        return bsm_gamma(
            d1=bsm_d1(
                MarketData.varying_spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            quantity=self.quantity,
            spot=MarketData.varying_spot,
            volatility=MarketData.volatility,
            maturity=self.maturity)
    def __vega__(self,MarketData):
        return bsm_vega(
            d1=bsm_d1(
                MarketData.varying_spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            quantity=self.quantity,
            spot=MarketData.varying_spot,
            maturity=self.maturity)
    def __theta__(self,MarketData):
        return bsm_theta(
            d1=bsm_d1(
                MarketData.varying_spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            d2=bsm_d2(
                MarketData.spot,
                self.strike,
                MarketData.volatility,
                self.maturity,
                MarketData.rate),
            type=self.type,
            strike=self.strike,
            rate=MarketData.rate,
            maturity=self.maturity,
            quantity=self.quantity,
            spot=MarketData.varying_spot,
            volatility=MarketData.volatility)

class Portfolio:
    def __init__(self,option_list):
        self.option_list=option_list
    def __price_portfolio__(self):
        price_portfolio=0
        for i in self.option_list:
            price_portfolio += i.__price__(MD)
        return price_portfolio
    def __portfolio_cost__(self):
        portfolio_cost=0
        for i in self.option_list:
            portfolio_cost += i.__base_price__(MD)
        return portfolio_cost
    def __delta_portfolio__(self):
        delta_portfolio=0
        for i in self.option_list:
            delta_portfolio += i.__delta__(MD)
        return delta_portfolio
    def __gamma_portfolio__(self):
        gamma_portfolio=0
        for i in self.option_list:
            gamma_portfolio += i.__gamma__(MD)
        return gamma_portfolio
    def __vega_portfolio__(self):
        vega_portfolio=0
        for i in self.option_list:
            vega_portfolio += i.__vega__(MD)
        return vega_portfolio   
    def __theta_portfolio__(self):
        theta_portfolio=0
        for i in self.option_list:
            theta_portfolio += i.__theta__(MD)
        return theta_portfolio  

option_list=[]

#Call_1=Options(100,1,1,1)
#option_list.append(Call_1)
#Call_2=Options(100,1,-1,1)
#option_list.append(Call_2)
#Call_3=Options(150,1,1,-1)
#option_list.append(Call_3)

print(option_list)
O=Portfolio(option_list)

def bsm_d1(spot,strike,volatility,maturity,rate):
    d1=(np.log(spot/strike)+(rate+((volatility**2)/2))*maturity)/(volatility*np.sqrt(maturity))
    return d1

def bsm_d2(spot,strike,volatility,maturity,rate):
    d2=(np.log(spot/strike)+(rate-((volatility**2)/2))*maturity)/(volatility*np.sqrt(maturity))
    return d2

def bsm_price(d1,d2,type,spot,strike,rate,maturity):
    if type==1:
        price=spot*norm.cdf(d1)-np.exp(-rate*maturity)*strike*norm.cdf(d2)
    else:
        price=np.exp(-rate*maturity)*strike*norm.cdf(-d2)-spot*norm.cdf(-d1)
    return price

def bsm_delta(d1,type,quantity):
    if type==1:
        delta=norm.cdf(d1)*quantity
    else:
        delta=(norm.cdf(d1)-1)*quantity
    return delta

def bsm_gamma(d1,quantity,spot,volatility,maturity):
    gamma=(norm.pdf(d1)/(spot*volatility*np.sqrt(maturity)))*quantity
    return gamma

def bsm_vega(d1,quantity,spot,maturity):
    vega=(spot*norm.pdf(d1)*np.sqrt(maturity))*quantity
    return vega

def bsm_theta(d1,d2,spot,maturity,rate,volatility,type,quantity,strike):
    if type==1:
        theta=((-(spot*volatility*norm.pdf(d1))/(2*np.sqrt(maturity)))-rate*strike*np.exp(-rate*maturity)*norm.cdf(d2))*quantity
    else:
        theta=((-(spot*volatility*norm.pdf(d1))/(2*np.sqrt(maturity)))+rate*strike*np.exp(-rate*maturity)*norm.cdf(-d2))*quantity
    return theta

#COMPOSITION DU PORTEFEUILLE D'OPTIONS

col_left, col_midle, col_right = st.columns([1, 3, 1])

with col_left:

    st.subheader("Portofolio")

    nombre_options=st.number_input("How many different options are in the portfolio?",
                                min_value=1,
                                max_value=100,
                                help="The number of different options. If you have 3 options but 2 of them share the same parameters (type, strike, maturity), write 2 instead of 3. You can specify the quantity of each option type later.",
                                )

    class Option_list_input:
        def __init__(self,nombre_options):
            self.nombre_options=nombre_options
            def __compo_portfolio__(self):
                for i in nombre_options:
                    T=st.selectbox("Option type",
                                ("Call","Put"),)
                    if T=="Call":
                        type=1
                    else:
                        type=2
                    K=st.number_input("Strike ?",
                                min_value=1.00,
                                max_value=1000.00,
                                value=100,
                    )
                    M=st.number_input("Maturity in years ?",
                                min_value=0.00,
                                max_value=10.00,
                                value=1.00,
                    )

        for i in range(nombre_options):
                    st.markdown(f"Option {i+1}")
                    Q=st.number_input("Quantity ?",
                                min_value=-1000,
                                max_value=1000,
                                value=1,
                                key=f"quantity_{i}",
                                help="If you are short on this position, enter a negative quantity"
                    )
                    TY=st.selectbox("Option type",
                                ("Call","Put"),
                                key=f"type_{i}")
                    if TY=="Call":
                        T=1
                    else:
                        T=2
                    K=st.number_input("Strike ?",
                                min_value=1.00,
                                max_value=1000.00,
                                value=100.00,
                                key=f"strike_{i}"
                    )
                    M=st.number_input("Maturity in years ?",
                                min_value=0.00,
                                max_value=10.00,
                                value=1.00,
                                key=f"matu_{i}"
                    )
                    st.space("medium")
                    option_list.append(Options(strike=K,maturity=M,type=T,quantity=Q))
                    
max_strike = max(opt.strike for opt in option_list)

with col_right :

    #SLIDER ET GRAPHES


    st.subheader("Market")

    range_slider_spot=np.linspace(EPS,1000,100000)
    slider_spot=st.select_slider(
        "Spot",
        options=range_slider_spot.round(2),
        value=100.00)

    range_slider_vol=np.linspace(EPS,1,1000)
    slider_vol=st.select_slider(
        "Volatility (sigma)",
        options=range_slider_vol.round(2),
        value=0.2)

    range_slider_rate=np.linspace(-0.1,0.3,1000)
    slider_rate=st.select_slider(
        "Rate",
        options=range_slider_rate.round(3),
        value=0.05)

    a=np.linspace(1,max(slider_spot,max_strike)*2,1000)
    MD=MarketData(slider_rate,a,slider_vol,slider_spot)

    P=O.__price_portfolio__()
    I=O.__portfolio_cost__()
    D=O.__delta_portfolio__()
    G=O.__gamma_portfolio__()
    V=O.__vega_portfolio__()
    T=O.__theta_portfolio__()

    st.subheader("About")

    st.write(
    """
    This tool was developed by **Félix Couraud**, student in Financial Markets at **ESCP Business School**. 

    I am currently seeking a **Sales & Trading internship starting July 2026**. 

    The source code is available at: https://github.com/fef40/pnl  
    Suggestions are welcome — feel free to reach out on LinkedIn:  
    https://www.linkedin.com/in/felixcrd/  

    
    """
)
    

with col_midle: # typo

    fig_pnl = px.line(
        x=a,
        y=P-I,
        labels={"x": "Spot", "y": "Instant P&L"}, 
        title="Instant P&L Chart",
        template="plotly_dark"
    )
    fig_pnl.update_layout(height=600)
    st.plotly_chart(fig_pnl)

    fig_delta = px.line(
        x=a,
        y=D,
        labels={"x": "Spot", "y": "Delta"}, 
        title="Delta of the portfolio",
        template="plotly_dark"
    )
    st.plotly_chart(fig_delta)

    fig_gamma = px.line(
        x=a,
        y=G,
        labels={"x": "Spot", "y": "Gamma"}, 
        title="Gamma of the portfolio",
        template="plotly_dark"
    )
    st.plotly_chart(fig_gamma)

    fig_vega = px.line(
        x=a,
        y=V,
        labels={"x": "Spot", "y": "Vega"}, 
        title="Vega of the portfolio",
        template="plotly_dark"
    )
    st.plotly_chart(fig_vega)

    fig_theta = px.line(
        x=a,
        y=T,
        labels={"x": "Spot", "y": "Theta"}, 
        title="Theta of the portfolio",
        template="plotly_dark"
    )
    st.plotly_chart(fig_theta)

    #Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    #.\.venv\Scripts\Activate.ps1

    #streamlit run instantPNLapp.py
