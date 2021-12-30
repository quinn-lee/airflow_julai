#!/bin/bash
echo "db_bak_wms.sh start `date`"

cd
export PGPASSFILE=/opt/rails-app/cron/db_backup/.pgpass

cd /opt/rails-app/cron/db_backup/
time=`date +%Y%m%d_%H%M%S`

database="et_wms_service_prod_db"

bakfile=wms_db_data_${database}_${time}.txt.gz
/usr/bin/pg_dump -h localhost -p 5432 -d et_wms_service_prod_db -U europe_time  -N bucardo|gzip > ${bakfile}

file_size=`stat -c "%s" $bakfile`
echo "bak file size: $file_size"

sftp -i /home/timegmbh/.ssh/id_rsa timegmbh@172.105.3.134 <<EOF
cd /backup/db_backup/wms_nordlicht_out
put ${bakfile}
bye
EOF

if [ $file_size -le 10000 ];then
        echo "bak file exception and not rm history file !!!!!"
else
	rm_time=`date -d "-2 day" +%Y%m%d`
	rm_file="wms_db_data_${database}_${rm_time}*txt.gz"
	echo "clear file: ${rm_file} `pwd`"
	rm ${rm_file}
fi

echo "db_bak_wms.sh end `date`"
