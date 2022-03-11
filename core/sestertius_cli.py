from commands import exchange

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .sestertius import Engine

class Console:
	def __init__(self):
		self.running = True

	def initialize(self, Sestertius:"Engine"):
		self.Sestertius = Sestertius

	def main(self):
		while self.running:
			command = input(self.level)
			if command == 'exit':
				self.exit()
			# elif command == 'test':
			# 	print(self.Sestertius.exchanges['loopring'].status_websocket())
				
	def exit(self):
		self.Sestertius.exit()
		self.running = False

	@property
	def level(self):
		return '#'