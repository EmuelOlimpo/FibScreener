# FibScreener v1.0
# Created by Emuel Olimpo
# Dated 09 May 2020

from psequant import get_pse_data
# from datetime import date
import matplotlib.pyplot as plt

startdate = "2019-12-27"
enddate = "2020-05-18"

# Data initialization
PSEI = (
    "AC", "AEV", "AGI", "ALI", "AP", "BDO", "BLOOM", "BPI", "DMC", "FGEN",
    "GLO", "GTCAP", "ICT", "JFC", "JGS", "LTG", "MBT", "MEG", "MER", "MPI",
    "PGOLD", "RLC", "RRHI", "SCC", "SECB", "SM", "SMC", "SMPH", "TEL", "URC"
)
indexYTD = []  # Holder for year-to-date performance
indexLoHi = []  # Holder for low and high values for the period
indexFib = []  # Holder for current Fibonacci levels


# Scrapes pricing data given the date range
def LoHi(stock):
    # Complete date of date, OHLCV for the given stock
    fullframe = get_pse_data(stock, startdate, enddate)
    highframe = max(fullframe['high'])
    lowframe = min(fullframe['low'])
    lastframe = fullframe['close'][-1]
    return (highframe, lowframe, lastframe)


# Outputs the current Fibonacci level given the price range
def CurrentFib(periodHigh, periodLow, periodLast):
    range = periodHigh - periodLow
    level_current = 1 - ((periodHigh - periodLast) / range)
    return level_current


# Outputs the year-to-date performance of a stock
def YearToDate(stock):
    fullframe = get_pse_data(stock, startdate, enddate)
    delta = (fullframe['close'][-1] / fullframe['close'][0]) - 1
    return delta


# Get the year-to-date performance
for i in PSEI:
    temp0 = YearToDate(i)
    temp1 = LoHi(i)
    indexYTD.append(temp0)
    indexLoHi.append(temp1)

# Get the current Fibonacci levels
for item in indexLoHi:
    temp2 = CurrentFib(item[0], item[1], item[2])
    indexFib.append(temp2)

# Generates key-value pairs of (Stock ticker, (YTD return, Fibonacci level))
coordinates = list(zip(indexYTD, indexFib))

plt.figure(figsize=(7, 7), clear=True)
plt.subplots_adjust(left=0.15)

for values in coordinates:
    x = values[0]
    y = values[1]
    plt.scatter(x, y)
    plt.annotate(PSEI[coordinates.index(values)], xy=(x, y),
                 textcoords='offset points', xytext=(0, 10),
                 ha='right', va='center')

plt.yticks(ticks=[0, 0.236, 0.382, 0.500, 0.618, 0.786, 1.000])
plt.xlabel("YTD performance (as of " + str(enddate) + ")")
plt.ylabel("Fibonacci retracement level")
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.gca().set_xlim([-.60, .60])
plt.gca().set_ylim([0, 1])


# TODO: fix saving to path plt.savefig('%s.png' % enddate, dpi=300)
plt.show()
