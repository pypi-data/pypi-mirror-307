import os
from SquidLibs.ErrorHandler import *


class TranslationManager:
    def __init__(self, language_code):
        from . import FileMan
        self.language_code = language_code
        self.translation_dir = f"{FileMan.paths['internals_path']}/lang/{self.language_code}"
        self.translations = {}

    def load_all_translation_files(self):
        """
        Load all translation files from the directory for the specified language.
        It loads any file that ends with `_translate.txt`.
        """
        # Construct the directory path for the current language dynamically

        if not os.path.isdir(self.translation_dir):
            raise FileNotFoundError(f"Language directory {self.translation_dir} not found.")
        else:
            print(self.translation_dir)
        # Loop through all files in the language directory
        for file_name in os.listdir(self.translation_dir):
            if file_name.endswith("_translate.txt"):
                self._load_translation_file(os.path.join(self.translation_dir, file_name))

    def _load_translation_file(self, file_path):
        """
        Internal method to load a single translation file and validate its language header.
        
        Args:
            file_path (str): The full path to the translation file.
        
        Raises:
            LanguageLabelMismatchError: If the language header in the file does not match the selected language.
            LanguageLabelGenericError: If the language header in the file is missing or invalid.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            # Check the first line for the language header
            first_line = file.readline().strip()

            if first_line.startswith('[',1) and first_line.endswith(']'):
                found_lang = first_line[2:-1]  # Extract the language code from brackets
                if found_lang != self.language_code:
                    raise ErrorHandler.LanguageLabelMismatchError(self.language_code, found_lang)
            else:
                raise ErrorHandler.GenericError(f"Missing or invalid language header in {file_path}. Found {first_line}.")

            # Load the rest of the translation key-value pairs
            for line in file:
                key, value = line.strip().split(';', 1)
                if value == '':
                    continue
                self.translations[key] = value

    def translate(self, key):
        """
        Translate the given key using the loaded translations.
        
        Args:
            key (str): The translation key to look up.
        
        Returns:
            str: The translated text, or the key itself if no translation is found.
        """
        return self.translations.get(key, key)

    def untranslate(self, value):
        """
        Untranslate the given value using the loaded translations.
        
        Args:
            value (str): The translation value to look up.
        
        Returns:
            key: The untranslated key, or the value itself if no translation is found.
        """
        if value.endswith(" -nt"): value = value[:-4]
        for key, val in self.translations.items():
            if value == val:
                return key
        return value

def setup_translation_manager(language_code="Default"):
    TransMan = TranslationManager(language_code)
    TransMan.load_all_translation_files()
    return TransMan