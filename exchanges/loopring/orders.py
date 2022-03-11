from dataclasses import dataclass, asdict
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..orders import SestertiusOrderObject
	from ..tickers import TickerService
	from .config import Config

TYPES = {'maker':'MAKER_ONLY', 'limit':'LIMIT_ORDER'}
STATES = [
	'processing',
	'processed',
	'cancelling',
	'cancelled',
	'expired',
	'waiting']

@dataclass # check if it can be done as dict/json print
class Object:
	# we still need to update with eddsa 
	# we can probably set a few of these to default values
	sellToken		: int
	buyToken		: int
	validUntil		: int
	orderType		: str
	exchange		: str
	accountId		: int
	maxFeeBips		: float
	storageId		: int	= 0
	allOrNone		: bool	= False
	fillAmountBOrS	: bool	= True

	def __str__(self):
		return asdict(self)

class Payload:

	def create(SOO:"SestertiusOrderObject", config:"Config", ts):
		buy, sell = Payload._side_objects(SOO, ts)
		return Object(
			sellToken	= sell,
			buyToken	= buy,
			validUntil	= Payload._valid_untill(config.valid_untill),
			orderType	= Payload._get_type(SOO.order_type),
			exchange	= config.exchange_address,
			accountId	= config.account_id,
			maxFeeBips	= config.max_fee_bips
		)

	def verify(data) -> bool: # should this be moved?
		if 'status' in data:
			if 'process' in data['status']:
				return True
		return False

	def status(self, status): # should this be moved?
		if status == 'processing':
			return 'open'
		elif status == 'processed':
			return 'closed'
		elif status == 'cancelled':
			return 'cancelled'
		else:
			return None

	def sell_ticker_id(SOO:"SestertiusOrderObject", ts:"TickerService") -> int:
		# should this be moved?
		if SOO.side == 'buy': 
			return ts.id(SOO.market)
		return ts.id(SOO.asset)

	def _side_objects(SOO:"SestertiusOrderObject", ts) -> tuple[dict, dict]:
		asset_id, market_id		= Payload._pair_ids(SOO, ts)
		buy_volume, sell_volume = Payload._volume(SOO, ts)
		
		if SOO.side == 'buy':
			buy	= {'tokenId': asset_id, 'volume': buy_volume}
			sell = {'tokenId': market_id, 'volume': sell_volume}
			return buy, sell 

		buy	= {'tokenId': market_id, 'volume': buy_volume} 
		sell = {'tokenId': asset_id, 'volume': sell_volume}
		return buy, sell

	def _volume(self, SOO:"SestertiusOrderObject", ts:"TickerService") -> tuple[int, int]:
		buy_volume = (SOO.volume * SOO.price)
		if SOO.side == 'buy':
			buy		= ts.true_vol_to_x_vol(SOO.asset, buy_volume)
			sell	= ts.true_vol_to_x_vol(SOO.market, SOO.volume)
			return int(buy), int(sell)

		buy		= ts.true_vol_to_x_vol(SOO.market, buy_volume)
		sell	= ts.true_vol_to_x_vol(SOO.asset, SOO.volume)
		return int(buy), int(sell)

	def _pair_ids(self, SOO:"SestertiusOrderObject", ts:"TickerService") -> tuple[int, int]:
		asset_id	= ts.id(SOO.asset)
		market_id	= ts.id(SOO.market)
		return asset_id, market_id

	def _get_type(t) -> str:
		if t in TYPES:
			return TYPES[t]
		raise KeyError(t)

	def _valid_untill(valid_untill) -> int:
		return int(time.time() + (60 * 60 * 24 * valid_untill))