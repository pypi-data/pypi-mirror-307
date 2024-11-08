# TheDebugger

TheDebugger é uma biblioteca Python que facilita a depuração de código utilizando modelos de linguagem avançados (LLMs). Ao aplicar o `SmartDebugger` como um decorador em funções, ele captura exceções, analisa erros com o auxílio de LLMs e fornece sugestões inteligentes para correção, tornando o processo de depuração mais eficiente e informativo.

## Recursos

- **Depuração Inteligente com Decoradores**: Aplique o `SmartDebugger` como um decorador para capturar e analisar erros automaticamente.
- **Integração com Diversos LLMs**: Por padrão, a biblioteca está configurada para o modelo `groq`, mas também suporta integração personalizada com outros LLMs como OpenAI.
- **Mensagens Coloridas**: Utiliza `colorama` para destacar erros e sugestões no terminal, melhorando a legibilidade.
- **Logging Avançado**: Registra detalhes dos erros e análises em arquivos de log para referência futura.

## Instalação

Instale o `thedebugger` diretamente do PyPI utilizando o `pip`:

```bash
pip install thedebugger
```

Ou instale a partir do repositório:

```bash
pip install git+https://github.com/seuusuario/thedebugger.git
```

## Requisitos

Este projeto depende das seguintes bibliotecas:

- `google-generativeai`
- `Pillow`
- `langchain-core`
- `langchain-groq`
- `openai`
- `colorama`

As dependências são automaticamente instaladas com o `pip install thedebugger`, mas você também pode instalar manualmente usando:

```bash
pip install google-generativeai Pillow langchain-core langchain-groq openai colorama
```

## Como Usar

### Inicialização Básica

Aqui está um exemplo de como utilizar o `SmartDebugger` como um decorador para capturar e analisar erros em uma função:

```python
from thedebugger.tools import SmartDebugger

# Inicializa o depurador
debugger = SmartDebugger(
    lang="pt",
    raises=False,
    llm_api_key="SUA_CHAVE_API",
    model_name="llama-3.1-70b-versatile",
    llm_type="groqchat",  # Tipos suportados: 'groqchat',
)

# Aplica o depurador como um decorador
@debugger
def divide(a: int, b: int) -> float:
    return a / b

# Teste da função decorada
try:
    resultado = divide(10, 0)
except:
    pass
```

### Uso com um LLM Personalizado

Você pode definir e utilizar um LLM personalizado, como o OpenAI, substituindo o `llm_type` padrão:

```python
import openai
from thedebugger.tools import SmartDebugger

def custom_openai_llm():
    openai.api_key = "SUA_API_KEY"
    
    class OpenAIWrapper:
        def generate_response(self, question):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}]
            )
            return response.choices[0].message['content']
    
    return OpenAIWrapper()

# Inicializa o depurador com o LLM personalizado
debugger = SmartDebugger(
    lang="pt",
    raises=False,
    llm_api_key="SUA_CHAVE_API",
    model_name="gpt-4",
    llm_type="openai",  # Tipo ajustado para usar OpenAI
    custom_llm_fn=custom_openai_llm
)

@debugger
def divide(a: int, b: int) -> float:
    return a / b

try:
    resultado = divide(10, 0)
except:
    pass
```

### Explicação dos Parâmetros

- **`lang`**: Define o idioma das mensagens de depuração (`"pt"` para português ou `"en"` para inglês).
- **`raises`**: Se `True`, re-lança a exceção original após a depuração.
- **`llm_api_key`**: Chave de API para autenticação no serviço de LLM.
- **`model_name`**: Nome do modelo de linguagem a ser utilizado.
- **`llm_type`**: Tipo de LLM a ser usado (`"groqchat"`, `"gemini"`, `"openai"` etc.).
- **`custom_llm_fn`**: Função opcional para inicializar um cliente LLM personalizado.

## Estrutura do Projeto

A seguir, a estrutura atualizada do projeto:

```
thedebugger/
├── thedebugger/
│   ├── __init__.py           # Inicializa o pacote
│   ├── llms.py               # Integração com modelos de linguagem
│   ├── tools.py              # Código principal do depurador (anteriormente the_debugger.py)
├── venv/
├── .gitignore
├── MANIFEST.in
├── README.md
├── requirements.txt
└── setup.py
```

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um _fork_ do repositório.
2. Crie uma _branch_ para sua feature ou correção:
    ```bash
    git checkout -b minha-feature
    ```
3. Faça o _commit_ das suas mudanças:
    ```bash
    git commit -m "Adicionei minha feature"
    ```
4. Envie para a _branch_ original:
    ```bash
    git push origin minha-feature
    ```
5. Abra um _pull request_ no GitHub.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Desenvolvido por **Saide Omar Saide** - [saideomarsaid@gmail.com](mailto:saideomarsaid@gmail.com)

---

## Notas Adicionais

- **Chave de API**: Certifique-se de manter suas chaves de API seguras e não compartilhá-las publicamente.
- **Customização**: O `SmartDebugger` foi projetado para ser flexível e pode ser adaptado para diferentes necessidades de depuração com diferentes LLMs.