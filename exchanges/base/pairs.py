from dataclasses import dataclass, field

@dataclass
class SestertiusPair:
	precision	: int	= 0.0
	ask			: int	= 0.0
	bid			: int	= 0.0
	orderbook	: list	= field(default_factory=list)
	amm_address	: str	= ''

	def update(self, data) -> None:
		for key in data:
			if not hasattr(self, key):
				raise AttributeError(key)
			setattr(self, key, data[key])

class PairService:
	def __init__(self):
		self.pairs = {}

	def register(self, pair, data) -> SestertiusPair:
		Pair = SestertiusPair()
		Pair.update(data)
		self.pairs[pair] = Pair
		return Pair

	def update(self, pair, data) -> SestertiusPair:
		Pair:SestertiusPair = self.pairs[pair]
		Pair.update(data)
		return Pair

	def get_by_amm(self, amm_address):
		for pair in self.pairs:
			if amm_address == self.pairs[pair].amm_address:
				return pair

	def get(self, pair) -> SestertiusPair:
		return self.pairs[pair]

	def ask(self, pair) -> float:
		return self.pairs[pair].ask

	def bid(self, pair) -> float:
		return self.pairs[pair].bid

	def orderbook(self, pair) -> list:
		return self.pairs[pair].orderbook

	def all(self) -> list:
		return [pair for pair in self.pairs]

	def exists(self, pair) -> bool:
		if pair in self.pairs:
			return True
		return False

	def delete(self, pair) -> None:
		self.pairs.pop(pair)