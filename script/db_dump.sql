-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: Project
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.16.04.1

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
-- Table structure for table `creditcardserver`
--

/*DROP TABLE IF EXISTS `creditcardserver`;*/
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditcardserver` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_no` bigint(20) unsigned NOT NULL,
  `c_name` varchar(50) DEFAULT NULL,
  `c_cvv` int(11) DEFAULT NULL,
  `c_expiry_month` int(11) DEFAULT NULL,
  `c_expiry_year` int(11) DEFAULT NULL,
  `c_limit` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `expense`
--

DROP TABLE IF EXISTS `expense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expense` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `owed_by` int(50) NOT NULL,
  `owed_to` int(50) NOT NULL,
  `amount` int(10) NOT NULL,
  `status_id` int(10) NOT NULL,
  `transaction_id` int(50) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_id_con_idx` (`transaction_id`),
  KEY `status_con_idx` (`status_id`),
  KEY `user_owed_to_con_idx` (`owed_to`),
  KEY `user_owed_by_con_idx` (`owed_by`),
  CONSTRAINT `status_con` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `transaction_id_con` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`payer_id`),
  CONSTRAINT `user_owed_by_con` FOREIGN KEY (`owed_by`) REFERENCES `users` (`id`),
  CONSTRAINT `user_owed_to_con` FOREIGN KEY (`owed_to`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `user_id` int(50) NOT NULL,
  `card_number` int(16) NOT NULL,
  `card_expiry_month` int(2) NOT NULL,
  `card_expity_year` int(4) NOT NULL,
  `card_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_con_idx` (`user_id`),
  CONSTRAINT `user_con` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `security_ans`
--

DROP TABLE IF EXISTS `security_ans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `security_ans` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answer` varchar(255) NOT NULL,
  `security_question_id` int(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `security_question_id_UNIQUE` (`security_question_id`),
  CONSTRAINT `security_question_cons` FOREIGN KEY (`security_question_id`) REFERENCES `security_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `security_question`
--

DROP TABLE IF EXISTS `security_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `security_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `payer_id` int(50) NOT NULL,
  `payee_id` int(50) NOT NULL,
  `amount` int(10) DEFAULT NULL,
  `status_id` int(10) NOT NULL,
  `details` varchar(255) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `payment_id` int(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_con_idx` (`payer_id`,`payee_id`),
  KEY `remarks_con_idx` (`status_id`),
  KEY `payment_id_con_idx` (`payment_id`),
  KEY `user_con_idx1` (`payee_id`),
  CONSTRAINT `payee_id_con` FOREIGN KEY (`payee_id`) REFERENCES `users` (`id`),
  CONSTRAINT `payer_id_con` FOREIGN KEY (`payer_id`) REFERENCES `users` (`id`),
  CONSTRAINT `payment_id_con` FOREIGN KEY (`payment_id`) REFERENCES `payments` (`id`),
  CONSTRAINT `status_id_con` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `security_ans_id` int(50) NOT NULL,
  `security_question_id` int(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `security_answer_cons` (`security_ans_id`),
  CONSTRAINT `security_answer_cons` FOREIGN KEY (`security_ans_id`) REFERENCES `security_ans` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-07 18:13:03
