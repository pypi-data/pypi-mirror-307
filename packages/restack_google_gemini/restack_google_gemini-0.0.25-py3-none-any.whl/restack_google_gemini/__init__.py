# src/restackio/integrations/gemini/__init__.py
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .functions.generate_content import gemini_generate_content, GeminiGenerateContentInput
from .functions.chat.start_chat import gemini_start_chat, GeminiStartChatInput
from .functions.chat.send_message import gemini_send_message, GeminiSendMessageInput
from .functions.chat.get_history import gemini_get_history, GeminiGetHistoryInput
from .service import GeminiServiceOptions, GeminiServiceInput, gemini_service

__all__ = [
    'gemini_generate_content',
    'GeminiGenerateContentInput',
    'GeminiServiceOptions',
    'GeminiServiceInput',
    'gemini_service',
    'gemini_start_chat',
    'GeminiStartChatInput',
    'gemini_send_message',
    'GeminiSendMessageInput',
    'gemini_get_history',
    'GeminiGetHistoryInput'
]
