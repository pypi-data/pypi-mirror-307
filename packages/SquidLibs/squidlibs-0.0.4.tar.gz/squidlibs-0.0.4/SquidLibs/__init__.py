__all__ = ['FileHelper', 'TranslationManager','ErrorHandler', 'windowMethods']
DEBUG = True

from .FileHelper import FileHelper  # Import FileHelper class
from .TranslationManager import setup_translation_manager  # Import setup function from TranslationManager

# Initialize instances or objects as needed
FileMan = FileHelper()
TransMan = setup_translation_manager()

from .ErrorHandler import ErrorHandler