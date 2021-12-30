#!/bin/bash

sftp -i /home/timegmbh/.ssh/id_rsa timegmbh@172.105.3.134 <<EOF
cd /opt/rails-app/et_wms/public
put /opt/rails-app/et_wms/public/plotly.html
bye
EOF
