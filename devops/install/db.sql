-- MySQL dump 10.13  Distrib 5.5.52, for Linux (x86_64)
--
-- Host: localhost    Database: devops
-- ------------------------------------------------------
-- Server version	5.5.52

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cabinet`
--

DROP TABLE IF EXISTS `cabinet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cabinet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `idc_id` int(11) NOT NULL,
  `power` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cabinet`
--

LOCK TABLES `cabinet` WRITE;
/*!40000 ALTER TABLE `cabinet` DISABLE KEYS */;
INSERT INTO `cabinet` VALUES (8,'1-1',10,'10A'),(9,'1-2',10,'10A'),(10,'1-3',10,'10A');
/*!40000 ALTER TABLE `cabinet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cobbler`
--

DROP TABLE IF EXISTS `cobbler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cobbler`
--

LOCK TABLES `cobbler` WRITE;
/*!40000 ALTER TABLE `cobbler` DISABLE KEYS */;
/*!40000 ALTER TABLE `cobbler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idc`
--

DROP TABLE IF EXISTS `idc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idc`
--

LOCK TABLES `idc` WRITE;
/*!40000 ALTER TABLE `idc` DISABLE KEYS */;
INSERT INTO `idc` VALUES (10,'SJHL','世纪互联','北京朝阳区','13507714311','12312@163.com','小罗哥','13507714311',4,4);
/*!40000 ALTER TABLE `idc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install`
--

DROP TABLE IF EXISTS `install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) NOT NULL COMMENT '给主机分配IP',
  `install_time` datetime NOT NULL COMMENT '安装时间',
  `os` varchar(50) NOT NULL COMMENT '操作系统',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install`
--

LOCK TABLES `install` WRITE;
/*!40000 ALTER TABLE `install` DISABLE KEYS */;
/*!40000 ALTER TABLE `install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintain`
--

DROP TABLE IF EXISTS `maintain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maintain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT NULL,
  `mail` varchar(20) DEFAULT NULL,
  `server_run` varchar(40) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  `remark` text,
  `xiajia` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintain`
--

LOCK TABLES `maintain` WRITE;
/*!40000 ALTER TABLE `maintain` DISABLE KEYS */;
/*!40000 ALTER TABLE `maintain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance`
--

DROP TABLE IF EXISTS `maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maintenance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maintenance_name` varchar(50) DEFAULT NULL,
  `hostname` varchar(50) DEFAULT NULL,
  `maintenance_time` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance`
--

LOCK TABLES `maintenance` WRITE;
/*!40000 ALTER TABLE `maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `maintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `power`
--

DROP TABLE IF EXISTS `power`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `power` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL COMMENT '权限英文名',
  `name_cn` varchar(40) NOT NULL COMMENT '权限中文名',
  `url` varchar(128) NOT NULL COMMENT '权限对应的url',
  `comment` varchar(128) NOT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `power`
--

LOCK TABLES `power` WRITE;
/*!40000 ALTER TABLE `power` DISABLE KEYS */;
INSERT INTO `power` VALUES (4,'git','git仓库','/project/project','测试'),(14,'cobbler','装机平台','/cobbler','赋予装机平台权限'),(6,'zabbix','监控','/zabbix','监控管理'),(7,'elk','性能展示','/show','性能展示'),(8,'testing','测试发布','/project/testing','代码测试发布'),(9,'apply','申请发布','/proect/apply','申请发布sss'),(10,'deploy','发布列表','/proect/deploy','发布列表'),(15,'cmdb','资产管理','/cmdb','资产管理和审计'),(17,'report','故障申报','/device/report','所有运维人员具有故障申报的权限'),(18,'maintain','故障处理','/device/maintain','管理员具有故障处理和知悉权'),(19,'down','服务器下架','/device/down','下架服务器查看');
/*!40000 ALTER TABLE `power` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(20) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `module_letter` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profile` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `distro` varchar(50) NOT NULL COMMENT 'profile name',
  `os` varchar(50) NOT NULL COMMENT '操作系统',
  `ks` varchar(100) NOT NULL COMMENT 'ks文件',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile`
--

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL COMMENT '项目名',
  `path` varchar(80) NOT NULL COMMENT '项目代码仓库路径',
  `principal` int(10) unsigned NOT NULL COMMENT '负责人',
  `p_user` int(10) unsigned DEFAULT NULL COMMENT '有权限的用户',
  `p_group` int(10) unsigned DEFAULT NULL COMMENT '有权限的组',
  `create_date` date NOT NULL COMMENT '创建时间',
  `is_lock` tinyint(1) unsigned DEFAULT '0' COMMENT '是否锁定 0-未锁定 1-锁定',
  `comment` varchar(256) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_apply`
--

DROP TABLE IF EXISTS `project_apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_apply` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project项目ID',
  `info` varchar(64) NOT NULL COMMENT '发布简介',
  `applicant` varchar(64) NOT NULL COMMENT '申请人',
  `version` varchar(64) DEFAULT NULL COMMENT '发布版本',
  `commit` varchar(64) NOT NULL COMMENT '代码最新版本',
  `apply_date` datetime NOT NULL COMMENT '申请时间',
  `status` int(10) DEFAULT '0' COMMENT '发布状态',
  `detail` text COMMENT '发布详情',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_apply`
--

LOCK TABLES `project_apply` WRITE;
/*!40000 ALTER TABLE `project_apply` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_apply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_deploy`
--

DROP TABLE IF EXISTS `project_deploy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_deploy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project的项目ID',
  `info` varchar(64) NOT NULL COMMENT '发布简介',
  `version` varchar(64) DEFAULT NULL COMMENT '发布版本',
  `commit` varchar(64) NOT NULL COMMENT '代码最新版本',
  `applicant` varchar(64) NOT NULL COMMENT '操作人',
  `apply_date` datetime NOT NULL COMMENT '操作时间',
  `status` int(10) DEFAULT '0' COMMENT '发布状态',
  `detail` text COMMENT '发布详情',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_deploy`
--

LOCK TABLES `project_deploy` WRITE;
/*!40000 ALTER TABLE `project_deploy` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_deploy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_test`
--

DROP TABLE IF EXISTS `project_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_test` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int(10) NOT NULL COMMENT '对应project项目ID',
  `host` varchar(64) NOT NULL COMMENT '测试主机',
  `commit` varchar(64) NOT NULL COMMENT '推送版本号',
  `pusher` varchar(128) NOT NULL COMMENT '推送人',
  `push_date` datetime NOT NULL COMMENT '推送时间',
  `comment` varchar(256) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_test`
--

LOCK TABLES `project_test` WRITE;
/*!40000 ALTER TABLE `project_test` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (9,'admin','312461613@qq.com','WEB','192.168.8.50','test','2016-10-09 14:32:43',1);
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL COMMENT 'è§’è‰2???',
  `name_cn` varchar(40) NOT NULL COMMENT 'è§’è‰2??-?–????',
  `p_id` varchar(20) NOT NULL COMMENT '???é??id????…?è???¤???ap_id,?-???o?-—??|??2?±????',
  `info` varchar(50) DEFAULT NULL COMMENT 'è§’è‰2???è?°?????ˉ',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'sa','运维组','4,14,6,7,8,9,10,15,1','超级管理员'),(7,'php','开发组','4,14,8,9,10','PHP开发'),(10,'zj','装机','14','专门装机用户'),(11,'cmdb','资产审计','15','资产管理'),(13,'report','故障申报','17','普通用户拥有故障申报的权限'),(14,'maintain','管理员具有故障知悉和下架权限','18,19','管理员具有故障知悉和下架权限');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server`
--

DROP TABLE IF EXISTS `server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server`
--

LOCK TABLES `server` WRITE;
/*!40000 ALTER TABLE `server` DISABLE KEYS */;
INSERT INTO `server` VALUES (1,'CMDB-test','192.168.10.1',1,'91846326-0152-58e4-e2c7-47c3dced468d','91846326-0152-58E4-E2C7-47C3DCED468D','Xen','HVM+domU','Intel(R)+Core(TM)+i3-4150+CPU+@+3.50GHz+2','CentOS+6.5+Final','50',990,'2e:6f:8c:13:05:43','2012-01-17',NULL,'dell',10,8,'5','2018-06-06 00:00:00','123133013','2016-10-08 00:00:00','xiaoluo',192168,'web',1,'1U'),(2,'CMDB-test','192.168.10.2',1,'91846326-0152-58e4-e2c7-47c3dced468d','91846326-0152-58E4-E2C7-47C3DCED468D','Xen','HVM+domU','Intel(R)+Core(TM)+i3-4150+CPU+@+3.50GHz+2','CentOS+6.5+Final','50',990,'44-45-53-54-00-00','2012-01-17',NULL,'dell',10,8,'3','2018-07-26 00:00:00','1340123312','2016-10-08 00:00:00','xiaoluo',0,'web',1,'1U'),(3,'CMDB-test','192.168.10.3',1,'91846326-0152-58e4-e2c7-47c3dced468d','91846326-0152-58E4-E2C7-47C3DCED468D','Xen','HVM+domU','Intel(R)+Core(TM)+i3-4150+CPU+@+3.50GHz+2','CentOS+6.5+Final','50',990,'44-45-53-54-00-01','2012-01-17',NULL,'dell',10,8,'5','2018-11-15 00:00:00','1231231241','2016-10-08 00:00:00','xiaoluo',0,'mysql',1,'1U'),(4,'CMDB-test','192.168.10.4',1,'91846326-0152-58e4-e2c7-47c3dced468d','91846326-0152-58E4-E2C7-47C3DCED468D','Xen','HVM+domU','Intel(R)+Core(TM)+i3-4150+CPU+@+3.50GHz+2','CentOS+6.5+Final','50',990,'44-45-53-54-00-02','2012-01-17',NULL,'dell',10,9,'3','2016-11-17 00:00:00','13312312312','2016-10-08 00:00:00','xiaoluo',0,'memcached',1,'1U'),(5,'CMDB-test','192.168.10.5',1,'91846326-0152-58e4-e2c7-47c3dced468d','91846326-0152-58E4-E2C7-47C3DCED468D','Xen','HVM+domU','Intel(R)+Core(TM)+i3-4150+CPU+@+3.50GHz+2','CentOS+6.5+Final','50',990,'44-45-53-54-00-03','2012-01-17',NULL,'dell',10,9,'6','2016-10-08 00:00:00','13512312312','2016-10-19 00:00:00','xiaoluo',0,'redis',1,'1U'),(6,'CMDB-test','192.168.10.6',1,'91846326-0152-58e4-e2c7-47c3dced468d','91846326-0152-58E4-E2C7-47C3DCED468D','Xen','HVM+domU','Intel(R)+Core(TM)+i3-4150+CPU+@+3.50GHz+2','CentOS+6.5+Final','50',990,'44-45-53-54-00-04','2012-01-17',NULL,'dell',10,9,'2','2016-10-08 00:00:00','13512312312','2016-10-13 00:00:00','xiaoluo',0,'nginx',1,'1U'),(7,'CMDB-test','192.168.10.7',1,'91846326-0152-58e4-e2c7-47c3dced468d','91846326-0152-58E4-E2C7-47C3DCED468D','Xen','HVM+domU','Intel(R)+Core(TM)+i3-4150+CPU+@+3.50GHz+2','CentOS+6.5+Final','50',990,'44-45-53-54-00-07','2012-01-17',NULL,'dell',10,10,'3','2018-03-01 00:00:00','13712312312','2016-10-08 00:00:00','xiaoluo',0,'lvs',1,'1U');
/*!40000 ALTER TABLE `server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `switch`
--

DROP TABLE IF EXISTS `switch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) DEFAULT NULL,
  `device` varchar(40) DEFAULT NULL,
  `port` int(8) DEFAULT NULL,
  `cabinet` int(4) DEFAULT NULL,
  `idc` int(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `switch`
--

LOCK TABLES `switch` WRITE;
/*!40000 ALTER TABLE `switch` DISABLE KEYS */;
/*!40000 ALTER TABLE `switch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(40) NOT NULL COMMENT '用户名',
  `password` varchar(64) NOT NULL COMMENT '密码',
  `name` varchar(80) NOT NULL COMMENT '姓名',
  `email` varchar(64) NOT NULL COMMENT '公司邮箱',
  `mobile` varchar(16) DEFAULT NULL COMMENT '手机号',
  `r_id` varchar(32) NOT NULL COMMENT '角色id,允许多个r_id,存为字符串类型',
  `is_lock` tinyint(1) unsigned NOT NULL COMMENT '是否锁定 0-未锁定 1-锁定',
  `join_date` datetime DEFAULT NULL COMMENT '注册时间',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','e10adc3949ba59abbe56e057f20f883e','admin','787696331@qq.com','183105199111','1,7,10,11,13,14',0,NULL,'2016-10-12 11:15:41'),(17,'xiaoluo','e10adc3949ba59abbe56e057f20f883e','小罗','18878774260@163.com','18878774260','7,10',0,'2016-08-24 16:33:54','2016-08-26 03:16:45'),(7,'kk','e10adc3949ba59abbe56e057f20f883e','kk','7896331@qq.com','11212121','1',0,'2016-04-13 14:53:33','2016-08-26 02:57:36');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zbhost`
--

DROP TABLE IF EXISTS `zbhost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zbhost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cmdb_hostid` int(11) DEFAULT NULL,
  `hostid` int(11) DEFAULT NULL,
  `server_run` varchar(40) DEFAULT NULL,
  `ip` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zbhost`
--

LOCK TABLES `zbhost` WRITE;
/*!40000 ALTER TABLE `zbhost` DISABLE KEYS */;
/*!40000 ALTER TABLE `zbhost` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-12 11:16:51
