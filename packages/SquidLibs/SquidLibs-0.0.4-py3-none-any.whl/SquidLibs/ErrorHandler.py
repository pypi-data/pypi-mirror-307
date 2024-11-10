import sys, traceback, warnings
import tkinter as tk
from SquidLibs import DEBUG
from tkinter import messagebox

# from SquidLibs.windowMethods import show_error_popup,show_warning_popup
class ErrorHandler:
    # Custom Exceptions
    class GenericError(Exception):
        def __init__(self, message):
            self.message = message
        def __str__(self):
            return self.message

    class MismatchedSettingsError(GenericError):
        def __init__(self, message, mismatchedSetting):
            super().__init__(message)
            self.mismatchedSetting = mismatchedSetting

    class LanguageLabelGenericError(GenericError):
        def __init__(self, message):
            super().__init__(message)

    class LanguageLabelMismatchError(MismatchedSettingsError):
        def __init__(self, lang_code, found_lang):
            message = (
                f"Mismatched language found when loading translation files (Expected {lang_code} but found {found_lang})."
            )
            super().__init__(message, 'LanguageLabelMismatch')

    # Custom Warnings
    class GenericWarning(Warning):
        def __init__(self, message):
            self.message = message
        def __str__(self):
            return self.message

    class SettingsWarning(GenericWarning):
        def __init__(self, setting_name, message):
            super().__init__(message)
            self.setting_name = setting_name


    # Display popups for errors and warnings
    @staticmethod
    def show_error_popup(error_msg, title="Error"):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(title, error_msg)
        root.destroy()

    @staticmethod
    def show_warning_popup(warning_msg, title="Warning"):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showwarning(title, warning_msg)
        root.destroy()

    @staticmethod
    def show_cancelable_warning_popup(warning_msg, title="Warning"):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        accepted = messagebox.askokcancel(title, warning_msg)
        root.destroy()
        return accepted

    # Global exception handler
    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        base_msg = str(exc_value)
        error_message = f"{base_msg}\nPlease report this to the developers."
        
        if DEBUG:
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            traceback_msg = ''.join(formatted_traceback[:-1]) if len(formatted_traceback) > 1 else ''.join(formatted_traceback)
            error_message = f"{traceback_msg}\n{error_message}"

        error_title = exc_type.__name__
        ErrorHandler.show_error_popup(error_message, title=error_title)

    # Warning handler to handle custom warnings
    @staticmethod
    def handle_warning(message, category, filename, lineno, file=None, line=None):
        warning_msg = f"{category.__name__}: {message}\nIn {filename} at line {lineno}"
        ErrorHandler.show_warning_popup(warning_msg, title="Warning")
# Set the custom exception and warning handlers
sys.excepthook = ErrorHandler.handle_exception
warnings.showwarning = ErrorHandler.handle_warning