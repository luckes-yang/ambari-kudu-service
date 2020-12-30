from resource_management import *
import os
from kudu_base import KuduBase


class KuduTserver(KuduBase):
    def install(self, env):
        self.install_packages(env)
        self.installKudu(env)
        self.configure(env)

    def configure(self, env):
        self.configureKuduTServer(env)

    def start(self, env):
        self.configure(env)
        cmd = 'service kudu-tserver start'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def stop(self, env):
        cmd = 'service kudu-tserver stop'
        Execute('echo "Running cmd: ' + cmd + '"')
        Execute(cmd)

    def status(self, env):
        check_process_status("/var/run/kudu/kudu-tserver-kudu.pid")

    def create_dirs(self, data_dir):
        Directory(data_dir,
                  create_parents=True,
                  cd_access="a",
                  mode=0o755,
                  owner='kudu',
                  group='kudu',
                  ignore_failures=True
                  )

    def configureKuduTServer(self, env):
        import params
        env.set_params(params)
        realm_name = os.popen(
            'grep "default_realm" /etc/krb5.conf ').read().strip(os.linesep).split(' ')[-1]
        File("/etc/kudu/conf/tserver.gflagfile",
             content=Template("kudu_tserver.j2", realm_name=realm_name),
             mode=0o644
             )
        self.create_dirs(params.tserver_env['fs_wal_dir'])


if __name__ == "__main__":
    KuduTserver().execute()
