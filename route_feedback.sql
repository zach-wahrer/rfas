-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 15, 2020 at 11:11 AM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `route_feedback_structure`
--

-- --------------------------------------------------------

--
-- Table structure for table `Boulder_Grade_Index`
--

CREATE TABLE `Boulder_Grade_Index` (
  `ID` int(2) NOT NULL,
  `Boulder Grade` varchar(5) CHARACTER SET hp8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Feedback_Data`
--

CREATE TABLE `Feedback_Data` (
  `Index` int(11) NOT NULL,
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
  `Comment8` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=hp8;

-- --------------------------------------------------------

--
-- Table structure for table `Route_Grade_Index`
--

CREATE TABLE `Route_Grade_Index` (
  `ID` int(2) NOT NULL,
  `Route Grade` varchar(6) CHARACTER SET hp8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Setter_Index`
--

CREATE TABLE `Setter_Index` (
  `ID` int(2) NOT NULL,
  `Name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Boulder_Grade_Index`
--
ALTER TABLE `Boulder_Grade_Index`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID` (`ID`);

--
-- Indexes for table `Feedback_Data`
--
ALTER TABLE `Feedback_Data`
  ADD PRIMARY KEY (`Index`),
  ADD KEY `Index` (`Index`),
  ADD KEY `Index_2` (`Index`);

--
-- Indexes for table `Route_Grade_Index`
--
ALTER TABLE `Route_Grade_Index`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID` (`ID`);

--
-- Indexes for table `Setter_Index`
--
ALTER TABLE `Setter_Index`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Boulder_Grade_Index`
--
ALTER TABLE `Boulder_Grade_Index`
  MODIFY `ID` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT for table `Feedback_Data`
--
ALTER TABLE `Feedback_Data`
  MODIFY `Index` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2634;
--
-- AUTO_INCREMENT for table `Route_Grade_Index`
--
ALTER TABLE `Route_Grade_Index`
  MODIFY `ID` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
--
-- AUTO_INCREMENT for table `Setter_Index`
--
ALTER TABLE `Setter_Index`
  MODIFY `ID` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
