from resource_management import *


class KuduBase(Script):
    impala_packages = [
        'kudu',
        'kudu-master',
        'kudu-tserver',
        'kudu-client0',
        'kudu-client-devel']

    def installKudu(self, env):
        cmd = 'useradd kudu'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd, ignore_failures=True)
        self.install_packages(env)
        if self.impala_packages is not None and len(self.impala_packages):
            for pack in self.impala_packages:
                Package(pack)
