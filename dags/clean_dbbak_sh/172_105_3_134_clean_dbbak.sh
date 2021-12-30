#!/bin/bash

echo "======== clean_dbbak.sh run start `date` ========"
db_bak_path="/backup/db_backup"

cd $db_bak_path

for db_bak_dir in `ls $db_bak_path` 
do 
	if test -d $db_bak_dir ; then
		#保留3天数据,校验是否存在后一天的记录
		check_time=`date -d "-3 day" +%Y%m%d`
		check_file="${db_bak_path}/${db_bak_dir}/*${check_time}*txt.gz"
		ls $check_file > /dev/null
		if [ $? -ne 0 ] ; then
			echo "no next file can not clean"
		else
			rm_time=`date -d "-3 day" +%Y%m%d`
			rm_file="${db_bak_path}/${db_bak_dir}/*${rm_time}*"
			echo "rm ${rm_file}"
			rm $rm_file
		fi
		
	else
		echo "$db_bak_dir no proc"
	fi
done
echo "==================== clean_dbbak.sh run end ===================="
echo ""
echo ""
