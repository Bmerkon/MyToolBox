

SHFE_D = ((900, 1015), (1030, 1130), (1330, 1500))
SHFE_N1 = ((900, 1015), (1030, 1130), (1330, 1500), (2100, 2300),)
SHFE_N2 = ((900, 1015), (1030, 1130), (1330, 1500), (2100, 2500),)  # cross 24:00
SHFE_N3 = ((900, 1015), (1030, 1130), (1330, 1500), (2100, 2630),)  # cross 24:00

DCE_D = ((900, 1015), (1030, 1130), (1330, 1500))
DCE_N = ((900, 1015), (1030, 1130), (1330, 1500), (2100, 2330), )

CZCE_D = ((900, 1015), (1030, 1130), (1330, 1500))
CZCE_N = ((900, 1015), (1030, 1130), (1330, 1500), (2100, 2330), )

CFFEX_D = ((915, 1130), (1300, 1515))
STOCK = ((930, 1130), (1300, 1500))


#IF YEAR > 2015

CFFEX = {
    'IF': STOCK, 'IH': STOCK, 'IC': STOCK, 'T': CFFEX_D, 'TF': CFFEX_D,
}

#ELSE

# CFFEX = {
#     'IF': CFFEX_D, 'IH': CFFEX_D, 'IC': CFFEX_D, 'T': CFFEX_D, 'TF': CFFEX_D,
# }

#ENDIF

SHFE = {
    'fu': SHFE_D, 'wr': SHFE_D,
    'ru': SHFE_N1, 'au': SHFE_N3, 'ag': SHFE_N3,
    'cu': SHFE_N2, 'al': SHFE_N2, 'zn': SHFE_N2, 'pb': SHFE_N2, 'sn': SHFE_N2,
    'ni': SHFE_N2, 'rb': SHFE_N2, 'hc': SHFE_N2, 'bu': SHFE_N2,

}

DCE = {
    'm': DCE_N, 'y': DCE_N, 'a': DCE_N, 'b': DCE_N,
    'p': DCE_N, 'j': DCE_N, 'jm': DCE_N, 'i': DCE_N,

    'c': DCE_D, 'cs': DCE_D, 'jd': DCE_D, 'bb': DCE_D,
    'fb': DCE_D, 'l': DCE_D, 'v': DCE_D, 'pp': DCE_D,
}

CZCE = {
    'WH': CZCE_D, 'PM': CZCE_D, 'RI': CZCE_D, 'LR': CZCE_D,
    'JR': CZCE_D, 'RS': CZCE_D, 'SF': CZCE_D, 'SM': CZCE_D,

    'SR': CZCE_N, 'CF': CZCE_N, 'TC': CZCE_N, 'ZC': CZCE_N,
    'FG': CZCE_N,
    'TA': CZCE_N, 'MA': CZCE_N, 'OI': CZCE_N, 'RM': CZCE_N,

    'ME': CZCE_D,
}

ALL = {}
ALL.update(CFFEX)
ALL.update(SHFE)
ALL.update(DCE)
ALL.update(CZCE)

OPTION_SESSIONS = ((930, 1130), (1300, 1500))
OPTION_MARKET_OPEN_AT0925 = 925
OPTION_MARKET_CLOSE_AT1505 = 1505
