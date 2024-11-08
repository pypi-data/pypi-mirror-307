# smartdebugger/the_debugger.py

import functools
import inspect
import traceback
from datetime import datetime
from typing import Callable, Optional
from colorama import Fore, Style, init
from llms import LLM

# Inicializa colorama (necessário no Windows)
init()

class SmartDebugger:
    def __init__(
        self,
        lang: str = "pt",
        raises: bool = True,
        llm_api_key: str = "",
        model_name: str = "default-model",
        llm_type: str = "groqchat",  # 'groqchat' ou 'genai' como padrão
        custom_llm_fn: Optional[Callable] = None  # Função opcional para LLM personalizado
    ):
        """
        Inicializa o decorador SmartDebugger com integração da LLM flexível.

        Args:
            lang (str): Idioma para as mensagens de debug ('pt' ou 'en').
            raises (bool): Re-lança a exceção original.
            llm_api_key (str): Chave de API para uso do LLM.
            model_name (str): Nome do modelo a ser utilizado.
            llm_type (str): Tipo de LLM a ser utilizado ('groqchat', 'genai' ou 'openai').
            custom_llm_fn (Optional[Callable]): Função personalizada para inicializar um cliente LLM customizado.
        """
        
        self.lang = lang.lower()
        self.raises = raises
        self.llm = LLM(
            model_name=model_name,
            api_key=llm_api_key,
            llm_type=llm_type,
            custom_llm_fn=custom_llm_fn
        )
        self.messages = {
            "pt": {
                "analyzing": "🔍 Analisando erro...",
                "error_found": "❌ Erro encontrado em",
                "suggestion": "💡 Sugestão de correção:",
                "no_error": "✅ Nenhum erro encontrado."
            },
            "en": {
                "analyzing": "🔍 Analyzing error...",
                "error_found": "❌ Error found in",
                "suggestion": "💡 Correction suggestion:",
                "no_error": "✅ No errors found."
            }
        }

    def __call__(self, func: Callable) -> Callable:
        """
        Decorador que intercepta exceções, analisa erros com o LLM e oferece sugestões de correção.

        Args:
            func (Callable): Função a ser decorada.

        Returns:
            Callable: Função decorada com tratamento de exceção e análise de erros.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Captura o erro e o código fonte
                error_info = self._get_error_info(e)
                source_code = self._get_source_code(func)
                
                # Exibição de erro
                self._display_error(error_info)

                # Análise do LLM para sugestão de correção
                question = (
                    f"Erro encontrado:\n{error_info['error_message']}\n"
                    f"Tipo de erro: {error_info['error_type']}\n"
                    f"Código na linha {error_info['line']}:\n{source_code}\n"
                    "Qual seria uma sugestão de correção?"
                )
                llm_response = self.llm.get_response(question)
                
                # Log e exibição de sugestão
                self._log_error(error_info, source_code, llm_response)
                self._display_suggestion(llm_response)
                
                if self.raises:
                    raise

        return wrapper

    def _get_error_info(self, error: Exception) -> dict:
        """Extrai informações detalhadas do erro."""
        tb = traceback.extract_tb(error.__traceback__)
        return {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file': tb[-1].filename,
            'line': tb[-1].lineno,
            'function': tb[-1].name
        }

    def _get_source_code(self, func: Callable) -> str:
        """Obtém o código fonte da função."""
        return inspect.getsource(func)

    def _log_error(self, error_info: dict, source_code: str, llm_response: str):
        """Registra os logs em arquivos."""
        log_entry = (
            f"\n{'='*50}\n"
            f"Timestamp: {error_info['timestamp']}\n"
            f"Error Type: {error_info['error_type']}\n"
            f"Error Message: {error_info['error_message']}\n"
            f"File: {error_info['file']}\n"
            f"Line: {error_info['line']}\n"
            f"Function: {error_info['function']}\n"
            f"\nSource Code:\n{source_code}\n"
            f"\nTraceback:\n{error_info['traceback']}\n"
            f"\nLLM Analysis:\n{llm_response}\n"
            f"{'='*50}\n"
        )

        # Log mais recente
        with open("logging.txt", "w", encoding="utf-8") as f:
            f.write(log_entry)

        # Histórico completo
        with open("all_logging.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)

    def _display_error(self, error_info: dict):
        """Exibe o erro formatado no terminal."""
        msgs = self.messages[self.lang]
        print(f"{Fore.RED} {msgs['error_found']}: {Style.RESET_ALL}")
        print(f"{error_info['file']}:{error_info['line']} ")
        print(f"\n{Fore.YELLOW } {msgs['analyzing']}{Style.RESET_ALL}")
        print(f"{error_info['error_type']}: {error_info['error_message']}")
    
    def _display_suggestion(self,llm_response: str):
        msgs = self.messages[self.lang]
        print(f"\n {Fore.GREEN} {msgs['suggestion']} {Style.RESET_ALL}")
        print(llm_response)

 