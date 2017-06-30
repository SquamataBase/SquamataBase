#! /bin/bash

python=$(which python3)
if [ "${python}" = "" ]
then
    echo "Missing python installation"
    exit 1
fi

pip=$(which pip3)
if [ "${pip}" = "" ]
then
    echo "Missing pip installation"
    exit 1
fi

wget=$(which wget)
if [ "${wget}" = "" ]
then
    echo "Missing wget installation"
    exit 1
fi

if [[ "$OSTYPE" == "cygwin" ]]
then
    echo "Windows installation not supported"
    exit 1
elif [[ "$OSTYPE" == "win32" ]]
then
    echo "Windows installation not supported"
    exit 1
elif [[ "$OSTYPE" == "msys" ]]
then
    echo "Windows installation not supported"
    exit 1
fi

python="$python -V"
v=$(${python})
if [[ $v != 'Python 3'* ]]
then
    echo "Only Python 3 is supported"
    exit 1
fi
python=$(which python3)

pip="$pip install -r requirements.txt"
${pip}

cd ..
wget="$wget https://github.com/SquamataBase/SquamataBase-Fixtures-0/archive/v1.tar.gz"
${wget}

tar xzf 'v1.tar.gz'


mv 'SquamataBase-Fixtures-0-1' 'SquamataBase-Fixtures-0'
cd 'SquamataBase-Fixtures-0/Taxonomy'
wget 'https://github.com/SquamataBase/SquamataBase-Fixtures-0/releases/download/v1/taxonomy.txt.zip'
unzip 'taxonomy.txt.zip'
cd '../Geography'
wget 'https://github.com/SquamataBase/SquamataBase-Fixtures-0/releases/download/v1/sb_adm_boundary.sql.zip'
unzip 'sb_adm_boundary.sql.zip'
cd '../../SquamataBase'
python="$python manage.py sb_init"
${python}


