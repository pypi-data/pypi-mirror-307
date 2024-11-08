 
# LearnFetch

**LearnFetch** is a Python library designed to search and extract data from the 'Toda Matéria' website. It is useful for accessing information from articles and educational content programmatically.

## Installation

To install LearnFetch, use `pip`. Make sure you have Python 3.12.3 or higher installed.
```python
pip install LearnFetch
```
## Usage

### Importing the Library

To get started with the library, import the `Pesquisador` class:

```python
from learnfetch import Pesquisador
```

### Creating an Instance and Performing a Search

Create an instance of the `Pesquisador` class and use the `get_response` method to perform searches:

```python
# Creating an instance of the Pesquisador class
researcher = Pesquisador()

# Performing a search
results = researcher.get_response("Photosynthesis")

# Displaying the results
print(results)
```

### Package Structure

The package structure includes:

- **`learnfetch/`**: Directory containing the package with the `pesquisador.py` module.
  - **`__init__.py`**: File that makes the directory a Python package.
  - **`pesquisador.py`**: Contains the `Pesquisador` class with methods for searching and extracting data.

- **`tests/`**: Directory for unit tests.
  - **`__init__.py`**: File that makes the directory a Python package.
  - **`test_pesquisador.py`**: File containing tests for the `Pesquisador` class.

## Complete Example

Here is a complete example of using the library:

```python
from learnfetch import Pesquisador

# Criando uma instância da classe Pesquisador
pesquisador = Pesquisador()

# Realizando uma busca
resultados = pesquisador.get_response("Redes neurais")

# Pegando um determinado dicionário da lista (por exemplo, o segundo)
if len(resultados) > 1:
        segundo_dicionario = resultados[1] 

        # Pegando um valor específico dentro de um dicionário
        conteudo = segundo_dicionario.get("content")
        print("Conteudo do Segundo Dicionário:")
        print(conteudo)
```
# Another
```python
    from learnfetch import Pesquisador
    # O uso de docx é opcional, estou usando somente para desmostrar umas das utilidades da biblioteca
    from docx import Document

    # Criar uma instância da classe Pesquisador
    researcher = Pesquisador()

    # Realizar uma busca
    termo_de_busca = "Fotossíntese"
    resultados = researcher.get_response(termo_de_busca)

    # Função para criar uma ficha de leitura para cada item
    def adicionar_ficha_ao_documento(doc, titulo, conteudo):
        doc.add_heading('Ficha de Leitura', level=1)
        doc.add_heading('Título:', level=2)
        doc.add_paragraph(titulo)
        doc.add_heading('Resumo:', level=2)
        doc.add_paragraph(conteudo)
        doc.add_heading('Comentários:', level=2)
        doc.add_paragraph('Adicione aqui suas observações pessoais.')
        doc.add_heading('Questões levantadas:', level=2)
        doc.add_paragraph('Liste aqui as questões ou dúvidas surgidas durante a leitura.')
        doc.add_paragraph("\n" + "="*50 + "\n")

    # Criar um documento Word
    documento = Document()

    # Verificar se a chave 'results' está presente no dicionário retornado
    if resultados:
        # Iterar sobre cada item na lista de resultados
        for item in resultados:
            titulo = item.get('title', 'Título não encontrado')
            conteudo = item.get('content', 'Conteúdo não encontrado')
            adicionar_ficha_ao_documento(documento, titulo, conteudo)
    else:
        print("Nenhum resultado encontrado.")

    # Salvar o documento
    nome_arquivo = f'ficha sobre {termo_de_busca}.docx'
    documento.save(nome_arquivo)
    print(f"As fichas de leitura foram salvas no arquivo {nome_arquivo}.")
```
## Contributing

If you would like to contribute to the project, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/SaideOmaer1240/LearnFetch).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, you can reach out to:

- **Author**: Saíde Omar Saíde
- **Email**: saideomarsaideleon@gmail.com
 

### Explanation of Sections:

1. **Introduction**: Describes the purpose of the library.
2. **Installation**: Instructions for installing the library using pip.
3. **Usage**: Examples of how to import, create an instance, and use the library.
4. **Package Structure**: Explains the structure of the package directories and files.
5. **Complete Example**: A detailed example of how to use the library.
6. **Contributing**: Information on how to contribute to the project.
7. **License**: Details about the project license.
8. **Contact**: Contact information for support and suggestions.

Make sure to adjust the content as needed to reflect the specifics of your project.