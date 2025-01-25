-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: pharmaceutique
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `companies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` varchar(14) DEFAULT NULL,
  `company_type` varchar(100) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES
(3,'12345678901234','Pharmacie','Pharmacie1','0612345678'),
(4,'23456789012345','Pharmacie','Pharmacie2','0623456789'),
(5,'34567890123456','Pharmacie','Pharmacie3','0634567890'),
(6,'45678901234567','Laboratoire','Laboratoire1','0645678901'),
(7,'56789012345678','Laboratoire','Laboratoire2','0656789012'),
(8,'67890123456789','Laboratoire','Laboratoire3','0667890123'),
(9,'78901234567890','Transporteur','Transporteur1','0678901234'),
(10,'89012345678901','Transporteur','Transporteur2','0689012345'),
(11,'90123456789012','Transporteur','Transporteur3','0690123456');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) DEFAULT NULL,
  `product_description` varchar(200) DEFAULT NULL,
  `dosage_mg` int(11) DEFAULT NULL,
  `manufacturer_id` int(11) DEFAULT NULL,
  `approval_date` date DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `product_type` enum('generic','brand') DEFAULT NULL,
  `administration_route` enum('oral','intravenous','nasal','topical','injection') DEFAULT NULL,
  `daily_dosage_frequency` int(11) DEFAULT NULL,
  `recommended_treatment_duration_days` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manufacturer_id` (`manufacturer_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`manufacturer_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `valid_dates` CHECK (`expiration_date` >= `approval_date`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES
(31,'Doliprane','Analgesique et antipyrétique à base de paracétamol',500,NULL,'2023-01-15','2025-01-15','generic','oral',3,7),
(32,'Efferalgan','Antalgique efficace pour la douleur légère à modérée',1000,NULL,'2022-06-10','2024-06-10','brand','oral',2,5),
(33,'Ibuprofène','Anti-inflammatoire non stéroïdien pour les douleurs articulaires',400,NULL,'2021-03-05','2023-03-05','generic','oral',3,10),
(34,'Aspirine','Analgésique, antipyrétique et anti-inflammatoire polyvalent',300,NULL,'2020-09-12','2022-09-12','generic','oral',2,5),
(35,'Amoxicilline','Antibiotique pour les infections bactériennes courantes',250,NULL,'2023-07-01','2025-07-01','brand','oral',3,10),
(36,'Paracétamol','Réduction des fièvres et douleurs légères',500,NULL,'2022-12-20','2025-12-20','generic','oral',2,7),
(37,'Cétirizine','Traitement des allergies saisonnières',10,NULL,'2023-01-10','2026-01-10','brand','oral',1,14),
(38,'Loratadine','Antihistaminique pour les rhinites allergiques',10,NULL,'2023-02-01','2025-02-01','generic','oral',1,10),
(39,'Spasfon','Traitement des douleurs spasmodiques',80,NULL,'2022-08-01','2024-08-01','brand','oral',2,5),
(40,'Fervex','Traitement des symptômes grippaux',NULL,NULL,'2023-11-01','2025-11-01','brand','oral',2,5),
(41,'Magnésium B6','Complément alimentaire pour réduire la fatigue',NULL,NULL,'2022-11-01','2025-11-01','brand','oral',1,30),
(42,'Vitamine D3','Améliore l’absorption du calcium et la santé osseuse',NULL,NULL,'2023-02-15','2026-02-15','brand','oral',1,60),
(43,'Oméga-3','Favorise la santé cardiovasculaire et cérébrale',NULL,NULL,'2021-05-10','2024-05-10','generic','oral',1,90),
(44,'Probiotiques','Renforce la flore intestinale',NULL,NULL,'2023-06-01','2025-06-01','brand','oral',1,30),
(45,'Curcuma','Anti-inflammatoire naturel',NULL,NULL,'2022-03-15','2025-03-15','brand','oral',1,45),
(46,'Zinc','Améliore le système immunitaire',NULL,NULL,'2021-07-01','2024-07-01','generic','oral',1,30),
(47,'Fer','Lutte contre l’anémie et la fatigue',NULL,NULL,'2022-10-20','2025-10-20','brand','oral',1,30),
(48,'Collagène','Améliore la santé de la peau et des articulations',NULL,NULL,'2023-04-01','2026-04-01','brand','oral',1,60),
(49,'Ginseng','Augmente l’énergie et la vitalité',NULL,NULL,'2022-12-01','2025-12-01','brand','oral',1,45),
(50,'Spiruline','Complément riche en nutriments et protéines',NULL,NULL,'2021-09-15','2024-09-15','generic','oral',1,30),
(51,'Spray Nasal','Solution saline pour décongestion nasale',NULL,NULL,'2023-03-20','2024-03-20','brand','nasal',4,5),
(52,'Crème Antifongique','Traitement topique pour infections fongiques cutanées',NULL,NULL,'2023-08-05','2025-08-05','brand','topical',2,14),
(53,'Gel Anti-Douleur','Soulagement rapide des douleurs musculaires',NULL,NULL,'2022-09-01','2024-09-01','generic','topical',2,7),
(54,'Patch Anti-Douleur','Relief prolongé des douleurs chroniques',NULL,NULL,'2023-05-15','2025-05-15','brand','topical',1,14),
(55,'Lentilles de Contact','Correction temporaire de la vision',NULL,NULL,'2022-11-01','2025-11-01','brand','topical',1,90),
(56,'Pansement Antiseptique','Protection contre les infections',NULL,NULL,'2021-04-01','2024-04-01','generic','topical',1,7),
(57,'Solution pour Lentilles','Nettoie et hydrate les lentilles de contact',NULL,NULL,'2023-02-10','2026-02-10','brand','topical',1,180),
(58,'Seringue Stérile','Usage unique pour injections médicales',NULL,NULL,'2023-01-01','2025-01-01','brand','intravenous',1,1),
(59,'Bande Élastique','Soutien pour blessures articulaires',NULL,NULL,'2023-09-01','2025-09-01','brand','topical',1,30),
(60,'Thermomètre Médical','Mesure précise de la température corporelle',NULL,NULL,'2023-12-01','2026-12-01','brand','topical',1,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_entreprise` (`company_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `email_format` CHECK (`email` like '%@%.%')
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(2,'user1@pharmacie1.com','Doe','password1','John','0612345678',3,'Pharmacie1'),
(3,'user2@pharmacie2.com','Smith','password2','Jane','0623456789',4,'Pharmacie2'),
(4,'user3@pharmacie3.com','Brown','password3','Alice','0634567890',5,'Pharmacie3'),
(5,'user1@laboratoire1.com','Taylor','password4','Robert','0645678901',6,'Laboratoire1'),
(6,'user2@laboratoire2.com','Anderson','password5','Emily','0656789012',7,'Laboratoire2'),
(7,'user3@laboratoire3.com','Thomas','password6','David','0667890123',8,'Laboratoire3'),
(8,'user1@transporteur1.com','Moore','password7','Michael','0678901234',9,'Transporteur1'),
(9,'user2@transporteur2.com','Wilson','password8','Emma','0689012345',10,'Transporteur2'),
(10,'user3@transporteur3.com','Davis','password9','Olivia','0690123456',11,'Transporteur3');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-08 20:02:32
