import google.generativeai as genai 
import PIL.Image
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class LLM:
    def __init__(self, model_name: str, api_key: str, llm_type: str = "groqchat", custom_llm_fn=None):
        """
        Classe base para integração com diferentes LLMs, incluindo suporte para LLMs personalizados.

        Args:
            model_name (str): Nome do modelo a ser utilizado.
            api_key (str): Chave de API para autenticação no serviço de LLM.
            llm_type (str): Tipo de LLM para utilizar ('groqchat', 'genai' ou outro).
            custom_llm_fn (callable): Função personalizada que inicializa um cliente LLM customizado.
                                      A função deve retornar um objeto LLM que implemente o método `generate_response`.
        """
        self.api_key = api_key
        self.model = model_name
        self.llm_type = llm_type.lower()
        self.system_msg = (
            "Observe a imagem fornecida e extraia estritamente o texto contido nela. "
            "Retorne apenas o texto como está na imagem, sem adicionar, interpretar ou modificar qualquer parte. "
            "Todo o conteúdo deve ser copiado exatamente como aparece."
        )
       
    
        # Configura o cliente LLM, usando uma função personalizada se fornecida
        if custom_llm_fn:
            self.llm_client = custom_llm_fn()
        elif self.llm_type == "groqchat":
            self.llm_client = self._initialize_groqchat()
        elif self.llm_type == "genai":
            self.llm_client = self._initialize_genai()
        else:
            raise ValueError("Tipo de LLM inválido ou custom_llm_fn ausente. Use 'groqchat', 'genai' ou forneça custom_llm_fn.")

    def _initialize_groqchat(self):
        """Inicializa o cliente padrão para ChatGroq."""
        parser = StrOutputParser()
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    'Você é uma IA chamada The debugger, você responde perguntas com respostas simples e sem brincadeiras.\nSe caso o usuário pedir um código, deve escrever neste formato:\n```linguagem\n código \n```:\nExemplo: ```python\n print("Olá, Mundo!")\n```\n```javascrip \nconsole.log("Olá, Mundo!");\n``` \n',
                ),
                ("human", "{question}"),
            ]
        )
        llm_groq = ChatGroq(temperature=0, groq_api_key=self.api_key, model_name=self.model)
        chain = prompt_template | llm_groq| parser
        return chain

    def _initialize_genai(self):
        """Configura o cliente padrão para o Google GenAI."""
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(model_name=self.model)

    def get_response(self, question: str) -> str:
        """
        Gera uma resposta para a pergunta, utilizando o modelo configurado.

        Args:
            question (str): Pergunta para o modelo.

        Returns:
            str: Resposta do modelo de linguagem.
        """
        try:
            # Verifica o tipo de LLM e usa o método apropriado
            if hasattr(self.llm_client, 'generate_content'):
                response = self.llm_client.generate_content([self.system_msg, question])
                return response.text
            elif hasattr(self.llm_client, 'invoke'):
                response = self.llm_client.invoke(question)
                return response
            else:
                response = self.llm_client.generate_response(question)
                return response
        except Exception as e:
            print(f"Erro ao obter resposta: {e}")
            return "Erro ao processar a solicitação."

    def get_response_genai(self, image_path: str) -> str:
        """
        Processa uma imagem e utiliza o modelo de linguagem Google GenAI para extrair texto.
        Disponível apenas para o tipo de LLM 'genai'.

        Args:
            image_path (str): Caminho para a imagem a ser processada.

        Returns:
            str: Texto extraído da imagem.
        """
        if self.llm_type != "genai" and not isinstance(self.llm_client, genai.GenerativeModel):
            raise ValueError("get_response_genai só está disponível para o tipo de LLM 'genai'")
        
        try:
            img = PIL.Image.open(image_path)
            response = self.llm_client.generate_content([self.system_msg, img])
            return response.text
        except Exception as e:
            print(f"Erro ao obter resposta: {e}")
            return "Erro ao processar a solicitação."
