# Standard library imports
import warnings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Third-party imports
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

# Local/application imports
from IRS_toolkit import utils

# Configure warnings
warnings.filterwarnings("ignore")


class Curve:
    """
       A class for handling yield curves used in pricing and preparing
    zero-coupon curves for cash flow computation and discounting.
        Args:
               curve (dataframe): dataframe
               date_curve (date): date curve

        Attributs:
                date : curve date
                df : a dataframe that contains dates and ZC rates and Dfs

        Functions:
                setup() : create the dataframe and interpolate rate
                ForwardRate(begin,end) : compute the forward rate for two giving dates
                Bootstrap() : compute the ZC curve using the formula refer to notion appendix
                monthly_avg_daily() : compute the monthly average of instantaneous forward rates  using spot ZC curve


    """

    def __init__(self, curve=None, date_curve=None, snowflake_instance=None):
        self.date_format = "%Y-%m-%d"

        self.snowflake_instance = snowflake_instance

        if date_curve is None:
            self.date = datetime.now(tz=ZoneInfo("Europe/Paris"))
        else:
            self.date = utils.str_to_datetime(date_curve)

        self.curve = curve

        self.df = self.curve.copy()
        self.interpolated_yield_curve = None
        """    def set_periodicity(self, period):
        self.periodicity = period"""
        self.setup()

    def setup(self):
        Dates = []
        list_tenor = self.curve.iloc[:, 0].tolist()
        for tenor in list_tenor:
            Dates.append(self.date + utils.tenor_to_period(tenor))
        self.df["Date"] = Dates

        self.df.loc[-1] = ["0D", np.nan, self.date]  # adding a row
        self.df.index = self.df.index + 1  # shifting index
        self.df.sort_index(inplace=True)

        self.df.rename(columns={"Rate": "StrippedRates"}, inplace=True)
        self.df["Period"] = (self.df["Date"] - self.date).apply(lambda x: x.days)
        self.df["day_count"] = self.df.apply(
            lambda x: utils.day_count(self.date, x["Date"]), axis=1
        )

    def interpolate_yield_curve(self):
        curve_data_ = self.curve.copy()
        curve_data_["relativedelta"] = curve_data_["Tenor"].apply(
            lambda x: utils.tenor_to_period(x)
        )

        now = self.date

        curve_data_["relative_date"] = curve_data_["relativedelta"].apply(
            lambda x: (now + x)
        )
        curve_data_["Period"] = curve_data_["relative_date"].apply(
            lambda x: (x - now).days
        )

        df = pd.DataFrame({"Period": np.arange(1, max(curve_data_["Period"]) + 1, 1)})
        curve_data_ = df.merge(curve_data_, "left")
        curve_data_["Rate"] = curve_data_["Rate"].astype(float)
        curve_data_["Rate"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        curve_data_["Date"] = curve_data_["Period"].apply(lambda x: now + timedelta(x))
        curve_data_["day_count"] = curve_data_.apply(
            lambda x: utils.day_count(self.date, x["Date"]), axis=1
        )

        curve_data_.loc[-1] = [
            0,
            "0D",
            np.nan,
            relativedelta(months=0),
            self.date,
            self.date,
            0,
        ]  # adding a row
        curve_data_.index = curve_data_.index + 1  # shifting index
        curve_data_.sort_index(inplace=True)
        curve_data_.reset_index(drop=True, inplace=True)
        curve_data_.rename(columns={"Rate": "StrippedRates"}, inplace=True)
        curve_data_ = curve_data_[
            ["day_count", "StrippedRates", "Date", "Period", "Tenor"]
        ]
        self.interpolated_yield_curve = curve_data_

    def ForwardRates(
        self,
        begin,
        end,
        relative_delta=None,
        date_convention="ACT/360",
    ):
        """
        compute forward rates

        Args:
            begin (date): start date
            end (date): end date

        Returns:
            float: forward rate
        """

        if relative_delta is None:
            relative_delta=relativedelta(days=0)

        try:
            # Convert string dates to datetime, if necessary
            begin_date = utils.str_to_datetime(begin) if isinstance(begin, str) else begin
            end_date = utils.str_to_datetime(end) if isinstance(end, str) else end
            end_date = end_date + relative_delta

            # Validation of date ranges
            if end_date < self.date or begin_date >= end_date:
                return None

            # Extract zero-coupon rates for the given dates
            zc_begin = self.df[self.df["Date"] == begin_date.strftime("%Y-%m-%d")]["ZC"]
            zc_end = self.df[self.df["Date"] == end_date.strftime("%Y-%m-%d")]["ZC"]

            if zc_begin.empty:
                return None  # Return None if no ZC rates found for the dates
            if zc_end.empty:
                return None  # Return None if no ZC rates found for the dates

            # Calculate discount factors (DF)
            num = (1 + zc_end.iloc[0]) ** utils.day_count(self.date, end_date)
            den = (1 + zc_begin.iloc[0]) ** utils.day_count(self.date, begin_date)
            result = (num / den) ** (
                1.0 / utils.day_count(begin_date, end_date, date_convention)
            ) - 1

            # Compute forward rate using the formula (DF2/DF1)^(1/delta(t)) - 1
            return result

        except Exception as e:
            print(f"An error occurred while calculating forward rates: {e}")
            return None  # Return a default value or None

    def Bootstrap(
        self, coupon_frequency="quarterly", date_convention="ACT/360", zc_curve=None
    ):
        """
        It Transform the yield curve to a zero-coupon (ZC) curve.

        This function processes the initial curve data to compute zero-coupon rates and discount factors.
        It handles different date calculations based on whether the current day is the first of the month.
        """
        if zc_curve is None:
            zc_curve = self.df.copy()

        coupon_periods = {
            "quarterly": 30 * 4,
            "yearly": 30,
            "monthly": 30 * 12,
            "semi_annual": 30 * 2,
        }[coupon_frequency]
        coupon_frequency_date = {
            "quarterly": 3,  # "3MS",
            "yearly": 12,
            "monthly": 1,
            "semi_annual": 6,
        }[coupon_frequency]

        zc_date = [
            self.date + relativedelta(months=i * coupon_frequency_date)
            for i in range(coupon_periods + 1)
        ]
        zc_curve_before = zc_curve[zc_curve["Date"] < zc_date[1]]
        zc_curve_before["Period"] = (zc_curve_before["Date"] - self.date).apply(
            lambda x: x.days
        )

        zc_curve_before["Coupon_period"] = zc_curve_before["day_count"]

        zc_curve_before["ZC"] = (
            1 + zc_curve_before["StrippedRates"] * zc_curve_before["Coupon_period"]
        ) ** (1 / zc_curve_before["Coupon_period"]) - 1
        zc_curve_before["DF"] = (
            1 / (1 + zc_curve_before["ZC"]) ** (zc_curve_before["Coupon_period"])
        )

        zc_curve_temp = zc_curve[zc_curve["Date"].isin(zc_date[1:])]
        zc_curve_temp.reset_index(drop=True, inplace=True)
        zc_curve_temp["Date_lagg"] = zc_curve_temp["Date"].shift()
        zc_curve_temp["Date_lagg"].fillna(self.date, inplace=True)
        zc_curve_temp["Coupon_period"] = zc_curve_temp.apply(
            lambda x: utils.day_count(x["Date_lagg"], x["Date"], date_convention), axis=1
        )
        zc_curve_temp["DF"] = 1
        for i in range(zc_curve_temp.shape[0]):
            zc_curve_temp.loc[i, "DF"] = (
                1
                - (
                    zc_curve_temp["StrippedRates"][i]
                    * zc_curve_temp["Coupon_period"]
                    * zc_curve_temp["DF"]
                )[:i].sum()
            ) / (
                1
                + zc_curve_temp["StrippedRates"][i] * zc_curve_temp["Coupon_period"][i]
            )
        zc_curve_temp["ZC"] = (1 / zc_curve_temp["DF"]) ** (
            1 / zc_curve_temp["day_count"]
        ) - 1

        zc_curve = pd.concat([zc_curve_before, zc_curve_temp[zc_curve_before.columns]])
        zc_curve.reset_index(inplace=True, drop=True)
        self.df = zc_curve.merge(zc_curve.dropna(), "left")
        dates = pd.DataFrame(
            {
                "Date": pd.date_range(
                    start=self.date,
                    end=self.date + relativedelta(years=30),
                    freq="D",
                ),
            }
        )

        self.df = dates.merge(zc_curve, "left")
        self.df["DF"] = self.df["DF"].astype(float)
        self.df["DF"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        self.df["Period"] = (self.df["Date"] - self.date).apply(lambda x: x.days)
        self.df["day_count"] = self.df.apply(
            lambda x: utils.day_count(self.date, x["Date"], date_convention), axis=1
        )
        self.df["ZC"] = (1 / self.df["DF"]) ** (1 / self.df["day_count"]) - 1
        self.df["StrippedRates"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        self.df.at[0, "DF"] = 1
        self.df.at[0, "Coupon_period"] = 0

    def monthly_avg_daily(
        self, start_date, end_date, frequency="D", relative_delta=None
    ):
        """

        Args:
            start_date (date): start date
            end_date (date): end date

        Returns:
            Dataframe: Monthly average of daily forward rates
        """
        if relative_delta is None:
            relative_delta=relativedelta(days=0)

        timedelta_dict = {
            "1D": relativedelta(day=1),
            "1W": relativedelta(weeks=1),
            "2W": relativedelta(weeks=2),
            "3W": relativedelta(weeks=3),
            "1M": relativedelta(months=1),
            "2M": relativedelta(months=2),
            "3M": relativedelta(months=3),
            "4M": relativedelta(months=4),
            "5M": relativedelta(months=5),
            "6M": relativedelta(months=6),
            "7M": relativedelta(months=7),
            "8M": relativedelta(months=8),
            "9M": relativedelta(months=9),
            "10M": relativedelta(months=10),
            "11M": relativedelta(months=11),
            "1Y": relativedelta(years=1),
            "15M": relativedelta(months=15),
            "18M": relativedelta(months=18),
            "21M": relativedelta(months=21),
            "2Y": relativedelta(years=2),
            "3Y": relativedelta(years=3),
            "4Y": relativedelta(years=4),
            "5Y": relativedelta(years=5),
            "6Y": relativedelta(years=6),
            "7Y": relativedelta(years=7),
            "8Y": relativedelta(years=8),
            "9Y": relativedelta(years=9),
            "10Y": relativedelta(years=10),
            "11Y": relativedelta(years=11),
            "12Y": relativedelta(years=12),
            "15Y": relativedelta(years=15),
            "20Y": relativedelta(years=20),
            "25Y": relativedelta(years=25),
            "30Y": relativedelta(years=30),
        }

        if frequency == "Between Tenor":
            date_list = []
            for tenor in timedelta_dict:
                date_forward = utils.str_to_datetime(start_date) + timedelta_dict[tenor]
                date_list.append(date_forward)
        else:
            date_list = pd.date_range(start_date, end=end_date, freq=frequency)

        foreward_df = pd.DataFrame([date_list[:-1], date_list[1:]]).T
        foreward_df.columns = ["start_date", "end_date"]
        foreward_list = []
        for i, j in zip(date_list[:-1], date_list[1:]):
            foreward_list.append(self.ForwardRates(i, j, relative_delta))
        foreward_df["foreward_ZC"] = foreward_list
        foreward_df["day_count"] = foreward_df.apply(
            lambda x: utils.day_count(x["start_date"], x["end_date"]), axis=1
        )
        foreward_df["foreward_simple"] = foreward_df.apply(
            lambda x: utils.ZC_to_simplerate(x["foreward_ZC"], x["day_count"]), axis=1
        )

        foreward_df = foreward_df.set_index("start_date")
        foreward_df.index = pd.to_datetime(foreward_df.index)

        return foreward_df.groupby(pd.Grouper(freq="M")).mean(), foreward_df

    def Bootstrap_12M_semi_yearly_coupon(self, coupon_frequency="quarterly"):
        """
        Transform the yield curve to a zero-coupon (ZC) curve.

        This function processes the initial curve data to compute zero-coupon rates and discount factors.
        It handles different date calculations based on whether the current day is the first of the month.
        """
        zc_curve = self.df.copy()

        coupon_periods = {
            "quarterly": 29 * 4,
            "yearly": 29,
            "monthly": 29 * 12,
            "semi_annual": 29 * 2,
        }[coupon_frequency]
        coupon_frequency_date = {
            "quarterly": pd.DateOffset(months=3),  # "3MS",
            "yearly": pd.DateOffset(years=1),
            "monthly": pd.DateOffset(months=1),
            "semi_annual": pd.DateOffset(months=6),
        }[coupon_frequency]

        # if self.date.day == 1:
        zc_date1 = pd.date_range(
            self.date.strftime(self.date_format),
            periods=2,
            freq=pd.DateOffset(months=6),
        )

        zc_date2 = pd.date_range(
            (self.date + pd.DateOffset(years=1)).strftime(self.date_format),
            periods=coupon_periods,
            freq=coupon_frequency_date,
        )

        zc_date = zc_date1.append(zc_date2)

        zc_curve_before = zc_curve[zc_curve["Date"] < zc_date[1]]
        zc_curve_before["Period"] = (zc_curve_before["Date"] - self.date).apply(
            lambda x: x.days
        )

        zc_curve_before["Coupon_period"] = zc_curve_before["day_count"]

        zc_curve_before["ZC"] = (
            1 + zc_curve_before["StrippedRates"] * zc_curve_before["Coupon_period"]
        ) ** (1 / zc_curve_before["Coupon_period"]) - 1
        zc_curve_before["DF"] = (
            1 / (1 + zc_curve_before["ZC"]) ** (zc_curve_before["Coupon_period"])
        )

        zc_curve_temp = zc_curve[zc_curve["Date"].isin(zc_date)]
        zc_curve_temp.reset_index(drop=True, inplace=True)
        zc_curve_temp["Date_lagg"] = zc_curve_temp["Date"].shift()
        zc_curve_temp["Date_lagg"].fillna(self.date, inplace=True)
        zc_curve_temp["Coupon_period"] = zc_curve_temp.apply(
            lambda x: utils.day_count(x["Date_lagg"], x["Date"]), axis=1
        )
        zc_curve_temp["DF"] = 1
        for i in range(zc_curve_temp.shape[0]):
            zc_curve_temp.loc[i, "DF"] = (
                1
                - (
                    zc_curve_temp["StrippedRates"][i]
                    * zc_curve_temp["Coupon_period"]
                    * zc_curve_temp["DF"]
                )[:i].sum()
            ) / (
                1
                + zc_curve_temp["StrippedRates"][i] * zc_curve_temp["Coupon_period"][i]
            )
        zc_curve_temp["ZC"] = (1 / zc_curve_temp["DF"]) ** (
            1 / zc_curve_temp["day_count"]
        ) - 1
        zc_curve = pd.concat([zc_curve_before, zc_curve_temp[zc_curve_before.columns]])
        zc_curve.reset_index(inplace=True, drop=True)
        self.df = self.df.merge(zc_curve.dropna(), "left")
        dates = pd.DataFrame(
            {
                "Date": pd.date_range(
                    start=self.date + relativedelta(days=1),
                    end=self.date + relativedelta(years=30),
                    freq="D",
                ),
            }
        )

        self.df = dates.merge(self.df, "left")
        self.df["DF"] = self.df["DF"].astype(float)
        self.df["DF"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        self.df["Period"] = (self.df["Date"] - self.date).apply(lambda x: x.days)
        self.df["day_count"] = self.df.apply(
            lambda x: utils.day_count(self.date, x["Date"]), axis=1
        )
        self.df["ZC"] = (1 / self.df["DF"]) ** (1 / self.df["day_count"]) - 1
        self.df["StrippedRates"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
