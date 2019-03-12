#!/usr/bin/bash


set +x

if [ $# -gt 0 ]
then
	case $1 in
		"start")
			docker run --name bugzillaDB -d -v /var/mysql/data:/var/lib/mysql -p 3306:3306 hectorany/bugzilla 
			docker ps | grep bugzillaDB
			;;
		"stop")
			DOCKEROBJ=`docker ps | grep bugzillaDB| awk -F' ' '{print $1}'`
			test -z $DOCKEROBJ && docker kill $DOCKEROBJ && docker rm $DOCKEROBJ
			;;
		"exec")
			DOCKEROBJ=`docker ps | grep bugzillaDB| awk -F' ' '{print $1}'`
			test -z $DOCKEROBJ || docker exec -it $DOCKEROBJ bash
			;;
		"all")
			docker container ls -a | grep bugzillaDB
			;;
		*)
			docker ps | grep bugzillaDB
			;;
	esac
else
			docker ps 
fi
