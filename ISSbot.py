
import time
import telepot
from telepot.loop import MessageLoop
from pprint import pprint

from datetime import datetime
import requests
import json
from pprint import pprint
from pytz import timezone


opcoes = '''
/iss - informações sobre a ISS
/loc - localização atual da ISS
/live - ISS ao vivo
/astros - pessoas na ISS
/prev - previsão de passagem da ISS
/sobre - desenvolvimento do bot
'''

info_sobre = '''
Esse bot foi desenvolvido com a finalidade de conduzir informações sobre a Estação Espacial Internacional, totalmente voluntário e sem finalidades financeiras 
'''


def info_iss(chat_id):
	bot.sendMessage(chat_id, '- Informações sobre a ISS 📡')
	bot.sendMessage(chat_id, 'https://pt.wikipedia.org/wiki/Esta%C3%A7%C3%A3o_Espacial_Internacional')
	#bot.setChatTitle(chat_id, 'Título')
	#bot.getLocation(chat_id)

def loc_iss(chat_id):
	bot.sendMessage(chat_id, '- Localização a ISS')
	#bot.sendPhoto(chat_id, "/iss_loc.PNG")
	#bot.sendPhoto(chat_id, photo=open('/iss_loc.PNG', 'rb'))
	#--------------------------- localizacao das coordenadas da ISS ----------------------------------------
	try:
		bot.sendMessage(chat_id, 'obtendo localização da estação espacial ...')

		loc = requests.get("http://api.open-notify.org/iss-now.json")
		loc = loc.json()

		if str(loc['message']) == 'success':
			print('✅ ISS localizada')
			bot.sendMessage(chat_id, '✅ ISS localizada')
			tempo = float(loc['timestamp'])
			tempo_uk = datetime.fromtimestamp(tempo)
			tempo = datetime.fromtimestamp(tempo, tz = timezone("America/Sao_Paulo"))
			latitude = float(loc['iss_position']['latitude'])
			longitude = float(loc['iss_position']['longitude'])

			data = str(tempo)[0:10]
			horario = str(tempo)[11:25]
			print('Horário: ', tempo)
			print('Localização da ISS - lat:',latitude, ' long:',longitude)
			bot.sendMessage(chat_id, 'Data: '+str(data))
			bot.sendMessage(chat_id, 'Horário: '+str(horario))
			bot.sendMessage(chat_id, 'Latitude: '+str(latitude)+'\n'+'Longitude: '+str(longitude))
			#bot.sendMessage(chat_id, 'Longitude: '+str(longitude))

			#bot.sendPhoto(chat_id, photo=open('/iss_loc.PNG', 'rb'))
			bot.sendLocation(chat_id, latitude, longitude)
			

		else:
			print('ISS não localizada')

		#--------------------------- localizacao da projeção da ISS no mundo ----------------------------------------
		try:
			url = 'http://open.mapquestapi.com/nominatim/v1/reverse.php?key=Ih1eaowjgCaw8xXvgSFGyv7yCjYMWcSD&format=json'
			url = url + '&lat='+str(latitude) + '&lon='+str(longitude)

			#url = 'http://open.mapquestapi.com/nominatim/v1/reverse.php?key=Ih1eaowjgCaw8xXvgSFGyv7yCjYMWcSD&format=json&lat=51.521435&lon=-0.16271'

			#print(url)

			reverse_loc = requests.get(url)
			reverse_loc = reverse_loc.json()

			bot.sendMessage(chat_id, 'obtendo localização da projeção da ISS no planeta ...')

			if 'error' in reverse_loc:
				print('🌏 OCEANO')
				bot.sendMessage(chat_id, '🌏 Oceano')


			else:
				print('🌎 TERRA')
				bot.sendMessage(chat_id, '🌎 Continente')
				#pprint(reverse_loc)

				pais = reverse_loc['address'] #Agrupa: [País, Sigla do país, estado]
				nome_pais = reverse_loc['display_name']

				#print(pais)
				#print(nome_pais)
				
				templist = []
				reverse_loc_list = []

				for key, value in reverse_loc.items():
					templist = [key, value]
					reverse_loc_list.append(templist)

				#print(reverse_loc_list)

				itens_locais = []
				for i in reverse_loc_list:
					if str(i[0]) == 'address':
						itens_locais.append(i)
					#if str(i[0]) == 'place_id':
					#	itens_locais.append(i)
					if str(i[0]) == 'display_name':
						itens_locais.append(i)
					#print(i[0])
				
				print(itens_locais)
				print('\n')

				print('\n\n\n')
				print(itens_locais[0][1])
				print('\n')
				print(itens_locais[1][1])

				bot.sendMessage(chat_id, (itens_locais[0][1]))

				dicio_detalhe_local = itens_locais[1][1]
				print(type(dicio_detalhe_local))

				print('\n\n\n')
				for key, value in dicio_detalhe_local.items():
					print(key+': '+value)
					detalhe_local = (key+': '+value+'\n')

				bot.sendMessage(chat_id, detalhe_local)
				print(detalhe_local)


				'''for i in itens_locais:
					aux = str(i[0])+': '+str(i[1])
					print(aux)
					bot.sendMessage(chat_id, aux)
				'''
			

		except Exception as e:
			print(e)


		#--------------------------- renderização da localização da ISS no mundo - Plano ----------------------------------------
		'''try:
			import datetime as dt
			import matplotlib.pyplot as plt
			import cartopy.crs as ccrs
			from cartopy.feature.nightshade import Nightshade


			#fig = plt.figure(figsize=(10, 5))
			fig = plt.figure()
			#fig.set_size_inches(5, 2.5) #--rápido---porém com pouca resolução
			#fig.set_size_inches(7.5, 3.75)
			plt.subplots_adjust(left=0, bottom=0.03, right=1, top=0.90, wspace=None, hspace=None)
			ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

			#print('tempo_uk: -----',str(tempo_uk))
			ano = str(tempo_uk)[0:4]
			mes = str(tempo_uk)[5:7]
			dia = str(tempo_uk)[8:10]
			hora = str(tempo_uk)[11:13]
			minuto = str(tempo_uk)[14:16]
			segundo = str(tempo_uk)[17:]

			date = dt.datetime(int(ano), int(mes), int(dia), int(hora), int(minuto), int(segundo))
			#date = datetime.datetime(1999, 12, 31, 12, 40, 55, 30)

			#ax.scatter(longitude, latitude)
			ax.scatter(longitude, latitude, marker='>', c='#05014a')
			ax.set_title('Posição da ISS em '+str(date))
			#ax.set_title('Position of ISS in {}, cidade'.format(date))
			ax.stock_img()
			#ax.add_feature(Nightshade(date, alpha=0.2))

			#plt.show()
			plt.savefig('iss_loc_plano.png')

			bot.sendPhoto(chat_id, photo=open('/iss_loc_plano.PNG', 'rb'))

		except Exception as e:
			print(e)


		#--------------------------- renderização da localização da ISS no mundo - Planeta----------------------------------------
		try:
			import datetime as dt
			import matplotlib.pyplot as plt
			import numpy as np

			import cartopy.crs as ccrs
			import cartopy.feature as cfeature


			ano = str(tempo_uk)[0:4]
			mes = str(tempo_uk)[5:7]
			dia = str(tempo_uk)[8:10]
			hora = str(tempo_uk)[11:13]
			minuto = str(tempo_uk)[14:16]
			segundo = str(tempo_uk)[17:]

			date = dt.datetime(int(ano), int(mes), int(dia), int(hora), int(minuto), int(segundo))
			#date = datetime.datetime(1999, 12, 31, 12, 40, 55, 30)

			fig = plt.figure()
			plt.subplots_adjust(left=0, bottom=0.03, right=1, top=0.90, wspace=None, hspace=None)
			ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(longitude, latitude))
			ax.scatter(longitude, latitude, transform=ccrs.Geodetic(), s=100, marker='>', c='#05014a')
			#ax.scatter(longitude, latitude, s=100,marker='>', c='#05014a')
			ax.set_title('Posição da ISS em '+str(date))

			ax.add_feature(cfeature.OCEAN, zorder=0)
			ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')

			ax.set_global()
			ax.gridlines()

			#plt.show()
			plt.savefig('iss_loc_planeta.png')
			bot.sendPhoto(chat_id, photo=open('/iss_loc_planeta.PNG', 'rb'))

		except Exception as e:
			print(e)
		'''

	except Exception as e:
		print(e)


def live_iss(chat_id):
	bot.sendMessage(chat_id, '- ISS ao vivo')
	bot.sendMessage(chat_id, 'Streams disponíveis da ISS ao vivo') 
	bot.sendMessage(chat_id, 'https://ustream.tv/channel/9408562') 
	bot.sendMessage(chat_id, 'http://ustream.tv/channel/17074538')

def astros_iss(chat_id):

	try:
		astro = requests.get("http://api.open-notify.org/astros.json")
		astro = astro.json()

		bot.sendMessage(chat_id, '- Astronautas na ISS')

		if str(astro['message']) == 'success':
			numero_astronautas = int(astro['number'])
			astronautas = astro['people']
			
			bot.sendMessage(chat_id, str(numero_astronautas)+' astronautas')

			pessoas = []

			for i in astronautas:
				if i['craft'] == 'ISS':
					pessoas.append(i['name'])
					bot.sendMessage(chat_id, str('👨‍🚀 ')+str(i['name']))

			
			print('Número de humanos na ISS: ', numero_astronautas)
			print('Astronautas: ', pessoas)

			#bot.sendMessage(chat_id, 'Atualmente a ISS tem:')
			
			#bot.sendMessage(chat_id, pessoas)
		
	except Exception as e:
		print(e)

def prev_iss(msg):
	(content_type, chat_type, chat_id) = telepot.glance(msg)
	usuario = msg['chat']['first_name']

	bot.sendMessage(chat_id, '- Previsão de passagem da ISS')

	print(content_type)
	if content_type == str('location'):
		latitude_atual = float(msg['location']['latitude'])
		longitude_atual = float(msg['location']['longitude'])
		localizacao_atual = [longitude_atual, latitude_atual]

		print('Sua posição atual é: ', localizacao_atual)
		bot.sendMessage(chat_id, 'Sua posição atual é: '+'\n'+'Latitude: '+str(latitude_atual)+'\n'+'Longitude: '+str(longitude_atual))

		try:
			url = "http://api.open-notify.org/iss-pass.json"
			url = url + "?lat=" + str(latitude_atual) + "&lon=" + str(longitude_atual)
			print(url)
			resp = requests.get(url)
			resp = resp.json()
			#pprint(resp)

			aux = []
			lista_previsao = []
			cont = 0
			duracao = []
			tempo_exposicao = []

			if resp['message'] == 'success':
				pprint(type(resp['response']))
				print(resp['response'])
				for i in resp['response']:
					#print(i['duration'])

					duracao.append(i['duration'])

					tempo = datetime.fromtimestamp(i['risetime'])
					#tempo = datetime.fromtimestamp(tempo, tz = timezone("America/Sao_Paulo"))
					tempo_exposicao.append(str(tempo))

				print(duracao)
				print(tempo_exposicao)

				bot.sendMessage(chat_id, 'Previsão de passagem da ISS nas coordenadas informadas:')
				bot.sendMessage(chat_id, 'Obsevação: A passagem é definida com 10° de altitude para o observador. Os tempos são calculados em UTC e o tempo em que o ISS está acima de 10° é em segundos.')

				for i in range(len(duracao)):
					bot.sendMessage(chat_id, '->'+str(tempo_exposicao[i])+' - '+str(duracao[i])+'s')


					#print(type(i))
					#for key, value in i.items():
					#	print(key, '-', value)
						#duracao.append(key)
						#tempo_exposicao.append(value)
						#print('\n')
				#print(duracao)
				#print(tempo_exposicao)
					#for key, value in i.items():
					#	aux = [key, value]
					#	lista_previsao.append(aux)

				#print(lista_previsao)
				#aux = []
				#for k in range(int(len(lista_previsao)/2)):
				#	aux.append(lista_previsao[k]+lista_previsao[k+1])

				#lista_previsao = aux
				#print(lista_previsao)
				#bot.sendMessage(chat_id,lista_previsao)

				#for key, value in 



		except Exception as error:
			print(error)

		




def sobre(chat_id):
	bot.sendMessage(chat_id, '- Sobre o desenvolvimento do bot')
	bot.sendMessage(chat_id, info_sobre)



def handle(msg):
	pprint(msg)

	(content_type, chat_type, chat_id) = telepot.glance(msg)
	#print(chat_id)
	print(content_type)
	print(chat_type)

	usuario = msg['chat']['first_name']
	tipo_entrada = str(content_type)


	if tipo_entrada == 'location':
		#bot.sendMessage(chat_id, 'Caso esteja tentando encontrar possíveis previsões da passagem da ISS na sua localização acesse o comando /prev')
		prev_iss(msg)

	if tipo_entrada == 'text':
		texto_entrada = msg['text']
	
		if texto_entrada == '/start':
			bot.sendMessage(chat_id, 'Olá '+str(usuario))
			bot.sendMessage(chat_id, 'Bem-vindo ao ISS Live, um bot com informações sobre a Estação Espacial Internacional. Aqui é disponibilizado algumas infomações relevantes da ISS, como atualizações em tempo-real de localização e posicionamento da estação, astronaltas e mídias')
			bot.sendMessage(chat_id, opcoes)

		elif texto_entrada == '/iss' or texto_entrada == 'iss' or texto_entrada == 'ISS' or texto_entrada == 'ISS':
			info_iss(chat_id)

		elif texto_entrada == '/loc' or texto_entrada == 'loc' or texto_entrada == '/LOC' or texto_entrada == 'LOC':
			loc_iss(chat_id)

		elif texto_entrada == '/live' or texto_entrada == 'live' or texto_entrada == '/LIVE' or texto_entrada == 'LIVE':
			live_iss(chat_id)

		elif texto_entrada == '/astros' or texto_entrada == 'astros' or texto_entrada == '/ASTROS' or texto_entrada == 'ASTROS':
			astros_iss(chat_id)

		elif texto_entrada == '/prev' or texto_entrada == 'prev' or texto_entrada == '/PREV' or texto_entrada == 'PREV':
			#prev_iss(msg)
			bot.sendMessage(chat_id, 'Envie a sua localização atual, através do GPS do seu dispositivo, para ser verificado previsão da passagem da ISS na sua região.')

		elif texto_entrada == '/sobre' or texto_entrada == 'sobre' or texto_entrada == '/SOBRE' or texto_entrada == 'SOBRE':
			sobre(chat_id)

		elif texto_entrada == 'dev':
			bot.sendMessage(chat_id, 'A3 é o meu dev <3')

		else:
			bot.sendMessage(chat_id,'\n Opções'+opcoes)

		print(texto_entrada)

		(content_type, chat_type, chat_id) = telepot.glance(msg)

		print('Chat:', content_type, chat_type, chat_id)





#hash_key = '1110882378:AAF1qnDty2S_GKYiiT_36Pjf4aq_WI_VTss'---------- Hash ISS_bot original
hash_key = '912653405:AAF3RL-fGnjc2Hc5-8mR4jt2Ie35KfYcGno' #----------Hash TuxBot-retirar!!!

bot = telepot.Bot(hash_key)


MessageLoop(bot, handle).run_as_thread()
print('Inicializado ...')

while True:
	time.sleep(10)