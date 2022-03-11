import logging
from . import utils
from exchanges.loopring.exchange import Loopring

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from exchanges.base.exchange import Exchange


__version__ = 0.1
logger = logging.getLogger(__name__)

class Engine:
	def __init__(self):
		self.running = True
		self.exchanges = {}

	def initialize(self):
		self.load_config()
		self.load_exchanges()
		self.load_strategies()

	@utils.loader
	def load_config(self, file=None) -> bool:
		file = 'config' if file is None else file
		self.config = utils.Config.load_yml(file)
		if isinstance(self.config, dict):
			return True
		return False

	@utils.loader
	def setup_loopring(self):
		self.Loopring = Loopring(self.config['exchanges']['loopring'])
		self.exchanges['loopring'] = self.Loopring
		self.Loopring.initialize()
		return True

	@utils.loader
	def setup_strategies(self):
		return True
	
	def load_exchanges(self):
		# manually add new exchanges here.
		if self.config['exchanges']['loopring']['enable']:
			self.setup_loopring()

	def load_strategies(self):
		return True

	def review_websocket(self, exchange:"Exchange"):
		# Check if a websocket had update long ago, if so renew it.
		pass

	def main(self):
		pass

	def command(self):
		pass
		#return COMMAND.