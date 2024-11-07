import pytest


@pytest.fixture
def tcmodel_quries(prismstudio):
    # ------------ almgren ------------
    ret = prismstudio.market.close().n_periods_pct_change(1)
    trade = (ret > 0).map({True: 1000000, False: -1000000})
    trade_amount = trade.abs()
    almgren = prismstudio.tcmodel.almgren(trade_amount, 10, 5)

    # ---------- bidaskspred ----------
    bas = prismstudio.tcmodel.bidaskspread()

    return {'almgren': almgren, 'bidaskspread': bas}


@pytest.fixture
def riskmodel_queires(prismstudio):
    qis = prismstudio.riskmodel.qis("M", 252, False)
    return {'qis': qis}