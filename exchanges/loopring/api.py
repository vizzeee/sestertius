import requests
import websocket
import threading

class REST:
	def __init__(self, api_key, address, acc_id):
		self.base_url   = 'https://api3.loopring.io'
		self.api_key    = api_key
		self.user_addr  = address
		self.acc_id     = acc_id

	def _get_headers(self, address=False):
		headers = {
			'Accept'    : 'application/json',
			'X-API-KEY' : self.api_key
		}
		if address == True:
			headers['X-API-SIG'] = self.user_addr

		return headers

	def get_websocket_key(self):
		url = self.base_url + '/v3/ws/key'
		return requests.get(url, headers=self._get_headers()).text

	def get_markets(self):
		url = f'{self.base_url}/api/v3/exchange/markets'
		return requests.get(url).text

	def get_exchange(self):
		url = f'{self.base_url}/api/v3/exchange/info'
		return requests.get(url).text

	def get_account(self, address):
		url = f'{self.base_url}/api/v3/account?owner={address}'
		return requests.get(url).text

	def get_pair(self, pair):
		url = f'{self.base_url}/api/v3/ticker?market={pair}'
		return requests.get(url).text

	def get_amm_pools(self):
		url = f'{self.base_url}/api/v3/amm/pools'
		return requests.get(url).text

	def get_tokens(self):
		url = f'{self.base_url}/api/v3/exchange/tokens'
		return requests.get(url).text

	def get_user_balances(self):
		url = f'{self.base_url}/api/v3/user/balances?accountId={self.acc_id}'
		return requests.get(url, headers=self._get_headers()).text

	def get_next_storageid(self, tokenid, max=0):
		url = f'{self.base_url}/api/v3/storageId?accountId={self.acc_id}'
		url += f'&sellTokenId={tokenid}&maxNext={max}'
		return requests.get(url, headers=self._get_headers()).text

	def get_order_fee(self):# FIX ????????
		url = f'{self.base_url}/api/v3/user/orderFee?accountId='
		#url += '{}&market={}&tokenB={}&amountB={}'.format(userid, market/pair, tokenid, volume)

	def post_order(self, payload):
		url = f'{self.base_url}/api/v3/order'
		return requests.post(url, headers=self._get_headers(), json=payload).text

	def cancel_order(self, address, accid, orderhash):
		url = f'{self.base_url}/api/v3/order'
		payload = {'accountId': accid, 'orderHash': orderhash}
		return requests.delete(url, headers=self._get_headers(address=address), json=payload).text

	def get_order(self, accid, hash):
		url = f'{self.base_url}/api/v3/order?accountId={accid}&orderHash={hash}'
		return requests.get(url, headers=self._get_headers()).text

class WSS(threading.Thread):
	def __init__(self, callback):
		threading.Thread.__init__(self)
		self.host		= 'wss://ws.api3.loopring.io/v3/ws'
		self.callback	= callback

	def run(self, key):
		self.WSS	= websocket.WebSocketApp(
			self.host + f'?wsApiKey={key}',
			on_message 	= self.callback,
  			on_error	= self.callback
		)
		self.WSS.run_forever()

	def exit(self):
		self.WSS.close()

	def send(self, payload):
		self.WSS.send(payload)