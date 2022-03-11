from dataclasses import dataclass

@dataclass
class SestertiusTicker:
	# double check if some of these should be float
	name			: str	= ''
	id				: int	= 0
	decimals		: int	= 0
	precision		: int	= 0
	precision_order	: int	= 0
	min				: int	= 0
	max				: int	= 0

	def update(self, data) -> None:
		for key in data:
			if not hasattr(self, key):
				raise AttributeError(key)
			setattr(self, key, data[key])

class TickerService:
	def __init__(self):
		self.tickers = {}

	def register(self, ticker, data) -> SestertiusTicker:
		Ticker = SestertiusTicker()
		Ticker.update(data)
		self.tickers[ticker] = Ticker
		return Ticker

	def update(self, ticker, data) -> SestertiusTicker:
		Ticker:SestertiusTicker = self.tickers[ticker]
		Ticker.update(data)
		return Ticker

	def get(self, ticker) -> SestertiusTicker:
		return self.tickers[ticker]

	def x_vol_to_true_vol(self, ticker, volume) -> float:
		decimals = format(0, f'.{self.tickers[ticker].decimals}f')
		true_vol = volume * float(str(decimals[:-1]) + '1')
		return true_vol

	def true_vol_to_x_vol(self, ticker, volume) -> float:
		x_vol = volume * pow(10, self.tickers[ticker].decimals)
		return x_vol

	def id(self, ticker):
		return self.tickers[ticker].id