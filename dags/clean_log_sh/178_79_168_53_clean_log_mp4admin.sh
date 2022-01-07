echo "CLEAN ADMIN LOG START!!! [`date`]"

eur_log_path="/opt/rails-app/europe_time_logistics/log"

log_bak_file="production.log.bak_`date +"%y%m%d"`"
cd $eur_log_path
cp production.log  $log_bak_file
echo "cp production.log to $log_bak_file end"
echo "log clean! [`date`]" > production.log
echo "clean production.log end"
gzip $log_bak_file
echo "gzip $log_bak_file end"

echo "CLEAN ADMIN LOG END!!! [`date`]"
