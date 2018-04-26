from MorningStar_wrapper import Wrapper

isin = 'US0010551028'
w = Wrapper(isin)
print(w.getTicker())