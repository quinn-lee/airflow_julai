#!/bin/bash

source /etc/profile
source $HOME/.bash_profile

cd ~/monitor
content="生产监控邮件,请勿回复,详见附件!"
title="生产环境服务器每日监控"

run_hour=`date +%k`	#用来判断 执行任务的 具体小时
echo "RUN HOUR : $run_hour"

content+="
硬盘空间"
echo "硬盘空间监控:" > tmp_result.txt
./remote_login.sh 1
if [ $? -ne 0 ];then
	title="生产环境服务器每日监控 - 警告"
	content+=">=85%,异常!"
else
	content+=",正常"
fi

#content+="
#捷克邮政单证号"
#echo -e "\n\n捷克邮政单证号监控:" >> tmp_result.txt
#./remote_login.sh 7
#if [ $? -ne 0 ];then
#	title="生产环境服务器每日监控 - 警告"
#	content+="<=20000,异常!"
#else
#	content+=",正常"
#fi

#content+="
#yto海外物流信息推送"
#echo -e "\n\nyto海外物流信息推送:" >> tmp_result.txt
#./remote_login.sh 13
#if [ $? -ne 0 ];then
#	title="生产环境服务器每日监控 - 警告"
#	content+=">0,异常!"
#else
#	content+=",正常"
#fi

#2018.04.04 切换为UPS,不再进行监控
#content+="
#dpd单证号"
#echo -e "\n\ndpd单证号监控:" >> tmp_result.txt
#./remote_login.sh 14
#if [ $? -ne 0 ];then
#       title="生产环境服务器每日监控 - 警告"
#       content+="<=15000,异常!"
#else
#       content+=",正常"
#fi

#content+="
#XYG-SHG单证号"
#echo -e "\n\nXYG-SHG单证号监控:" >> tmp_result.txt
#./remote_login.sh 16
#if [ $? -ne 0 ];then
#        title="生产环境服务器每日监控 - 警告"
#        content+="<=1000,异常!"
#else
#        content+=",正常"
#fi


#content+="
#财务系统支付成功异步通知监控"
#echo -e "\n\n财务系统支付成功异步通知监控:" >> tmp_result.txt
#./remote_login.sh 19
#if [ $? -ne 0 ];then
#        title="生产环境服务器每日监控 - 警告"
#        content+=",异常!"
#else
#        content+=",正常"
#fi


echo "每日监控 end `date`" >> tmp_result.txt

#echo -e $content | mail -s "$title" -r "liyixiaoqd@126.com" -A "tmp_result.txt" samuel.uling@quaie.com levine.li@quaie.com jianing.sheng@mypost4u.com xuemei.gong@mypost4u.com amy.wang@quaie.com yixiao.li@quaie.com
#java -jar sendMail.jar conf daily "$title" "$content" "tmp_result.txt"
echo "$content" | mail -s "$title" -a tmp_result.txt samuel.uling@quaie.com,levine.li@quaie.com,chang.cai@quaie.com
