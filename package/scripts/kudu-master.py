from resource_management import *
import os
from kudu_base import KuduBase


class KuduMaster(KuduBase):
    def install(self, env):
        self.install_packages(env)
        self.installKudu(env)
        self.configure(env)

    def configure(self, env):
        self.configureKuduMaster(env)

    def start(self, env):
        self.configure(env)
        cmd = 'service kudu-master start'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def stop(self, env):
        cmd = 'service kudu-master stop'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def status(self, env):
        check_process_status("/var/run/kudu/kudu-master-kudu.pid")

    def create_dirs(self, data_dir):
        Directory(data_dir,
                  create_parents=True,
                  cd_access="a",
                  mode=0o755,
                  owner='kudu',
                  group='kudu',
                  ignore_failures=True
                  )

    def configureKuduMaster(self, env):
        import params
        env.set_params(params)
        realm_name = os.popen(
            'grep "default_realm" /etc/krb5.conf ').read().strip(os.linesep).split(' ')[-1]
        File("/etc/kudu/conf/master.gflagfile",
             content=Template("kudu_master.j2", realm_name=realm_name),
             mode=0o644
             )

        self.create_dirs(params.master_env['fs_wal_dir'])


if __name__ == "__main__":
    KuduMaster().execute()
