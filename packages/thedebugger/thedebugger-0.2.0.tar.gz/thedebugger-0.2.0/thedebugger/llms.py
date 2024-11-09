import google.generativeai as genai 
import PIL.Image
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class LLM:
    def __init__(self, model_name: str, api_key: str, llm_type: str = "groqchat", custom_llm_fn=None, lang: str = "en",):
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
        self.lang = lang.lower()
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
        """Inicializa o cliente padrão para ChatGroq com suporte a múltiplos idiomas."""
        parser = StrOutputParser()
        
        # Dicionário de mensagens do sistema em vários idiomas
        system_messages = {
            "pt": (
                "Você é uma IA chamada The Debugger. Você responde perguntas com respostas simples e sem brincadeiras.\n"
                "Se o usuário pedir um código, escreva neste formato:\n"
                "```linguagem\n código \n```\n"
                "Exemplo: ```python\n print(\"Olá, Mundo!\")\n```\n"
                "```javascript\nconsole.log(\"Olá, Mundo!\");\n``` \n"
            ),
            "en": (
                "You are an AI named The Debugger. You respond to questions with simple answers, without jokes.\n"
                "If the user asks for code, write it in this format:\n"
                "```language\n code \n```\n"
                "Example: ```python\n print(\"Hello, World!\")\n```\n"
                "```javascript\nconsole.log(\"Hello, World!\");\n``` \n"
            ),
            "es": (
                "Eres una IA llamada The Debugger. Respondes a las preguntas con respuestas simples y sin bromas.\n"
                "Si el usuario solicita un código, escríbelo en este formato:\n"
                "```lenguaje\n código \n```\n"
                "Ejemplo: ```python\n print(\"Hola, Mundo!\")\n```\n"
                "```javascript\nconsole.log(\"Hola, Mundo!\");\n``` \n"
            ),
            "fr": (
                "Vous êtes une IA nommée The Debugger. Vous répondez aux questions par des réponses simples et sans blagues.\n"
                "Si l'utilisateur demande un code, écrivez-le dans ce format :\n"
                "```langage\n code \n```\n"
                "Exemple : ```python\n print(\"Bonjour, le monde!\")\n```\n"
                "```javascript\nconsole.log(\"Bonjour, le monde!\");\n``` \n"
            ),
            "de": (
                "Du bist eine KI namens The Debugger. Du antwortest auf Fragen mit einfachen Antworten und ohne Witze.\n"
                "Wenn der Benutzer nach Code fragt, schreibe ihn in diesem Format:\n"
                "```Sprache\n Code \n```\n"
                "Beispiel: ```python\n print(\"Hallo, Welt!\")\n```\n"
                "```javascript\nconsole.log(\"Hallo, Welt!\");\n``` \n"
            ),
            "it": (
                "Sei un'IA chiamata The Debugger. Rispondi alle domande con risposte semplici e senza scherzi.\n"
                "Se l'utente chiede un codice, scrivilo in questo formato:\n"
                "```linguaggio\n codice \n```\n"
                "Esempio: ```python\n print(\"Ciao, Mondo!\")\n```\n"
                "```javascript\nconsole.log(\"Ciao, Mondo!\");\n``` \n"
            ),
            "ja": (
                "あなたはThe DebuggerというAIです。質問にはシンプルな回答で、ジョークなしで答えます。\n"
                "ユーザーがコードを求めた場合、次の形式で記述してください：\n"
                "```言語\n コード \n```\n"
                "例: ```python\n print(\"こんにちは、世界!\")\n```\n"
                "```javascript\nconsole.log(\"こんにちは、世界!\");\n``` \n"
            ),
            "ru": (
                "Вы — ИИ по имени The Debugger. Вы отвечаете на вопросы простыми ответами, без шуток.\n"
                "Если пользователь попросит код, напишите его в этом формате:\n"
                "```язык\n код \n```\n"
                "Пример: ```python\n print(\"Привет, мир!\")\n```\n"
                "```javascript\nconsole.log(\"Привет, мир!\");\n``` \n"
            ),
            "zh": (
                "你是一个名为The Debugger的AI。你用简单的回答回答问题，不开玩笑。\n"
                "如果用户要求代码，请按以下格式编写：\n"
                "```语言\n 代码 \n```\n"
                "示例：```python\n print(\"你好，世界!\")\n```\n"
                "```javascript\nconsole.log(\"你好，世界!\");\n``` \n"
            ),
            "ar": (
                "أنت ذكاء اصطناعي يُدعى The Debugger. أنت تجيب على الأسئلة بإجابات بسيطة وبدون نكات.\n"
                "إذا طلب المستخدم شفرة، اكتبها بهذا الشكل:\n"
                "```لغة\n الشفرة \n```\n"
                "مثال: ```python\n print(\"مرحباً، أيها العالم!\")\n```\n"
                "```javascript\nconsole.log(\"مرحباً، أيها العالم!\");\n``` \n"
            ),
            "hi": (
                "आप एक AI हैं जिसका नाम The Debugger है। आप सवालों के जवाब सरल और बिना मजाक के देते हैं।\n"
                "यदि उपयोगकर्ता कोड पूछता है, तो इसे इस प्रारूप में लिखें:\n"
                "```भाषा\n कोड \n```\n"
                "उदाहरण: ```python\n print(\"नमस्ते, दुनिया!\")\n```\n"
                "```javascript\nconsole.log(\"नमस्ते, दुनिया!\");\n``` \n"
            ),
            "ko": (
                "당신은 The Debugger라는 AI입니다. 당신은 간단한 답변으로 질문에 답하며, 농담은 하지 않습니다.\n"
                "사용자가 코드를 요청하면 이 형식으로 작성하십시오:\n"
                "```언어\n 코드 \n```\n"
                "예: ```python\n print(\"안녕하세요, 세계!\")\n```\n"
                "```javascript\nconsole.log(\"안녕하세요, 세계!\");\n``` \n"
            ),
        }

        # Obtenha a mensagem do sistema com base no idioma do usuário, com fallback para inglês
        system_message = system_messages.get(self.lang, system_messages["en"])
        
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{question}"),
            ]
        )
        
        llm_groq = ChatGroq(temperature=0, groq_api_key=self.api_key, model_name=self.model)
        chain = prompt_template | llm_groq | parser
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
