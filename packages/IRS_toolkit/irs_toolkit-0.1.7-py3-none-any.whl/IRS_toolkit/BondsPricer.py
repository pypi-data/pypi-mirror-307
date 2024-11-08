import warnings
from datetime import datetime, timedelta

import pandas as pd
from dateutil.relativedelta import relativedelta

from IRS_toolkit import Cash_flow, utils

warnings.filterwarnings("ignore")
"""FixedRateBond
    this class compute the float leg of the swap

    legFloat(nominal,start_date,maturity_date,curve,periodicity)

    Attributes
    ----------
    date_format : str
        to set the format using for dates.
    face_value : float
        The notional amount of the bond.
    issue_date : date
        issue date of the the bond.
    maturity_date : date
        maturity date of the bond.
    curve : DataFrame
        ZCcurve that will be used for pricing
    coupon_rate : float
        the coupon rate of the bond
    coupon_frequency: str
        periodicity of payment
    cashflow : DataFrame
        cash flows details.
    NPV : float
        the net present value of the float leg.
    accurad_coupon : float
        the accurad coupon of the bond at the specified
        valuation date
    redemption_rate
        the redemption rate at maturity
    WPV
        Wighted present value (for duration)

    Methods
    -------
    schedule()
        Generates a schedule of payment dates based on
        the specified periodicity.
    import_schedule(Path)
        Imports a payment schedule from a specified file path.
    compute_cash_flow()
        Computes and populates the cash flow details based
        on the payment schedule.
    discount_cashflows(discount_curve)
        Discounts the cash flows using a provided discount curve.


eg:
    c=FixedRateBond('2023-08-01', '2026-08-01',
        1500000000, 0.035, 'ANNUAL', 1)

"""


class FixedRateBond:
    def __init__(
        self,
        issue_date,
        maturity_date,
        face_value,
        coupon_rate,
        coupon_frequency,
        redemption_rate,
    ):
        self.date_format = "%Y-%m-%d"
        self.issue_date = issue_date
        self.maturity_date = maturity_date
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.coupon_frequency = coupon_frequency
        self.redemption_rate = redemption_rate
        self.schedule()
        self.compute_cash_flow()

    def Frequency(self):
        if self.coupon_frequency == "ANNUAL":
            return 12.0
        elif self.coupon_frequency == "SEMI-ANNUAL":
            return 6.0
        elif self.coupon_frequency == "QUARTERLY":
            return 3.0
        elif self.coupon_frequency == "MONTHLY":
            return 1.0
        else:
            raise ValueError("Frequency unknown try : for exemple QUARTERLY'")

    def schedule(self):
        delta = relativedelta(
            datetime.strptime(self.maturity_date, self.date_format),
            datetime.strptime(self.issue_date, self.date_format),
        )
        period = round(
            (delta.years * 12 + delta.months + delta.days / 31) / self.Frequency()
        )
        end = (
            pd.date_range(
                self.maturity_date,
                periods=period,
                freq=pd.offsets.MonthBegin(-self.Frequency()),
            )
            .to_series()
            .sort_index()
            .index
        )
        start = end + pd.offsets.MonthBegin(-self.Frequency())
        self.cashflow = pd.DataFrame({"start_date": start, "end_date": end})
        self.cashflow["start_date"][0] = self.issue_date
        self.cashflow["end_date"][-1] = self.maturity_date
        self.cashflow["Period"] = (
            self.cashflow.end_date - self.cashflow.start_date
        ).apply(lambda x: x.days)
        self.cashflow["day_count"] = self.cashflow.apply(
            lambda x: utils.day_count(x["start_date"], x["end_date"]), axis=1
        )

    def scheduleImp(self, Path):
        schedule_data = []
        schedule_data = pd.read_csv(Path, sep=";", header=0)
        # function to convert str to datetime

        def convert(strg):
            return datetime.strptime(strg, "%d/%m/%Y")

        schedule_data = schedule_data.applymap(convert)
        schedule_data["Period"] = (
            schedule_data.end_date - schedule_data.start_date
        ).apply(lambda x: x.days)
        self.cashflow = schedule_data

    def compute_cash_flow(self):
        self.cashflow["cashflow"] = (
            self.face_value
            * self.coupon_rate
            * self.cashflow.apply(
                lambda x: utils.day_count(x["start_date"], x["end_date"], "ACT/360"), axis=1
            )
        )

        self.cashflow["cashflow"][len(self.cashflow["cashflow"]) - 1] += (
            self.face_value * self.redemption_rate
        )

    def discount_cashflow(self, discount_curve, date_valo_=None):
        dates = [date.strftime(self.date_format) for date in self.cashflow.end_date]
        amounts = self.cashflow.cashflow.to_list()
        discount_cashflow = Cash_flow.cash_flow(dates, amounts)
        if date_valo_:
            date_valo = datetime.strptime(date_valo_, self.date_format)
            A = discount_cashflow.NPV(date_valo_, discount_curve)
            B = discount_cashflow.WPV(date_valo_, discount_curve)
            self.NPV = discount_cashflow.NPV
            last_coupon = self.cashflow[self.cashflow.start_date <= date_valo]
            self.accured_coupon = (
                utils.day_count(last_coupon.start_date.iloc[-1,], date_valo, "ACT/360")
                * self.coupon_rate
                * self.face_value
            )
            self.duration = B / A
        else:
            discount_cashflow.NPV(self.issue_date, discount_curve)
            self.NPV = discount_cashflow.NPV
            self.duration = (
                discount_cashflow.cashflows["discount_cashflow_amounts"]
                * self.cashflow.day_count.cumsum()
            ).sum() / self.NPV
            self.accured_coupon = 0.0

        self.cashflow[["discount_cashflow_amounts", "DF"]] = (
            discount_cashflow.cashflows[["discount_cashflow_amounts", "DF"]]
        )


"""Floaters
    this class compute the float leg of the swap

    legFloat(nominal,start_date,maturity_date,curve,periodicity)

    Attributes
    ----------
    date_format : str
        to set the format using for dates.
    face_value : float
        The notional amount of the bond.
    issue_date : date
        issue date of the the bond.
    maturity_date : date
        maturity date of the bond.
    curve : DataFrame
        ZCcurve that will be used for pricing
    coupon_frequency: str
        periodicity of payment
    cashflow : DataFrame
        cash flows details.
    NPV : float
        the net present value of the float leg.
    accurad_coupon : float
        the accurad coupon of the bond at the specified
        valuation date
    redemption_rate
        the redemption rate at maturity
    WPV
        Wighted present value (for duration)

    Methods
    -------
    schedule()
        Generates a schedule of payment dates based on
        the specified periodicity.
    import_schedule(Path)
        Imports a payment schedule from a specified file path.
    compute_cash_flow()
        Computes and populates the cash flow details based
        on the payment schedule.
    discount_cashflows(discount_curve)
        Discounts the cash flows using a provided discount curve.


eg:
    c=FloatingRateBond('2023-08-01', '2026-08-01',
        1500000000, curve, 'ANNUAL', 1)

"""


class FloatingRateBond:
    def __init__(
        self,
        issue_date,
        maturity_date,
        face_value,
        curve,
        coupon_frequency,
        redemption_rate,
    ):
        self.date_format = "%Y-%m-%d"
        self.issue_date = issue_date
        self.maturity_date = maturity_date
        self.face_value = face_value
        self.curve = curve
        self.coupon_frequency = coupon_frequency
        self.redemption_rate = redemption_rate
        self.schedule()
        self.compute_cash_flow()

    def Frequency(self):
        if self.coupon_frequency == "ANNUAL":
            return 12.0
        elif self.coupon_frequency == "SEMI-ANNUAL":
            return 6.0
        elif self.coupon_frequency == "QUARTERLY":
            return 3.0
        elif self.coupon_frequency == "MONTHLY":
            return 1.0
        else:
            raise ValueError("Frequency unknown try : for exemple 'QUARTERLY'")

    def schedule(self):
        delta = relativedelta(
            datetime.strptime(self.maturity_date, self.date_format),
            datetime.strptime(self.issue_date, self.date_format),
        )
        period = round(
            (delta.years * 12 + delta.months + delta.days / 31) / self.Frequency()
        )
        end = (
            pd.date_range(
                self.maturity_date,
                periods=period,
                freq=pd.offsets.MonthBegin(-self.Frequency()),
            )
            .to_series()
            .sort_index()
            .index
        )
        start = end + pd.offsets.MonthBegin(-self.Frequency())
        self.cashflow = pd.DataFrame({"start_date": start, "end_date": end})
        self.cashflow["start_date"][0] = self.issue_date
        self.cashflow["end_date"][-1] = self.maturity_date
        self.cashflow["Period"] = (
            self.cashflow.end_date - self.cashflow.start_date
        ).apply(lambda x: x.days)
        self.cashflow["day_count"] = self.cashflow.apply(
            lambda x: utils.day_count(x["start_date"], x["end_date"]), axis=1
        )

    def scheduleImp(self, Path):
        schedule_data = []
        schedule_data = pd.read_csv(Path, sep=";", header=0)
        # function to convert str to datetime

        def convert(strg):
            return datetime.strptime(strg, "%d/%m/%Y")

        schedule_data = schedule_data.applymap(convert)
        schedule_data["Period"] = (
            schedule_data.end_date - schedule_data.start_date
        ).apply(lambda x: x.days)
        self.cashflow = schedule_data

    def compute_cash_flow(self):
        """self.cashflow["cashflow"] = (
            self.face_value * self.coupon_rate * self.cashflow.apply(
                lambda x: day_count(x['start_date'], x["end_date"], 'ACT/360'),
                axis=1)
        )"""
        self.cashflow["forward_zc"] = self.cashflow.apply(
            lambda x: self.curve.ForwardRates(x["start_date"], x["end_date"]), axis=1
        )
        self.cashflow["forward_simple_rate"] = self.cashflow.apply(
            lambda x: utils.ZC_to_simplerate(x["forward_zc"], x["day_count"]), axis=1
        )

        self.cashflow["cashflow"] = (
            self.face_value
            * self.cashflow.forward_simple_rate
            * self.cashflow.day_count
        )

        self.cashflow["cashflow"][len(self.cashflow["cashflow"]) - 1] += (
            self.face_value * self.redemption_rate
        )

    def discount_cashflow(self, discount_curve, date_valo_=None):
        dates = [date.strftime(self.date_format) for date in self.cashflow.end_date]
        amounts = self.cashflow.cashflow.to_list()
        discount_cashflow = Cash_flow.cash_flow(dates, amounts)
        if date_valo_:
            date_valo = datetime.strptime(date_valo_, self.date_format)
            A = discount_cashflow.NPV(date_valo_, discount_curve)
            B = discount_cashflow.WPV(date_valo_, discount_curve)
            self.NPV = discount_cashflow.NPV
            self.last_coupon = self.cashflow[self.cashflow.start_date <= date_valo]
            self.next_coupon = self.cashflow[self.cashflow.start_date >= date_valo]
            # this calculation to compute the compounded ester
            ForwardCompounded = 1.0
            step = timedelta(days=1)
            date_range = [
                self.last_coupon.start_date.iloc[-1] + i * step
                for i in range(
                    (date_valo - self.last_coupon.start_date.iloc[-1]).days + 1
                )
            ]
            for i in range(len(date_range) - 1):
                ForwardCompounded *= (
                    1 + self.curve.ForwardRates(date_range[i], date_range[i + 1])
                ) ** (utils.day_count(date_range[i], date_range[i + 1], "ACT/360"))
            ForwardCompounded_ = (
                ForwardCompounded
                ** (
                    1
                    / utils.day_count(
                        self.last_coupon.start_date.iloc[-1], date_valo, "ACT/360"
                    )
                )
                - 1
            )
            self.accured_coupon = (
                utils.day_count(date_valo, self.last_coupon.end_date.iloc[-1], "ACT/360")
                * ForwardCompounded_
                * self.face_value
            )
            self.duration = B / A
        else:
            discount_cashflow.NPV(self.issue_date, discount_curve)
            self.NPV = discount_cashflow.NPV
            self.duration = (
                discount_cashflow.cashflows["discount_cashflow_amounts"]
                * self.cashflow.day_count.cumsum()
            ).sum() / self.NPV

        self.cashflow[["discount_cashflow_amounts", "DF"]] = (
            discount_cashflow.cashflows[["discount_cashflow_amounts", "DF"]]
        )
