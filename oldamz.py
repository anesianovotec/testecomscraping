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
        produto_tags = soup.find_all('div', class_='s-result-item')
        for tag in produto_tags:
            # Use o método find para encontrar a tag p com a classe "preco" dentro de cada tag de produto
            img_tag = tag.find('img', class_='s-image')
            preco_tag = tag.find('span', class_='a-offscreen')
            link_tag = tag.find('a', class_='a-link-normal')
            descr_tag = tag.find('span', class_='a-size-base-plus')
            if img_tag and preco_tag and link_tag:
                # Acesse o texto dentro da tag de preço para obter o valor
                img = img_tag['src']
                link = 'https://www.amazon.com.br/' + link_tag['href']
                nome = descr_tag.text
                imagens.append(img)
                precos.append(preco_tag.text)
                links.append(link)
                nomes.append(nome)

                # Imprima o preço
                print("Imagem : ", img, ", Preco: ", preco_tag.text,
                      ", Link: ", link, ", descricao: ", nome)
            else:
                print("não encontrado alguma coisa para este produto.")

    try:
        idusuario = id
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
        data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime(
            '%Y/%m/%d %H:%M')
        print(data_e_hora_sao_paulo_em_texto)

        n = len(imagens)
        print("total produtos: ", n)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="scraping"
        )
        print("conectou")
        for x in range(n):
            print(x)
            mycursor = mydb.cursor()
            if (imagens[x] == None):
              img_produto = "sem_foto.png"
            else:
              img_produto = imagens[x]
              sql = "INSERT INTO coletaweb (idusuario, busca, link, descricao, preco, imagem, localbusca, datahora, logobusca) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
              val = (idusuario, busca, links[x], nomes[x], precos[x],
                   img_produto, local, data_e_hora_sao_paulo_em_texto, logo)
              mycursor.execute(sql, val)
              mydb.commit()
              print("X: ", x)
              print(mycursor.rowcount, "record inserted.")
    except NameError:
        print("Deu um erro")
    except:
        print("Erro desconhecido no banco de dados")


amazonBusca("1", "memória+ram")
