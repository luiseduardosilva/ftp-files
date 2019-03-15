'''
	Enviar Arquivos via FTP 1.0
	By : LuisSilva 07/01/2019
	Python 3.x
'''
import ftplib, os, time, configparser
from datetime import datetime


# CONFIG.INI
config = configparser.ConfigParser()

# LISTA DE CONEXÕES
conexoes = []

def logo():
	return print('''\r
	 ________   _________   _______      ________   _____    _____      ________    ______   
	|_   __  | |  _   _  | |_   __ \    |_   __  | |_   _|  |_   _|    |_   __  | .' ____ \  
	  | |_ \_| |_/ | | \_|   | |__) |     | |_ \_|   | |      | |        | |_ \_| | (___ \_| 
	  |  _|        | |       |  ___/      |  _|      | |      | |   _    |  _| _   _.____`.  
	 _| |_        _| |_     _| |_        _| |_      _| |_    _| |__/ |  _| |__/ | | \____) | 
	|_____|      |_____|   |_____|      |_____|    |_____|  |________| |________|  \______.' 
				

					By : LuisSilva - 07/01/2019

	''')


# RETORNAR LISTA DE CONEXÕES
def getConexoes():
	return (conexoes)

# GERAR ARQUIVO CONFIG.INI PADRÃO
def criarIni():
	
	try:
		# CRIAR ARQUIVO
		cfgfile = open("config.ini",'w')
		
		# ADD CAMPOS
		config.add_section('Default')
		
		#`CONEXÃO FTP
		config.set('Default','host','127.0.0.1')
		config.set('Default','username', 'usuario')
		config.set('Default','password', 'teste')
		
		# DIRETORIO LOCAL
		config.set('Default','dir', '')
		
		# DIRETORIO FTP
		config.set('Default','remoto', '')
			
		config.write(cfgfile)
		cfgfile.close()

	except Exception as e:
		print(e)
		time.sleep(10)
try:
	config.read('config.ini')
	cont = 0
	
	for x in config.sections():
		b ={
			'host' 		: config[x]['host'],
			'username' 	: config[x]['username'],
			'password' 	: config[x]['password'],
			'dir' 		: config[x]['dir'],
			'remoto' 	: config[x]['remoto']}
		conexoes.append(b)
	
	if not (os.path.isfile('config.ini')):
		print("GERANDO CONFIG.INI PADRAO")
		criarIni()

except configparser.DuplicateOptionError:
	logo()
	print('CAMPO DUPLICADO EM CONFIG.INI')
	time.sleep(10)
	exit()
except Exception as e:
	raise (e)
	time.sleep(10)

# LOGO
logo()

# FTP == 0
if len(getConexoes()) == 0:
	print('NENHUMA CONEXÃO ENCONTRADA NO CONFIG.INI')
	time.sleep(10)
	exit()

# SERVIDORES
print(("%d SERVIDORES FTPs\n" %len(getConexoes())) if len(getConexoes()) > 1 else ("%d SERVIDOR FTP ENCONTRADO\n" %len(getConexoes())))

# DATA LOCAL
data = datetime.today().strftime('%Y-%m-%d')

try:
	for x in getConexoes():
		# FTP
		server 			= x['host']
		username 		= x['username']
		password 		= x['password']
		
		# PASTA LOCAL
		diretorio 		= x['dir']

		# PASTA FTP
		diretorio_ftp 	= x['remoto']

		# CONTADOR
		cont = 0

		if (not (os.path.exists(diretorio))):
			print('DIRETORIO NÃO EXISTE %s %s' %(diretorio, data))
			time.sleep(10)
			exit()
		try:
			ftp = ftplib.FTP(server, username, password)
			try:
				ftp.cwd(diretorio_ftp)
			except Exception as e:
				print('HOST: %s [OK]' %(x['host']))
				print("DIRETORIO REMOTO %s NÃO EXISTE" %diretorio_ftp)
				time.sleep(5)
				exit()
			print('HOST: %s\nDIRETORIO [OK] %s  %s ' %(x['host'], diretorio, data))
			for root, dirs, files in os.walk(diretorio, topdown=False):
					for name in files:
						data_arquivo = os.stat(os.path.join(root, name)).st_mtime
						data_arquivo = datetime.utcfromtimestamp(data_arquivo).strftime('%Y-%m-%d')
						if data_arquivo == data:
							with open((os.path.join(root, name)), 'rb') as f:
								ftp.storbinary('STOR %s' %name, f)
								f.close()
								cont += 1
			ftp.quit()
			print("ARQUIVOS ENVIADOS: %d\n" % cont)
		except ftplib.error_perm:
			print('LOGIN OU SENHA INCORRETO')
			time.sleep(10)
		except ftplib.socket.gaierror:
			print('HOST NÃO É VALIDO')
			time.sleep(10)
		except Exception as e:
			raise (e)
			time.sleep(10)
	input('PRESSIONE ENTER PARA SAIR')
except Exception as e:
	raise e
	time.sleep(10)