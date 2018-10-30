import config
import spur
import logging
from logging import Logger

class Docker():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    def run_cmd(self, cmd, interactive = True):
        try:
            logging.info(cmd)
            logging.info(config.CONFIG['host'])
            logging.info(config.CONFIG['host_user'])
            logging.info(config.CONFIG['host_password'])
            shell = spur.SshShell(
                hostname=config.CONFIG['host'], 
                username=config.CONFIG['host_user'], 
                password=config.CONFIG['host_password'], 
                missing_host_key=spur.ssh.MissingHostKey.accept
            )
            with shell:
                if interactive:
                    result = shell.run(cmd.split(' '))
                else:
                    result = shell.spawn(cmd.split(' '))
                logging.info('Run: ' + cmd)
        except Exception as e:
            logging.warning('Run failed: ' + cmd)
            logging.warning(e.__doc__ )

    def start(self, cmd):
        self.run_cmd(cmd, interactive = False)

    def stop(self, name):
        self.run_cmd("docker stop " + name)
        self.run_cmd("docker rm " + name)