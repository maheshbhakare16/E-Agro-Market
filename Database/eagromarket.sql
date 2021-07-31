-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: localhost    Database: eagromarket
-- ------------------------------------------------------
-- Server version	8.0.25-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `farmer_signup`
--

DROP TABLE IF EXISTS `farmer_signup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmer_signup` (
  `sr_no` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(20) DEFAULT NULL,
  `lname` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `address` varchar(80) NOT NULL,
  `email` varchar(20) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`sr_no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmer_signup`
--

LOCK TABLES `farmer_signup` WRITE;
/*!40000 ALTER TABLE `farmer_signup` DISABLE KEYS */;
INSERT INTO `farmer_signup` VALUES (1,'MAHESH','BHAKARE','mahesh16','MAHESHB','MAHESH@GMAIL.COM','2019-11-07','male','1234567890');
/*!40000 ALTER TABLE `farmer_signup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `sr_no` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `productname` varchar(30) NOT NULL,
  `quantity` varchar(20) NOT NULL,
  `contact_no` varchar(20) NOT NULL,
  `price` varchar(20) NOT NULL,
  `fullname` varchar(20) NOT NULL,
  `cur_date` datetime DEFAULT NULL,
  `photo` varchar(20) NOT NULL,
  PRIMARY KEY (`sr_no`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (2,'mahesh16','onion','12','1234567890','123','mahesh bhakare','2021-07-29 19:40:42','logo.png');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signup`
--

DROP TABLE IF EXISTS `signup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `signup` (
  `sr_no` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(20) DEFAULT NULL,
  `lname` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `address` varchar(80) NOT NULL,
  `email` varchar(20) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `gstn` varchar(20) NOT NULL,
  PRIMARY KEY (`sr_no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signup`
--

LOCK TABLES `signup` WRITE;
/*!40000 ALTER TABLE `signup` DISABLE KEYS */;
INSERT INTO `signup` VALUES (1,'MAHESH','BHAKARE','mahesh16','MAHESHB','MAHESH@GMAIL.COM','2019-11-13','male','1234567890','12345678');
/*!40000 ALTER TABLE `signup` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-31 14:44:26
