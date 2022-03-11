from dataclasses import dataclass

@dataclass
class SestertiusOrderObject:
	"""
	this object will be created by our strategies 
	and used on the exchange
	"""
	price				: float	= 0.0
	volume				: float	= 0.0
	pair				: str	= ''
	side				: str	= ''
	order_type			: str	= ''
	strategy			: str	= ''
	linked_id			: str	= ''

	@property
	def market(self):
		return self.pair.split('-')[1]

	@property
	def asset(self):
		return self.pair.split('-')[0]

@dataclass
class StoredOrder:
	""" the information we will store """
	pair				: str
	side				: str
	status				: str
	price				: float
	volume				: float
	ref					: str
	linked_ref			: str
	time_open			: int
	time_close			: int
	strategy			: str
	exchange_name		: str
	exchange_ref		: str
	exchnage_payload	: dict

	def update(self, data) -> None:
		for key in data:
			if not hasattr(self, key):
				raise AttributeError(key)
			setattr(self, key, data[key])

class OrderService:
	def __init__(self):
		self.orders = []

	def new_order_object(self) -> SestertiusOrderObject:
		return SestertiusOrderObject

	def register(self, data) -> StoredOrder:
		Order = StoredOrder()
		Order.update(data)
		self.orders.append(Order)
		return Order

	def update(self, ref, data) -> StoredOrder:
		Ticker:StoredOrder = self.get(ref)
		Ticker.update(data)
		return Ticker

	def get(self, ref):
		for Order in self.orders:
			if Order.ref == ref or Order.exchange_ref == ref:
				return Order

	def link(self):
		pass