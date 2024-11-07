from ..._prismcomponent.prismcomponent import _PrismComponent, _PrismDataComponent
from ..._utils import _validate_args, _get_params


__all__ = [
    'holiday',
    'weekend',
    'tradinghour',
]


_data_category = __name__.split(".")[-1]


class _PrismReferenceComponent(_PrismDataComponent, _PrismComponent):
    _component_category_repr = _data_category


class holiday(_PrismReferenceComponent):
    """
    | Detailed holiday information specific to the trading location of each listing.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> holiday = ps.reference.holiday()
        >>> hol.get_data('bigtech', '2010-01-01')
                listingid       date
        0         2587303 2010-01-01
        1         2587303 2010-01-18
        2         2587303 2010-02-15
        3         2587303 2010-04-02
        4         2587303 2010-05-31
                      ...        ...
        21890  1761029585 2030-09-13
        21891  1761029585 2030-10-03
        21892  1761029585 2030-10-09
        21893  1761029585 2030-12-25
        21894  1761029585 2030-12-31
    """
    def __init__(
        self
    ):
        super().__init__()


class weekend(_PrismReferenceComponent):
    """
    | Detailed weekend information specific to the trading location of each listing.
    | Default frequency is aperiodic daily.

    Parameters
    ----------
        None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> we = ps.reference.weekend()
        >>> we.get_data('bigtech', '2010-01-01')
             listingid  weekend  startdate    enddate
        0     20210064        6 1700-01-01 2199-12-31
        1    100667466        6 1700-01-01 2199-12-31
        2     20124021        6 1700-01-01 2199-12-31
        3     34684671        6 1700-01-01 2199-12-31
        4     32517592        6 1700-01-01 2199-12-31
        ..         ...      ...        ...        ...
        147   20219913        7 1700-01-01 2199-12-31
        148   20194944        7 1700-01-01 2199-12-31
        149  112319252        7 1700-01-01 2199-12-31
        150    2622898        7 1700-01-01 2199-12-31
        151  289105086        7 1700-01-01 2199-12-31
    """
    def __init__(
        self
    ):
        super().__init__()


class tradinghour(_PrismReferenceComponent):
    """
    | Detailed trading-hour information specific to the trading location of each listing. Local time, with timezone included.

    Parameters
    ----------
        None

    Returns
    -------
        prism._PrismComponent

    Examples
    --------
        >>> tradinghour = ps.reference.tradinghour()
        >>> tradinghour.get_data('bigtech', '2010-01-01')
             listingid  starthour  startminute  endhour  endminute     pytz_timezone
        0      2587303          9           30       16          0  America/New_York
        1      2588568          9           30       16          0  America/New_York
        2      2590360          9           30       16          0  America/New_York
        3      2613214          9           30       16          0  America/New_York
        4      2621295          9           30       16          0  America/New_York
        ..         ...        ...          ...      ...        ...               ...
        70   664143006          9            0       15         30        Asia/Seoul
        71   698666600          9            0       15         30        Asia/Seoul
        72  1683465366          9           30       16          0  America/New_York
        73  1684108147          9            0       17         30  Europe/Stockholm
        74  1761029585          9            0       15         30        Asia/Seoul
    """
    def __init__(
        self
    ):
        super().__init__()
