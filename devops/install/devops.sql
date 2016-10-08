CREATE TABLE `user` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`username` varchar(40) NOT NULL COMMENT '用户名',
`password` varchar(64) NOT NULL COMMENT '密码',
`name` varchar(80) NOT NULL COMMENT '姓名',
`email` varchar(64) NOT NULL COMMENT '公司邮箱',
`mobile` varchar(16) COMMENT '手机号',
`r_id`  varchar(32)   NOT NULL COMMENT '角色id,允许多个r_id,存为字符串类型',      
`is_lock` tinyint(1) unsigned NOT NULL COMMENT '是否锁定 0-未锁定 1-锁定',
`join_date` datetime DEFAULT NULL COMMENT '注册时间',
`last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
PRIMARY KEY (`id`),
UNIQUE  KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `role` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`name` varchar(20)  NOT NULL COMMENT '角色名',
`name_cn` varchar(40) NOT NULL COMMENT '角色中文名',
`p_id` varchar(20) NOT NULL COMMENT '权限id，允许多个p_id,存为字符串类型',
`info` varchar(50) DEFAULT NULL COMMENT '角色描述信息',
 PRIMARY  KEY (`id`),
 UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `power` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`name` varchar(32) NOT NULL COMMENT '权限英文名',
`name_cn` varchar(40) NOT NULL COMMENT '权限中文名',
`url` varchar(128) NOT NULL COMMENT '权限对应的url',
`comment` varchar(128) NOT NULL COMMENT '备注',
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL COMMENT '项目名',
  `path` varchar(80) NOT NULL COMMENT '项目代码仓库路径',
  `principal` int(10) unsigned NOT NULL COMMENT '负责人',
  `p_user` int(10) unsigned DEFAULT NULL COMMENT '有权限的用户',
  `p_group` int(10) unsigned DEFAULT  NULL COMMENT '有权限的组',
  `create_date` date NOT NULL COMMENT '创建时间',
  `is_lock` tinyint(1) unsigned DEFAULT '0' COMMENT '是否锁定 0-未锁定 1-锁定',
  `comment` varchar(256) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `project_test` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project项目ID',
  `host` varchar(64) NOT NULL COMMENT '测试主机',
  `commit` varchar(64) NOT NULL COMMENT '推送版本号',
  `pusher` varchar(128) NOT NULL COMMENT '推送人',
  `push_date` datetime NOT NULL COMMENT '推送时间',
  `comment` varchar(256) COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `project_apply` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project项目ID',
  `info` varchar(64) NOT NULL COMMENT '发布简介',
  `applicant` varchar(64) NOT NULL COMMENT '申请人',
  `version` varchar(64) DEFAULT NULL COMMENT '发布版本',
  `commit` varchar(64) NOT NULL COMMENT '代码最新版本',
  `apply_date` datetime NOT NULL COMMENT '申请时间',
  `status` int(10) DEFAULT 0 COMMENT '发布状态',
  `detail` text COMMENT '发布详情',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `project_deploy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project的项目ID',
  `info` varchar(64) NOT NULL COMMENT '发布简介',
  `version` varchar(64) DEFAULT NULL COMMENT '发布版本',
  `commit` varchar(64) NOT NULL COMMENT '代码最新版本',
  `applicant` varchar(64) NOT NULL COMMENT '操作人',
  `apply_date` datetime NOT NULL COMMENT '操作时间',
  `status` int(10) DEFAULT 0 COMMENT '发布状态',
  `detail` text COMMENT '发布详情',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `cobbler` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) NOT NULL COMMENT '????????o???é…?IP',
  `MAC` varchar(50) NOT NULL COMMENT 'é€?è??MAC??°??€????????‰è￡…',
  `hostname` varchar(50) DEFAULT NULL COMMENT '?????o???',
  `os` varchar(50) NOT NULL COMMENT '?3????',
  `status` int(11) NOT NULL,
  `gateway` varchar(50) DEFAULT NULL,
  `subnet` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8; 


CREATE TABLE `install` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) NOT NULL COMMENT '给主机分配IP',
  `install_time` datetime NOT NULL COMMENT '安装时间',
  `os` varchar(50) NOT NULL COMMENT '操作系统',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `profile` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `distro` varchar(50) NOT NULL COMMENT 'profile name',
  `os` varchar(50) NOT NULL COMMENT '操作系统',
  `ks` varchar(100) NOT NULL COMMENT 'ks文件',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `cabinet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `idc_id` int(11) NOT NULL,
  `power` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8; 

CREATE TABLE `idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `idc_name` varchar(30) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(30) NOT NULL,
  `user_interface` varchar(50) NOT NULL,
  `user_phone` varchar(20) NOT NULL,
  `rel_cabinet_num` int(11) DEFAULT NULL,
  `pact_cabinet_num` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

CREATE TABLE `maintenance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maintenance_name` varchar(50) DEFAULT NULL,
  `hostname` varchar(50) DEFAULT NULL,
  `maintenance_time` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(20) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `module_letter` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(20) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `vm_status` int(11) DEFAULT NULL,
  `st` varchar(50) DEFAULT NULL,
  `uuid` varchar(100) DEFAULT NULL,
  `manufacturers` varchar(100) DEFAULT NULL,
  `server_type` varchar(100) DEFAULT NULL,
  `server_cpu` varchar(200) DEFAULT NULL,
  `os` varchar(30) DEFAULT NULL,
  `server_disk` varchar(20) DEFAULT NULL,
  `server_mem` int(11) DEFAULT NULL,
  `mac_address` varchar(30) DEFAULT NULL,
  `manufacture_date` date DEFAULT NULL,
  `check_update_time` datetime DEFAULT NULL,
  `supplier` varchar(30) DEFAULT NULL,
  `idc_id` int(11) DEFAULT NULL,
  `cabinet_id` int(11) DEFAULT NULL,
  `cabinet_pos` varchar(10) DEFAULT NULL,
  `expire` datetime DEFAULT NULL,
  `supplier_phone` varchar(20) DEFAULT NULL,
  `server_up_time` datetime DEFAULT NULL,
  `server_purpose` varchar(30) DEFAULT NULL,
  `host` int(11) DEFAULT NULL,
  `server_run` varchar(30) DEFAULT NULL,
  `host_status` int(4) DEFAULT '1',
  `host_models` varchar(10) DEFAULT '1U',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

 CREATE TABLE `zbhost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cmdb_hostid` int(11) DEFAULT NULL,
  `hostid` int(11) DEFAULT NULL,
  `server_run` varchar(40) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT NULL,
  `mail` varchar(20) DEFAULT NULL,
  `server_run` varchar(40) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  `remark` text,
  `reporttime` varchar(30) DEFAULT NULL,
  `status` int(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

 CREATE TABLE `maintain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT NULL,
  `mail` varchar(20) DEFAULT NULL, 
  `server_run` varchar(40) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  `remark` text DEFAULT NULL,
  `xiajia` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `switch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) DEFAULT NULL,
  `device` varchar(40) DEFAULT NULL,
  `port` int(8) DEFAULT NULL,
  `cabinet` int(4) DEFAULT NULL,
  `idc` int(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
