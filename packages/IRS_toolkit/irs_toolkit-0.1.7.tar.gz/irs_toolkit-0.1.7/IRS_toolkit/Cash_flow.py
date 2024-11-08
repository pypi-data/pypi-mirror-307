import datetime
import warnings

import pandas as pd
from dateutil.relativedelta import relativedelta

from IRS_toolkit import utils

warnings.filterwarnings("ignore")


class cash_flow:
    """
    cash flows handling
        Args:
            dates (Datframe): dates
            amounts (Dataframe): coupons
    """

    def __init__(self, dates, amounts):
        dates = [utils.str_to_datetime(dt) for dt in dates]
        self.cashflows = pd.DataFrame(
            {"cash_flow_date": dates, "cash_flow_amount": amounts}
        )

    def NPV(self, valuation_date, curve, relative_delta=None):
        """
        Compute the Net present value

        Args:
            valuation_date (date): valuation date
            curve (curve): yield curve

        Returns:
            float: Net present value of future cash flows
        """
        if relative_delta is None:
            relative_delta=relativedelta(days=0)
        self.cashflows["discount_cashflow_amounts"] = 0
        self.cashflows["DF"] = 0

        valuation_date = utils.str_to_datetime(valuation_date)
        valuation_date = valuation_date + datetime.timedelta(days=1)

        for ind, dt in self.cashflows.iterrows():
            if dt.cash_flow_date > valuation_date:
                self.cashflows.loc[ind, "DF"] = 1 / (
                    1
                    + curve.ForwardRates(
                        valuation_date, dt.cash_flow_date, relative_delta
                    )
                ) ** (utils.day_count(valuation_date, dt.cash_flow_date))

        self.cashflows["discount_cashflow_amounts"] = (
            self.cashflows.DF * self.cashflows.cash_flow_amount
        )
        self.NPV = self.cashflows["discount_cashflow_amounts"].sum()
        return self.cashflows["discount_cashflow_amounts"].sum()

    # wighted present value for bonds
    def WPV(self, valuation_date, curve, relative_delta=None):
        """
        Weighted Net present value

        Args:
            valuation_date (date): valuation date
            curve (curve): yield curve

        Returns:
            float: time weightide Net present value of future cash flows
        """
        if relative_delta is None:
            relative_delta=relativedelta(days=0)

        self.cashflows["wdiscount_cashflow_amounts"] = 0
        self.cashflows["DF"] = 0

        valuation_date = utils.str_to_datetime(valuation_date)

        for ind, dt in self.cashflows.iterrows():
            if dt.cash_flow_date > valuation_date:
                self.cashflows.loc[ind, "DF"] = 1 / (
                    1
                    + curve.ForwardRates(
                        valuation_date, dt.cash_flow_date, relative_delta
                    )
                ) ** (utils.day_count(valuation_date, dt.cash_flow_date))

        self.cashflows["wdiscount_cashflow_amounts"] = (
            self.cashflows.DF
            * self.cashflows.cash_flow_amount
            * self.cashflows.cash_flow_date.apply(
                lambda x: utils.day_count(valuation_date, x, "ACT/360")
            )
        )
        self.WPV = (self.cashflows["wdiscount_cashflow_amounts"]).sum()
        return self.cashflows["wdiscount_cashflow_amounts"].sum()
