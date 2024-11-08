#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def clims(year_from, year_to, period_len=30) -> pd.DataFrame:
    """Calculate DataFrame of climate averaging periods.

    NOAA-like periods such that the periods are like centred moving averages,
    except they are held constant for 5 years.

    Parameters
    ----------
        year_from : int
            Year from.
        year_to : int
           Year to. Assumed to be the current year so modifies periods such
           no 'future' data is needed.
        period_len : int, optional
           Length of averaging periods in years. Must be multiple of 10.
           Defaults to 30 years, the NOAA standard.

    Returns
    -------
        periods : DataFrame
            Climate averaging periods.
    """

    if period_len % 10 != 0:
        print('period_len must be a multiple of 10')
        return None

    delta = period_len // 2

     # All years this function is likely to be run for (can be extended)
    all_years = np.arange(1800, 2101, dtype=int)

    # Select year range required and integer divide by 5 to chunk
    years = pd.Index(np.arange(year_from, year_to+1, dtype=int), name='years')
    chunks = (all_years-1)//5

    # Calculate N-year windows
    periods_all = pd.DataFrame({'year_from': chunks*5 - delta + 1,
                                'year_to': chunks*5 + delta}, index=all_years)

    # Modify periods such that only data available in present year-1 used
    periods = periods_all.where(periods_all['year_to'] < year_to - 1
                               ).ffill().astype(int).reindex(years)
    return periods
