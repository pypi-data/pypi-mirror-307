import math
import warnings

import pandas as pd
from dateutil.relativedelta import relativedelta

from IRS_toolkit import Cash_flow, utils

warnings.filterwarnings("ignore")


class legFloat:
    """
    this class compute the float leg of the swap

        Args:
            nominal (float): notionel amount
            start_date (date): start date
            maturity_date (date): end date
            curve (curve): yield curve
            periodicity (int, optional): coupon payment periodicity. Defaults to 3.
            type_fill (str, optional): type of filling schedule. Defaults to "Forward".
    """

    def __init__(
        self,
        nominal,
        start_date,
        maturity_date,
        curve,
        periodicity=3,
        type_fill="Forward",
        date_convention="ACT/360",
        relative_delta=None,
    ):
        self.date_format = "%Y-%m-%d"
        self.nominal = nominal
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.periodicity = periodicity
        self.curve = curve
        self.cashflow = pd.DataFrame()
        self.type_fill = type_fill
        self.accrued_coupon_float = 0
        self.date_convention = date_convention
        if relative_delta is None:
            relative_delta=relativedelta(days=0)
        self.relative_delta = relative_delta

    def schedule(self, freqc=3):
        """
        this function construct the  schedule of float leg

        Args:
            freqc (int, optional): Payment frequency in months. Defaults to 3.

        'Raises:'
            ValueError: if type of fill is not compatible
        """
        delta = relativedelta(
            utils.str_to_datetime(self.maturity_date), utils.str_to_datetime(self.start_date)
        )

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
            lambda x: utils.day_count(x["start_date"], x["end_date"], self.date_convention),
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
            lambda x: utils.day_count(x["start_date"], x["end_date"], self.date_convention),
            axis=1,
        )

        self.cashflow = schedule_data

    def compute_cash_flow(self, date_value, ESTR=None):
        """
        this function computes the float cash flows

        Args:
            date_value (date): used to split the into accrued coupon and rest
        """

        self.cashflow["forward_zc"] = self.cashflow.apply(
            lambda x: self.curve.ForwardRates(
                x["start_date"], x["end_date"], self.relative_delta
            ),
            axis=1,
        )
        # here we want to know which coupon we are computing so that we can split to float coupon and accured coupon

        for i in range(0, len(self.cashflow.end_date), 1):
            if (
                pd.Timestamp(date_value) > list(self.cashflow.start_date)[i]
                and pd.Timestamp(date_value) < list(self.cashflow.end_date)[i]
            ):
                self.cashflow["forward_zc"][self.cashflow.index[i]] = (
                    self.curve.ForwardRates(
                        pd.Timestamp(date_value),
                        list(self.cashflow.end_date)[i],
                        self.relative_delta,
                    )
                )
                self.cashflow.day_count[self.cashflow.index[i]] = utils.day_count(
                    pd.Timestamp(date_value),
                    list(self.cashflow.end_date)[i],
                    self.date_convention,
                )

        self.cashflow["forward_simple_rate"] = self.cashflow.apply(
            lambda x: utils.ZC_to_simplerate(x["forward_zc"], x["day_count"]), axis=1
        )

        self.cashflow["cashflow"] = self.nominal * (
            (1 + self.cashflow.forward_zc) ** (self.cashflow.day_count) - 1
        )

        self.accrued_coupon_float = utils.Accrued_coupon(
            self.curve, self.cashflow, self.nominal, date_value, ESTR
        )

    def discount_cashflow(
        self, discount_curve, date_valo=None, relative_delta=None
    ):
        """
        used to discount future cashflows to the date_valo

        Args:
            discount_curve (curve): yield curve
            date_valo (date, optional): valuation date. Defaults to None.
        """

        if relative_delta is None:
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

        self.NPV = discount_cashflow.NPV + self.accrued_coupon_float
