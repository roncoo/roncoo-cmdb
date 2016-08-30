#!/bin/sh
#coding=utf8
##################################################################
#将如下IP修改成你cobbler服务器的IP地址
ip=192.168.63.238
#将如下net修改成你Cobbler所在网段的NET  
net=192.168.63.0  
#修改成dhcp计划分配的IP段
begin=192.168.63.250
end=192.168.63.253
echo "$ip    www.xiaoluo.com" >> /etc/hosts
yum install cobbler cobbler-web pykickstart dhcp debmirror syslinux cman fence-agents  vim -y
/etc/init.d/iptables stop
/etc/init.d/httpd start
/etc/init.d/cobblerd start
service cobblerd restart
sed -i -e 's/= yes/= no/g' /etc/xinetd.d/rsync
sed -i -e 's/= yes/= no/g' /etc/xinetd.d/tftp
sed -i 's@next_server: 127.0.0.1@next_server: '$ip'@g' /etc/cobbler/settings
sed -i 's@server: 127.0.0.1@server: '$ip'@g' /etc/cobbler/settings
cp /usr/share/syslinux/pxelinux.0 /var/lib/cobbler/loaders/
cp  /usr/share/syslinux/meminfo.c32  /var/lib/cobbler/loaders/
sed -i 's$@arches="i386"$#@arches="i386"$g' /etc/debmirror.conf
sed  -i 's$@dists="sid"$#@dists="sid"$g' /etc/debmirror.conf
sed -i 's@default_password_crypted@#default_password_crypted@g' /etc/cobbler/settings
echo "default_password_crypted:  "$1$ac756ac7$erF27Ljjp3rDItLVqHLOg/"" >> /etc/cobbler/settings
cobbler get-loaders
service cobblerd restart
cobbler sync
####用cobbler check 查看到底有哪些步骤没有操作完成。
cobbler check
#dhcp 
cat > /etc/dhcp/dhcpd.conf <<EOF
option domain-name "xiaoluo.com";
option domain-name-servers $ip;
default-lease-time 43200;
max-lease-time 86400;
log-facility local7;
subnet $net netmask 255.255.255.0 {
     range $begin $end;
     option routers $ip;
}
next-server $ip;
filename="pxelinux.0";
EOF
/etc/init.d/dhcpd restart
service xinetd  restart
service cobblerd restart
mkdir /opt/xiaoluo
mount /dev/cdrom /opt/xiaoluo 
cobbler import --name=centos-6.5-x86_64 --path=/opt/xiaoluo

