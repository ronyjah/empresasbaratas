from selenium import webdriver
import csv
import time
import locale
import math 
diretorio="./"
locale.setlocale( locale.LC_ALL, '' )

def empresasBaratas():
	yearCurrent = '2019'
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--no-sandbox')
	prefs = {"download.default_directory" : diretorio}
	chrome_options.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(diretorio+'chromedriver',chrome_options=chrome_options)
	driver.set_window_position(-2000,0)
	driver.get("https://www.fundamentus.com.br/resultado.php?setor=")

	empresas = list()
	cotacao = list()
	precolucro = list()
	patliq = list()
	roe = list()
	empfiltradas = list()
	print('Pesquisando no site fundamentos as empresas mais baratas entre as 878. Aguarde')
	for index in range (1,878):		
		emp = driver.find_element_by_xpath('//*[@id="resultado"]/tbody/tr['+str(index)+']/td[1]/span/a').text
		empresas.append(emp)

		quote = driver.find_element_by_xpath('//*[@id="resultado"]/tbody/tr['+str(index)+']/td[2]').text
		cotacao.append(quote)
		
		precLuc = driver.find_element_by_xpath('//*[@id="resultado"]/tbody/tr['+str(index)+']/td[3]').text
		precolucro.append(locale.atof(precLuc))	

		pat = driver.find_element_by_xpath('//*[@id="resultado"]/tbody/tr['+str(index)+']/td[18]').text
		patliq.append(locale.atof(pat))

		indiceRoe_s = driver.find_element_by_xpath('//*[@id="resultado"]/tbody/tr['+str(index)+']/td[16]').text
		roe.append(locale.atof(indiceRoe_s[:-1]))

	print ('DONE. Listas criadas')
	print ('iniciando analise fundamentalista')
	for l in range(len(empresas)):
		#Definido p/l sem consulta bibliogrAfica
		if ((precolucro[l] > 2.5) and (precolucro[l] < 20.0)):
			if (patliq[l]>10000000.0):
				if (roe[l] >10.0):   
					empfiltradas.append(empresas[l])
	print ('DONE')
	print(' Listando empresas baratas. Aguarde:')
	for l in range(len(empfiltradas)):
		driver.get("https://www.fundamentus.com.br/detalhes.php?papel="+empfiltradas[l])

		lpa_s = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[3]/tbody/tr[2]/td[6]/span').text
		vpa_s = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[3]/tbody/tr[3]/td[6]/span').text
		preco_s = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[1]/tbody/tr[1]/td[4]/span').text
		ano = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[1]/tbody/tr[2]/td[4]/span').text
		yearLastquote = ano[6:10]


		
		lpa = locale.atof(lpa_s)
		vpa = locale.atof(vpa_s)
		preco = locale.atof(preco_s)


		precojusto = math.sqrt(22.5*vpa*lpa)
		# Definido 80%. Sem consulta bibliogrAfica
		if (preco < (0.8*precojusto)) and yearLastquote == yearCurrent:
			print(empfiltradas[l])


