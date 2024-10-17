import re
from subprocess import Popen, PIPE
from random import random
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Docker:
    def kill_and_remove(self, ctr_name):
        command = ['docker', 'rm', '-f', ctr_name]
        try:
            self.execute(command)
            return True
        except RuntimeError as e:
            logger.error(f"Error removing container: {e}")
            return False

    def random_container_name(self, prefix):
        retstr = prefix + '-'
        for i in range(5):
            retstr += chr(int(round(random() * (122-97) + 97)))
        return retstr

    def get_container_ip(self, ctr_name):
        self.wait_for_container(ctr_name)
        command = ['docker', 'inspect',
                   '--format', '{{.NetworkSettings.IPAddress}}',
                   ctr_name]
        ip = re.sub(r'[^0-9.]*', '', self.execute(command))
        if not ip:
            raise RuntimeError(f"Could not get IP for container {ctr_name}")
        return ip

    def execute(self, command, dump_streams=False):
        logger.info("Running: " + ' '.join(command))
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        
        if p.returncode != 0:
            error_msg = err.decode('utf-8')
            logger.error(f"Command failed: {error_msg}")
            raise RuntimeError(error_msg)
            
        if dump_streams:
            logger.info(out.decode('utf-8'))
            logger.info(err.decode('utf-8'))
            
        return out.decode('utf-8')

    def start_container(self, container_name="", image="", cmd="", host=""):
        if not container_name or not image:
            raise ValueError("Container name and image are required")
            
        command = ['docker', 'run', '-d']
        if host:
            command.extend(['-h', host])
        command.extend(['--name', container_name, image])
        if cmd:
            command.extend(cmd.split())
            
        self.execute(command)

    def wait_for_container(self, ctr_name, max_retries=30):
        command = ['docker', 'inspect',
                   '--format', '{{.State.Status}}',
                   ctr_name]
                   
        for i in range(max_retries):
            try:
                status = re.sub(r'[^a-z]*', '', self.execute(command))
                logger.info(f"Container {ctr_name} status: {status}")
                
                if status == "running":
                    return True
                    
                if status == "exited":
                    logs_command = ['docker', 'logs', ctr_name]
                    logger.error(f"Container exited. Logs: {self.execute(logs_command)}")
                    return False
                    
                time.sleep(1)
                
            except Exception as e:
                logger.warning(f"Error checking container status: {e}")
                time.sleep(1)
                
        raise RuntimeError(f"Container {ctr_name} failed to start after {max_retries} attempts")
