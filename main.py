import logging.config
from core import sestertius, sestertius_cli, utils

def configure_logging():
	config = utils.Config.load_yml('logging')
	logging.config.dictConfig(config)

def banner():
	text	= 'cAN dEvS DO soMEtHiNg???'
	version	= f'v{sestertius.__version__}'
	length	= 55
	padding	= ' ' * (length - (len(text) + len(version)))	
	print('\n'
		'                               __               __   _                   \n'
		'            _____ ___   _____ / /_ ___   _____ / /_ (_)__  __ _____      \n'
		'    ______ / ___// _ \ / ___// __// _ \ / ___// __// // / / // ___/______\n'
		'   /_____//__  //  __//__  // /_ /  __// /   / /_ / // /_/ //__  //_____/\n'
		'         /____/ \___//____/ \__/ \___//_/    \__//_/ \__,_//____/        \n'
		'       --=======================================================--      \n'
		f'         {text}{padding}{version}\n'
	)

def main():
	banner()
	configure_logging()

if __name__ == '__main__':
	main()