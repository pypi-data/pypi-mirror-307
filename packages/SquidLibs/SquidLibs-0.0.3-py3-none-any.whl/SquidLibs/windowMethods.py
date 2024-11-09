import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from SquidLibs import TransMan as tm

# -------------------- Window and Layout Creation --------------------
def create_window(title, sizeX, sizeY):
    """
    Create and return the main application window.
    
    Args:
        title (str): The window title.
        sizeX (int): Width of the window.
        sizeY (int): Height of the window.
        
    Returns:
        root (Tk): The created main window.
    """
    root = tk.Tk()
    root.title(tm.translate(title))
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Center the window
    center_x = int(screen_width / 2 - sizeX / 2)
    center_y = int(screen_height / 2 - sizeY / 2)
    root.geometry(f'{sizeX}x{sizeY}+{center_x}+{center_y}')
    root.resizable(True, True)
    
    return root

def create_notebook(parent):
    """
    Create and return a Notebook widget for adding tabs.
    
    Args:
        parent (Widget): The parent widget for the notebook.
        
    Returns:
        notebook (Notebook): The created Notebook widget.
    """
    return ttk.Notebook(parent)

def create_tab(notebook, title, icon=None):
    """
    Create and add a tab to the provided notebook widget.
    
    Args:
        notebook (Notebook): The notebook widget to add the tab to.
        title (str): The title of the tab.
        icon (PhotoImage): Optional icon for the tab.
    
    Returns:
        tab (Frame): The created tab frame.
    """
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=tm.translate(title), image=icon, compound='left' if icon else None)
    return tab

# -------------------- Widget Creation --------------------

def create_side_panel(parent, side='right', width=250, **kwargs):
    """
    Create and return a customizable static side panel.
    
    Args:
        parent (Widget): The parent widget for the side panel.
        side (str): Specifies which side to place the panel ('left' or 'right').
        width (int): Width of the side panel.
        kwargs: Additional styling options (e.g., bg for background color).
    
    Returns:
        side_panel (Frame): The created side panel.
    """
    side_panel = create_frame(parent, width=width, bg=kwargs.get('bg', 'lightgrey'))
    
    # Place the panel on the left or right side
    if side == 'right':
        side_panel.grid(row=0, column=1, sticky='ns')
    elif side == 'left':
        side_panel.grid(row=0, column=0, sticky='ns')

    return side_panel

def create_frame(parent, **kwargs):
    """
    Create and return a Frame widget.
    
    Args:
        parent (Widget): The parent widget for the frame.
        kwargs: Additional styling options.
    
    Returns:
        frame (Frame): The created Frame widget.
    """
    return tk.Frame(parent, **kwargs)

def create_label_frame(parent, label, **kwargs):
    """
    Create and return a Frame widget.
    
    Args:
        parent (Widget): The parent widget for the frame.
        kwargs: Additional styling options.
    
    Returns:
        frame (Frame): The created Frame widget.
    """
    return tk.LabelFrame(parent, text=tm.translate(label), **kwargs)

def create_button(parent, text, icon=None, **kwargs):
    """
    Create and return a Button widget with an optional icon.
    
    Args:
        parent (Widget): The parent widget for the button.
        text (str): The button text.
        icon (PhotoImage): Optional image to be displayed on the button.
        kwargs: Additional button options.
    
    Returns:
        button (Button): The created Button widget.
    """
    button = tk.Button(parent, text=tm.translate(text), image=icon, compound='left', **kwargs)
    return button

def create_label(parent, text, translate=True, **kwargs):
    """
    Create and return a Label widget.
    
    Args:
        parent (Widget): The parent widget for the label.
        text (str): The label text.
        kwargs: Additional label options.
    
    Returns:
        label (Label): The created Label widget.
    """
    if translate:
        return tk.Label(parent, text=tm.translate(text), **kwargs)
    else:
        return tk.Label(parent, text=text, **kwargs)
    

def create_checkbox(parent, text, state=None, var=None, cmd=None, **kwargs):
    """
    Create and return a Checkbutton (checkbox) widget.
    
    Args:
        parent (Widget): The parent widget for the checkbox.
        text (str): The checkbox text.
        variable (tk.Variable): The variable to bind the checkbox state.
        command (function, optional): The function to call when the checkbox is toggled.
        kwargs: Additional options for the Checkbutton.
    
    Returns:
        checkbox (tk.Checkbutton): The created Checkbutton widget.
    """
    return tk.Checkbutton(parent, text=tm.translate(text), state=state, variable=var, command=cmd, **kwargs)


def create_dropdown(parent, contents, **kwargs):
    """
    Create and return a dropdown (Combobox) widget.
    
    Args:
        parent (Widget): The parent widget for the dropdown.
        contents (list): List of options for the dropdown.
        kwargs: Additional dropdown options.
    
    Returns:
        dropdown (Combobox): The created Combobox widget.
    """
    dropdown = ttk.Combobox(parent, values=contents)
    dropdown.set(contents[0])  # Set default value
    dropdown.config(**kwargs)
    return dropdown

def create_listbox(parent, items=None, height=5, withScrollbar=True, **kwargs):
    """
    Create and return a Listbox widget with dynamic updating functionality.

    Args:
        parent (Widget): The parent widget for the listbox.
        items (list): List of items to populate the listbox.
        height (int): Number of visible rows in the listbox.
        withScrollbar (bool): Whether to add a vertical scrollbar to the listbox.
        kwargs: Additional listbox options.

    Returns:
        listbox (Listbox): The created Listbox widget.
        update_listbox (function): Function to update the listbox items.
    """
    # Create the Listbox widget
    listbox = tk.Listbox(parent, height=height, **kwargs)
    if items:
        for item in items:
            listbox.insert(tk.END, item)
    listbox.configure(selectmode=tk.SINGLE)

    def update_listbox(new_items):
        """Refresh the listbox contents with new items."""
        listbox.delete(0, tk.END)
        for item in new_items:
            listbox.insert(tk.END, item)

    # Add a scrollbar if requested
    if withScrollbar:
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=listbox.yview)
        listbox['yscrollcommand'] = scrollbar.set

        # Use .grid() for both listbox and scrollbar
        listbox.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')


    return listbox, update_listbox




def addSwitcherButtons(parent, selected_option, label1, label2, icon1=None, icon2=None, bg1='lightblue', bg2='lightgrey', font=('Arial', 12)):
    """
    Create two switcher buttons with a pressed-down effect.

    Args:
    - parent: The parent frame where the buttons will be added.
    - label1: Text for the first button.
    - label2: Text for the second button.
    - icon1: Optional icon for the first button.
    - icon2: Optional icon for the second button.
    - bg1: Background color for the selected button (default 'lightblue').
    - bg2: Background color for the unselected button (default 'lightgrey').
    - font: Font to use for the buttons (default Arial, size 12).
    """

    # Create a variable to track the selected option
    selected_option.set(tm.translate(label1))  # Default selection
    def update_selection(selected):
        """Update button styles based on the selection."""
        selected_option.set(tm.translate(selected))
        # Update button styles and relief based on which is selected
        if selected_option.get() == tm.translate(label1):
            button1.config(bg=bg1, relief='sunken')  # Pressed down appearance
            button2.config(bg=bg2, relief='raised')  # Raised appearance for unselected
        else:
            button1.config(bg=bg2, relief='raised')
            button2.config(bg=bg1, relief='sunken')

    # Create a frame for the buttons
    switcher_frame = create_frame(parent, bg='lightgrey')
    switcher_frame.grid(row=0, column=0, sticky='nsew')

    # Create the two switcher buttons
    button1 = create_button(switcher_frame, tm.translate(label1), icon=icon1, bg=bg1, width=12, height=2,  # Default selected
                            relief='sunken', font=font, command=lambda: update_selection(label1))
    button2 = create_button(switcher_frame, tm.translate(label2), icon=icon2, bg=bg2, width=12, height=2,
                            relief='raised', font=font, command=lambda: update_selection(label2))

    # Grid the buttons
    button1.grid(row=0, column=0, sticky='ew', padx=5, pady=5, ipadx=32, ipady=15)
    button2.grid(row=0, column=1, sticky='ew', padx=5, pady=5, ipadx=32, ipady=15)
    return switcher_frame  # Return the frame and the selected option

# -------------------- Status Bar and Progress Bar --------------------

def create_status_bar(parent):
    """
    Create and return a status bar with a status message area and hideable progress bar.
    
    Args:
        parent (Widget): The parent widget for the status bar.
    
    Returns:
        status_bar (Frame): The created status bar.
        update_status (function): Function to update the status message.
        show_progress_bar (function): Function to show the progress bar.
        hide_progress_bar (function): Function to hide the progress bar.
        update_progress (function): Function to update the progress bar value.
    """
    # Create the status bar frame
    status_bar = create_frame(parent, bd=1, relief=tk.SUNKEN)
    status_bar.grid(row=1, column=0, columnspan=2, sticky='ew')
    
    # Create label for status messages (left side)
    status_label = create_label(status_bar, text="", anchor='w')
    status_label.pack(side='left', fill='x', padx=5, pady=5, expand=True)
    
    # Create a progress bar (right side)
    progress_bar = ttk.Progressbar(status_bar, mode='determinate', length=150)
    progress_bar.pack(side='right', padx=5, pady=5)
    
    # Initially hide the progress bar
    progress_bar.pack_forget()

    # Define status and progress bar control functions
    def update_status(message, error=False):
        """Update the status message. Display in red if error=True."""
        status_label.config(text=tm.translate(message), fg='red' if error else 'black')
        
    def show_progress_bar():
        """Show the progress bar."""
        progress_bar.pack(side='right', padx=5, pady=5)

    def hide_progress_bar():
        """Hide the progress bar."""
        progress_bar.pack_forget()

    def update_progress(value):
        """Update the progress bar's value (0-100)."""
        progress_bar['value'] = value

    return status_bar, update_status, show_progress_bar, hide_progress_bar, update_progress


# -------------------- Icon Handling --------------------

def on_tab_changed(event, notebook, tab_icons):
    """Update icons when the tab changes."""
    selected_tab = event.widget.select()  # Get the selected tab
    for index, (unselected_icon, selected_icon) in enumerate(tab_icons):
        if notebook.index(selected_tab) == index:
            notebook.tab(index, image=selected_icon)  # Use selected icon
        else:
            notebook.tab(index, image=unselected_icon)  # Use unselected icon

def load_icons(image_path, size=(32, 32), split=False):
    """
    Load and resize image(s) for use in tkinter.
    
    Args:
        image_path (str): Path to the image file.
        size (tuple): Desired size of the icon after resizing (width, height).
        split (bool): Whether to split the image into two parts (for tabs).
    
    Returns:
        If split=False:
            - icon (PhotoImage): Resized image as a PhotoImage.
        If split=True:
            - unselected_icon (PhotoImage): Left half of the image, resized.
            - selected_icon (PhotoImage): Right half of the image, resized.
    """
    try:
        image = Image.open(image_path)

        if split:
            # Handle splitting the image for tabs
            icon_width, icon_height = image.size
            half_width = icon_width // 2

            # Crop unselected and selected icons
            unselected_icon_image = image.crop((0, 0, half_width, icon_height))
            selected_icon_image = image.crop((half_width, 0, icon_width, icon_height))

            # Resize icons if necessary
            unselected_icon_resized = unselected_icon_image.resize(size, Image.Resampling.LANCZOS)
            selected_icon_resized = selected_icon_image.resize(size, Image.Resampling.LANCZOS)

            return ImageTk.PhotoImage(unselected_icon_resized), ImageTk.PhotoImage(selected_icon_resized)
        else:
            # Resize the entire image if not splitting
            resized_image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
    
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None if not split else (None, None)
