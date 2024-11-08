import IRS_toolkit.Blackscholes as Black


class Swaption:
    def __init__(self):
        return

    def price(self):
        x = Black.Call(
            Stock_price=60, Strike=65, r=0.08, T=0.25, call_price=4, volatility=0.3
        )
        x.price()

        coupon_frequency = 4
        maturity = 30
        number_of_cashflows = coupon_frequency * maturity

        # A=
