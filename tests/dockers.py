import config
import spur
import logging
from logging import Logger

class Docker():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    def start(self, cmd):
        try:
            logging.debug(cmd)
            logging.debug(config.CONFIG['host'])
            logging.debug(config.CONFIG['host_user'])
            logging.debug(config.CONFIG['host_password'])
            shell = spur.SshShell(
                hostname=config.CONFIG['host'], 
                username=config.CONFIG['host_user'], 
                password=config.CONFIG['host_password'], 
                missing_host_key=spur.ssh.MissingHostKey.accept
            )
            with shell:
                result = shell.spawn(cmd.split(' '))
                logging.debug('Docker started')
        except Exception as e:
            logging.warning('Docker start failed')
            logging.warning(e.__doc__ )

    def run_cmd_interactive(self, cmd):
        try:
            shell = spur.SshShell(
                hostname=config.CONFIG['host'], 
                username=config.CONFIG['host_user'], 
                password=config.CONFIG['host_password'], 
                missing_host_key=spur.ssh.MissingHostKey.accept
            )
            with shell:
                result = shell.run(cmd.split(' '))
                logging.debug('Run interactive: ' + cmd)
        except Exception as e:
            logging.warning('Run interactive failed: ' + cmd)
            logging.warning(e.__doc__ )

    def stop(self, name):
        self.run_cmd_interactive("docker stop " + name)
        self.run_cmd_interactive("docker rm " + name)