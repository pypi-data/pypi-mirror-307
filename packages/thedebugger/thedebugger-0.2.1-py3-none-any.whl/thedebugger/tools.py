# smartdebugger/toolspy
import functools
import inspect
import os
import traceback
from datetime import datetime
from typing import Callable, Optional
from colorama import Fore, Style, init
from thedebugger.llms import LLM

# Inicializa o colorama (necessário para cores no Windows)
init()

class SmartDebugger:
    def __init__(
        self,
        lang: str = "en",
        raises: bool = True,
        llm_api_key: str = "",
        model_name: str = "default-model",
        llm_type: str = "groqchat",  # 'groqchat' ou 'genai' como padrão
        custom_llm_fn: Optional[Callable] = None  # Função opcional para LLM personalizado
    ):
        """
        Inicializa o decorador SmartDebugger com integração da LLM flexível.

        Args:
            lang (str): Idioma para as mensagens de debug ('pt', 'en', etc.).
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
            custom_llm_fn=custom_llm_fn,
            lang=lang,
        )
        self.messages = {
            "pt": {
                "analyzing": "🔍 Analisando erro...",
                "error_found": "❌ Erro encontrado em",
                "suggestion": "💡 Sugestão de correção:",
                "no_error": "✅ Nenhum erro encontrado.",
                "prompt": "Qual seria uma sugestão de correção?"
            },
            "en": {
                "analyzing": "🔍 Analyzing error...",
                "error_found": "❌ Error found in",
                "suggestion": "💡 Correction suggestion:",
                "no_error": "✅ No errors found.",
                "prompt": "What would be a suggestion for correction?"
            },
            "es": {
                "analyzing": "🔍 Analizando error...",
                "error_found": "❌ Error encontrado en",
                "suggestion": "💡 Sugerencia de corrección:",
                "no_error": "✅ No se encontraron errores.",
                "prompt": "¿Cuál sería una sugerencia de corrección?"
            },
            "fr": {
                "analyzing": "🔍 Analyse de l'erreur...",
                "error_found": "❌ Erreur trouvée dans",
                "suggestion": "💡 Suggestion de correction:",
                "no_error": "✅ Aucun erreur trouvé.",
                "prompt": "Quelle serait une suggestion de correction?"
            },
            "de": {
                "analyzing": "🔍 Fehleranalyse...",
                "error_found": "❌ Fehler gefunden in",
                "suggestion": "💡 Korrekturvorschlag:",
                "no_error": "✅ Keine Fehler gefunden.",
                "prompt": "Was wäre ein Korrekturvorschlag?"
            },
            "it": {
                "analyzing": "🔍 Analizzando l'errore...",
                "error_found": "❌ Errore trovato in",
                "suggestion": "💡 Suggerimento di correzione:",
                "no_error": "✅ Nessun errore trovato.",
                "prompt": "Quale sarebbe un suggerimento di correzione?"
            },
            "ja": {
                "analyzing": "🔍 エラーを分析中...",
                "error_found": "❌ エラーが見つかりました:",
                "suggestion": "💡 修正の提案:",
                "no_error": "✅ エラーは見つかりませんでした。",
                "prompt": "修正の提案は何ですか？"
            },
            "ru": {
                "analyzing": "🔍 Анализ ошибки...",
                "error_found": "❌ Ошибка найдена в",
                "suggestion": "💡 Предложение по исправлению:",
                "no_error": "✅ Ошибок не обнаружено.",
                "prompt": "Какое было бы предложение по исправлению?"
            },
            "zh": {
                "analyzing": "🔍 分析错误...",
                "error_found": "❌ 错误发现于",
                "suggestion": "💡 修改建议:",
                "no_error": "✅ 未发现错误。",
                "prompt": "更正建议是什么？"
            },
            "ar": {
                "analyzing": "🔍 جاري تحليل الخطأ...",
                "error_found": "❌ تم العثور على خطأ في",
                "suggestion": "💡 اقتراح التصحيح:",
                "no_error": "✅ لم يتم العثور على أخطاء.",
                "prompt": "ما هو اقتراح التصحيح؟"
            },
            "hi": {
                "analyzing": "🔍 त्रुटि का विश्लेषण कर रहे हैं...",
                "error_found": "❌ त्रुटि मिली",
                "suggestion": "💡 सुधार का सुझाव:",
                "no_error": "✅ कोई त्रुटि नहीं मिली।",
                "prompt": "सुधार का सुझाव क्या होगा?"
            },
            "ko": {
                "analyzing": "🔍 오류 분석 중...",
                "error_found": "❌ 오류 발견 위치:",
                "suggestion": "💡 수정 제안:",
                "no_error": "✅ 오류가 없습니다.",
                "prompt": "수정 제안은 무엇입니까?"
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

                # Análise do LLM para sugestão de correção com pergunta personalizada
                msgs = self.messages.get(self.lang, self.messages["en"])
                question = (
                    f"Error found:\n{error_info['error_message']}\n"
                    f"Error type: {error_info['error_type']}\n"
                    f"Code on line {error_info['line']}:\n{source_code}\n"
                    f"{msgs['prompt']}"
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
            
            # Cria a pasta 'logs' se não existir
            os.makedirs("logs", exist_ok=True)
            
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
            with open("logs/logging.txt", "w", encoding="utf-8") as f:
                f.write(log_entry)

            # Histórico completo
            with open("logs/all_logging.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)


    def _display_error(self, error_info: dict):
        """Exibe o erro formatado no terminal."""
        msgs = self.messages.get(self.lang, self.messages["en"])
        print(f"{Fore.RED}{msgs['error_found']}: {Style.RESET_ALL}")
        print(f"{error_info['file']}:{error_info['line']} ")
        print(f"\n{Fore.YELLOW}{msgs['analyzing']}{Style.RESET_ALL}")
        print(f"{error_info['error_type']}: {error_info['error_message']}")
    
    def _display_suggestion(self, llm_response: str):
        """Exibe a sugestão de correção do LLM no terminal."""
        msgs = self.messages.get(self.lang, self.messages["en"])
        print(f"\n{Fore.GREEN}{msgs['suggestion']} {Style.RESET_ALL}")
        print(llm_response)
