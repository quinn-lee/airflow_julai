#!/bin/bash

source /etc/profile
source $HOME/.bash_profile

cd ~/monitor
content="生产监控邮件,请勿回复,详见附件!"
title="生产环境服务器每小时监控"

#content+="
#nginx"
#echo -e "\n\nnginx监控:" > tmp_result.txt
#./remote_login.sh 6
#if [ $? -ne 0 ];then
#	title="生产环境服务器每小时监控 - 警告"
#	content+=",异常!"
#else
#	content+=",正常"
#fi

#content+="
#unison"
#echo -e "\n\nunison监控:" >> tmp_result.txt
#./remote_login.sh 10 
#if [ $? -ne 0 ];then
#	title="生产环境服务器每小时监控 - 警告"
#	content+=",异常!"
#else
#	content+=",正常"
#fi


content+="
应用内存"
echo -e "\n\n应用内存监控:" >> tmp_result.txt
./remote_login.sh 2
if [ $? -ne 0 ];then
        title="生产环境服务器每小时监控 - 警告"
        content+=",异常!"
else
        content+=",正常"
fi

#content+="
#mypost4u邮件发送队列监控"
#echo -e "\n\nmypost4u邮件发送队列监控:" >> tmp_result.txt
#./remote_login.sh 9
#if [ $? -ne 0 ];then
#        title="生产环境服务器每小时监控 - 警告"
#        content+=">=30,异常!"
#else
#        content+=",正常"
#fi

#content+="
#mypost4u邮件发送队列retour监控"
#echo -e "\n\nmypost4u邮件发送队列retour监控:" >> tmp_result.txt
#./remote_login.sh 11
#if [ $? -ne 0 ];then
#        title="生产环境服务器每小时监控 - 警告"
#        content+=">=30,异常!"
#else
#        content+=",正常"
#fi


#content+="
#财务系统支付成功异步通知监控"
#echo -e "\n\n财务系统支付成功异步通知监控:" >> tmp_result.txt
#./remote_login.sh 17
#if [ $? -ne 0 ];then
#        title="生产环境服务器每小时监控 - 警告"
#        content+=",异常!"
#else
#        content+=",正常"
#fi


#content+="
#微信支付包裹处理监控"
#echo -e "\n\n微信支付包裹处理监控:" >> tmp_result.txt
#./remote_login.sh 18
#if [ $? -ne 0 ];then
#        title="生产环境服务器每小时监控 - 警告"
#        content+=",异常!"
#else
#        content+=",正常"
#fi

echo "每小时监控 end `date`" >> tmp_result.txt

echo "========"
echo "每小时监控 end! [$title][$content]"
echo "========"
if [ "$title" != "生产环境服务器每小时监控" ];then
	#echo -e $content | mail -s "$title" -r "liyixiaoqd@126.com" -A "tmp_result.txt" samuel.uling@quaie.com levine.li@quaie.com jianing.sheng@mypost4u.com xuemei.gong@mypost4u.com yixiao.li@quaie.com
	#java -jar sendMail.jar conf hour "$title" "$content" "tmp_result.txt"  
	echo "$content" | mail -s "$title" -a tmp_result.txt samuel.uling@quaie.com,levine.li@quaie.com,chang.cai@quaie.com
else
	echo "daily_hour_mail normal"
	#java -jar sendMail.jar conf hour "测试发送:$title" "$content" "tmp_result.txt"  
	#echo -e $content | mail -s "$title" -r "liyixiaoqd@126.com" -a "tmp_result.txt" "yixiao.li@quaie.com"
fi
