from abc import ABC, abstractmethod
from . import pairs, tickers, orders, balances

class Exchange(ABC):
	# Set state vaibles here like prices and shit.
	pair_service	= pairs.PairService()
	ticker_service	= tickers.TickerService()
	order_service	= orders.OrderService()

	@abstractmethod
	def initialize():
		""" returns true or false """
		pass

	@abstractmethod
	def run_websocket():
		""" connect websocket """
		pass

	@abstractmethod
	def status_websocket():
		""" returns a bool """
		pass

	@abstractmethod
	def send_websocket():
		""" send websocket commands """
		pass
	
	@abstractmethod
	def exit():
		""" exit the exchange/websocket """
		pass
	
	@abstractmethod
	def update():
		""" callback for the websocket, updates the state of the exchange, prices etc """
		pass

	@abstractmethod
	def ask():
		""" returns ask price for the pair """
		pass

	@abstractmethod
	def bid():
		""" returns bid price for the pair """
		pass

	@abstractmethod
	def order():
		""" places an order on the exchange """
		pass
	
	@abstractmethod
	def order_details():
		""" gets the order details """
		pass
	
	@abstractmethod
	def order_cancel():
		""" cancels an order """
		pass