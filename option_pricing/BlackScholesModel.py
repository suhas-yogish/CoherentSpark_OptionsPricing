import requests
import numpy as np
from scipy.stats import norm 
import json

# Local package imports
from .base import OptionPricingModel

class BlackScholesModel(OptionPricingModel):
    
    def __init__(self, underlying_spot_price, strike_price, days_to_maturity, risk_free_rate, sigma):
        """
        Initializes variables used in Black-Scholes formula .

        underlying_spot_price: current stock or other underlying spot price
        strike_price: strike price for option cotract
        days_to_maturity: option contract maturity/exercise date
        risk_free_rate: returns on risk-free assets (assumed to be constant until expiry date)
        sigma: volatility of the underlying asset (standard deviation of asset's log returns)
        """
        self.S = underlying_spot_price
        self.K = strike_price
        self.T = days_to_maturity / 365
        self.r = risk_free_rate
        self.sigma = sigma
        
        
    def _calculate_call_option_price(self): 
        """
        Calculates price for call option according to the formula.        
        Formula: S*N(d1) - PresentValue(K)*N(d2)
        """

        url = "https://excel.staging.coherent.global/coherent/api/v3/folders/Microsoft Envision/services/BlackScholes/Execute"

        payload = json.dumps({
          "request_data": {
            "inputs": {
              "ExercisePrice": self.K,
              "RisklessRate": self.r,
              "StdDev": self.sigma,
              "StockPrice": self.S,
              "TimeToExpiry": self.T
            }
          },
          "request_meta": {
            "version_id": "49294d02-b796-4966-8d2f-c76193ebad6b",
            "call_purpose": "Spark - API Tester",
            "source_system": "SPARK",
            "correlation_id": "",
            "requested_output": None,
            "service_category": ""
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
        Calculates price for put option according to the formula.        
        Formula: PresentValue(K)*N(-d2) - S*N(-d1)
        """  
        url = "https://excel.staging.coherent.global/coherent/api/v3/folders/Microsoft Envision/services/BlackScholes/Execute"

        payload = json.dumps({
          "request_data": {
            "inputs": {
              "ExercisePrice": self.K,
              "RisklessRate": self.r,
              "StdDev": self.sigma,
              "StockPrice": self.S,
              "TimeToExpiry": self.T
            }
          },
          "request_meta": {
            "version_id": "4ed3f377-ef3d-488a-b5bd-d2df160be49f",
            "call_purpose": "Spark - API Tester",
            "source_system": "SPARK",
            "correlation_id": "",
            "requested_output": None,
            "service_category": ""
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'x-tenant-name': 'coherent',
          'x-synthetic-key': 'facaae76-30e7-4201-9cc7-683dd3a751c6'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        outputs = json.loads(response.text)['response_data']['outputs']   
        
        return outputs['putprice']
        

    def _calculate_greeks(self): 
        """
        Calculates price for put option according to the formula.        
        Formula: PresentValue(K)*N(-d2) - S*N(-d1)
        """  
        url = "https://excel.staging.coherent.global/coherent/api/v3/folders/Microsoft Envision/services/BlackScholes/Execute"

        payload = json.dumps({
          "request_data": {
            "inputs": {
              "ExercisePrice": self.K,
              "RisklessRate": self.r,
              "StdDev": self.sigma,
              "StockPrice": self.S,
              "TimeToExpiry": self.T
            }
          },
          "request_meta": {
            "version_id": "4ed3f377-ef3d-488a-b5bd-d2df160be49f",
            "call_purpose": "Spark - API Tester",
            "source_system": "SPARK",
            "correlation_id": "",
            "requested_output": None,
            "service_category": ""
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
