# How often do major short squeezes happen?
## Introduction
This directory contains the results of a short squeeze analysis that tries to answer the question:
> How often do major short squeezes happen?

In order to answer the question we look into rapid price increases of stocks currently
listed on the NYSE, NASDAQ and AMEX. We assume that a major short squeeze can have only taken place
if a major price increase can be observed. Since a rapid price increase does not imply
a short squeeze has taken place, we can only use this to get a lower bound on how many major
short squeezes could have taken place at maximum on the major US stock exchanges.

This document summarizes our findings and describes how the results were computed.

## What is the content of this directory?
 - **README.md**:
   It is the file you are reading right now.
 - **create_filtered_tickers.sh**:
   A script file which runs the filtering steps of this analysis. It is part of the workflow to reproduce the results
   as described below.
 - **transform_ljson_to_csv.py**:
   A helper script which is used by **create_filtered_tickers.sh**. You don't have to worry about this.
 - **unfiltered_ticker_counts.csv**:
   A csv file which contains the ticker counts that were originally downloaded without applying any filters.
   The counts are sliced per exchange and min market cap (in million).
 - **$EX_min_$MMC_multi_$PIM_days_$CTD.csv**:
   Each file with this naming schema contains aggregated data about the tickers that satisfied one of the
   short squeeze filters applied in this study.
   
## On which dimensions did we analyse the tickers?
- $EX - Exchange the ticker is listed on: NYSE, NASDAQ, AMEX
- $MMC - Min market cap (state: 06/06/2021): 1000m, 100m, 10m
- $PIM - Price increase multiplier we need to observe to count as a major short squeeze: 2 (= double price), 3, 5
- $CTD - Maximum consecutive trading days in which we need to observe the increase: 5, 10

For each combination of the above dimensions we create a own list of tickers (=one file per list)
with the following information for each ticker:
- Ticker symbol
- Adjusted close price (that triggered the ticker to satisfy the requirement)
- Date (of the close price when the multiplier threshold was exceeded)
- Percentage increase (between lowest adjusted close price of the consecutive days and the adjusted close price;
  This value reflects only the increase the first day the threshold was exceeded. It may not be the maximum increase
  the ticker has ever had.)

## Why did we use adjusted closing prices?
We assume that major short squeezes take multiple days and must thus be observable over multiple days.
The intention of measuring only a single price metric is to avoid any additional noise coming from
using multiple metrics. By using the closing price we want to reduce the likelihood of labeling
high volatility as a short squeeze. We choose the adjusted closing prices in hopes that these are the
most standardized price labels possible across the dataset.

## Which date range did we use?
We used the maximum available dat range for each ticker provided by yahoo finance API.

## Collected data

Price increase for US stocks across NYSE, NASDAQ and AMEX:

| Min Market Cap | Price increase multiplier (2 = 100% increase, 3 = 200%, 5=400%) | Consecutive days | Stock count | Relative to all stocks from exchange with min market cap |
| :------------- | :-------------------------------------------------------------: | :--------------- | :---------- | -------------------------------------------------------: |
| 1000           |                                5                                | 5                | 7           |                                                    0.89% |
| 1000           |                                2                                | 5                | 54          |                                                    6.90% |
| 100            |                                5                                | 5                | 32          |                                                    1.24% |
| 100            |                                2                                | 5                | 326         |                                                   12.68% |
| 10             |                                5                                | 5                | 121         |                                                    3.39% |
| 10             |                                2                                | 5                | 916         |                                                   25.64% |


More detailed overview over of price increase for US stocks:

| Exchange | Min Market Cap | Price increase multiplier (2 = 100% increase, 3 = 200%, 5=400%) | Consecutive days | Stock count | Relative to all stocks from exchange with min market cap |
| :------- | :------------: | :-------------------------------------------------------------- | :--------------- | ----------: | -------------------------------------------------------: |
| amex     |      1000      | 2                                                               | 10               |           1 |                                                   50.00% |
| amex     |      1000      | 2                                                               | 5                |           1 |                                                   50.00% |
| amex     |      1000      | 3                                                               | 10               |           1 |                                                   50.00% |
| amex     |      1000      | 3                                                               | 5                |           1 |                                                   50.00% |
| amex     |      1000      | 5                                                               | 5                |           0 |                                                    0.00% |
| amex     |      100       | 2                                                               | 10               |           9 |                                                   45.00% |
| amex     |      100       | 2                                                               | 5                |           7 |                                                   35.00% |
| amex     |      100       | 3                                                               | 10               |           4 |                                                   20.00% |
| amex     |      100       | 3                                                               | 5                |           3 |                                                   15.00% |
| amex     |      100       | 5                                                               | 10               |           1 |                                                    5.00% |
| amex     |      100       | 5                                                               | 5                |           1 |                                                    5.00% |
| amex     |       10       | 2                                                               | 10               |          70 |                                                   49.30% |
| amex     |       10       | 2                                                               | 5                |          62 |                                                   43.66% |
| amex     |       10       | 3                                                               | 10               |          34 |                                                   23.94% |
| amex     |       10       | 3                                                               | 5                |          25 |                                                   17.61% |
| amex     |       10       | 5                                                               | 10               |          16 |                                                   11.27% |
| amex     |       10       | 5                                                               | 5                |          11 |                                                    7.75% |
| nasdaq   |      1000      | 2                                                               | 10               |          41 |                                                   16.33% |
| nasdaq   |      1000      | 2                                                               | 5                |          25 |                                                    9.96% |
| nasdaq   |      1000      | 3                                                               | 10               |           9 |                                                    3.59% |
| nasdaq   |      1000      | 3                                                               | 5                |           5 |                                                    1.99% |
| nasdaq   |      1000      | 5                                                               | 10               |           1 |                                                    0.40% |
| nasdaq   |      1000      | 5                                                               | 5                |           1 |                                                    0.40% |
| nasdaq   |      100       | 2                                                               | 10               |         271 |                                                   25.16% |
| nasdaq   |      100       | 2                                                               | 5                |         196 |                                                   18.20% |
| nasdaq   |      100       | 3                                                               | 10               |          97 |                                                    9.01% |
| nasdaq   |      100       | 3                                                               | 5                |          63 |                                                    5.85% |
| nasdaq   |      100       | 5                                                               | 10               |          29 |                                                    2.69% |
| nasdaq   |      100       | 5                                                               | 5                |          22 |                                                    2.04% |
| nasdaq   |       10       | 2                                                               | 10               |         810 |                                                   75.21% |
| nasdaq   |       10       | 2                                                               | 5                |         618 |                                                   57.38% |
| nasdaq   |       10       | 3                                                               | 10               |         358 |                                                   33.24% |
| nasdaq   |       10       | 3                                                               | 5                |         262 |                                                   24.33% |
| nasdaq   |       10       | 5                                                               | 10               |         119 |                                                   11.05% |
| nasdaq   |       10       | 5                                                               | 5                |          91 |                                                    8.45% |
| nyse     |      1000      | 2                                                               | 10               |          49 |                                                    9.25% |
| nyse     |      1000      | 2                                                               | 5                |          28 |                                                    5.28% |
| nyse     |      1000      | 3                                                               | 10               |          15 |                                                    2.83% |
| nyse     |      1000      | 3                                                               | 5                |           9 |                                                    1.70% |
| nyse     |      1000      | 5                                                               | 10               |           6 |                                                    1.13% |
| nyse     |      1000      | 5                                                               | 5                |           6 |                                                    1.13% |
| nyse     |      100       | 2                                                               | 10               |         195 |                                                   13.23% |
| nyse     |      100       | 2                                                               | 5                |         123 |                                                    8.34% |
| nyse     |      100       | 3                                                               | 10               |          45 |                                                    3.05% |
| nyse     |      100       | 3                                                               | 5                |          23 |                                                    1.56% |
| nyse     |      100       | 5                                                               | 10               |          11 |                                                    0.75% |
| nyse     |      100       | 5                                                               | 5                |           9 |                                                    0.61% |
| nyse     |       10       | 2                                                               | 10               |         358 |                                                   15.21% |
| nyse     |       10       | 2                                                               | 5                |         236 |                                                   10.03% |
| nyse     |       10       | 3                                                               | 10               |          84 |                                                    3.57% |
| nyse     |       10       | 3                                                               | 5                |          48 |                                                    2.04% |
| nyse     |       10       | 5                                                               | 10               |          23 |                                                    0.98% |
| nyse     |       10       | 5                                                               | 5                |          19 |                                                    0.81% |


All tickers with a minimum market cap of 10 million (today) that multiplied their price >5 times over 5 consecutive trading days:

| Ticker | Date (the increase was observed) | Adjusted Close Price (at given date) | Price increase (between lowest price of the previous 5 trading days and price at given date) |
| :----: | :------------------------------: | :----------------------------------: | :------------------------------------------------------------------------------------------: |
|  ACCD  |            2020-07-02            |              29.700001               |                                      54.000001818181815                                      |
|  AGRX  |            2019-11-05            |                 2.4                  |                                       6.46900269541779                                       |
|  AGX   |            1995-10-13            |               5.517584               |                                      32.00009279450657                                       |
|  ALT   |            2018-09-20            |                26.23                 |                                      6.142857142857143                                       |
|  AMC   |            2021-01-27            |                 19.9                 |                                       6.7003367003367                                        |
|  AMEH  |            2009-04-13            |                 17.0                 |                                             8.5                                              |
|  AMPY  |            2016-10-24            |              18.869616               |                                      226.49881166726686                                      |
|  AMRN  |            1998-12-02            |                83.75                 |                                      5.583333333333333                                       |
|  APVO  |            2020-11-09            |              32.740002               |                                      5.196825714285714                                       |
|  AREC  |            2018-03-01            |                 1.1                  |                                             22.0                                             |
|  ARWR  |            1995-12-07            |                650.0                 |                                      5.319149066754887                                       |
|  ASLN  |            2019-11-27            |                 2.32                 |                                      5.484633569739953                                       |
|  ATHX  |            2009-12-22            |                 5.55                 |                                      5.6060606060606055                                      |
|  ATNM  |            2013-03-20            |                225.0                 |                                             5.0                                              |
|  AWH   |            2009-05-12            |                 0.25                 |                                      8.333333333333334                                       |
|  AYTU  |            2008-10-22            |               591219.5               |                                      5.049999846516928                                       |
|  BLNK  |            2010-04-09            |                1625.0                |                                      12.264150943396226                                      |
|  BNGO  |            2019-10-16            |                 2.85                 |                                      5.480769230769231                                       |
|  BTBT  |            2021-01-04            |                29.27                 |                                      5.055267702936097                                       |
|  BYRN  |            2016-04-04            |                 2.7                  |                                             5.4                                              |
|  CASS  |            1996-07-01            |               2.526119               |                                      32.45312760955305                                       |
|  CODX  |            2020-02-27            |                15.96                 |                                      5.232786885245902                                       |
|  COMS  |            2010-11-01            |             1820.160034              |                                      9.677419226892592                                       |
|  CRIS  |            2020-12-09            |                 7.69                 |                                      5.340277777777779                                       |
|  CRMT  |            1993-06-17            |                3.375                 |                                             5.4                                              |
|  CTIC  |            2009-03-26            |                195.0                 |                                      5.416666666666667                                       |
|  CTRM  |            2021-05-28            |                 3.05                 |                                      8.495821727019498                                       |
|  CVE   |            2009-12-09            |              17.986408               |                                      117.4998562805404                                       |
|  DRIO  |            2019-11-18            |                 4.3                  |                                      21.07843137254902                                       |
|  DUO   |            2020-06-09            |              47.060001               |                                      5.0640267943613475                                      |
|  DVAX  |            2008-12-17            |                 17.4                 |                                      6.959999999999999                                       |
|  ENZ   |            1991-12-04            |               3.997582               |                                      5.000002501513416                                       |
|  EPM   |            2002-05-10            |              12.903817               |                                      5.624999782041245                                       |
|  ESTE  |            1995-03-30            |                 0.5                  |                                             5.0                                              |
|  EXPR  |            2021-01-27            |                 9.55                 |                                      8.232758620689657                                       |
|  EYES  |            2021-03-08            |                11.77                 |                                       8.23076923076923                                       |
|  FSTX  |            2020-11-27            |                6.995                 |                                      5.7809917355371905                                      |
|  GBNH  |            2021-02-08            |                15.473                |                                      5.381913043478261                                       |
|  GBOX  |            2018-05-22            |                 2.4                  |                                      6.666666666666667                                       |
|  GEVO  |            2018-06-19            |                 19.5                 |                                      5.555555555555556                                       |
|  GIII  |            1998-12-29            |               2.958333               |                                      5.259258666666667                                       |
|  GME   |            2021-01-27            |              347.51001               |                                      8.883180441799091                                       |
|  GNPX  |            2020-01-22            |                 1.9                  |                                      5.571847507331378                                       |
|  GTX   |            2021-05-12            |                 5.77                 |                                       9.84641638225256                                       |
|  HGEN  |            2015-11-19            |                 52.0                 |                                      11.555555555555555                                      |
|  HROW  |            2011-11-22            |                 6.0                  |                                             5.0                                              |
|  HUBB  |            1994-10-31            |              12.428244               |                                      9.859311622859382                                       |
|  ICPT  |            2014-01-10            |              445.829987              |                                      6.578574689917723                                       |
|  IDEX  |            2008-12-17            |                18.75                 |                                             5.0                                              |
|  IMMP  |            2015-05-20            |              19.700001               |                                      11.819998236000353                                      |
|  INPX  |            2020-01-03            |                20.475                |                                      5.986842105263158                                       |
|  IOVA  |            2013-07-25            |                 10.0                 |                                             5.0                                              |
|  IPA   |            2002-07-08            |                 12.0                 |                                             8.0                                              |
|  KODK  |            2020-07-29            |              33.200001               |                                      15.809524285714286                                      |
|  KOSS  |            2021-01-27            |                 58.0                 |                                      17.365269461077844                                      |
|  KRTX  |            2019-11-18            |                 96.0                 |                                       5.64373897707231                                       |
|  KXIN  |            2020-10-19            |                 8.15                 |                                      15.092592592592592                                      |
|  LFVN  |            1997-05-01            |              47.599998               |                                      6.666666386554622                                       |
|  LMNL  |            2010-04-09            |                159.0                 |                                            9.9375                                            |
|  LOV   |            2017-11-06            |                 10.0                 |                                       10.1010101010101                                       |
|  LRMR  |            2020-05-29            |                 12.3                 |                                      14.089347079037802                                      |
| LTRPB  |            2020-04-15            |              34.689999               |                                      9.104986614173228                                       |
|   LX   |            2017-12-26            |                14.39                 |                                      13.448598130841122                                      |
|  MCF   |            1998-04-23            |               0.943497               |                                      10.666647824268255                                      |
|  MCRB  |            2020-08-10            |              22.700001               |                                      5.550122493887531                                       |
|  MDVL  |            2010-07-29            |                1470.0                |                                      8.781362321912628                                       |
|  MFA   |            2020-03-27            |               1.569659               |                                      5.166666118069156                                       |
|  MMAC  |            2009-01-06            |                 4.6                  |                                      5.749999999999999                                       |
|  MNMD  |            2019-08-13            |                 0.05                 |                                             5.0                                              |
|  MTA   |            2010-01-12            |              15.997301               |                                      14.695662119122925                                      |
|  MTBC  |            2017-05-01            |                 2.4                  |                                      5.714285714285714                                       |
|  MUX   |            1991-12-24            |               0.121154               |                                      5.166702204784852                                       |
|  MVIS  |            2020-05-05            |                 1.3                  |                                             5.2                                              |
|  NAKD  |            2018-06-20            |                850.0                 |                                             6.25                                             |
|  NBEV  |            2018-09-20            |                 7.85                 |                                             5.0                                              |
|  NCTY  |            2021-01-07            |                 17.1                 |                                      5.000000000000001                                       |
|   NG   |            2008-12-17            |                 2.41                 |                                      5.020833333333334                                       |
|  NLTX  |            2015-08-07            |                10.42                 |                                      6.058139534883721                                       |
|  NUAN  |            1999-11-15            |               8.603896               |                                      5.129032738813787                                       |
|  NVR   |            1993-10-01            |                10.25                 |                                      27.333333333333332                                      |
|  OAS   |            2020-11-20            |              30.802532               |                                      258.5493217835079                                       |
|  OCGN  |            2020-12-23            |                 2.6                  |                                      8.843537414965986                                       |
|  OEG   |            1999-10-29            |               23.4375                |                                             5.0                                              |
|  OPBK  |            2010-01-26            |               3.250312               |                                      8.750005384101824                                       |
|  ORGO  |            2019-01-09            |              82.349998               |                                      8.113300295566502                                       |
|  ORLA  |            2018-12-19            |                 0.83                 |                                      829.9999999999999                                       |
|  PARR  |            2012-09-18            |                 14.2                 |                                      5.461538461538461                                       |
|  PAYS  |            2011-11-14            |                 0.11                 |                                             11.0                                             |
|  PCYG  |            2002-11-22            |                 2.5                  |                                             5.0                                              |
|  PDS   |            2020-11-12            |                14.54                 |                                      21.70149253731343                                       |
|  PED   |            2013-09-30            |              42.400002               |                                          10.6000005                                          |
|  PRTG  |            2003-04-23            |                 35.0                 |                                             10.0                                             |
|  PYR   |            2014-01-14            |                 0.48                 |                                      10.434782608695652                                      |
|  QIPT  |            2019-01-10            |                 0.41                 |                                            5.125                                             |
|  RGLD  |            1992-06-05            |               0.797423               |                                      7.9999899676959805                                      |
|  SBRA  |            2003-05-14            |               1.803055               |                                      5.740732486205788                                       |
|  SCPS  |            2020-12-17            |              33.959999               |                                      5.736486317567568                                       |
|  SMTI  |            1995-04-19            |                500.0                 |                                             5.0                                              |
|  SPI   |            2017-05-25            |              19.299999               |                                      5.830815407854985                                       |
|  SRNE  |            2009-07-15            |                22.25                 |                                             8.9                                              |
|  STXS  |            2013-08-05            |               8.658759               |                                       5.33145925590239                                       |
|   SU   |            1993-12-01            |               0.804692               |                                      36.200098969814206                                      |
|  SUNW  |            2010-09-08            |                22.75                 |                                      9.615384615384615                                       |
|  TGTX  |            2011-07-21            |               28.6875                |                                             5.1                                              |
|  TXMD  |            2009-07-21            |                150.0                 |                                      8.823529411764707                                       |
|  UAVS  |            2007-05-21            |                2437.5                |                                             10.0                                             |
|  UGRO  |            2020-10-15            |                 0.88                 |                                      14.193548387096774                                      |
|  UONE  |            2020-06-16            |              27.190001               |                                      18.006623178807946                                      |
|  UVE   |            2005-11-16            |               0.221477               |                                      9.999864547588947                                       |
|   VG   |            2009-08-26            |                 2.17                 |                                            5.425                                             |
|  VISL  |            2013-04-22            |               684000.0               |                                      39.583333333333336                                      |
|  VTGN  |            2014-08-18            |                 15.0                 |                                             25.0                                             |
|  VTNR  |            1997-05-27            |                198.0                 |                                             5.5                                              |
|  WETF  |            2004-11-18            |               1.260181               |                                      37.49980657640232                                       |
|  WIMI  |            2020-07-13            |                24.74                 |                                      7.0685714285714285                                      |
|  WLL   |            2020-04-23            |                 1.68                 |                                             5.25                                             |
|  WNW   |            2020-12-16            |              65.099998               |                                      5.402489460580912                                       |
|  WTRG  |            1981-07-01            |               1.352904               |                                      12.429981073482665                                      |
|  WTRH  |            2020-03-18            |                 1.97                 |                                      6.354838709677419                                       |
|  WWR   |            2020-10-06            |                 11.8                 |                                      5.130434782608696                                       |
|  YMTX  |            2018-10-18            |                207.0                 |                                      5.914285714285715                                       |

All tickers with a minimum market cap of 1000 million (today) that multiplied their price >5 times over 5 consecutive trading days:

| Ticker | Date (the increase was observed) | Adjusted Close Price (at given date) | Price increase (between lowest price of the previous 5 trading days and price at given date) |
| :----: | :------------------------------: | :----------------------------------: | :------------------------------------------------------------------------------------------: |
|  AMC   |            2021-01-27            |                 19.9                 |                                       6.7003367003367                                        |
|  CVE   |            2009-12-09            |              17.986408               |                                      117.4998562805404                                       |
|  GME   |            2021-01-27            |              347.51001               |                                      8.883180441799091                                       |
|  NUAN  |            1999-11-15            |               8.603896               |                                      5.129032738813787                                       |
|  NVR   |            1993-10-01            |                10.25                 |                                      27.333333333333332                                      |
|   SU   |            1993-12-01            |               0.804692               |                                      36.200098969814206                                      |
|  WTRG  |            1981-07-01            |               1.352904               |                                      12.429981073482665                                      |

Important note:
The market cap are from today (06/06/2021).
The observed increases might have happened at a time when the company's valuation was significantly smaller.
The more recent events should therefore be closer to the market cap we used for slicing the data in this study.

## Conclusion
Since this analysis is missing short interest changes, it is difficult to distinguish between
short squeezes and bull runs.
Depending on how we define our thresholds for major short squeezes the event happens at most
very rarely (<X%; for Xx increase) or occasionally (>X%; for Xx increase).

We invite everyone to analyze the aggregated data (csv-files) further.
Besides short squeezes, the data might be helpful for getting a better grasp on how often major price increases
happen at the stock market. We only lightly touched the bigger picture and the extreme price increases in this document.

A few additional observations:
- The higher the market cap the less often extreme price increases happen.
- None of the big tech companies (`AAPL`, `AMZN`, `GOOG`, `MSFT`, `TSLA`) have experienced a (closing)
  price increase of (>2x) within 10 trading days in their entire (recorded) history.
- This is how some well-known highly shorted stock faired:
  - `AMD`: no increase of >2x within 5 or 10 consecutive trading days
  - `BB`: 3.37x within 10 days (27/01/2021); no increase of >2x within 5 days
  - `KOSS`: 17.37x within 5 days (27/01/2021)
  - `NAKD`: 3.1x within 5 days (07/02/2017)
  - `NOK`: no increase of >2x within 5 or 10 consecutive trading days
  - `PLTR`: no increase of >2x within 5 or 10 consecutive trading days
- Only three major price increases (>5x) have happened for >1000 million market cap stocks within the last 20 years.
  Two of them happened this year on the same date (27/01/2021): `AMC` (6.7x) and `GME` (8.9x).
  

## Potential future work
- Take the market cap into consideration when the price increases have happened in order to have a better classification
  of short squeezes in relation to a stock's market cap.
- The code only filters for the first price increase above the thresholds per ticker. A stock might have increased 
  multiple times above the thresholds in its lifetime. It could be valuable for the bigger picture to understand if
  certain stocks run into these events more often than others.
- It is possible to filter stock by sector. By doing so, we could understand if certain sectors (or combinations of
  sectors and time spans) lead are more targeted by these events.
- Take short interest changes into account (at the time of the price increases) in order to better understand
  if an actual short squeeze or bull run happened.
- Take the movement of the rest of the market into account (at the time of the price increases of a specific ticker)
  in order to understand if the increase had a correlation with the overall market.

## Appendix - How to reproduce the results?
### 1. Download price data (no filtering)
Source of truth for ticker symbols:
https://github.com/shilewenuw/get_all_tickers

Source of truth for price data:
https://github.com/ranaroussi/yfinance

Shell commands - NYSE data:
```
# Load market cap min 1000m
mkdir ./ticker_data__nyse_min_1000m
poetry run python bin/pull_data.py -v --nyse --min-market-cap=1000 --output-path ./ticker_data__nyse_min_1000m 2>&1 | tee nyse_min_1000m.log

# Load market cap min 100m (use already cached 1000m data)
mkdir ./ticker_data__nyse_min_100m
poetry run python bin/pull_data.py -v --nyse --min-market-cap=100 --ticker-source-dir ./ticker_data__nyse_min_1000m --output-path ./ticker_data__nyse_min_100m  2>&1 | tee nyse_min_100m.log

# Load market cap min 10m (use already cached 100m data)
mkdir ./ticker_data__nyse_min_10m
poetry run python bin/pull_data.py -v --nyse --min-market-cap=10 --ticker-source-dir ./ticker_data__nyse_min_100m --output-path ./ticker_data__nyse_min_10m  2>&1 | tee nyse_min_10m.log
```

Shell commands - NASDAQ data:
```
# Load market cap min 1000m
mkdir ./ticker_data__nasdaq_min_1000m
poetry run python bin/pull_data.py -v --nasdaq --min-market-cap=1000 --output-path ./ticker_data__nasdaq_min_1000m 2>&1 | tee nasdaq_min_1000m.log

# Load market cap min 100m (use already cached 1000m data)
mkdir ./ticker_data__nasdaq_min_100m
poetry run python bin/pull_data.py -v --nasdaq --min-market-cap=100 --ticker-source-dir ./ticker_data__nasdaq_min_1000m --output-path ./ticker_data__nasdaq_min_100m  2>&1 | tee nasdaq_min_100m.log

# Load market cap min 10m (use already cached 100m data)
mkdir ./ticker_data__nasdaq_min_10m
poetry run python bin/pull_data.py -v --nasdaq --min-market-cap=100 --ticker-source-dir ./ticker_data__nasdaq_min_100m --output-path ./ticker_data__nasdaq_min_10m  2>&1 | tee nasdaq_min_10m.log
```

Shell commands - AMEX data:
```
# Load market cap min 1000m
mkdir ./ticker_data__amex_min_1000m
poetry run python bin/pull_data.py -v --amex --min-market-cap=1000 --output-path ./ticker_data__amex_min_1000m 2>&1 | tee amex_min_1000m.log

# Load market cap min 100m (use already cached 1000m data)
mkdir ./ticker_data__amex_min_100m
poetry run python bin/pull_data.py -v --amex --min-market-cap=100 --ticker-source-dir ./ticker_data__amex_min_1000m --output-path ./ticker_data__amex_min_100m  2>&1 | tee amex_min_100m.log

# Load market cap min 10m (use already cached 100m data)
mkdir ./ticker_data__amex_min_10m
poetry run python bin/pull_data.py -v --amex --min-market-cap=10 --ticker-source-dir ./ticker_data__amex_min_100m --output-path ./ticker_data__amex_min_10m  2>&1 | tee amex_min_10m.log
```

### 2. Filter data for the various squeeze definitions
Source of truth for ticker symbols:
https://github.com/shilewenuw/get_all_tickers

Source of truth for price data:
The downloaded data from step 1.

This produces the following files:
- File with the counts of the unfiltered ticket counters: `unfiltered_ticker_counts.csv`
- A file for each combination of exchange, min market cap, price increase multiplier and consecutive trading days:
  `<exchange>_min_<min_market_cap>_multi_<price_increase_multiplier>_days_<consecutive_days>.csv`

Command:
```
results_1/create_filtered_tickers.sh
```

### 3. Create analysis tables from the filtered data
Source of truth:
Files created in step 2.

This produces the following files:
- File with a markdown table giving an overview over the results: `detailed_overview_table.md`
- File with a more aggregate overview table: `simple_overview_table.md`
- File the most extreme observed price increases (minimum market cap 1000 million): `most_extreme_short_squeezes_min_1000.md`
- File with a more aggregate overview table (minimum market cap 10 million): `most_extreme_short_squeezes_min_10.md`
  
Command:
```
poetry run python results_1/create_analysis_tables.py
```
