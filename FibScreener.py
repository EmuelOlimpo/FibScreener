# FibScreener v1.0
# Created by Emuel Olimpo
# Dated 09 May 2020

from psequant import get_pse_data
import matplotlib.pyplot as plt

startdate = "2019-12-27"
enddate = "2020-06-02"  # datetime.strftime(datetime.now(), "%Y-%m-%d")

# Data initialization
PSEI = (
    "AC", "AEV", "AGI", "ALI", "AP", "BDO", "BLOOM", "BPI", "DMC", "FGEN",
    "GLO", "GTCAP", "ICT", "JFC", "JGS", "LTG", "MBT", "MEG", "MER", "MPI",
    "PGOLD", "RLC", "RRHI", "SCC", "SECB", "SM", "SMC", "SMPH", "TEL", "URC"
)
x_axis = []  # Holder for year-to-date performance
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


def curr_RSI(stock):
    fullframe = get_pse_data(stock, startdate, enddate)
    period_data = fullframe['close'].to_list()

    up_mov = []
    down_mov = []
    for prev, curr in zip(period_data[0:15], period_data[1:15]):
        if curr > prev:
            up_mov.append(curr - prev)
            down_mov.append(0)
        elif prev > curr:
            up_mov.append(0)
            down_mov.append(prev - curr)
    up_mov_init = sum(up_mov) / 14
    down_mov_init = sum(down_mov) / 14

    up_mov_exp = []
    down_mov_exp = []

    up_mov_exp.append(up_mov_init)
    down_mov_exp.append(down_mov_init)

    for prev, curr in zip(period_data[14:], period_data[15:]):
        if curr > prev:
            today_up_mov = curr - prev
            today_up_ave = ((up_mov_exp[-1] * 13) + today_up_mov) / 14
            up_mov_exp.append(today_up_ave)
            down_mov_exp.append(((down_mov_exp[-1] * 13) + 0) / 14)
        elif prev > curr:
            today_down_mov = prev - curr
            today_down_ave = ((down_mov_exp[-1] * 13) + today_down_mov) / 14
            down_mov_exp.append(today_down_ave)
            up_mov_exp.append(((up_mov_exp[-1] * 13) + 0) / 14)

    RS_exp = list(x/y for x, y in zip(up_mov_exp, down_mov_exp))
    RSI = 100-(100/(1+RS_exp[-1]))
    return RSI


# Get the year-to-date performance
for i in PSEI:
    temp0 = curr_RSI(i)
    x_axis.append(temp0)
    temp1 = LoHi(i)
    indexLoHi.append(temp1)

# Get the current Fibonacci levels
for item in indexLoHi:
    temp2 = CurrentFib(item[0], item[1], item[2])
    indexFib.append(temp2)

# Generates key-value pairs of (Stock ticker, (YTD return, Fibonacci level))
coordinates = list(zip(x_axis, indexFib))

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
plt.xticks(ticks=[0, 30, 50, 70, 100])
plt.xlabel("RSI (as of " + str(enddate) + ")")
plt.ylabel("Fibonacci retracement level")
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.gca().set_xlim([0, 100])
plt.gca().set_ylim([0, 1])


# TODO: fix saving to path plt.savefig('%s.png' % enddate, dpi=300)
plt.show()
