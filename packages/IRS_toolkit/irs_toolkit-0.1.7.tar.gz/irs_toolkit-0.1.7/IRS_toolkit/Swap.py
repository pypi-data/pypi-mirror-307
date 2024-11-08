import warnings

import pandas as pd
from scipy.optimize import minimize

from IRS_toolkit import legFix

warnings.filterwarnings("ignore")


class Swap:
    """
    A class that provides various outputs related to swap pricing.


    Args:
        fix_leg (legFix): fixed leg
        float_leg (legFloat): float leg
    """

    def __init__(self, fix_leg, float_leg):
        self.fix_leg = fix_leg
        self.float_leg = float_leg

    def NPV(self, discount_curve, date_valo=None):
        """
        Net present value of the swap

        Args:
            discount_curve (curve): yield curve
            date_valo (date, optional): valuation date. Defaults to None.
            RunningCouv (float, optional): spread. Defaults to 0.00.
            GainGC (float, optional): spread. Defaults to 0.00.

        Returns:
            float: Net present value
        """
        self.fix_leg.discount_cashflow(discount_curve, date_valo)
        self.float_leg.discount_cashflow(discount_curve, date_valo)
        self.NPV_ = self.fix_leg.NPV - self.float_leg.NPV
        self.discount_curve = discount_curve
        return self.NPV_

    def fair_rate(self, date_valo, ImpSchedule=None):
        """
        fair rate of the swap

        Args:
            date_valo (date): date valuation
            ImpSchedule (dataframe) : in case you use imported schedule

        Returns:
            float, float: fair rate, theorical fair rate
        """
        fix_rate = self.fix_leg.fix_rate

        def loss_func(fix_rate):
            leg_fix = legFix.legFix(
                self.fix_leg.nominal,
                self.fix_leg.start_date,
                self.fix_leg.maturity_date,
                fix_rate,
                self.fix_leg.periodicity,
            )
            if ImpSchedule is not None:
                leg_fix.scheduleImp(ImpSchedule)
            else:
                leg_fix.schedule()
            leg_fix.compute_cash_flow(pd.Timestamp(date_valo))
            leg_fix.discount_cashflow(self.float_leg.curve, date_valo)
            return (leg_fix.NPV - self.float_leg.NPV) * (
                leg_fix.NPV - self.float_leg.NPV
            )

        res = minimize(
            loss_func,
            fix_rate,
            method="nelder-mead",
            options={"xatol": 1e-8, "disp": True},
        )
        self.faire_rate = float(res.x)
        self.faire_rate_theory = (
            self.float_leg.NPV
            / (
                self.fix_leg.nominal
                * self.fix_leg.cashflow.iloc[:, 3]
                * self.fix_leg.cashflow.DF
            ).sum()
        )
        return self.faire_rate, self.faire_rate_theory
