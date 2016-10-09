#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#

import xmlrpclib
import os 

class CobblerAPI(object):
    def __init__(self,url,user,password):
   	self.remote = xmlrpclib.Server(url)
	self.token = self.remote.login(user,password)
	self.ret = {
            "result": True,
            "comment": [],
        }
 
    def add_system(self,hostname,ip_add,mac_add,profile,gateway,subnet):
        '''
        Add Cobbler System Infomation
        '''

        system_id = self.remote.new_system(self.token) 
        self.remote.modify_system(system_id,"name",hostname,self.token) 
        self.remote.modify_system(system_id,"hostname",hostname,self.token) 
        self.remote.modify_system(system_id,'modify_interface', { 
 	    "macaddress-eth0"   : mac_add,
            "ipaddress-eth0"    : ip_add,
            "gateway-eth0"      : gateway,
            "subnet-eth0"       : subnet,
            "static-eth0"       : 1,
            "name-servers-eth0"      : "114.114.114.114,8.8.8.8", 
            }, self.token) 
        self.remote.modify_system(system_id,"profile",profile,self.token) 
        self.remote.save_system(system_id, self.token) 
        try:
            self.remote.sync(self.token)
	    os.system("cobbler system edit --name=%s --gateway=%s"%(hostname,gateway))
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
        return self.ret

    def get_profile(self):
	"""
	get cobbler profile return
	"""
	try:
	    os = self.remote.get_profiles(self.token)	
	    for i in os:
	        self.ret['comment'].append(i['name'])
	    return self.ret
	except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
            return self.ret

    def get_distro(self):
	"""
	get cobbler distro return
	"""
        try:
            os = self.remote.get_distros(self.token)
            for i in os:
                self.ret['comment'].append(i['name'])
            return self.ret
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
            return self.ret

    def create_profile(self,name,distro,ks):	
	"""
	    create cobbler profile
	"""
        profile_id = self.remote.new_profile(self.token)
        self.remote.modify_profile(profile_id,"name",name,self.token)
        self.remote.modify_profile(profile_id,"distro",distro,self.token)
        self.remote.modify_profile(profile_id,"kickstart",ks,self.token)
        self.remote.save_profile(profile_id, self.token)
	try:
            self.remote.sync(self.token)
	except Exception as e:
	    self.ret['result'] = False
	    self.ret['comment'].append(str(e))
	return self.ret

    def remove_profile(self,name):
	"""
            remove cobbler profile
        """
	try:
	    self.remote.remove_profile(name,self.token)
	except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
        return self.ret

    def remove_system(self,name):
	"""
            remove cobbler profile
        """
        try:
            self.remote.remove_system(name,self.token)
        except Exception as e:
            self.ret['result'] = False
            self.ret['comment'].append(str(e))
        return self.ret
	


def system(url,user,password,hostname,ip_add,mac_add,profile,gateway,subnet):
    cobbler = CobblerAPI(url,user,password)
    ret = cobbler.add_system(hostname,ip_add,mac_add,profile,gateway,subnet)
    return ret

def get_profile(url,user,password):
    cobbler = CobblerAPI(url,user,password)
    ret = cobbler.get_profile()
    return ret

def get_distro(url,user,password):
    cobbler = CobblerAPI(url,user,password)
    ret = cobbler.get_distro()
    return ret

def profile_create(url,user,password,name,distro,ks): 
    cobbler = CobblerAPI(url,user,password)
    ret = cobbler.create_profile(name,distro,ks)
    return ret

def profile_remove(url,user,password,name):
    cobbler = CobblerAPI(url,user,password)
    ret = cobbler.remove_profile(name)
    return ret

def system_remove(url,user,password,name):
    cobbler = CobblerAPI(url,user,password)
    ret = cobbler.remove_system(name)
    return ret
if __name__ == '__main__':
  #  main()
    system =  CobblerAPI("http://192.168.63.182/cobbler_api","xiaoluo","123456")
    print system.add_system("test",'192.168.63.102','00:50:54:2D:32:DE','centos-6.5-x86_64','192.168.10.254','255.255.255.0')
