#!/bin/bash

set +x
# gensql.sh -f buglist-file -n table-name
# using this script to format buglist file as sql insert file.
# when got sql insert file, you can insert all data to mysql.
#
function usage ()
 {
	 echo -e  "Usage:"
	 echo -e "importDB.sh -f buglist-file -h host -u user -p password -d database-name -n table-name"
	 echo -e "\t -f buglist-file: \tthe argument is a buglist file, formated with html, which is get from bugzilla "
	 echo -e "\t -h host: \tthe argument is the host of the db"
	 echo -e "\t -u user: \tthe argument is the user to access the db"
	 echo -e "\t -p password:\tpassword of the user to access the db"
	 echo -e "\t -d database-name: \tthe argument is the database name in mysql you want to use"
	 echo -e "\t -n table-name: \tthe argument is the table name in mysql you want to creat"
	 echo -e "\t example:\tgensql.sh -f buglist.html -h 127.0.0.1 -u libadm -p password -n bugzilla2017"
 }

if [ $# -lt 12 ]
then
	usage
	exit
fi

#####
GPATH=`dirname $0`
BUGLISTFILE=""
TABLENAME=""
TEMPFILE="temp."$$

while getopts ":f:n:h:u:d:p:" opt
do
	case $opt in
		'f')
			BUGLISTFILE=$OPTARG
			;;
		'h')
			HOST=$OPTARG
			;;
		'u')
			USER=$OPTARG
			;;
		'p')
			PASSWORD=$OPTARG
			;;
		'd')
			DATABASE=$OPTARG
			;;
		'n')
			TABLENAME=$OPTARG
			;;
		\? ) echo "Unknown option: -$OPTARG" >&2; exit 1;;
		:  ) echo "Missing option argument for -$OPTARG" >&2; exit 1;;
		*  ) echo "Unimplemented option: -$OPTARG" >&2; exit 1;;
	esac
done

if [ ${BUGLISTFILE}X = 'X' ] || [ ${TABLENAME}X = 'X' ]
then
	usage
	exit
fi



sed -e 's#<tr valign="\?TOP"\? align="\?LEFT"\?>#\n<tr valign="TOP" align="LEFT">#gi' -e 's#</\?nobr>##g' $BUGLISTFILE  | \
	grep '^<tr valign="TOP" align="LEFT">' | \
	sed  -e 's#</\?td \?>\(<td>\)\?#^#g' -e 's#\(^.*id=\)\([0-9]*\)\(">[0-9]\{5\}\)</a>#\2#gi' -e 's#<br />#<br>#g' > $TEMPFILE

SQLFILE="${GPATH}/sql/insert_${TABLENAME}_$$.sql"
echo "use $DATABASE;">$SQLFILE
cat $TEMPFILE | awk -F'^' -v table=$TABLENAME \
	'{ \
		inst = "INSERT INTO " table" VALUES ( "; 		\
		for( i = 0; i < NF; i++ ) 						\
		{												\
			param = $(i+1);								\
			gsub(/\\n/," ",param);              	    \
			gsub(/"/,"",param);							\
			if(i == 0)									\
			{											\
				gsub(/ /,"",param)						\
			}											\
			if(  i == 17 )								\
			{											\
				split($(i+1),arr,"<br>");				\
				ret = "";								\
				for( j in arr )							\
				{										\
					gsub(/^.*">/,"",arr[j]);			\
					gsub(/<\/a>/,"",arr[j]);			\
					ret = (arr[j]","ret);				\
				}										\
				ret = substr(ret,2,length(ret)-2);		\
				param = sprintf( "%s,",ret);			\
			}											\
			if(i == 18 )								\
			{											\
				gsub(/<br>/,",",$(i+1));				\
				param = sprintf("%s,",$(i+1));			\
			}											\
			if( i == 24 )								\
			{											\
				split($(i+1),ar,"<br>");				\
				ret = "";								\
				for( j in ar )							\
				{										\
					gsub(/^.*">/,"",ar[j]);				\
					gsub(/<\/a>/,"",ar[j]);				\
					gsub(/^.*AR=/,"",ar[j]);			\
					gsub(/">.*$/,"",ar[j]);				\
					ret = (ar[j]","ret);				\
				}										\
				ret = substr(ret,2,length(ret)-2);		\
				param = sprintf( "%s,",ret);			\
			}											\
			if( i == 26 )								\
				continue;								\
			if( i == 27 )								\
				inst = inst "\"" param"\");";			\
			else										\
				if( i == 0 )							\
					inst = inst "" param ", ";			\
				else									\
					inst = inst "\"" param"\", ";		\
		}												\
		printf("%s\n",inst);							\
	}' >> $SQLFILE 
rm -rf $TEMPFILE
echo -e "SQL file for ${TABLENAME} is done:\tinsert_${TABLENAME}_$$.sql"
echo -e "Executing SQL file on:\tHOST:\t${HOST}\n\tDataBase:\t${DATABASE}\n\tUser:\t${USER}\n\tPassword:${PASSWORD}\n\t"

mysql -h${HOST} -u${USER} -p${PASSWORD} -e "source $SQLFILE"
