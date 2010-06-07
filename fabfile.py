from fabric.api import env, run, local, put

import datetime
import pdb

LOCAL_PROJECT_PATH = '/Users/mliu/Programming/djcode/'

REMOTE_BACKUP_DIR = '/home/mliu/webapps/django/backups/'
REMOTE_PROJECT_PATH = '/home/mliu/webapps/django/'

env.roledefs = {
    'web': ['markliu.me']
}
#set(fab_user='mark', 
#    fab_hosts=['markliu.me'],
#    root=LOCAL_PROJECT_DIR,
#    site='markliu')

class App:
    def __init__(self, name, local_path=LOCAL_PROJECT_PATH, remote_path=REMOTE_PROJECT_PATH, remote_backup_dir=REMOTE_BACKUP_DIR):
        self.name = name
        self.local_path = local_path
        self.remote_path = remote_path
        self.remote_backup_dir = remote_backup_dir
        self.tarname = self.name + '.tar.gz'

    def _remote_backup_name(self, basename = 'backup', extension = '.tar.gz'):
        now = datetime.datetime.now()
        minute = now.minute
        hour = now.hour
        day = now.day
        month = now.month
        year = now.year
        return basename + '_' + str(year) + '_' + str(month) + '_' + str(day) + '_' + str(hour) + '-' + str(minute) + extension

    #def remote_backup(self):
    #    pdb.set_trace()
    #    run('cd ' + self.remote_path + self.name + ';tar -cvzf ' + self._remote_backup_name(basename=self.name) + ' .; \
    #       mv ' + self._remote_backup_name(basename=self.name) + ' ' + self.remote_backup_dir) #backup old one

    def _remote_delete(self):
        run('rm -r ' + self.remote_path + self.name)

    def _local_package(self):
        local('cd ' + self.local_path + self.name + '; \
              git archive --format=tar HEAD | gzip > ' + self.tarname)

    def _put_package(self):
        put(self.local_path + self.name + '/' + self.tarname, self.remote_path + self.tarname)

    def _remote_unpackage(self):
        run('cd ' + self.remote_path + '; \
            mkdir ' + self.name + '; \
            cd ' + self.name + '; \
            tar zxf ../' + self.tarname + '; \
            mv ../' + self.tarname + ' ' + self.remote_backup_dir + self._remote_backup_name(basename=self.name)) 
                #move the .tar.gz file to the backup directory so we have a history of it

    def _clean_local(self):
        local('cd ' + self.local_path + self.name + '; \
              rm ' + self.tarname)

    def replace_remote(self):
        self._local_package()
        self._remote_delete()
        self._put_package()
        self._remote_unpackage()
        self._clean_local()

    def deploy(self):
        self.replace_remote()

class MainApp(App):
    def upload_settings(self):
        put(self.local_path + self.name + '/settings.py', self.remote_path + self.name + '/settings.py')
    def move_media(self):
        run('cd ' + self.remote_path + '; \
            tar cvzf media.tar.gz media; \
            mv media.tar.gz ' + self.remote_backup_dir + self._remote_backup_name(basename='media') + '; \
            cp -a media /home/mliu/webapps/; \
            rm -r media')
    def sync_virtualenv(self):
        run('pip install -E markliu -r ' + self.remote_path + self.name + '/requirements.txt')

    def deploy(self):
        self.replace_remote()
        self.upload_settings()
        self.move_media()
        self.sync_virtualenv()

def production():
    env.hosts = env.roledefs['web']
    env.user = 'mliu'

def restart_webserver():
    run('source ~/python-environments/markliu/bin/activate; \
        cd ~/webapps/django/apache2/bin/; \
        ./restart; \
        deactivate')

def error_log():
    run('more ~/logs/user/error_django.log')

def deploy():
    markliu = MainApp('markliu')
    markliu.deploy()
    coltrane = App('coltrane')
    coltrane.deploy()
    django_twitter_tags = App('django_twitter_tags')
    django_twitter_tags.deploy()

    restart_webserver() 



    #_backup_dir(REMOTE_PROJECT_DIR, REMOTE_BACKUP_DIR, REMOTE_PROJECT_NAME)

    #local('cd ' + LOCAL_PROJECT_DIR + ';git archive --format=tar HEAD | gzip > ' + LOCAL_PROJECT_NAME + '.tar.gz')
    #run('rm -r ' + dir) #remove the old one
    #put(LOCAL_PROJECT_DIR + LOCAL_PROJECT_NAME + '.tar.gz', REMOTE_PROJECT_DIR +  REMOTE_PROJECT_NAME + '.tar.gz') #put the new one
    #run('cd ' + REMOTE_PROJECT_DIR + '; tar -xzf ' + REMOTE_PROJECT_NAME + '.tar.gz') #unzip it
    #run('cd ' + REMOTE_PROJECT_DIR + '; rm ' + REMOTE_PROJECT_NAME + '.tar.gz') #remove it
    
    #move the media appropriately
    #restart
