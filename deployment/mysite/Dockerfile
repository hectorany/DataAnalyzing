FROM centos

COPY CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo
RUN echo -e "proxy=http://135.251.33.16:80\nproxy=https://135.251.33.16:80">> /etc/yum.conf

#RUN yum clean all && yum makecache && yum -y update && yum -y install epel-release  python-pip python-wheel python-devel mysql-devel gcc
RUN yum -y install epel-release  
RUN yum -y install python-pip python-wheel python-devel mysql-devel gcc mysql

RUN pip install --upgrade pip --proxy="http://135.251.33.16:80" && pip install Django==1.11 django-bootstrap-toolkit MySQL-python nltk uwsgi --proxy="http://135.251.33.16:80"
#RUN python -c "import nltk;nltk.set_proxy('http://135.251.33.16:80');nltk.download('all')"
RUN python -c "import nltk;nltk.set_proxy('http://135.251.33.16:80');nltk.download('punkt');nltk.download('stopwords');"

RUN mv /usr/lib/python2.7/site-packages/nltk/text.py /usr/lib/python2.7/site-packages/nltk/text.py.bak && cat /usr/lib/python2.7/site-packages/nltk/text.py.bak | sed -e 's/print(tokenwrap(colloc_strings, separator="; "))/return tokenwrap(colloc_strings, separator="; ")/g' > /usr/lib/python2.7/site-packages/nltk/text.py

EXPOSE 8001
CMD bash -c 'uwsgi --ini /var/www/mysite/uwsgi.ini'

