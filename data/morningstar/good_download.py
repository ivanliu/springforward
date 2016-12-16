# Copyright (c) 2015 Peter Cerno
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
u"""Example showing how to download financial data from
financials.morningstar.com for all tickers in S&P 500 (October 2015).
"""

from __future__ import absolute_import
import pymysql
import time
import good_morning as gm
import sys

DB_HOST = u'db_host'
DB_USER = u'db_user'
DB_PASS = u'db_pass'
DB_NAME = u'db_name'

conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)

kr = gm.KeyRatiosDownloader()
fd = gm.FinancialsDownloader()

# Taken from: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
# Notes:
# * Instead of BF-B use BF.B.
# * Instead of BRK-B use BRK.B.
sp500_2015_10 = [
    u'A', u'AA', u'AAL', u'AAP', u'AAPL', u'ABBV', u'ABC', u'ABT', u'ACE', u'ACN', u'ADBE',
    u'ADI', u'ADM', u'ADP', u'ADS', u'ADSK', u'ADT', u'AEE', u'AEP', u'AES', u'AET',
    u'AFL', u'AGN', u'AIG', u'AIV', u'AIZ', u'AKAM', u'ALL', u'ALLE', u'ALTR', u'ALXN',
    u'AMAT', u'AME', u'AMG', u'AMGN', u'AMP', u'AMT', u'AMZN', u'AN', u'ANTM', u'AON',
    u'APA', u'APC', u'APD', u'APH', u'ARG', u'ATVI', u'AVB', u'AVGO', u'AVY', u'AXP',
    u'AZO', u'BA', u'BAC', u'BAX', u'BBBY', u'BBT', u'BBY', u'BCR', u'BDX', u'BEN',
    u'BF.B', u'BHI', u'BIIB', u'BK', u'BLK', u'BLL', u'BMY', u'BRCM', u'BRK.B', u'BSX',
    u'BWA', u'BXLT', u'BXP', u'C', u'CA', u'CAG', u'CAH', u'CAM', u'CAT', u'CB', u'CBG',
    u'CBS', u'CCE', u'CCI', u'CCL', u'CELG', u'CERN', u'CF', u'CHK', u'CHRW', u'CI',
    u'CINF', u'CL', u'CLX', u'CMA', u'CMCSA', u'CMCSK', u'CME', u'CMG', u'CMI', u'CMS',
    u'CNP', u'CNX', u'COF', u'COG', u'COH', u'COL', u'COP', u'COST', u'CPB', u'CPGX',
    u'CRM', u'CSC', u'CSCO', u'CSX', u'CTAS', u'CTL', u'CTSH', u'CTXS', u'CVC', u'CVS',
    u'CVX', u'D', u'DAL', u'DD', u'DE', u'DFS', u'DG', u'DGX', u'DHI', u'DHR', u'DIS',
    u'DISCA', u'DISCK', u'DLPH', u'DLTR', u'DNB', u'DO', u'DOV', u'DOW', u'DPS', u'DRI',
    u'DTE', u'DUK', u'DVA', u'DVN', u'EA', u'EBAY', u'ECL', u'ED', u'EFX', u'EIX', u'EL',
    u'EMC', u'EMN', u'EMR', u'ENDP', u'EOG', u'EQIX', u'EQR', u'EQT', u'ES', u'ESRX',
    u'ESS', u'ESV', u'ETFC', u'ETN', u'ETR', u'EW', u'EXC', u'EXPD', u'EXPE', u'F',
    u'FAST', u'FB', u'FCX', u'FDX', u'FE', u'FFIV', u'FIS', u'FISV', u'FITB', u'FLIR',
    u'FLR', u'FLS', u'FMC', u'FOSL', u'FOX', u'FOXA', u'FSLR', u'FTI', u'FTR', u'GAS',
    u'GD', u'GE', u'GGP', u'GILD', u'GIS', u'GLW', u'GM', u'GMCR', u'GME', u'GNW', u'GOOG',
    u'GOOGL', u'GPC', u'GPS', u'GRMN', u'GS', u'GT', u'GWW', u'HAL', u'HAR', u'HAS',
    u'HBAN', u'HBI', u'HCA', u'HCBK', u'HCN', u'HCP', u'HD', u'HES', u'HIG', u'HOG',
    u'HON', u'HOT', u'HP', u'HPQ', u'HRB', u'HRL', u'HRS', u'HSIC', u'HST', u'HSY', u'HUM',
    u'IBM', u'ICE', u'IFF', u'INTC', u'INTU', u'IP', u'IPG', u'IR', u'IRM', u'ISRG',
    u'ITW', u'IVZ', u'JBHT', u'JCI', u'JEC', u'JNJ', u'JNPR', u'JPM', u'JWN', u'K', u'KEY',
    u'KHC', u'KIM', u'KLAC', u'KMB', u'KMI', u'KMX', u'KO', u'KORS', u'KR', u'KSS', u'KSU',
    u'L', u'LB', u'LEG', u'LEN', u'LH', u'LLL', u'LLTC', u'LLY', u'LM', u'LMT', u'LNC',
    u'LOW', u'LRCX', u'LUK', u'LUV', u'LVLT', u'LYB', u'M', u'MA', u'MAC', u'MAR', u'MAS',
    u'MAT', u'MCD', u'MCHP', u'MCK', u'MCO', u'MDLZ', u'MDT', u'MET', u'MHFI', u'MHK',
    u'MJN', u'MKC', u'MLM', u'MMC', u'MMM', u'MNK', u'MNST', u'MO', u'MON', u'MOS', u'MPC',
    u'MRK', u'MRO', u'MS', u'MSFT', u'MSI', u'MTB', u'MU', u'MUR', u'MYL', u'NAVI', u'NBL',
    u'NDAQ', u'NEE', u'NEM', u'NFLX', u'NFX', u'NI', u'NKE', u'NLSN', u'NOC', u'NOV',
    u'NRG', u'NSC', u'NTAP', u'NTRS', u'NUE', u'NVDA', u'NWL', u'NWS', u'NWSA', u'O',
    u'OI', u'OKE', u'OMC', u'ORCL', u'ORLY', u'OXY', u'PAYX', u'PBCT', u'PBI', u'PCAR',
    u'PCG', u'PCL', u'PCLN', u'PCP', u'PDCO', u'PEG', u'PEP', u'PFE', u'PFG', u'PG',
    u'PGR', u'PH', u'PHM', u'PKI', u'PLD', u'PM', u'PNC', u'PNR', u'PNW', u'POM', u'PPG',
    u'PPL', u'PRGO', u'PRU', u'PSA', u'PSX', u'PVH', u'PWR', u'PX', u'PXD', u'PYPL',
    u'QCOM', u'QRVO', u'R', u'RAI', u'RCL', u'REGN', u'RF', u'RHI', u'RHT', u'RIG', u'RL',
    u'ROK', u'ROP', u'ROST', u'RRC', u'RSG', u'RTN', u'SBUX', u'SCG', u'SCHW', u'SE',
    u'SEE', u'SHW', u'SIAL', u'SIG', u'SJM', u'SLB', u'SLG', u'SNA', u'SNDK', u'SNI',
    u'SO', u'SPG', u'SPLS', u'SRCL', u'SRE', u'STI', u'STJ', u'STT', u'STX', u'STZ',
    u'SWK', u'SWKS', u'SWN', u'SYK', u'SYMC', u'SYY', u'T', u'TAP', u'TDC', u'TE', u'TEL',
    u'TGNA', u'TGT', u'THC', u'TIF', u'TJX', u'TMK', u'TMO', u'TRIP', u'TROW', u'TRV',
    u'TSCO', u'TSN', u'TSO', u'TSS', u'TWC', u'TWX', u'TXN', u'TXT', u'TYC', u'UA', u'UAL',
    u'UHS', u'UNH', u'UNM', u'UNP', u'UPS', u'URBN', u'URI', u'USB', u'UTX', u'V', u'VAR',
    u'VFC', u'VIAB', u'VLO', u'VMC', u'VNO', u'VRSK', u'VRSN', u'VRTX', u'VTR', u'VZ',
    u'WAT', u'WBA', u'WDC', u'WEC', u'WFC', u'WFM', u'WHR', u'WM', u'WMB', u'WMT', u'WRK',
    u'WU', u'WY', u'WYN', u'WYNN', u'XEC', u'XEL', u'XL', u'XLNX', u'XOM', u'XRAY', u'XRX',
    u'XYL', u'YHOO', u'YUM', u'ZBH', u'ZION', u'ZTS']

for ticker in sp500_2015_10:
    print ticker,; sys.stdout.write(u'')
    try:
        kr.download(ticker, conn)
        fd.download(ticker, conn)
        time.sleep(1)
        print u' ... success'
    except Exception, e:
        print u' ... failed', e
