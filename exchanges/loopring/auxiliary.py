import json
from libs import eddsa_aux
from . import orders

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .api import REST
	from .config import Config
	from .orderbook import OrderbookService
	from .storage import StorageService, TickerStorage
	from ..base.tickers import TickerService
	from ..base.pairs import PairService
	from ..base.orders import SestertiusOrderObject


class API:

	def set_exchange_address(config:"Config", rest:"REST") -> None:
		json_data = rest.get_exchange()
		config.exchange_address = json.loads(json_data)['exchangeAddress']

	def set_storage(ticker_id, storage:"StorageService", rest:"REST") -> "TickerStorage":
		# provide the sell ticker in the pair
		json_data = rest.get_next_storageid(ticker_id)
		ticker = storage.register(ticker_id, json.loads(json_data))
		return ticker

	def get_wss_key(rest:"REST") -> str:
		json_data = rest.get_websocket_key()
		return json.loads(json_data)['key']

	def update_tickers(rest:"REST", ticker_service:"TickerService") -> None:
		json_data = rest.get_tokens()
		for ticker in json.loads(json_data):
			name = ticker.pop('symbol')
			data = {
				'name' 			: ticker['name'],
				'id'			: ticker['tokenId'],
				'decimals'		: ticker['decimals'],
				'precision'		: ticker['precision'],
				'precision_order':ticker['precisionForOrder'],
				'min'			: ticker['orderAmounts']['minimum'],
				'max'			: ticker['orderAmounts']['maximum']
			}
			ticker_service.register(name, data)

	def update_pairs(rest:"REST", pair_service:"PairService") -> None:
		json_data = rest.get_markets()
		for market in json.loads(json_data)['markets']:
			pair = market.pop('market')
			
			# if pair is disabled and we have it, delete it.
			if not market['enabled'] and pair_service.exists(pair):
				pair_service.delete(pair)
				continue

			data = {'precision': market['precisionForPrice']}
			pair_service.register(pair, data)			

	def update_amm_pool_addresses(rest:"REST", pair_service:"PairService"):
		json_data = rest.get_amm_pools()
		for amm_pair in json.loads(json_data)['pools']:
			pair = amm_pair['market'].replace('AMM-', '')

			if pair_service.exists(pair):
				pair_service.update(pair, {'amm_address':amm_pair['address']})

	def order(rest:"REST", config:"Config", ts:"TickerService",
		SOO:"SestertiusOrderObject"):

		Payload = orders.Payload.create(SOO, config, ts)
		signed_payload, hashed_payload = EDDSA.sign_payload(
			Payload, config.private_key)
		Payload.eddsaSignature = signed_payload
		data = rest.post_order(json.dumps(Payload))
		print(json.loads(data))

class WSS:
	def ping(data, send):
		if data == 'ping':
			send('pong')
			return True
		return False

	def data(json_data, TMPOBS):
		data = json.loads(json_data)
		if 'data' not in data:
			raise NotImplementedError(f'"data" not found in {data}')

		if data['topic']['topic'] == 'orderbook':
			WSS._update_orderbook(data, TMPOBS)

		elif data['topic']['topic'] == 'ammpool':
			WSS._update_orderbook_amm(data, TMPOBS)

		raise NotImplementedError(data)
		
	def _update_orderbook(data, TMPOBS:"OrderbookService"):
		TMPOBS.ob(data)

	def _update_orderbook_amm(data, TMPOBS:"OrderbookService"):
		TMPOBS.ob_amm(data)


class EDDSA:
	def sign_payload(payload, key):
		signer = eddsa_aux.OrderEddsaSignHelper(key)
		hashed_payload = signer.hash(payload)
		signed_payload = signer.sign(payload)
		return signed_payload, hashed_payload

	def sign_url(key, url):
		# ??????????
		signer = eddsa_aux.UrlEddsaSignHelper(key)
		signer.sign(url)
