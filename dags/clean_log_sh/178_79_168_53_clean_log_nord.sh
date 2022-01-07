echo "CLEAN NORD LOG START!!! [`date`]"

eur_log_path="/opt/rails-app/nordlicht_wms_backend/log"

log_bak_file="production.log.bak_`date +"%y%m%d"`"
cd $eur_log_path
cp production.log  $log_bak_file
echo "cp production.log to $log_bak_file end"
echo "log clean! [`date`]" > production.log
echo "clean production.log end"
gzip $log_bak_file
echo "gzip $log_bak_file end"

echo "CLEAN NORD LOG END!!! [`date`]"
