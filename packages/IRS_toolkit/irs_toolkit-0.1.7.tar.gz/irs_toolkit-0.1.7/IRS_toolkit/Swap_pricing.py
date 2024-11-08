import pandas as pd

from IRS_toolkit import price_swap, utils


def run(
    date,
    notional_amount,
    start_date,
    maturity_date,
    valuation_date,
    fixed_rate,
    spread,
    ESTR,
    type_=None,
    periodicities=None,
):
    if type_ is None:
        type_=["Forward", "Back"]
    if periodicities is None:
        periodicities=["Annual", "Semi-Annual", "Quarterly", "Monthly"]
    curve_date = date.strftime("%Y-%m-%d")

    curve, curveUp, curveD = price_swap.stressedcurve(curve_date)
    start_date = start_date.strftime("%Y-%m-%d")
    maturity_date = maturity_date.strftime("%Y-%m-%d")
    valuation_date = valuation_date.strftime("%Y-%m-%d")

    new_column1 = [
        "start date",
        "end date",
        "fix Period (days)",
        "fix period days",
        "fix cashflow",
        "fix DCF",
        "DF",
    ]
    new_column2 = [
        "start date",
        "end date",
        "float Period years",
        "float period years",
        "forward_ZC",
        "forward_simple_rate",
        "float cashflow",
        "float DCF",
        "float DF",
    ]
    legfix, legV, SWAP = price_swap.Price_swap(
        curve,
        notional_amount,
        start_date,
        maturity_date,
        fixed_rate / 100,
        valuation_date,
        spread / 10000,
        ESTR,
        utils.PayFrequency(periodicities),
        None,
        type_,
    )
    NPV = SWAP.NPV(curve, valuation_date)
    legfix.cashflow.columns = new_column1
    legfix.cashflow.iloc[
        :,
        [
            0,
            1,
            3,
            4,
            5,
            6,
        ],
    ]

    legV.cashflow.columns = new_column2
    legV.cashflow.iloc[
        :,
        [
            0,
            1,
            3,
            4,
            6,
            7,
        ],
    ]

    legfixU, legVU, swapU = price_swap.Price_swap(
        curveUp,
        notional_amount,
        start_date,
        maturity_date,
        fixed_rate / 100,
        valuation_date,
        spread / 10000,
        ESTR,
        utils.PayFrequency(periodicities),
        None,
        type_,
    )
    NPVU = swapU.NPV(curveUp, valuation_date)
    legfixD, legVD, swapD = price_swap.Price_swap(
        curveD,
        notional_amount,
        start_date,
        maturity_date,
        fixed_rate / 100,
        valuation_date,
        spread / 10000,
        ESTR,
        utils.PayFrequency(periodicities),
        None,
        type_,
    )
    NPVD = swapD.NPV(curveD, valuation_date)
    df_fixed = pd.DataFrame(
        {
            "NPV Fixed leg (€)": legfix.NPV,
            "Fair rate (%)": SWAP.fair_rate(valuation_date)[1] * 100,
            "Fixed Leg DV01 (€) ": utils.DV01(
                SWAP.fix_leg.NPV, swapU.fix_leg.NPV, swapD.fix_leg.NPV
            ),
        }
    )
    NPV_all_in = (
        SWAP.fix_leg.NPV
        - SWAP.float_leg.NPV
        + legfix.spread
        + legV.accrued_coupon_float
    )

    df_swap = pd.DataFrame(
        {
            "NPV of the swap (€) ": NPV,
            "Swap spread (GC & hedging costs) (€)": legfix.spread,
            "Swap DV01 (€)": utils.DV01(NPV, NPVU, NPVD),
        }
    )

    print(SWAP.float_leg.NPV, swapU.float_leg.NPV, swapD.float_leg.NPV)
    df_float = pd.DataFrame(
        {
            "NPV Float leg (€) : ": legV.NPV,
            "Accrued coupon on the float leg (€):": legV.accrued_coupon_float,
            "Float Leg DV01 (€)": utils.DV01(
                SWAP.float_leg.NPV, swapU.float_leg.NPV, swapD.float_leg.NPV
            ),
        }
    )
    return df_fixed, df_swap, df_float
