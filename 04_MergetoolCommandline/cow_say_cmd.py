import argparse
import cmd
import shlex
import cowsay


class CowsayCmd(cmd.Cmd):
    intro = "Welcome to the interactive Cowsay shell. Type help or ? to list commands.\n"
    prompt = "(cowsay) "

    # Providing simple tab completion for certain fields
    # Note: Autocompletion for non-alphabetic characters may not work.
    eyes_options = ['oo', '00', 'OO', 'xx', '==', '$$']
    tongue_options = ['  ', 'U ', '++', '--', 'WW']
    cow_types = cowsay.list_cows()

    def do_list_cows(self, arg):
        'List available cowfiles: list_cows'
        print("\n".join(self.cow_types))

    def _parse_and_execute(self, line, command, action_fn):
        'Helper method to parse arguments and execute the cowsay commands'
        args = shlex.split(line)
        parser = argparse.ArgumentParser(prog=command)
        parser.add_argument('message', nargs='?', default='', help="Cow's message")
        parser.add_argument('--cow', default='default', help='Select cowfile')
        parser.add_argument('--eyes', default='oo', help='Select eyes')
        parser.add_argument('--tongue', default='  ', help='Select tongue')

        try:
            parsed_args = parser.parse_args(args)
            print(action_fn(parsed_args.message, cow=parsed_args.cow,
                            eyes=parsed_args.eyes, tongue=parsed_args.tongue))
        except SystemExit:
            pass  # argparse throws SystemExit on error; prevent this from closing the shell

    def do_cowsay(self, line):
        'Speak as a cow: cowsay message [--cow COW] [--eyes EYES] [--tongue TONGUE]'
        self._parse_and_execute(line, 'cowsay', cowsay.cowsay)

    def do_cowthink(self, line):
        'Think as a cow: cowthink message [--cow COW] [--eyes EYES] [--tongue TONGUE]'
        self._parse_and_execute(line, 'cowthink', cowsay.cowthink)

    def complete_eyes(self, text, line, begidx, endidx):
        if not text:
            return self.eyes_options
        else:
            return [option for option in self.eyes_options if option.startswith(text)]

    def complete_tongue(self, text, line, begidx, endidx):
        if not text:
            return self.tongue_options
        else:
            return [option for option in self.tongue_options if option.startswith(text)]

    def complete_cow(self, text, line, begidx, endidx):
        if not text:
            return self.cow_types
        else:
            return [option for option in self.cow_types if option.startswith(text)]

    def completedefault(self, text, line, begidx, endidx):
        if '--eyes' in line:
            return self.complete_eyes(text, line, begidx, endidx)
        elif '--tongue' in line:
            return self.complete_tongue(text, line, begidx, endidx)
        elif '--cow' in line:
            return self.complete_cow(text, line, begidx, endidx)
        return []

    def do_exit(self, line):
        'Exit the cowsay shell'
        print("Exiting the interactive cowsay shell.")
        return True  # This stops the Cmd application loop


if __name__ == '__main__':
    CowsayCmd().cmdloop()
