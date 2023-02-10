#Bibliotecas utilizadas; (Necessário baixar "selenium")
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "" #IMPORTANTE: Insira o caminho o qual desejas baixar as imagens (deve ser a mesma pasta que está o WebDriver, "chromedriver.exe").

wd = webdriver.Chrome(PATH)

def pegar_imagens(wd, delay, max_images):
	def descer_tela(wd): #Fução para descer a tela enquanto procura pelas imagens
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Comando em JavaScript
		time.sleep(delay)

	url = "https://www.google.com/search?q=dogs&tbm=isch&ved=2ahUKEwjHpZ_76Pf8AhWjDtQKHahRDU0Q2-cCegQIABAA&oq=dogs&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIFCAAQgAQyBQgAEIAEMgQIABBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOggIABCABBCxAzoICAAQsQMQgwFQ1AhYwgxgmhFoAHAAeACAAXCIAfQDkgEDMy4ymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=QjDcY8f8MqOd0Aaoo7XoBA&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images: #Loop nas thumbnails de classe "Q4LuWd", até que se satisfaça o número de imagens requisitado.
		descer_tela(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd") #Procura por imagens de específica classe, "Q4LuWd".

		for img in thumbnails[len(image_urls) + skips:max_images]: #Esse "for" começa apartir da última imagem que foi "coletada", assim, impedindo que haja imagens repitidas.
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb") #Procura por imagens de específica classe, "n3VNCb"; Essa classe geralmente é reservada a imagens de maior resolução
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'): #Verifica se a div possui os atrigutos 'src' e 'http' e se sim, adiciona a 'image_urls'.
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, nome_arquivo):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content) #image_content é convertido em binário pelo 'BytesIO' 
		image = Image.open(image_file) #image_file é convertido em propriamente em uma imagem, utilizando a biblioteca 'PIL'.
		file_path = download_path + nome_arquivo

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Requisição Concluida")
	except Exception as e:
		print('ERRO -', e)

urls = pegar_imagens(wd, 1, 5)

for i, url in enumerate(urls):
	download_image("imgs/", url, str(i) + ".jpg") #Nomeia os arquivos baixados.

wd.quit()

#Código o qual utilizei como base para esse projeto: https://towardsdatascience.com/image-scraping-with-python-pegar_imagens