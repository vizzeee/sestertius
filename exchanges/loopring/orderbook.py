from dataclasses import field
from typing import TYPE_CHECKING

from exchanges.base.pairs import PairService, SestertiusPair

if TYPE_CHECKING:
	from exchanges.base.tickers import TickerService

class Orderbook:
	pair		: str	= ''
	amm_alias	: str	= ''
	ob_amm		: dict	= field(default_factory=dict['bids':[], 'asks':[]])
	ob			: dict	= field(default_factory=dict['bids':[], 'asks':[]])

	@property
	def market(self):
		return self.pair.split('-')[1]

	@property
	def asset(self):
		return self.pair.split('-')[0]

	def update(self, data) -> None:
		for key in data:
			if not hasattr(self, key):
				raise AttributeError(key)
			setattr(self, key, data[key])

class OrderbookService:

	def __init__(self, ticker_service:"TickerService", pair_service:PairService):
		self.obpairs = {}
		self.ticker_service = ticker_service
		self.pair_service = pair_service

	def register(self, pair, data) -> Orderbook:
		OBPair = Orderbook()
		OBPair.update(data)
		self.obpairs[pair] = OBPair
		return OBPair

	def update(self, pair, data) -> Orderbook:
		# used for the amm_alias mainly
		OBPair:Orderbook = self.obpairs[pair]
		OBPair.update(data)
		return OBPair

	def ob(self, data):
		OBPair:Orderbook = self.obpairs(data['topic']['market'])
		bids = []
		asks = []
		for level in data['data']['bids']:
			price = float(level[0])
			volume = self.ticker_service.x_vol_to_true_vol(OBPair.asset, level[1])
			bids.append([price, volume])
		for level in data['data']['asks']:
			price = float(level[0])
			volume = self.ticker_service.x_vol_to_true_vol(OBPair.asset, level[1])
			asks.append([price, volume])

		OBPair.ob['bids'] = bids
		OBPair.ob['asks'] = asks

		# update the true orderbook
		Pair:"SestertiusPair" = self.pair_service.get(data['topic']['market'])
		Pair.orderbook = self._sorted_orderbook(Pair)

	def ob_amm(self, data):
		asset, market = self._amm_to_tickers(data['topic']['poolAddress'])
		OBPair:Orderbook = self.obpairs(f'{asset}-{market}')

		asset_volume = self.ticker_service.x_vol_to_true_vol(
			asset, data['data'][0][0])
		market_volume = self.ticker_service.x_vol_to_true_vol(
			market, data['data'][0][1])

		ask, bid = self._calculate_amm_price(asset_volume, market_volume)
		OBPair.ob_amm['bids'] = [[bid, asset_volume]]
		OBPair.ob_amm['asks'] = [[ask, asset_volume]]

		# update the true orderbook
		Pair:"SestertiusPair" = self.pair_service.get(f'{asset}-{market}')
		Pair.orderbook= self._sorted_orderbook(OBPair)

	def _calculate_amm_price(self, asset_volume, market_volume):
		price = market_volume / asset_volume
		ask = price * 1.00314
		bid = price * 0.996
		return ask, bid

	def _amm_to_tickers(self, amm_address):
		# we need the pair service here!
		pair = self.pair_service.get_by_amm(amm_address)
		asset = pair.split('-')[0]
		market = pair.split('-')[1]
		return asset, market

	def _calculate_price(self, asset_volume, market_volume):
		price = market_volume / asset_volume
		ask = price * 1.00314
		bid = price * 0.996
		return ask, bid

	def _sorted_orderbook(self, OBPair:Orderbook):
		bids = OBPair.ob['bids'] + OBPair.ob_amm['bids']
		asks = OBPair.ob['asks'] + OBPair.ob_amm['asks']
		return {'bids': sorted(bids, reverse=True), 'asks': sorted(asks)}