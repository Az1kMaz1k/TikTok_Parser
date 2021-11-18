import requests
from bs4 import BeautifulSoup as BS
import json
import pandas as pd

#Создаем сессию
s=requests.Session()
s.headers.update({'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 OPR/75.0.3969.149'})

def user_not(nik):
	with open('user_not.txt','a') as f:
		f.write(nik+'\n')
		f.close

def tiktok_parser():
	#Переменная для хранения списка ников
	niks=[]
	#Переменные для ников
	uniqueId=[]
	#Переменная кол-во подписчиков
	followerCount=[]
	#Переменная кол-во видео
	videoCount=[]
	#Счетчик
	q=0
	#Для имени файлов
	a=1

	#Берем имя пользователя из списка
	with open('1.txt', 'r') as f:
		niks=f.readlines()
		f.close()

	for nik in niks:
		#Если проверили 100 человек записываем в файл
		if q==500:
			#Выгружаем все в excel файл
			df=pd.DataFrame({'Ник':uniqueId,
				'Подписчиков':followerCount,
				'Кол-во видео':videoCount})

			#Сохраняем на диске
			df.to_excel('tiktok_list'+str(a)+'.xlsx')
			print('Save '+str(q))
			#Переменные для ников
			uniqueId=[]
			#Переменная кол-во подписчиков
			followerCount=[]
			#Переменная кол-во видео
			videoCount=[]
			#Обнуляем счетчик
			q=0
			#Иттерируем а для имени
			a+=1
		print(nik)
		#Удаляем переход строки
		nik=nik.strip()
		#Получаем данные пользователя
		try:
			url='https://www.tiktok.com'+nik+'?lang=ru-RU'
			r=s.get(url)
			src=r.text
			q+=1
			#Скрамливаем bs4
			try:
				soup = BS(src, 'html.parser')
				data=soup.find('script', id='__NEXT_DATA__')
				data=str(data)
				data=data.replace('</script>','')
				data=data.split('>',1)
				data=json.loads(data[1])
				#Парсим данные
				#Если кол-во подписчиков меньше 1000
				try:
					if int(data['props']['pageProps']['userInfo']['stats']['followerCount'])<1000:
						user_not(nik)
						continue
				except Exception:
					print('follower - none')
					continue
				#Если кол-во видео в профиле меньше 10 идем дальше
				try:
					if int(data['props']['pageProps']['userInfo']['stats']['videoCount'])<10:
						#Запускаем функцию записи пользователя который не прошел проверку
						user_not(nik)
						continue
				except Exception:
					print('videoCount - none')
					continue	
				#Если последнее видео старше 1 недели идем дальше
				try:
					if int(data['props']['pageProps']['items'][0]['createTime'])<1632258000:
						#Запускаем функцию записи пользователя который не прошел проверку
						user_not(nik)
						continue
				except Exception:
					print('createTime - none')
					#Запускаем функцию записи пользователя который не прошел проверку
					user_not(nik)
					continue
				#Если просмотров видео больше 1000
				try:
					if int(data['props']['pageProps']['items'][4]['stats']['playCount'])<1000:
						#Запускаем функцию записи пользователя который не прошел проверку
						user_not(nik)
						continue
				except Exception:
					print('playCount 5 - none')
					#Запускаем функцию записи пользователя который не прошел проверку
					user_not(nik)
					continue
				try:
					if int(data['props']['pageProps']['items'][5]['stats']['playCount'])<1000:
						#Запускаем функцию записи пользователя который не прошел проверку
						user_not(nik)
						continue
				except Exception:
					print('playCount 6 - none')
					#Запускаем функцию записи пользователя который не прошел проверку
					user_not(nik)
					continue
			except Exception:
				print('Failed bs4')
				print(src)
				continue
		except Exception:
			print('User not found')
			#Запускаем функцию записи пользователя который не прошел проверку
			user_not(nik)
			continue
		uniqueId.append(url)
		followerCount.append(str(data['props']['pageProps']['userInfo']['stats']['followerCount']))
		videoCount.append(str(data['props']['pageProps']['userInfo']['stats']['videoCount']))
										
	#Выгружаем все в excel файл
	df=pd.DataFrame({'Ник':uniqueId,
		'Подписчиков':followerCount,
		'Кол-во видео':videoCount})

	#Сохраняем на диске
	df.to_excel('tiktok_list'+str(q)+'.xlsx')
	print('Save '+str(q))
	print('Jobs done')

if __name___ == "__main___":
	tiktok_parser()