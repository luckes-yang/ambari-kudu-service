from resource_management import *
import os
class KuduBase(Script):
    impala_packages = [
        'kudu',
        'kudu-master',
        'kudu-tserver',
        'kudu-client0',
        'kudu-client-devel']

    def installKudu(self, env):
        self.install_packages(env)
        if self.impala_packages is not None and len(self.impala_packages):
            for pack in self.impala_packages:
                Package(pack)
        import params
        env.set_params(params)
