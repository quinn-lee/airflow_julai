#!/bin/bash
echo "db_bak.sh start `date`"

cd
source .bashrc

cd db
time=`date +%Y%m%d_%H%M%S`

database="finance_production"
passwd=${FINANCEPASS}

bakfile=db_data_${database}_${time}.txt.gz
#mysqldump -h $host -u $username -p$passwd $database |gzip > db_data_${database}_${time}.txt.gz
mysqldump -ufinance -p$passwd $database |gzip > ${bakfile}

file_size=`stat -c "%s" $bakfile`
echo "bak file size: $file_size"

sftp -i $HOME/.ssh/id_rsa timegmbh@178.79.168.53 <<EOF
cd /home/timegmbh/finance_db_backup/finance
put ${bakfile}
bye
EOF


if [ $file_size -le 10000 ];then
        echo "bak file exception and not rm history file !!!!!"
else
	rm_time=`date -d "-3 day" +%Y%m%d`
	rm_file="db_data_${database}_${rm_time}*txt.gz"
	echo "clear file: ${rm_file} `pwd`"
	rm ${rm_file}
fi

echo "db_bak.sh end `date`"
