# Third party imports
import requests
import numpy as np
from scipy.stats import norm 
import json

# Local package imports
from .base import OptionPricingModel


class MonteCarloPricing(OptionPricingModel):
    """ 
    Class implementing calculation for European option price using Monte Carlo Simulation.
    We simulate underlying asset price on expiry date using random stochastic process - Brownian motion.
    For the simulation generated prices at maturity, we calculate and sum up their payoffs, average them and discount the final value.
    That value represents option price
    """

    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations):
        """
        Initializes variables used in Black-Scholes formula .

        underlying_spot_price: current stock or other underlying spot price
        strike_price: strike price for option cotract
        days_to_maturity: option contract maturity/exercise date
        risk_free_rate: returns on risk-free assets (assumed to be constant until expiry date)
        sigma: volatility of the underlying asset (standard deviation of asset's log returns)
        number_of_simulations: number of potential random underlying price movements 
        """
        # Parameters for Brownian process
        self.S_0 = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma 

        # Parameters for simulation
        self.N = number_of_simulations
        self.num_of_steps = days_to_maturity
        self.dt = self.T / self.num_of_steps


    def _calculate_call_option_price(self): 
        """
        Call option price calculation. Calculating payoffs for simulated prices at expiry date, summing up, averiging them and discounting.   
        Call option payoff (it's exercised only if the price at expiry date is higher than a strike price): max(S_t - K, 0)
        """

        url = "https://excel.staging.coherent.global/coherent/api/v3/folders/Microsoft Envision/services/MonteCarloSimulation/Execute"

        payload = json.dumps({
          "request_data": {
            "inputs": {
              "daystoexpire": self.num_of_steps,
              "numSimulations": self.N,
              "historicvolatility": self.sigma,
              "price": self.S_0,
              "riskfreerate": self.r,
              "strikeprice": self.K
            }
          },
          "request_meta": {
            "version_id": "4d5274e8-9b0d-49f6-873e-536537b237be",
            "call_purpose": "Spark - API Tester",
            "source_system": "SPARK",
            "correlation_id": "",
            "requested_output": None,
            "service_category": "",
            "compiler_type": "Type3"
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'x-tenant-name': 'coherent',
          'x-synthetic-key': 'facaae76-30e7-4201-9cc7-683dd3a751c6'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        outputs = json.loads(response.text)['response_data']['outputs']
        
        return outputs

    def _calculate_put_option_price(self): 
        """
        Put option price calculation. Calculating payoffs for simulated prices at expiry date, summing up, averiging them and discounting.   
        Put option payoff (it's exercised only if the price at expiry date is lower than a strike price): max(K - S_t, 0)
        """
        
        url = "https://excel.staging.coherent.global/coherent/api/v3/folders/Microsoft Envision/services/MonteCarloSimulation/Execute"

        payload = json.dumps({
          "request_data": {
            "inputs": {
              "daystoexpire": self.num_of_steps,
              "historicvolatility": self.sigma,
              "numSimulations": self.N,
              "price": self.S_0,
              "riskfreerate": self.r,
              "strikeprice": self.K
            }
          },
          "request_meta": {
            "version_id": "4d5274e8-9b0d-49f6-873e-536537b237be",
            "call_purpose": "Spark - API Tester",
            "source_system": "SPARK",
            "correlation_id": "",
            "requested_output": None,
            "service_category": "",
            "compiler_type": "Type3"
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'x-tenant-name': 'coherent',
          'x-synthetic-key': 'facaae76-30e7-4201-9cc7-683dd3a751c6'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        outputs = json.loads(response.text)['response_data']['outputs']
        
        return outputs
