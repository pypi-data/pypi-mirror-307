import os
import platform
import signal
import readchar
from tabulate import tabulate


class Menu:
    def __init__(self, insert_index=False, end_with_select=False):
        """
        Initialize the Menu instance.

        Parameters:
        insert_index (bool): Whether to insert the index of the selected option in the function call.
        end_with_select (bool): Whether to end the menu after an option is selected.
        """
        signal.signal(signal.SIGINT, self.__exit)
        if platform.system() == 'Darwin':  # macOS
            self.enter, self.command = ('\r', 'clear')
            self.exit = 'exit'
        elif os.name == 'nt':  # Windows
            self.enter, self.command = ('\r', 'cls')
        else:  # Linux and others
            self.enter, self.command = ('\n', 'clear')
        self.fluxo = {}
        self.__parameters = {}
        self.__selected_option = 0
        self.execute = True
        self.insert_index = insert_index
        self.end_with_select = end_with_select
        self.n_columns = 1

    def show(self):
        """
        Decorator to register a function in the menu.

        Parameters:
        name (str): The name to be used for the menu option.
        """
        def call(func):
            def wrapper(*args, **kwargs):
                self.fluxo[func.__name__] = func
                if func.__name__ not in self.__parameters.keys():
                    self.__parameters[func.__name__] = {'args': args, 'kwargs': kwargs}
                else:
                    raise ValueError(f"This name '{func.__name__}' has already exist")
            return wrapper
        return call
    
    def options_selecion(self,options:list[str])->str:
        """
        Menu of list of data that you want to select, that isn't callable

        Parameters:
        options list[str]: list of options to select

        Return:
        value selected on menu
        """
        selection = [None]
        self.insert_index = True
        self.end_with_select = True
        def option_selected(index):
            selection[0] = options[index]
        
        self.fluxo = {option:option_selected for option in options}
        self.__parameters = {option:{'args':[],'kwargs':{}} for option in options}
        self.start()
        return selection[0]

    def __menu(self):
        """
        Display the menu options in a formatted table.
        """
        os.system(self.command)
        controls = [
            ["W", "Move up"],
            ["A", "Move left"],
            ["S", "Move down"],
            ["D", "Move right"],
            ["Enter", "Select option"],
            ["Q", "Exit"]
        ]

        num_options = len(self.fluxo.keys())
        max_options_per_column = 6
        num_columns = (num_options + max_options_per_column - 1) // max_options_per_column

        # Create the table for the options
        options_table = [[] for _ in range(max_options_per_column)]
        options = list(self.__parameters.keys())

        for idx, option in enumerate(options):
            row = idx % max_options_per_column
            if idx == self.__selected_option:
                options_table[row].append(f"\033[1;37;42m[*] {option}\033[m")
            else:
                options_table[row].append(f"[ ] {option}")

        for row in options_table:
            while len(row) < num_columns:
                row.append("")

        combined_table = []
        for i in range(max(len(controls), len(options_table))):
            control_row = controls[i] if i < len(controls) else ["", ""]
            options_row = options_table[i] if i < len(options_table) else [""] * num_columns
            combined_table.append(control_row + ["|"] + options_row)

        # Print the combined table
        header_options = ["" for _ in range(num_columns)]
        print(tabulate(combined_table, headers=["Key", "Action"] + ["|"] + header_options, tablefmt="simple_grid"))

    def start(self):
        """
        Start the menu loop, allowing user interaction to select options.
        """
        num_options = len(self.__parameters.keys())
        max_options_per_column = 6
        num_columns = (num_options + max_options_per_column - 1) // max_options_per_column
        column_height = max_options_per_column

        if num_options > 0:
            while self.execute:
                self.__menu()
                key = readchar.readchar()
                if key == 'w':
                    self.__selected_option = (self.__selected_option - 1) % num_options
                elif key == 's':
                    self.__selected_option = (self.__selected_option + 1) % num_options
                elif key == 'a':
                    current_col = self.__selected_option // column_height
                    if current_col > 0:
                        self.__selected_option -= column_height
                    else:
                        self.__selected_option = (num_columns - 1) * column_height + (self.__selected_option % column_height)
                        if self.__selected_option >= num_options:
                            self.__selected_option = num_options - 1
                elif key == 'd':
                    current_col = self.__selected_option // column_height
                    if current_col < num_columns - 1:
                        self.__selected_option += column_height
                        if self.__selected_option >= num_options:
                            self.__selected_option = num_options - 1
                    else:
                        self.__selected_option %= column_height
                elif key == self.enter:
                    name = list(self.fluxo.keys())[self.__selected_option]
                    if self.insert_index:
                        self.fluxo[name](self.__selected_option, *self.__parameters[name]['args'], **self.__parameters[name]['kwargs'])
                        if self.end_with_select:
                            self.execute = False
                        if self.execute:
                            input("Any-> Voltar")
                    else:
                        self.fluxo[name](*self.__parameters[name]['args'], **self.__parameters[name]['kwargs'])
                        if self.end_with_select:
                            self.execute = False
                        if self.execute:
                            input("Any-> Voltar")
                elif key == 'q':
                    self.__exit()
        else:
            print("Remember to call the method to input on menu; this menu is empty.")

    def __exit(self):
        """
        Exit the menu and stop the execution loop.
        """
        self.execute = False
        os.system(self.command)