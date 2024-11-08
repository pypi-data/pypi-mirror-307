from dateutil.relativedelta import relativedelta

from IRS_toolkit import Curve, Swap, legFix, legFloat


def Price_swap(
    curve,
    Nominal,
    start_date,
    maturity_date,
    fixedRate,
    valuation_date,
    spread=0.0,
    spread1=0.0,
    ESTR=None,
    payfrecuency=None,
    Imported_schedule=None,
    type_fill="Back",
    float_start_date=None,
    legFix_date_convention="ACT/360",
    legFloat_date_convention="ACT/360",
    relative_delta=None,
):
    """This function is used to price an interest rate swap ( you need to provide correct parametrs)

    Args:
        curve (curve): yield curve
        Nominal (float): Nominal amount
        start_date (date): start date (for the fixed leg)
        maturity_date (date): maturity date
        fixedRate (float): swap fixed rate
        valuation_date (date): valuation date
        payfrecuency (int, optional): payment coupon period. Defaults to None.
        Imported_schedule (dataframe, optional): imported schedule. Defaults to None.
        type_fill (str, optional): type of filling schedule 'Backward' or 'forward'
        float_start_date (str, optional) : start date of the float leg

    Returns:
        legFix,legFloat,Swap: three main compounents of swap
    """
    if float_start_date is None:
        float_start_date = start_date

    if relative_delta is None:
        relative_delta=relativedelta(days=0)

    legfix = legFix.legFix(
        Nominal,
        start_date,
        maturity_date,
        fixedRate,
        payfrecuency,
        type_fill,
        legFix_date_convention,
    )

    if Imported_schedule is not None:
        Imported_schedule["start_date"] = list(Imported_schedule["start_date"])
        Imported_schedule["end_date"] = list(Imported_schedule["end_date"])

    if Imported_schedule is not None:
        legfix.scheduleImp(Imported_schedule)
    else:
        legfix.schedule(payfrecuency)

    legfix.compute_cash_flow(valuation_date, spread, spread1)

    legfix.discount_cashflow(curve, valuation_date, relative_delta)

    # FLOAT

    legfloat = legFloat.legFloat(
        Nominal,
        float_start_date,
        maturity_date,
        curve,
        payfrecuency,
        type_fill,
        legFloat_date_convention,
        relative_delta,
    )
    if Imported_schedule is not None:
        legfloat.scheduleImp(Imported_schedule)
    else:
        legfloat.schedule(payfrecuency)
    legfloat.compute_cash_flow(valuation_date, ESTR)
    legfloat.discount_cashflow(curve, valuation_date, relative_delta)
    # SWAP
    swap = Swap.Swap(legfix, legfloat)
    return legfix, legfloat, swap


def Curves(curve_data, date_curve, shift=0.0,snowflake_instance=None):
    """This function is made to procvide you with a ZC curve  and shifted curve for a given shift

    Args:
        curve_data (dataframe): yield curve
        date_curve (date): date curve
        shift (float, optional): applied parallel shift. Defaults to 0.0.

    Returns:
        _type_: _description_
    """
    try:

        curve_data_ = curve_data[["Instrument", "Mid_geo"]]
        curve_data_.columns = ["Tenor", "Rate"]
        curve_data_.Rate = curve_data_.Rate + shift / 10000

        curve = Curve.Curve(curve_data_, date_curve,snowflake_instance)
        curve.Bootstrap()

        # up stressed curve
        curve_StressedUp = curve_data.copy()
        curve_StressedUp.Mid_geo = curve_StressedUp.Mid_geo + 0.0001
        curve_data_U = curve_StressedUp[["Instrument", "Mid_geo"]]
        curve_data_U.columns = ["Tenor", "Rate"]
        # curve ZC preprocess
        curveUp = Curve.Curve(curve_data_U, date_curve,snowflake_instance)
        curveUp.Bootstrap()

        # down curve
        curve_StressedDown = curve_data.copy()
        curve_StressedDown.Mid_geo = curve_StressedDown.Mid_geo - 0.0001
        curve_data_D = curve_StressedDown[["Instrument", "Mid_geo"]]
        curve_data_D.columns = ["Tenor", "Rate"]
        # curve ZC preprocess
        curveD = Curve.Curve(curve_data_D, date_curve,snowflake_instance)
        curveD.Bootstrap()
        return curve, curveUp, curveD
    except Exception as e:
        print("provided curve is not compatible : {e}")
