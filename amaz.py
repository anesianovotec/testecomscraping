import urllib3 
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime 
from pytz import timezone 

def amazonBusca(id, buscaproduto):
  
  http = urllib3.PoolManager() 
  busca = buscaproduto
  local = 'Amazon'
  logo = 'https://th.bing.com/th?id=ODLS.217e90ee-97e6-490d-91a9-4886074bb40f&w=32&h=32&qlt=90&pcl=fffffa&o=6&pid=1.2'
  url = 'https://www.amazon.com.br/s?k='+busca
  print(url)
  r = http.request('GET', url) 
  statusHTTP = r.status
  imagens = []
  precos = []
  links = []
  nomes = []
  if (statusHTTP == 200):
    soup = BeautifulSoup(r.data, 'html.parser') 
    for elem in soup:
      print(elem)
      item = soup.find('img', {'class':'s-image'})
      imagens.append(item['src'])
      print(item['src'])
      item = soup.find('span', {'class': 'a-price-whole'})
      prec = item.text.replace("R$", '')
      precos.append(prec)
      print(prec)
      item = soup.find('a', {'class': 'a-link-normal'})
      links.append('https://www.amazon.com.br' + item["href"])
      print('https://www.amazon.com.br' + item["href"])
      item = soup.find('span', {'class': 'a-text-normal'})
      nomes.append(item.text)
      print(item.text)
  else:
    print("Não encontrou mais nada no site")

  try:
    idusuario = id
    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%Y/%m/%d %H:%M')
    print(data_e_hora_sao_paulo_em_texto)
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="scraping"
    )
    n = len(imagens)
    for x in range(n):
      print(x)
      mycursor = mydb.cursor()
      if (imagens[x] == None):
        img_produto = "sem_foto.png"
      else:
        img_produto = imagens[x]
      sql = "INSERT INTO coletaweb (idusuario, busca, link, descricao, preco, imagem, localbusca, datahora, logobusca) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
      val = (idusuario, busca, links[x], nomes[x], precos[x], img_produto, local, data_e_hora_sao_paulo_em_texto, logo )
      mycursor.execute(sql, val)
      mydb.commit()
      print("X: ", x)
      print(mycursor.rowcount, "record inserted.")
  except NameError:
    print("Deu um erro")
  except:
    print("Erro desconhecido")


amazonBusca("1","memória+ram")