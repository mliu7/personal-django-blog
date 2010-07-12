from fabric.api import env, run, local, put

import datetime
import pdb

LOCAL_PROJECT_PATH = '/Users/mliu/Programming/djcode/'

REMOTE_BACKUP_DIR = '/home/mliu/webapps/django/backups/'
REMOTE_PROJECT_PATH = '/home/mliu/webapps/django/'

env.roledefs = {
    'web': ['markliu.me']
}

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
        put(self.local_path + self.name + '/markliu/settings.py', self.remote_path + self.name + '/markliu/settings.py')

    def move_media(self):
        run('cd ' + self.remote_path + self.name + '/markliu; \
            tar cvzf media.tar.gz media; \
            mv media.tar.gz ' + self.remote_backup_dir + self._remote_backup_name(basename='media') + '; \
            cp -a media /home/mliu/webapps/; \
            rm -r media')

    def sync_virtualenv(self):
        run('source ~/python-environments/markliu/bin/activate; \
            pip install -r ' + self.remote_path + self.name + '/requirements.txt; \
            add2virtualenv ' + self.remote_path + 'django-google-webmaster; \
            add2virtualenv ' + self.remote_path + 'django-twitter-tags; \
            add2virtualenv ' + self.remote_path + 'coltrane-blog')

    def deploy(self):
        self.replace_remote()
        self.upload_settings()
        self.move_media()

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
    coltrane = App('coltrane-blog')
    coltrane.deploy()
    django_twitter_tags = App('django-twitter-tags')
    django_twitter_tags.deploy()
    django_google_webmaster = App('django-google-webmaster')
    django_google_webmaster.deploy()

    markliu.sync_virtualenv()
    restart_webserver() 
