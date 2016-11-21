-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: devops
-- ------------------------------------------------------
-- Server version	5.1.73

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
INSERT INTO `power` VALUES (4,'git','git仓库','/project/project','测试'),(14,'cobbler','装机平台','/cobbler','赋予装机平台权限'),(6,'zabbix','监控','/zabbix','监控管理'),(7,'elk','性能展示','/show','性能展示'),(8,'testing','测试发布','/project/testing','代码测试发布'),(9,'apply','申请发布','/proect/apply','申请发布sss'),(10,'deploy','发布列表','/proect/deploy','发布列表'),(15,'cmdb','资产管理','/cmdb','CMDB管理和用户管理'),(16,'device','设备保障','/device','设备保障申请，需由管理员进行下架协调'),(17,'report','申请报障','/device/report','可以进行故障申报'),(18,'maintain','故障处理','/device/maintain','管理员权限故障处理'),(19,'down','下架服务器查看','/device/down','下架服务器查看');
/*!40000 ALTER TABLE `power` ENABLE KEYS */;
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
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'sa','运维组','4,14,6,7,8,9,10,15,1','超级管理员'),(10,'zj','装机','14','专门装机用户'),(11,'zabbix','监控用户组','6','监控用户组合管理员组'),(12,'cmdb','cmdb管理组','15','资产管理和审计'),(13,'device','设备保障组','16','设备保障'),(14,'report','故障申报','17','普通用户故障申报'),(15,'maintain','管理员故障处理','18,19','管理员拥有故障处理功能');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
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
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','e10adc3949ba59abbe56e057f20f883e','admin','787696331@qq.com','183105199111','1,10,11,12,13,14,15',0,NULL,'2016-11-10 12:35:36'),(17,'xiaoluo','e10adc3949ba59abbe56e057f20f883e','小罗','18878774260@163.com','18878774260','10,14',0,'2016-08-24 16:33:54','2016-09-28 20:23:27');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-21 11:44:22
