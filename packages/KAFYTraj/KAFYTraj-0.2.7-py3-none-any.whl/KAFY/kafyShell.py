import cmd
from os import path as os_path
from os import listdir as os_listdir

from readline import set_completer,parse_and_bind
from KAFY.commandsParser import parse_command


class KafyShell(cmd.Cmd):
    intro = "\n\n\n\n\nWelcome to the KAFYTraj shell. Type help or ? to list commands.\nKAFYTraj (c) 2024 Youssef Hussein, University of Minnesota. All rights reserved.\n"
    prompt = "kafy> "
    _hist = []

    def default(self, line):
        "Executes the given command using the command parser."
        try:
            print(line)
            parse_command(line)
        except ValueError as e:
            print(f"Command Error: {e}. Type 'help' for available commands.")

    def do_exit(self, arg):
        "Exit the shell"
        print("Exiting the KAFYTraj shell.")
        return True

    def do_history(self, arg):
        "Show command history."
        for i, cmd in enumerate(self._hist):
            print(f"{i}: {cmd}")

    def do_copyright(self, arg):
        """Display copyright information."""
        print(
            "KAFYTraj (c) 2024 Youssef Hussein, University of Minnesota. All rights reserved."
        )

    def do_credits(self, arg):
        """Display credits."""
        print("KAFYTraj was developed by Youssef Hussein with contributions from...")
        print("Special thanks to .....")

    def do_license(self, arg):
        """Display license information."""
        print(
            "This software is licensed under the MIT License.\n"
            "See the LICENSE file in the project repository for details."
        )

    def preloop(self):
        self._hist = []
        # Enable tab completion
        set_completer(self.path_completer)
        parse_and_bind("tab: complete")

    def postcmd(self, stop, line):
        self._hist.append(line)
        return stop

    def help_start_new_project(self):
        print("Start a new project: start new project <location>")

    def help_add_pretraining_data(self):
        print("Add pretraining data: add pretraining data from <data_location>")

    def help_add_model(self):
        print(
            "Add a model: add pretraining model <model_family> from <source> using <config_path> as <save_as_name>"
        )

    # def help_finetune_model(self):
    #     print(
    #         "Fine-tune a model: finetune <task> for <pretrained_model> using <config_path> with <output_name>"
    #     )

    # def help_summarize_data(self):
    #     print("Summarize data: summarize from <data_path> using <model_path>")

    def path_completer(self, text, state):
        "Autocomplete for file paths."
        if not text:
            text = "."
        directory, partial_filename = os_path.split(text)
        if not directory:
            directory = "."

        matches = [
            os_path.join(directory, f)
            for f in os_listdir(directory)
            if f.startswith(partial_filename)
        ]

        try:
            return matches[state]
        except IndexError:
            return None


def main():
    import sys

    if len(sys.argv) > 1:
        # If a command is provided, pass it directly to the parser
        command = " ".join(sys.argv[1:])
        try:
            parse_command(command)
        except ValueError as e:
            print(f"Command Error: {e}.")
            sys.exit(1)
    else:
        # If no command is provided, start the shell interface
        KafyShell().cmdloop()


if __name__ == "__main__":
    main()
