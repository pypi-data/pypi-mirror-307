import math
import warnings
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from IRS_toolkit import Cash_flow, utils

warnings.filterwarnings("ignore")


class legFix:
    """
    this class compute the float leg of the swap

        Args:
            nominal (float): notionel amount
            start_date (date): start date
            maturity_date (date): end date
            fix_rate (float): swap fixed rate
            periodicity (int, optional): coupon payment periodicity. Defaults to 3.
            type_fill (str, optional): type of filling schedule. Defaults to "Forward".
    """

    def __init__(
        self,
        nominal,
        start_date,
        maturity_date,
        fix_rate,
        periodicity=3,
        type_fill="Forward",
        date_convention="ACT/360",
    ):
        self.date_format = "%Y-%m-%d"
        self.nominal = nominal
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.fix_rate = fix_rate
        self.periodicity = periodicity
        self.cashflow = pd.DataFrame()
        self.type_fill = type_fill
        self.accrued_coupon_fix = 0
        self.spread = 0
        self.date_convention = date_convention

    def schedule(self, freqc=3):
        """
        construct the schedule of the fixed leg

        Args:
            freqc (int, optional): frequency of coupon payment in month. Defaults to 3.
        """

        def convert(strg):
            if type(strg) is str:
                if strg == "NaT":
                    return "N/A"
                return datetime.strptime(strg, self.date_format)
            else:
                return strg

        delta = relativedelta(convert(self.maturity_date), convert(self.start_date))
        months = (delta.years * 12 + delta.months + delta.days / 30) / freqc
        period = math.ceil(months)

        if self.type_fill == "Forward":
            start_range = pd.date_range(
                start=self.start_date, periods=period, freq=pd.DateOffset(months=freqc)
            )

            end_range = start_range + pd.DateOffset(months=freqc)

            self.cashflow = pd.DataFrame(
                {"start_date": start_range, "end_date": end_range}
            )

            for i in range(1, len(self.cashflow), 1):
                if self.cashflow["start_date"][i] != self.cashflow["end_date"][i - 1]:
                    self.cashflow["start_date"][i] = self.cashflow["end_date"][i - 1]

        elif self.type_fill == "Back":
            end_range = pd.date_range(
                end=self.maturity_date, periods=period, freq=pd.DateOffset(months=freqc)
            )

            start_range = end_range - pd.DateOffset(month=freqc)

            self.cashflow = pd.DataFrame(
                {"start_date": start_range, "end_date": end_range}
            )

            for i in range(1, len(self.cashflow), 1):
                if self.cashflow["start_date"][i] != self.cashflow["end_date"][i - 1]:
                    self.cashflow["start_date"][i] = self.cashflow["end_date"][i - 1]
        else:
            raise ValueError("Error: Not an available option.")

        self.cashflow["start_date"].iloc[0] = pd.Timestamp(self.start_date)
        self.cashflow["end_date"].iloc[-1] = pd.Timestamp(self.maturity_date)

        self.cashflow["Period"] = (
            self.cashflow.end_date - self.cashflow.start_date
        ).apply(lambda x: x.days)

        self.cashflow["day_count"] = self.cashflow.apply(
            lambda x: utils.day_count(
                x["start_date"], x["end_date"], self.date_convention
            ),
            axis=1,
        )

    def scheduleImp(self, Path):
        """
        the function is an alternative of schedule function it is used to
        import the schedule

        Args:
            Path (csv): a given excel files
        """

        schedule_data = Path
        schedule_data = schedule_data.applymap(utils.str_to_datetime)
        schedule_data["Period"] = (
            schedule_data.end_date - schedule_data.start_date
        ).apply(lambda x: x.days)
        schedule_data["day_count"] = schedule_data.apply(
            lambda x: utils.day_count(
                x["start_date"], x["end_date"], self.date_convention
            ),
            axis=1,
        )

        self.cashflow = schedule_data

    def compute_cash_flow(self, date_value, spreadHC=0.0, spreadGC=0.0):
        """
        this function compute the float cash flows

        """
        self.cashflow["cashflow"] = (
            self.nominal * self.fix_rate * self.cashflow.day_count
        )
        """        for i in range(0, len(self.cashflow.end_date) - 1, 1):
            if (
                pd.Timestamp(date_value) > self.cashflow.start_date[i]
                and pd.Timestamp(date_value) < self.cashflow.end_date[i]
            ):
                self.cashflow.day_count[i] = day_count(
                    pd.Timestamp(date_value), self.cashflow.end_date[i]
                )
                self.cashflow["cashflow"][i] = (
                    self.nominal * self.fix_rate * self.cashflow.day_count[i]
                )"""

        coupon_period = utils.day_count(
            utils.previous_coupon_date(self.cashflow, pd.Timestamp(date_value)),
            pd.Timestamp(date_value),
            self.date_convention,
        )
        self.accrued_coupon_fix = self.nominal * self.fix_rate * coupon_period
        self.spreadHC = utils.Spread_amount(
            self.cashflow, self.nominal, spreadHC, date_value
        )
        self.spreadGC = utils.Spread_amount(
            self.cashflow, self.nominal, spreadGC, date_value
        )
        self.spread = self.spreadGC + self.spreadHC

    def discount_cashflow(
        self, discount_curve, date_valo=None, relative_delta=None
    ):
        """
        used to discount future cashflows to the date_valo

        Args:
            discount_curve (curve): yield curve
            date_valo (date, optional): valuation date. Defaults to None.
        """
        relative_delta=relativedelta(days=0)

        dates = [date.strftime(self.date_format) for date in self.cashflow.end_date]

        amounts = self.cashflow.cashflow.to_list()

        discount_cashflow = Cash_flow.cash_flow(dates, amounts)

        if date_valo:
            discount_cashflow.NPV(date_valo, discount_curve, relative_delta)
        else:
            discount_cashflow.NPV(discount_curve.date, discount_curve, relative_delta)
        self.cashflow[["discount_cashflow_amounts", "DF"]] = (
            discount_cashflow.cashflows[["discount_cashflow_amounts", "DF"]].values
        )
        self.NPV = discount_cashflow.NPV
