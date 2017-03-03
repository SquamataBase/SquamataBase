import os
import stat
from django.conf import settings

SERVICE_HOME = os.path.dirname(os.path.abspath(__file__))
bash_script = \
'''#!/bin/bash

python=$(which python3)
if [ "${python}" = "" ]
then
    echo "Missing python3"
    exit 1
fi

index=0
browsers=($(which xdg-open) $(which gnome-open) $(which firefox) $(which google-chrome) $(which open))
while [ "${browsers[index]}" = "" ]
do
    if [ $index = 4]
    then
        break
    fi
    index=$(( $index+1 ))
done
browser=${browsers[index]}
if [ "${browser}" = "" ]
then
    echo "Could not find web browser for development server"
    exit 1
fi
browser="$browser http://localhost:8000/admin/"

if [ "$1" = "" ]
then
    cd %s
    python="$python manage.py shell"
    ${python}
elif [ "$1" = "ui" ]
then
    cd %s
    sleep 2 && ${browser} &
    python="$python manage.py runserver --nothreading"
    ${python}
    echo ""
elif [ "$1" = "backup" ]
then
    cd %s
    python="$python manage.py sb_backup"
    ${python}
elif [ "$1" = "services" ]
then
    cd %s
    python="$python manage.py sb_services ${2} ${3}"
    ${python}
else
    exit 0
fi

exit 0
''' % (settings.BASE_DIR, settings.BASE_DIR, settings.BASE_DIR)

if not os.path.exists(os.path.join(SERVICE_HOME, 'squamatabase')):
    with open(os.path.join(SERVICE_HOME, 'squamatabase'), 'w') as o:
        o.write(bash_script)
    st = os.stat(os.path.join(SERVICE_HOME, 'squamatabase'))
    os.chmod(os.path.join(SERVICE_HOME, 'squamatabase'), st.st_mode | stat.S_IEXEC)
    with open(os.path.join(os.environ['HOME'], '.bash_profile'), 'a') as o:
        o.write('\n# path to SquamataBase command\n')
        o.write('export PATH="%s:$PATH"\n' % SERVICE_HOME)

del SERVICE_HOME
del bash_script
del stat
