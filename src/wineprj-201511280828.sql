-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: wineprj
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

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
-- Table structure for table `poster`
--

DROP TABLE IF EXISTS `poster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `poster` (
  `poster_id` varchar(36) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `show_place` varchar(20) NOT NULL,
  `seq` smallint(6) NOT NULL,
  PRIMARY KEY (`poster_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `poster`
--

LOCK TABLES `poster` WRITE;
/*!40000 ALTER TABLE `poster` DISABLE KEYS */;
INSERT INTO `poster` VALUES ('post1.jpg','海报1','home',1),('post2.jpg','海报2','home',2),('post3.jpg','海报3','home',3);
/*!40000 ALTER TABLE `poster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `pid` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `img_url` text,
  `parent_id` varchar(36) DEFAULT NULL,
  `description` text,
  `volume` smallint(6) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `grape_sort` varchar(50) DEFAULT NULL,
  `scene` varchar(20) DEFAULT NULL,
  `wine_level` varchar(50) DEFAULT NULL,
  `sort` varchar(50) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('04fd62b5-f6e6-4dd5-a8e8-8835bb37f27e','wine68','photo/4.jpg,photo/5.jpg',NULL,'一分价钱一分货,好喝',596,184,'圣保罗','美国','东南奥','西拉','节日拜访','DO','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('06521463-6222-4c8c-98e9-6a49057e6df0','wine40','photo/9.jpg,photo/5.jpg',NULL,'高大上,一分价钱一分货',386,111,'大宝','意大利','奥克','西拉','节日拜访','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('07017471-946e-4919-80d2-198dd82ede59','wine47','photo/9.jpg,photo/6.jpg',NULL,'有品位,酸就是瑟',498,64,'圣保罗','法国','波尔多','美乐','节日拜访','VCE','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('0811f23b-141d-422e-9ae9-ee0a66f66d19','wine92','photo/6.jpg,photo/1.jpg',NULL,'一分价钱一分货,有品位',751,116,'浪迪','美国','波尔多','美乐','聚会','AOC','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('0a419373-a81b-4410-acf1-022c4189ebf8','wine17','photo/0.jpg,photo/3.jpg',NULL,'有品位,有品位',549,191,'博若莱','意大利','波尔多','美乐','聚会','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('17c73f01-e2fd-45a9-987e-71afc27d7049','wine80','photo/8.jpg,photo/0.jpg',NULL,'酸就是瑟,一分价钱一分货',807,95,'圣保罗','美国','西安','西拉','聚会','DO','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('1875a920-c3e0-4f50-96a2-a437da13a5f1','wine22','photo/8.jpg,photo/0.jpg',NULL,'好喝,高大上',995,146,'博若莱','美国','勃艮第','长相思','商务','VDQS','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('196d4a31-5616-45b2-9063-92272561f723','wine5','photo/8.jpg,photo/3.jpg',NULL,'一分价钱一分货,一分价钱一分货',499,170,'圣保罗','利亚','波尔多','美乐','节日拜访','DO','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('1bebf9bd-0e54-4e6e-9c47-ccb6f5e23344','wine59','photo/4.jpg,photo/7.jpg',NULL,'有品位,好喝',679,87,'博若莱','美国','东南奥','赤霞珠','聚会','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('1e9f1a12-6f1a-4db8-9e6d-ecf99d7b5f56','wine4','photo/9.jpg,photo/9.jpg',NULL,'酸就是瑟,高大上',668,83,'大宝','中国','西安','美乐','商务','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('1f30552b-778c-4736-9f4c-cda71cd76278','wine31','photo/8.jpg,photo/4.jpg',NULL,'有品位,酸就是瑟',640,160,'圣保罗','利亚','奥克','西拉','聚会','DO','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('2607b3c2-5caf-4ec4-99ae-59464c8fcea4','wine20','photo/7.jpg,photo/6.jpg',NULL,'高大上,酸就是瑟',784,70,'拉菲','美国','波尔多','美乐','泡妞','DO','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('28c7adc0-5550-4121-a1e6-14d31c190bb1','wine65','photo/6.jpg,photo/3.jpg',NULL,'一分价钱一分货,有品位',407,75,'大宝','中国','奥克','长相思','聚会','DO','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('33267c44-bc0c-4ee0-9e65-dc527b8d3f5a','wine73','photo/8.jpg,photo/9.jpg',NULL,'一分价钱一分货,有品位',635,198,'大宝','中国','奥克','美乐','商务','DO','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('34496866-88b2-4c34-8439-e4d95265bb2a','wine93','photo/7.jpg,photo/3.jpg',NULL,'高大上,一分价钱一分货',601,109,'拉菲','法国','西安','西拉','聚会','AOC','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('34527c03-0d67-447c-878a-51201b272dfb','wine69','photo/0.jpg,photo/5.jpg',NULL,'一分价钱一分货,高大上',557,114,'博若莱','利亚','奥克','赤霞珠','商务','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('35a07cae-3a7e-46d9-8eeb-e441a8dbf1be','wine52','photo/8.jpg,photo/4.jpg',NULL,'有品位,有品位',999,143,'大宝','法国','波尔多','美乐','商务','VDQS','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('3b1cb8db-9e12-482d-b7a4-83ea8fc41ddf','wine51','photo/1.jpg,photo/1.jpg',NULL,'高大上,酸就是瑟',407,194,'大宝','利亚','东南奥','赤霞珠','节日拜访','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('3cea1f9f-922e-433f-a0d6-52d3d7216b42','wine44','photo/0.jpg,photo/9.jpg',NULL,'好喝,一分价钱一分货',510,166,'拉菲','美国','波尔多','美乐','商务','DO','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('3dce6862-d392-4605-9bf8-f292c07d2179','wine96','photo/5.jpg,photo/9.jpg',NULL,'高大上,酸就是瑟',685,191,'浪迪','利亚','西安','马卡贝奥','泡妞','AOC','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('40428b3f-aec2-4666-93fc-dee36fefb2e0','wine56','photo/3.jpg,photo/6.jpg',NULL,'好喝,一分价钱一分货',761,176,'浪迪','利亚','勃艮第','长相思','泡妞','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('43529600-ec6e-40c2-9fd5-4ca420cafbcc','wine0','photo/4.jpg,photo/4.jpg',NULL,'好喝,有品位',594,102,'浪迪','中国','奥克','赤霞珠','聚会','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('43c0abbf-fa65-41cd-83f1-336ae1033b26','wine36','photo/1.jpg,photo/7.jpg',NULL,'高大上,高大上',911,174,'大宝','中国','波尔多','长相思','泡妞','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('43d3c508-a35a-4d55-886f-5a1107ba71ad','wine55','photo/6.jpg,photo/2.jpg',NULL,'酸就是瑟,有品位',895,97,'博若莱','利亚','西安','长相思','聚会','VCE','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('45d18396-f75d-45d0-8994-900cc2a72831','wine37','photo/4.jpg,photo/6.jpg',NULL,'一分价钱一分货,酸就是瑟',991,131,'圣保罗','意大利','西安','赤霞珠','聚会','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('460cf6d6-4d2c-4418-8985-125a9117a939','wine2','photo/7.jpg,photo/3.jpg',NULL,'有品位,一分价钱一分货',896,193,'拉菲','法国','奥克','长相思','泡妞','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('46fbf599-6739-49e4-b208-febfcb9aa91a','wine30','photo/5.jpg,photo/9.jpg',NULL,'高大上,一分价钱一分货',536,195,'博若莱','美国','波尔多','马卡贝奥','聚会','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('476521d9-d7d8-409b-9cce-3073365d7714','wine50','photo/6.jpg,photo/9.jpg',NULL,'好喝,有品位',656,109,'浪迪','意大利','波尔多','马卡贝奥','泡妞','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('4d52b80f-7c0a-4a0b-9f9d-0859894b0423','wine3','photo/7.jpg,photo/5.jpg',NULL,'一分价钱一分货,高大上',922,107,'博若莱','意大利','勃艮第','马卡贝奥','泡妞','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('4fcaac22-8e8c-4a78-aa13-e477ece13ed1','wine16','photo/8.jpg,photo/0.jpg',NULL,'一分价钱一分货,好喝',419,152,'大宝','法国','波尔多','美乐','聚会','AOC','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('56a9701f-8d7d-4782-b55e-8bf8db74cbb5','wine34','photo/0.jpg,photo/3.jpg',NULL,'酸就是瑟,酸就是瑟',806,138,'博若莱','利亚','西安','美乐','商务','VDQS','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('64e523f0-f21b-426b-82c9-2113091b9eba','wine19','photo/7.jpg,photo/1.jpg',NULL,'高大上,高大上',745,178,'大宝','中国','西安','马卡贝奥','聚会','DO','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('67208973-efee-45f8-ae0c-48303d3ee1fa','wine97','photo/4.jpg,photo/8.jpg',NULL,'高大上,有品位',667,158,'浪迪','美国','奥克','美乐','泡妞','DO','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('67832f40-ab02-46d0-9603-63992c408c1f','wine1','photo/9.jpg,photo/3.jpg',NULL,'高大上,一分价钱一分货',521,166,'拉菲','意大利','奥克','赤霞珠','泡妞','AOC','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('680e47c0-9ccb-456e-8ab2-b8d877afeb0e','wine21','photo/1.jpg,photo/7.jpg',NULL,'好喝,好喝',942,130,'博若莱','法国','西安','长相思','商务','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('683fabad-550c-46da-9fec-6958eb48abb7','wine66','photo/9.jpg,photo/5.jpg',NULL,'酸就是瑟,有品位',443,196,'拉菲','法国','波尔多','美乐','商务','VDQS','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('68861321-a70e-4e24-a063-42c1d877d5bd','wine25','photo/3.jpg,photo/0.jpg',NULL,'好喝,有品位',417,124,'圣保罗','美国','奥克','美乐','聚会','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('69542dda-e429-4e54-861e-f6e9fd0bf846','wine27','photo/1.jpg,photo/8.jpg',NULL,'有品位,高大上',996,119,'大宝','中国','西安','赤霞珠','聚会','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('699bfca5-882d-4946-8cd0-7d11e4fc1914','wine13','photo/4.jpg,photo/9.jpg',NULL,'一分价钱一分货,好喝',752,192,'圣保罗','中国','勃艮第','马卡贝奥','聚会','AOC','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('6f219d01-af9d-4286-b47b-277c0a6bb758','wine72','photo/5.jpg,photo/7.jpg',NULL,'好喝,高大上',605,177,'浪迪','中国','波尔多','美乐','聚会','DO','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('6fcde5de-ab0b-4a76-8899-bd65d4314c64','wine71','photo/9.jpg,photo/0.jpg',NULL,'好喝,一分价钱一分货',972,192,'博若莱','法国','波尔多','美乐','泡妞','VCE','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('73a87e10-540d-4414-9587-dd6962e4214f','wine88','photo/6.jpg,photo/0.jpg',NULL,'一分价钱一分货,酸就是瑟',690,88,'圣保罗','意大利','波尔多','马卡贝奥','聚会','AOC','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('73ec8af5-c819-48c5-bbf6-1eb2b2eb9a37','wine98','photo/4.jpg,photo/0.jpg',NULL,'高大上,酸就是瑟',615,104,'浪迪','利亚','波尔多','长相思','商务','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('74fb3962-c3a0-40f5-9ca3-112314d40500','wine12','photo/4.jpg,photo/6.jpg',NULL,'酸就是瑟,高大上',414,118,'博若莱','利亚','奥克','赤霞珠','商务','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('7a6470ac-c5fa-4ebb-88ce-7a461ab85097','wine70','photo/1.jpg,photo/5.jpg',NULL,'有品位,好喝',464,81,'浪迪','美国','奥克','长相思','泡妞','VCE','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('7aca6f6d-4fbb-413c-81a6-1857ebdafecd','wine74','photo/5.jpg,photo/7.jpg',NULL,'一分价钱一分货,高大上',732,150,'拉菲','意大利','西安','马卡贝奥','商务','DO','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('7ad6c364-ccfc-4862-ab6c-dc64b9a878d1','wine67','photo/1.jpg,photo/1.jpg',NULL,'酸就是瑟,好喝',586,170,'圣保罗','法国','勃艮第','赤霞珠','聚会','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('83c0ed1a-2f70-4556-9cdd-8037bd686489','wine38','photo/9.jpg,photo/6.jpg',NULL,'高大上,酸就是瑟',876,50,'博若莱','利亚','奥克','美乐','泡妞','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('86201e3c-05ac-4862-8270-5634f93ced6c','wine6','photo/7.jpg,photo/0.jpg',NULL,'好喝,有品位',607,149,'大宝','法国','西安','长相思','聚会','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('869aa7d5-9fd4-4469-bcd8-c8eccf9148a9','wine81','photo/0.jpg,photo/5.jpg',NULL,'高大上,酸就是瑟',840,138,'拉菲','法国','勃艮第','长相思','节日拜访','VCE','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('885f7af3-ab19-4c8d-b4b5-3f05264d4c74','wine99','photo/9.jpg,photo/9.jpg',NULL,'一分价钱一分货,高大上',613,139,'拉菲','意大利','波尔多','长相思','节日拜访','VDQS','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('8932b13b-ef0b-401b-9e51-600aab86cfa3','wine28','photo/5.jpg,photo/3.jpg',NULL,'高大上,高大上',609,73,'浪迪','中国','勃艮第','美乐','节日拜访','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('8e9cafda-7c39-478b-b45e-969ccefd1577','wine42','photo/2.jpg,photo/9.jpg',NULL,'高大上,高大上',581,191,'圣保罗','利亚','奥克','赤霞珠','泡妞','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('8ef9237c-2cba-449a-ba62-1a7ed3f4249b','wine63','photo/8.jpg,photo/8.jpg',NULL,'有品位,好喝',842,139,'大宝','中国','东南奥','赤霞珠','泡妞','AOC','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('9042a297-4ab4-4be6-8b3e-a06cba99d42a','wine18','photo/5.jpg,photo/6.jpg',NULL,'一分价钱一分货,高大上',708,50,'拉菲','法国','东南奥','马卡贝奥','商务','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('915a9730-7f5d-49e6-9a31-d5ed3b27b988','wine76','photo/2.jpg,photo/4.jpg',NULL,'有品位,高大上',693,149,'博若莱','意大利','波尔多','美乐','泡妞','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('932c7efb-3c8e-43b6-82df-5d1e05f53aa5','wine58','photo/5.jpg,photo/3.jpg',NULL,'有品位,好喝',844,167,'大宝','法国','勃艮第','西拉','聚会','DO','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('93d81fd8-7ed8-492e-84d5-707eb61d18aa','wine41','photo/2.jpg,photo/9.jpg',NULL,'高大上,一分价钱一分货',515,81,'拉菲','利亚','西安','长相思','泡妞','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('9532d416-62ab-400a-8283-701c8eb26d83','wine29','photo/6.jpg,photo/1.jpg',NULL,'酸就是瑟,一分价钱一分货',977,91,'圣保罗','法国','东南奥','赤霞珠','商务','VDQS','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('95f522d4-a29c-4892-a657-0bd719145b94','wine84','photo/3.jpg,photo/3.jpg',NULL,'有品位,有品位',453,180,'圣保罗','意大利','东南奥','长相思','聚会','VCE','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('a0bb0dea-2a9b-475a-a1b5-ad44ed93ce1d','wine77','photo/0.jpg,photo/2.jpg',NULL,'高大上,好喝',863,145,'拉菲','意大利','东南奥','赤霞珠','聚会','VDQS','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('a1b7c356-6f7d-4f76-ba02-96bfce5f661a','wine86','photo/2.jpg,photo/5.jpg',NULL,'高大上,高大上',626,89,'浪迪','中国','西安','美乐','商务','VDQS','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('a63ff175-e1fa-4588-bef0-31b7af6f0e6a','wine26','photo/1.jpg,photo/9.jpg',NULL,'有品位,一分价钱一分货',939,177,'拉菲','意大利','西安','美乐','聚会','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('a7801068-f835-4a6d-b84f-7b026c617bc3','wine62','photo/9.jpg,photo/7.jpg',NULL,'一分价钱一分货,有品位',514,170,'大宝','利亚','勃艮第','长相思','聚会','DO','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('a9c2aada-9e0a-4f74-98bd-8098b44b781c','wine53','photo/9.jpg,photo/5.jpg',NULL,'高大上,好喝',399,137,'圣保罗','意大利','奥克','美乐','聚会','DO','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('aaff76e9-db2e-4015-8bca-f047e38d7dff','wine79','photo/9.jpg,photo/6.jpg',NULL,'酸就是瑟,好喝',910,57,'圣保罗','法国','勃艮第','美乐','商务','VCE','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('ad867189-2d79-4e5e-acd5-7a673913d914','wine60','photo/6.jpg,photo/5.jpg',NULL,'有品位,高大上',723,75,'大宝','法国','勃艮第','美乐','泡妞','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('aeea9990-68fa-4163-a2cd-d9378a2d656b','wine43','photo/1.jpg,photo/4.jpg',NULL,'好喝,一分价钱一分货',565,87,'圣保罗','中国','西安','马卡贝奥','节日拜访','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('b1e97e2e-fc29-4672-9666-8afdd342e7da','wine23','photo/4.jpg,photo/6.jpg',NULL,'酸就是瑟,高大上',904,65,'圣保罗','意大利','勃艮第','长相思','商务','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('b2e96831-f30e-466c-81dc-ce97d9c51d8b','wine64','photo/8.jpg,photo/3.jpg',NULL,'好喝,一分价钱一分货',747,97,'圣保罗','利亚','东南奥','马卡贝奥','泡妞','DO','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('b48846be-4377-4f69-96d0-5c5d09bd0c67','wine7','photo/3.jpg,photo/0.jpg',NULL,'一分价钱一分货,高大上',502,106,'大宝','利亚','东南奥','长相思','泡妞','DO','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('b5ebdf9b-627b-4993-94b7-cc3cd6e2bc39','wine15','photo/3.jpg,photo/6.jpg',NULL,'一分价钱一分货,高大上',760,156,'圣保罗','法国','西安','马卡贝奥','商务','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('b7338048-f6a3-4a8f-99c1-6b2c486fdbff','wine78','photo/6.jpg,photo/1.jpg',NULL,'高大上,一分价钱一分货',863,165,'浪迪','利亚','东南奥','西拉','泡妞','DO','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('bbe86692-8331-4819-a3fb-1f32830e29cb','wine24','photo/0.jpg,photo/8.jpg',NULL,'酸就是瑟,酸就是瑟',912,54,'博若莱','利亚','东南奥','美乐','泡妞','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('bc82a44e-6abc-428c-b52e-425a69225641','wine48','photo/9.jpg,photo/3.jpg',NULL,'酸就是瑟,酸就是瑟',759,90,'博若莱','利亚','东南奥','马卡贝奥','泡妞','VDQS','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('c271bd5e-2b8d-4d43-9bc8-c145aa87ee1f','wine87','photo/6.jpg,photo/0.jpg',NULL,'好喝,高大上',386,96,'博若莱','利亚','奥克','美乐','节日拜访','VCE','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('c3360d94-df45-45a0-94fb-f3638189a9c4','wine61','photo/6.jpg,photo/4.jpg',NULL,'好喝,高大上',432,93,'圣保罗','美国','波尔多','美乐','商务','VCE','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('c685e3f9-b9ca-4fc7-8daa-80430fb10b8d','wine85','photo/3.jpg,photo/3.jpg',NULL,'高大上,酸就是瑟',914,198,'拉菲','中国','勃艮第','长相思','节日拜访','AOC','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('c78a161b-d550-495f-803d-bc168657b794','wine14','photo/3.jpg,photo/6.jpg',NULL,'好喝,好喝',862,106,'拉菲','意大利','西安','马卡贝奥','泡妞','VDQS','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('c7974825-29a5-42d9-a7de-e06a4a1227e7','wine46','photo/7.jpg,photo/5.jpg',NULL,'酸就是瑟,好喝',586,169,'大宝','中国','波尔多','马卡贝奥','节日拜访','AOC','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('c871d6ac-342a-4ee4-a859-9628547720fc','wine57','photo/3.jpg,photo/8.jpg',NULL,'一分价钱一分货,有品位',458,156,'大宝','法国','波尔多','美乐','商务','VDQS','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('c8a06287-03bc-47d1-b2d9-62de33918757','wine33','photo/9.jpg,photo/1.jpg',NULL,'有品位,好喝',834,178,'博若莱','中国','西安','长相思','节日拜访','AOC','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('cc511a9c-5d4d-42c4-83dc-f05a5424291e','wine45','photo/0.jpg,photo/7.jpg',NULL,'好喝,一分价钱一分货',610,148,'拉菲','利亚','奥克','西拉','聚会','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('cfbfe526-ee57-43e8-8df4-5c31ef723ba0','wine9','photo/9.jpg,photo/9.jpg',NULL,'酸就是瑟,酸就是瑟',987,163,'博若莱','美国','西安','马卡贝奥','泡妞','VDQS','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('d095c1ef-48dc-4b86-9f44-c4a03b7a5d3c','wine82','photo/7.jpg,photo/9.jpg',NULL,'有品位,高大上',708,95,'拉菲','美国','西安','长相思','泡妞','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('dc557512-e9f0-4994-a608-b78b8c6b4f91','wine83','photo/7.jpg,photo/4.jpg',NULL,'高大上,有品位',772,76,'大宝','美国','东南奥','马卡贝奥','商务','VCE','白葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('de7fe2c6-4090-4972-9418-5df9f9a394d2','wine91','photo/0.jpg,photo/8.jpg',NULL,'有品位,酸就是瑟',658,81,'大宝','法国','西安','赤霞珠','商务','VDQS','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('dfc97271-fa90-472d-8807-626e1c188b38','wine54','photo/7.jpg,photo/9.jpg',NULL,'一分价钱一分货,好喝',952,85,'博若莱','法国','东南奥','马卡贝奥','聚会','VCE','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('e07c8691-7304-4042-97cf-4f78aaadf645','wine39','photo/9.jpg,photo/5.jpg',NULL,'一分价钱一分货,一分价钱一分货',727,65,'浪迪','美国','奥克','美乐','节日拜访','DO','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('e9048739-4625-44e2-98f8-398fa1d816fc','wine11','photo/7.jpg,photo/4.jpg',NULL,'好喝,高大上',595,52,'博若莱','中国','东南奥','长相思','泡妞','DO','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('ec91e521-370a-46ac-80fb-919975b5f6a2','wine90','photo/1.jpg,photo/6.jpg',NULL,'一分价钱一分货,有品位',440,165,'博若莱','中国','勃艮第','西拉','商务','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('ee2fe1d3-5fde-4ea2-b280-6db65601302c','wine75','photo/0.jpg,photo/1.jpg',NULL,'一分价钱一分货,高大上',462,199,'圣保罗','意大利','西安','美乐','商务','VCE','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('eed9048b-b796-4ecc-a1fb-7ac3f8c6444c','wine10','photo/9.jpg,photo/5.jpg',NULL,'好喝,有品位',597,89,'浪迪','法国','奥克','马卡贝奥','泡妞','VDQS','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('efb5d3e6-9b33-4e8a-885f-41a709170a9a','wine8','photo/7.jpg,photo/3.jpg',NULL,'好喝,酸就是瑟',914,98,'浪迪','利亚','勃艮第','美乐','商务','DO','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('f071a6d4-26b6-4a84-b61e-f750e816bccd','wine32','photo/2.jpg,photo/2.jpg',NULL,'一分价钱一分货,酸就是瑟',598,106,'拉菲','意大利','勃艮第','西拉','商务','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('f266fbc4-0e98-4ffc-b591-719a3831b128','wine89','photo/5.jpg,photo/8.jpg',NULL,'有品位,有品位',696,99,'拉菲','意大利','东南奥','西拉','商务','AOC','桃红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('f2b7623f-6513-45f9-ab91-a6930d163831','wine95','photo/3.jpg,photo/1.jpg',NULL,'酸就是瑟,高大上',658,149,'浪迪','法国','东南奥','赤霞珠','商务','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('f634a1b5-295b-40d7-b7f5-c63432bbcebd','wine49','photo/5.jpg,photo/2.jpg',NULL,'高大上,好喝',615,111,'圣保罗','中国','波尔多','西拉','商务','AOC','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('f667a2e9-95d4-4947-861e-26b8e8735eeb','wine35','photo/8.jpg,photo/4.jpg',NULL,'好喝,一分价钱一分货',648,120,'博若莱','利亚','波尔多','西拉','聚会','VCE','起泡酒','2015-11-28 17:55:57','2015-11-28 09:55:57'),('f87a684c-aa96-4aa8-972a-5a8568cd661e','wine94','photo/0.jpg,photo/5.jpg',NULL,'酸就是瑟,酸就是瑟',876,199,'拉菲','法国','勃艮第','美乐','泡妞','AOC','红葡萄酒','2015-11-28 17:55:57','2015-11-28 09:55:57');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `session` (
  `sid` varchar(36) NOT NULL,
  `sval` text NOT NULL,
  `expiry_time` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ship_city`
--

DROP TABLE IF EXISTS `ship_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ship_city` (
  `city_id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `district` text NOT NULL,
  PRIMARY KEY (`city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ship_city`
--

LOCK TABLES `ship_city` WRITE;
/*!40000 ALTER TABLE `ship_city` DISABLE KEYS */;
INSERT INTO `ship_city` VALUES ('5e245b8f-8dbb-4a6d-b735-605f0372a4c1','江苏省','南通市,南京市,苏州市,常州市'),('bd950ef9-043f-49f1-bc3b-d6c7e6d22a1b','上海市','闵行区,静安区,徐汇区,黄浦区');
/*!40000 ALTER TABLE `ship_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'wineprj'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-11-28 20:30:21
