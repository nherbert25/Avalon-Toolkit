import functools


class Test_class():

    def __init__(self) -> None:
        self.a = 'cat'
        self.b = 'dog'
        self.my_dict = {
            'function1': self.function1,
            'function2': self.function2,
            'function3': self.function3
        }

    def printing(self, a, b):
        # print(a)
        b = 37
        # print(b)
        # print(self.b)
        self.b = 45

    def print_b(self):
        print(self.b)

    def function1(self):
        print('function1')

    def function2(self, a, b):
        print('function2')
        print('function2', a, b)

    def function3(self, a, b, c, d):
        print(
            f'function3 testing \r\n testing first variable: {a} \r\n testing second variable: {b} \r\n testing third variable: {c} \r\n testing fourth variable: {d} \r\n ')

    # def process_network_command(command, arg*):
    #   send(dispatch[command](arg*))

    # function that takes the single list of arbitrary elements and seperates it into a command + variables, then sends that command to the corresponding function

    def process_network_command(self, command):
        if len(command) > 1:
            adaptive_func = self.my_dict[command[0]]
            for ele in command[1:]:
                print("testingasdfsadfasdfasdfasdfasd", command, ele)
                adaptive_func = functools.partial(
                    adaptive_func, ele)
            adaptive_func()
            return
        else:
            self.my_dict[command[0]]()


my_obj = Test_class()


# help(my_obj)


# my_obj.my_dict['function1']()
# my_obj.my_dict['function2']('cat', '4')
# my_obj.my_dict['function3']('meo', 234, 34, 12)


# client_board_state.client_queue.append(['!INITIAL_CONNECT', username])
# ['!INITIAL_CONNECT', username]
# ['!TEAMSELECT', client_board_state.selected_players]
# ['!VOTE', client_board_state.username, 'approve']


# it's coming in as a single list
# ['!DISCONNECT']
# ['!VOTE', 'nate', 'approve']
# ['!TEAMSELECT', ['nate', 'frank', 'cat']]


# function that takes the single list of arbitrary elements and seperates it into a command + variables, then sends that command to the corresponding function
# def process_network_command(command):
#    if len(command) > 1:
#        for ele in command[-1:]:
#            functools.partial(my_dict[command[0]], )
#    my_obj.my_dict[command[0]]()#


# testing
test_commands = [['function1'],
                 ['function2', 'nate', 'approve'],
                 ['function3', ['nate', 'frank', 'cat'],
                     3, 12341234, 'it works!!!!']]


for command in test_commands:
    print(f"Processing command: {command}")
    my_obj.process_network_command(command)
