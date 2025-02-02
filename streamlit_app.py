# Standart python imports
from enum import Enum
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Third party imports
import streamlit as st

# Local package imports
from option_pricing import BlackScholesModel, MonteCarloPricing, BinomialTreeModel, Ticker

history_df = pd.DataFrame()
class OPTION_PRICING_MODEL(Enum):
    BLACK_SCHOLES = 'Black Scholes Model'
    MONTE_CARLO = 'Monte Carlo Simulation'
    BINOMIAL = 'Binomial Model'

@st.cache
def get_historical_data(ticker):
    """Getting historical data for speified ticker and caching it with streamlit app."""
    return Ticker.get_historical_data(ticker)

# Ignore the Streamlit warning for using st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

markdown_about = """## Coherent Spark

[![N|Solid](https://cdn-dobio.nitrocdn.com/kxxhJEeIPqWRFfdFTzrYPqOhMMlkFVKR/assets/static/optimized/rev-822d44c/app/uploads/2021/11/Logo-Coherent.gif)](https://coherent.global/spark/)

### Building business software is now as easy as creating an Excel worksheet.

- Convert spreadsheets into ready-to-integrate APIs
- Centralize, secure & audit business logic
- Automate complex modeling, testing & business impact simulation """

markdown_app = """# Options Pricing Models

[![ygMrMX.md.png](https://iili.io/ygMrMX.md.png)](https://coherent.global/spark/)

### Building business software is now as easy as creating an Excel worksheet.

- Convert spreadsheets into ready-to-integrate APIs
- Centralize, secure & audit business logic
- Automate complex modeling, testing & business impact simulation"""

st.set_page_config(
    page_title="Coherent Spark Options Pricing",
    page_icon=":rocket:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://coherent.global/contact/',
        'Report a Bug': None,
        'About': markdown_about
    }
)

st.markdown(markdown_app)
# st_player("https://vimeo.com/673532746?embedded=true&source=vimeo_logo&owner=136556090")

# embed Coherent Spark video
components.html(
    """
    <iframe src="https://player.vimeo.com/video/673532746?h=7ce2921baa" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen </iframe>
    """,
    height=360,
)

# User selected model from sidebar 
pricing_method = st.sidebar.radio('Please select option pricing method', options=[model.value for model in OPTION_PRICING_MODEL])

markdown_BSM = """
### Black Scholes Model

- This web app is integrated with Yahoo Finance API and can retrieve the spot price for any ticker.
- Along with the retrieved spot price, the user inputs the remaining variables on the front-end.
- An API call is made to the Coherent Spark service with the above inputs.
- The model outputs including the Call Price, Put Price displayed.

[![ygW9zN.md.png](https://iili.io/ygW9zN.md.png)](https://freeimage.host/i/ygW9zN) """

markdown_MCS = """
### Monte Carlo Simulation Model

- This web app is integrated with Yahoo Finance API and can retrieve the spot price for any ticker.
- Along with the retrieved spot price, the user inputs the remaining variables on the front-end.
- An API call is made to the Coherent Spark service with the above inputs.
- The model outputs including the Call Price, Put Price & Simulation results displayed. """

if pricing_method == OPTION_PRICING_MODEL.BLACK_SCHOLES.value:
    
    st.markdown(markdown_BSM)
    # Parameters for Black-Scholes model
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    sigma = st.slider('Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    
    inputs_dict = {'ticker':ticker, 'strike_price':strike_price, 'risk_free_rate':risk_free_rate, 'sigma':sigma, 'exercise_date':exercise_date}
    inputs_df = pd.DataFrame(inputs_dict, index=[0,])
    
    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for selected ticker
        data = get_historical_data(ticker)
        st.write(data.tail(50))
        fig = px.line(data, y='Adj Close', x=data.index)
        st.plotly_chart(fig, use_container_width=True)
        

        # Formating selected model parameters
        spot_price = Ticker.get_last_price(data, 'Adj Close') 
        risk_free_rate = risk_free_rate / 100
        sigma = sigma / 100
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # Calculating option price
        BSM = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
        options_output = BSM.calculate_option_price('Call Option')

        call_option_price = options_output['callprice']
        put_option_price = options_output['putprice']
        Delta = options_output['Delta']
        Gamma = options_output['Gamma']
        Theta = options_output['Theta']
        Vega = options_output['Vega']
        Rho = options_output['Rho']
        
        outputs_df = pd.DataFrame(options_output, index=[0,])
        outputs_df = outputs_df[['callprice', 'putprice', 'Delta', 'Gamma', 'Theta', 'Vega','Rho']]
        
        concat_df = pd.concat([inputs_df, outputs_df], axis='columns')
        
        # Displaying call/put option price
        st.dataframe(outputs_df)
        history_df = history_df.append(concat_df)
        
        expander = st.expander("See history")
        expander.write(history_df)
        
        

elif pricing_method == OPTION_PRICING_MODEL.MONTE_CARLO.value:
    
    st.markdown(markdown_MCS)
    
    # Parameters for Monte Carlo simulation
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 0)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    sigma = st.slider('Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_simulations = st.slider('Number of simulations', 100, 5000, 100)
    num_of_movements = st.slider('Number of price movement simulations to be visualized ', 0, int(number_of_simulations/10), 100)

    if st.button(f'Calculate option price for {ticker}'):
        # Getting data for selected ticker
        data = get_historical_data(ticker)
        st.write(data.tail())
        fig = px.line(data, y='Adj Close', x=data.index)
        st.plotly_chart(fig, use_container_width=True)

        # Formating simulation parameters
        spot_price = Ticker.get_last_price(data, 'Adj Close') 
        risk_free_rate = risk_free_rate / 100
        sigma = sigma / 100
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # ESimulating stock movements
        MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)

        # Calculating call/put option price
        options_output = MC.calculate_option_price('Call Option')
        
        call_option_price = options_output['CallPrice']
        put_option_price = options_output['PutPrice']
        
        st.subheader(f'Simulation Outputs:')
        
        simulation = pd.DataFrame(options_output['simulation'])
        
        st.dataframe(simulation.head(num_of_movements))

        # Displaying call/put option price
        st.subheader(f'Call option price: ${call_option_price}')
        st.subheader(f'Put option price: ${put_option_price}')

elif pricing_method == OPTION_PRICING_MODEL.BINOMIAL.value:
    # Parameters for Binomial-Tree model
    ticker = st.text_input('Ticker symbol', 'AAPL')
    strike_price = st.number_input('Strike price', 300)
    risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
    sigma = st.slider('Sigma (%)', 0, 100, 20)
    exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))
    number_of_time_steps = st.slider('Number of time steps', 5000, 100000, 15000)

    if st.button(f'Calculate option price for {ticker}'):
         # Getting data for selected ticker
        data = get_historical_data(ticker)
        st.write(data.tail())
        Ticker.plot_data(data, ticker, 'Adj Close')
        st.pyplot()

        # Formating simulation parameters
        spot_price = Ticker.get_last_price(data, 'Adj Close') 
        risk_free_rate = risk_free_rate / 100
        sigma = sigma / 100
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # Calculating option price
        BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps)
        call_option_price = BOPM.calculate_option_price('Call Option')
        put_option_price = BOPM.calculate_option_price('Put Option')

        # Displaying call/put option price
        st.subheader(f'Call option price: {call_option_price}')
        st.subheader(f'Put option price: {put_option_price}')
