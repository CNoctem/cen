from collections import defaultdict


class Args:
    COMMANDS = ['help', 'clone:1']

    def __init__(self):
        self.command = ''
        self.command_arg = ''
        self.command_dict = defaultdict(int)
        self.define_commands()
        self.injected_functions = {}

    def define_commands(self):
        for c in self.COMMANDS:
            pts = c.split(':')
            self.command_dict[pts[0]] = 0 if len(pts) == 1 else int(pts[1])

    def parse(self, args):
        for i in range(len(args)):
            a = args[i]
            if a in self.command_dict:
                num_args = self.command_dict[a]
                if num_args == 0:
                    self.run_command(a)
                else:
                    params = []
                    for j in range(num_args):
                        i += 1
                        params.append(args[i])
                    self.run_command(a, params=params)

    def run_command(self, cmd_name, *args, **kwargs):
        parameters = kwargs.get('params', None)
        if cmd_name not in self.command_dict:
            print('Unknown command: ', cmd_name)
        else:
            if hasattr(Args, cmd_name):
                method = getattr(Args, cmd_name)
                self.call_native(method, parameters)
            else:
                method = self.injected_functions[cmd_name]
                self.call_alien(method, parameters)

    def call_native(self, method, parameters):
        if parameters is not None:
            method(self, parameters)
        else:
            method(self)

    def call_alien(self, method, parameters):
        if parameters is not None:
            method(parameters)
        else:
            method()

    def inject(self, name, func, *args, **kwargs):
        num_args = kwargs.get('n_params', 0)
        self.COMMANDS.append(name + '' if num_args == 0 else ':' + str(num_args))
        self.injected_functions[name] = func
        self.define_commands()

    def help(self):
        print('HELP')

    def clone(self, params):
        print('Cloning', params[0])


if __name__ == '__main__':
    def foo():
        print('foo')


    a = Args()
    a.inject('foo', foo)
    a.parse(['clone', 'this', 'foo'])
