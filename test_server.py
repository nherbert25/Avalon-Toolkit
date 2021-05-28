import unittest
import server


class Test_Server(unittest.TestCase):

    def test_process_network_command(self):
        result = 5
        self.assertEqual(result, 534)


if __name__ == '__main__':
    unittest.main()
