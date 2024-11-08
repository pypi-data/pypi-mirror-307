import numpy as np
import scipy.stats as si
from scipy.optimize import fmin


def NORMSDIST(x):
    return si.norm.cdf(x, 0.0, 1.0)


class Call:
    def __init__(
        self, Stock_price=60, Strike=65, r=0.08, T=0.25, call_price=4, volatility=0.0
    ) -> None:
        self.Stock_price = Stock_price
        self.Strike = Strike
        self.r = r
        self.T = T
        self.call_price = call_price
        self.volatility = volatility

    def compute_ImpliedVolatility(self):
        def ImpliedVolatility(s):
            d1 = (
                np.log(self.Stock_price / self.Strike) + (self.r + 0.5 * s**2) * self.T
            ) / (s * np.sqrt(self.T))
            d2 = (
                np.log(self.Stock_price / self.Strike) + (self.r - 0.5 * s**2) * self.T
            ) / (s * np.sqrt(self.T))
            of = (
                self.Stock_price * NORMSDIST(d1)
                - self.Strike * np.exp(-self.r * self.T) * NORMSDIST(d2)
            ) - self.call_price
            val = of**2
            return val

        return fmin(ImpliedVolatility, 1)

    def price(self):
        d1 = (
            np.log(self.Stock_price / self.Strike)
            + (self.r + 0.5 * self.volatility**2) * self.T
        ) / (self.volatility * np.sqrt(self.T))
        d2 = (
            np.log(self.Stock_price / self.Strike)
            + (self.r - 0.5 * self.volatility**2) * self.T
        ) / (self.volatility * np.sqrt(self.T))
        BlackScholesCall = self.Stock_price * NORMSDIST(d1) - self.Strike * np.exp(
            -self.r * self.T
        ) * NORMSDIST(d2)
        self.call_price = BlackScholesCall
        return BlackScholesCall


class Put:
    def __init__(
        self,
        Stock_price=60,
        Strike=65,
        r=0.08,
        T=0.25,
        put_price=4,
        volatility=0.0,
    ) -> None:
        self.Stock_price = Stock_price
        self.Strike = Strike
        self.r = r
        self.T = T
        self.put_price = put_price
        self.volatility = volatility

    def compute_ImpliedVolatility(self):
        def ImpliedVolatility(s):
            d1 = (
                np.log(self.Stock_price / self.Strike) + (self.r + 0.5 * s**2) * self.T
            ) / (s * np.sqrt(self.T))
            d2 = (
                np.log(self.Stock_price / self.Strike) + (self.r - 0.5 * s**2) * self.T
            ) / (s * np.sqrt(self.T))
            of = (
                self.Strike * np.exp(-self.r * self.T) * NORMSDIST(-d2)
                - self.Stock_price * NORMSDIST(-d1)
            ) - self.put_price
            val = of**2
            return val

        return fmin(ImpliedVolatility, 1)

    def price(self):
        d1 = (
            np.log(self.Stock_price / self.Strike)
            + (self.r + 0.5 * self.volatility**2) * self.T
        ) / (self.volatility * np.sqrt(self.T))
        d2 = (
            np.log(self.Stock_price / self.Strike)
            + (self.r - 0.5 * self.volatility**2) * self.T
        ) / (self.volatility * np.sqrt(self.T))
        BlackScholesPut = self.Strike * np.exp(-self.r * self.T) * NORMSDIST(
            -d2
        ) - self.Stock_price * NORMSDIST(-d1)
        self.put_price = BlackScholesPut
        return BlackScholesPut
