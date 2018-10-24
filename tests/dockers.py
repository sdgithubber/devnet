import config
import spur

class Docker():
    def start(self, cmd):
        try:
            print(cmd)
            print(config.CONFIG['host'])
            print(config.CONFIG['host_user'])
            print(config.CONFIG['host_password'])
            shell = spur.SshShell(
                hostname=config.CONFIG['host'], 
                username=config.CONFIG['host_user'], 
                password=config.CONFIG['host_password'], 
                missing_host_key=spur.ssh.MissingHostKey.accept
            )
            with shell:
                result = shell.spawn(cmd.split(' '))
                print('Docker started')
        except Exception as e:
            print('Docker start failed')
            print(e.__doc__ )

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
                print('Run interactive: ' + cmd)
        except Exception as e:
            print('Run interactive failed: ' + cmd)
            print(e.__doc__ )

    def stop(self, name):
        self.run_cmd_interactive("docker stop " + name)
        self.run_cmd_interactive("docker rm " + name)

if __name__ == '__main__':
    unittest.main()