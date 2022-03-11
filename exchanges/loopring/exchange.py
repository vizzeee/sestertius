from typing import TYPE_CHECKING
from exchanges.base import exchange
from . import api, auxiliary, config, orderbook, orders, storage

if TYPE_CHECKING:
	from exchanges.base.orders import SestertiusOrderObject

class Loopring(exchange.Exchange):
	def __init__(self, cfg):
		self.Config 		= config.new(cfg)
		self.Storage		= storage.StorageService()

	def initialize(self):
		self.REST = api.REST(
			self.Config.api_key,
			self.Config.account_address,
			self.Config.account_id)
		auxiliary.API.set_exchange_address(self.Config, self.REST)
		auxiliary.API.update_tickers(self.REST, self.ticker_service)
		auxiliary.API.update_pairs(self.REST, self.pair_service)
		auxiliary.API.update_amm_pool_addresses(self.REST, self.pair_service)
		self.TMPOrderbook = orderbook.OrderbookService(
			self.ticker_service, self.pair_service)
		return True

	def run_websocket(self):
		self.WSS = api.WSS(self.update)
		key = auxiliary.API.get_wss_key(self.REST)
		self.WSS.start(key)

	def status_websocket(self):
		# have some kind of threshhold for how long without updates?
		pass

	def send_websocket(self, data):
		self.WSS.send(data)
	
	def exit(self):
		pass
	
	def update(self, websocket, data):
		if auxiliary.WSS.ping(data, self.send_websocket):
			# set latest ping as threshhold???
			return
		auxiliary.WSS.data(data, self.TMPOrderbook)

	def ask(self, pair):
		return self.pair_service.ask(pair)

	def bid(self, pair):
		return self.pair_service.bid(pair)

	def order(self, SOO:"SestertiusOrderObject"):
		# we should be able to impove the args here
		PayloadService = auxiliary.LoopringPayload()
		payload = PayloadService.create()
	
	def order_details(api=False):
		# Check
		pass
	
	def order_cancel():
		pass