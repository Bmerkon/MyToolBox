select adjdate,ExgTradingCode,adjtradingcode from Opt_Adjustment
where ExgTradingCode in (
select tradingcode from Opt_OptionContract
where
ULAName='50ETF'
and
ifreal=1
and
Exchange=83
and
listingdate<='2017-05-05'
and
(delistingdate>='2015-02-09' 
or delistingdate is null)
)