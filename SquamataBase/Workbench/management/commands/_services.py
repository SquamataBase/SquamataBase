import os
from django.conf import settings

class Service(object):
    SERVICE_HOME = os.path.join(os.environ['HOME'], 'Library', 'LaunchAgents')

    def start(self):
        if os.path.exists(self.LABEL):
            print('The %s is already running.' % self.VERBOSE_NAME)
            return 1
        else:
            with open(self.LABEL, 'w') as f:
                f.write(self.plist)
            os.system("launchctl load -w %s" % self.LABEL)
            print('The %s is now running.' % self.VERBOSE_NAME)
            return 0
    
    def stop(self):
        if not os.path.exists(self.LABEL):
            print('The %s is not running.' % self.VERBOSE_NAME)
            return 1
        else:
            os.system("launchctl unload -w %s" % self.LABEL)
            os.remove(self.LABEL)
            print('The %s is now stopped.' % self.VERBOSE_NAME)
            return 0

    def restart(self):
        if not self.stop():
            self.start()

    def is_active(self):
        return os.path.exists(self.LABEL)

    def status(self):
        return '(started)' if self.is_active() else '(stopped)'

class UIService(Service):
    def __init__(self):
        self.VERBOSE_NAME = 'SquamataBase User Interface service'
        self.LABEL = os.path.join(self.SERVICE_HOME, 'squamatabase.ui.plist')
        self.plist = \
'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>KeepAlive</key>
            <true/>
        <key>Label</key>
            <string>squamatabase.ui</string>
        <key>ProgramArguments</key>
            <array>
                <string>/usr/local/opt/python3/bin/python3</string>
                <string>manage.py</string>
                <string>runserver</string>
                <string>--nothreading</string>
            </array>
        <key>RunAtLoad</key>
            <true/>
        <key>WorkingDirectory</key>
            <string>%s</string>
        <key>StandardErrorPath</key>
            <string>/usr/local/var/log/squamatabase.log</string>
    </dict>
</plist>
''' % settings.BASE_DIR


class BackupService(Service):
    def __init__(self):
        self.VERBOSE_NAME = 'SquamataBase Backup service'
        self.LABEL = os.path.join(self.SERVICE_HOME, 'squamatabase.backup.plist')
        self.plist = \
'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
            <string>squamatabase.backup</string>
        <key>ProgramArguments</key>
            <array>
                <string>/usr/local/opt/python3/bin/python3</string>
                <string>manage.py</string>
                <string>sb_backup</string>
            </array>
        <key>WorkingDirectory</key>
            <string>%s</string>
        <key>StandardOutPath</key>
            <string>/usr/local/var/log/squamatabase.backups.log</string>
        <key>StandardErrorPath</key>
            <string>/usr/local/var/log/squamatabase.backups.log</string>
        <key>StartInterval</key>
            <integer>86400</integer>
    </dict>
</plist>
''' % settings.BASE_DIR


SERVICES = {
    'ui': UIService(),
    'backup': BackupService()
}

        