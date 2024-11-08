import requests as req
from bs4 import BeautifulSoup as bs  

class Pesquisador:
    """
    Classe Pesquisador para realizar buscas no site 'Toda Matéria' e extrair informações relevantes.

     Métodos:
        get_response(query: str) -> list:
            Realiza a busca no site 'Toda Matéria' usando a consulta fornecida e retorna os dados encontrados.
    Exemplo:
     .. code-block:: python
            from learnfetch import Pesquisador
            # Criar uma instância da classe Pesquisador
            researcher = Pesquisador()

            # Realizar uma busca
            termo_de_busca = input("Insira o termo de busca: ")
            resultados = researcher.get_response(termo_de_busca)
            # Verificar se a chave 'results' está presente no dicionário retornado
            if resultados:
                # Iterar sobre cada item na lista de resultados
                for item in resultados:
                    titulo = item.get('title', 'Título não encontrado')
                    conteudo = item.get('content', 'Conteúdo não encontrado')
                    print(f"Título: {titulo}")
                    print(f"Conteúdo: {conteudo}")
            else:
                print("Nenhum resultado encontrado.") 




    
    """

    def __init__(self):
        """
        Inicializa uma instância da classe Pesquisador com a URL base e o domínio do site 'Toda Matéria'.
        """
        self.url = 'https://www.todamateria.com.br/?s='
        self.domain = 'https://www.todamateria.com.br'
        self.text = ''
        self.dados = []
        
    def get_response(self, query: str) -> list:
        """
        Realiza a busca no site 'Toda Matéria' usando a consulta fornecida.

        Args:
            query (str): Termo de busca a ser utilizado.

        Returns:
            list: Uma lista de dicionários contendo os dados extraídos dos resultados da busca.

        Exceções:
            Em caso de erro nas requisições HTTP ou ao acessar o conteúdo das páginas, mensagens de erro são impressas no console.
        """
        url = f'{self.url}{query}'
        res = req.get(url)
        
        if res.status_code == 200:
            print("Dados encontrados com sucesso!")
            soup = bs(res.content, 'html.parser')
            all_data = soup.find_all('a', class_='card-item')
            
            for data in all_data:
                try:  
                    link = data['href']
                    title = data['title']
                    urlpattern = f'{self.domain}{link}'
                    acessando = f'Acessando o link "{urlpattern}" ...'
                    print(acessando)
                    response = req.get(urlpattern)
                    
                    if response.status_code == 200:
                        acessado = 'Link acessado com sucesso!'
                        print(acessado)
                        try:
                            soup = bs(response.content, 'html.parser')
                            
                            content_wrapper = soup.find('div', class_='content-wrapper')
                            if content_wrapper:
                                try:
                                    contents = content_wrapper.find_all(['p', 'figure']) 
                                    
                                    self.text += f'Pesquisar sobre: {title}\n {acessando} \n {acessado} \n \n'
                                    
                                    if contents:
                                        for content in contents:
                                            try:
                                                p = content.text.strip()
                                                self.text += p + '\n'
                                                try:
                                                    img = content.find('img')
                                                    # Verifica se há uma imagem correspondente para este parágrafo
                                                    if img:
                                                        img_src = img.get('src')
                                                        print('Imagem encontrada!')
                                                except:
                                                    img_src = 'null'
                                                
                                                try:
                                                    figcaption = content.find('figcaption')
                                                    fig = figcaption.text
                                                    self.text += f'[{fig}: {img_src}]\n'
                                                except:
                                                    figcaption = 'null'
                                                
                                            
                                            except:
                                                print('Erro ao pegar o parágrafo novo!')
                                            
                                            
                                             
                                                    
                                        self.dados.append({"title": title, "content": self.text})
                                        self.text = ''
                                    else:
                                        print('Nenhum parágrafo encontrado!')
                                except:
                                    print('Erro ao pegar o conteúdo!')
                            else:
                                print('Nenhum conteúdo encontrado!')
                            
                        except:
                            print('Erro ao acessar o conteúdo do artigo')
                except:
                    print('Erro ao obter o link:')
        else:
            print(f'Erro ao obter os dados: {res.status_code}')
        
        return self.dados 

