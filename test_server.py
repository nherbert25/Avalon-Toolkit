import unittest
import server

#https://www.youtube.com/watch?v=6tNS--WetLI
#https://www.youtube.com/watch?v=1Lfv5tUGsn8
#https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python

class Test_Process_Network_Command(unittest.TestCase):

    def setUp(self):
        self.Test_Server = server.Server()
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



    def test_process_network_command(self):
        #result = 5
        #self.assertEqual(result, 534)
        result = self.Test_Server.network_commands




        result['function1'] = function1
        result['function2'] = function2
        result['function3'] = function3

        print(result)


        # test_commands = [['function1'],
        #                 ['function2', 'nate', 'approve'],
        #                 ['function3', ['nate', 'frank', 'cat'],
        #                     3, 12341234, 'it works!!!!']]


        test_commands = [['function1'],
                        ['function2', 'nate', 'approve'],
                        ['function3', ['nate', 'frank', 'cat'],
                            3, 12341234, 'it works!!!!']]


        for command in test_commands:
            print(f"Processing command: {command}")
            self.Test_Server.process_network_command(command)

        


if __name__ == '__main__':
    unittest.main()
