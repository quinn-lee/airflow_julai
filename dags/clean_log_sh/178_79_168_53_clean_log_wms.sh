echo "CLEAN WMS LOG START!!! [`date`]"

eur_log_path="/opt/rails-app/et_wms/log"

log_bak_file="production.log.bak_`date +"%y%m%d"`"
cd $eur_log_path
cp production.log  $log_bak_file
echo "cp production.log to $log_bak_file end"
echo "log clean! [`date`]" > production.log
echo "clean production.log end"
gzip $log_bak_file
gzip "lograge_production_`date -d '1 days ago' +"%Y%m%d"`.log"
echo "gzip $log_bak_file end"

echo "CLEAN WMS LOG END!!! [`date`]"
