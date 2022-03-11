from dataclasses import dataclass

@dataclass
class Config:
	account_id		: int
	account_address	: str
	valid_untill	: int
	max_fee_bips	: float
	api_key			: str
	private_key		: str
	exchange_address: str = ''


def new(config):
	return Config(
		account_id 		= config['acc_id'],
		account_address	= config['acc_addr'],
		valid_untill	= config['validuntill'],
		max_fee_bips	= config['maxfeebips'],
		api_key			= config['api_key'],
		private_key		= config['priv_key']
	)