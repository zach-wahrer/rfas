-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 29, 2014 at 08:15 AM
-- Server version: 5.5.37
-- PHP Version: 5.4.6-1ubuntu1.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `route_feedback`
--

-- --------------------------------------------------------

--
-- Table structure for table `Boulder_Grade_Index`
--

CREATE TABLE IF NOT EXISTS `Boulder_Grade_Index` (
  `ID` int(2) NOT NULL AUTO_INCREMENT,
  `Boulder Grade` varchar(5) CHARACTER SET hp8 NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID` (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

--
-- Dumping data for table `Boulder_Grade_Index`
--

INSERT INTO `Boulder_Grade_Index` (`ID`, `Boulder Grade`) VALUES
(1, 'VEasy'),
(2, 'V0'),
(3, 'V1'),
(4, 'V2'),
(5, 'V3'),
(6, 'V4'),
(7, 'V5'),
(8, 'V6'),
(9, 'V7'),
(10, 'V8'),
(11, 'V9'),
(12, 'V10'),
(13, 'V11'),
(14, 'V12'),
(15, 'V13'),
(16, 'V14'),
(17, 'V15');

-- --------------------------------------------------------

--
-- Table structure for table `Feedback_Data`
--

CREATE TABLE IF NOT EXISTS `Feedback_Data` (
  `Index` int(11) NOT NULL AUTO_INCREMENT,
  `Name1` varchar(2) NOT NULL,
  `Name2` varchar(2) NOT NULL,
  `Name3` varchar(2) NOT NULL,
  `Type` varchar(1) NOT NULL,
  `Grade` varchar(2) NOT NULL,
  `OriginalGrade` varchar(2) NOT NULL,
  `Date` date NOT NULL,
  `Soft1.Quality` varchar(3) NOT NULL,
  `Soft2.Quality` varchar(3) NOT NULL,
  `Soft3.Quality` varchar(3) NOT NULL,
  `Soft4.Quality` varchar(3) NOT NULL,
  `Soft5.Quality` varchar(3) NOT NULL,
  `Soft6.Quality` varchar(3) NOT NULL,
  `Soft7.Quality` varchar(3) NOT NULL,
  `Soft8.Quality` varchar(3) NOT NULL,
  `On1.Quality` varchar(3) NOT NULL,
  `On2.Quality` varchar(3) NOT NULL,
  `On3.Quality` varchar(3) NOT NULL,
  `On4.Quality` varchar(3) NOT NULL,
  `On5.Quality` varchar(3) NOT NULL,
  `On6.Quality` varchar(3) NOT NULL,
  `On7.Quality` varchar(3) NOT NULL,
  `On8.Quality` varchar(3) NOT NULL,
  `Hard1.Quality` varchar(3) NOT NULL,
  `Hard2.Quality` varchar(3) NOT NULL,
  `Hard3.Quality` varchar(3) NOT NULL,
  `Hard4.Quality` varchar(3) NOT NULL,
  `Hard5.Quality` varchar(3) NOT NULL,
  `Hard6.Quality` varchar(3) NOT NULL,
  `Hard7.Quality` varchar(3) NOT NULL,
  `Hard8.Quality` varchar(3) DEFAULT NULL,
  `Comment1` varchar(100) NOT NULL,
  `Comment2` varchar(100) NOT NULL,
  `Comment3` varchar(100) NOT NULL,
  `Comment4` varchar(100) NOT NULL,
  `Comment5` varchar(100) NOT NULL,
  `Comment6` varchar(100) NOT NULL,
  `Comment7` varchar(100) NOT NULL,
  `Comment8` varchar(100) NOT NULL,
  PRIMARY KEY (`Index`),
  KEY `Index` (`Index`),
  KEY `Index_2` (`Index`)
) ENGINE=InnoDB  DEFAULT CHARSET=hp8 AUTO_INCREMENT=2631 ;

--
-- Table structure for table `Route_Grade_Index`
--

CREATE TABLE IF NOT EXISTS `Route_Grade_Index` (
  `ID` int(2) NOT NULL AUTO_INCREMENT,
  `Route Grade` varchar(6) CHARACTER SET hp8 NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID` (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23 ;

--
-- Dumping data for table `Route_Grade_Index`
--

INSERT INTO `Route_Grade_Index` (`ID`, `Route Grade`) VALUES
(1, '5.Easy'),
(2, '5.5'),
(3, '5.6'),
(4, '5.7'),
(5, '5.8'),
(6, '5.9'),
(7, '5.10-'),
(8, '5.10'),
(9, '5.10+'),
(10, '5.11-'),
(11, '5.11'),
(12, '5.11+'),
(13, '5.12-'),
(14, '5.12'),
(15, '5.12+'),
(16, '5.13-'),
(17, '5.13'),
(18, '5.13+'),
(19, '5.14-'),
(20, '5.14'),
(21, '5.14+'),
(22, '5.15-');

-- --------------------------------------------------------

--
-- Table structure for table `Setter_Index`
--

CREATE TABLE IF NOT EXISTS `Setter_Index` (
  `ID` int(2) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

--
-- Dumping data for table `Setter_Index`
--

INSERT INTO `Setter_Index` (`ID`, `Name`) VALUES
(1, 'Default');


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
