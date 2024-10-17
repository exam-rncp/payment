import os
import unittest
from util.Docker import Docker

class GoServices(unittest.TestCase):
    def test_go(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        code_dir = script_dir + "/.."
        go_path = os.environ['GOPATH']
        
        command = [
            'docker', 'run',
            '--rm',
            '-v', f"{go_path}:/go/",
            '-v', f"{code_dir}:/go/src/github.com/exam-rncp/payment",
            '-w', '/go/src/github.com/exam-rncp/payment',
            '-e', 'GOPATH=/go/',
            'golang:1.7',
            '/bin/sh', '-c', 'go test -v'
        ]

        docker = Docker()
        try:
            output = docker.execute(command, dump_streams=True)
        except RuntimeError as e:
            print(f"Error running tests: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main()