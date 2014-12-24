-- MySQL Script generated by MySQL Workbench
-- Tue Dec  2 15:43:42 2014
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema finedb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema finedb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `finedb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `finedb` ;

-- -----------------------------------------------------
-- Table `finedb`.`BOOKINFO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`BOOKINFO` (
  `book_num` CHAR(5) NOT NULL,
  `name` VARCHAR(200) NOT NULL,
  `author` VARCHAR(200) NULL,
  `publisher` VARCHAR(200) NULL,
  `publish_year` TINYINT(4) NULL,
  `ISBN` VARCHAR(13) NOT NULL,
  `location1` VARCHAR(10) NULL,
  `location2` VARCHAR(100) NULL,
  `large_ctag` VARCHAR(100) NULL,
  `medium_ctag` VARCHAR(100) NULL,
  `small_ctag` VARCHAR(100) NULL,
  `cover_img` VARCHAR(200) NULL,
  PRIMARY KEY (`book_num`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `finedb`.`USER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`USER` (
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(40) NOT NULL,
  `userName` VARCHAR(20) NOT NULL,
  `attendOrNot` INT NULL DEFAULT 0,
  `semesterNum` INT NULL DEFAULT 1,
  `majorNameFirst` INT NULL DEFAULT NULL,
  `majorNameSecond` INT NULL DEFAULT NULL,
  PRIMARY KEY (`email`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `finedb`.`ISBN_PREFER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`ISBN_PREFER` (
  `bookISBN` VARCHAR(13) NOT NULL,
  `READ_count` INT NOT NULL DEFAULT 1,
  `WISH_count` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`bookISBN`),
  INDEX `ISBN_PREFER_idx` (`WISH_count`,`READ_count` DESC)
)
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `finedb`.`BOOKLIST_READ`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`BOOKLIST_READ` (
  `USER_email` VARCHAR(45) NOT NULL,
  `bookISBN` VARCHAR(13) NOT NULL,
  CONSTRAINT `fk_BOOKLIST_READ_USER`
    FOREIGN KEY (`USER_email`)
    REFERENCES `finedb`.`USER` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_BOOKLIST_READ_ISBN_PREFER`
    FOREIGN KEY (`bookISBN`)
    REFERENCES `finedb`.`ISBN_PREFER` (`bookISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `finedb`.`BOOKLIST_WISH`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`BOOKLIST_WISH` (
  `USER_email` VARCHAR(45) NOT NULL,
  `bookISBN` CHAR(13) NOT NULL,
  CONSTRAINT `fk_BOOKLIST_WISH_USER`
    FOREIGN KEY (`USER_email`)
    REFERENCES `finedb`.`USER` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_BOOKLIST_WISH_ISBN_PREFER`
    FOREIGN KEY (`bookISBN`)
    REFERENCES `finedb`.`ISBN_PREFER` (`bookISBN`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `finedb`.`POST`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`POST` (
  `postId` INT NOT NULL,
  `post` TEXT NULL,
  `postImg` VARCHAR(45) NULL,
  `USER_email` VARCHAR(45) NOT NULL,
  `postISBN` VARCHAR(13),
  `likeCount` INT NOT NULL DEFAULT 0,
  `scrapCount` INT NOT NULL DEFAULT 0,
  `commentCount` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`postId`),
  INDEX `fk_POST_USER1_idx` (`USER_email` ASC),
  CONSTRAINT `fk_POST_USER1`
    FOREIGN KEY (`USER_email`)
    REFERENCES `finedb`.`USER` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `finedb`.`LIKE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`LIKE` (
  `POST_postId` INT NOT NULL,
  `USER_email` VARCHAR(45) NOT NULL,
  INDEX `fk_LIKE_POST1_idx` (`POST_postId` ASC),
  INDEX `fk_LIKE_USER1_idx` (`USER_email` ASC),
  CONSTRAINT `fk_LIKE_POST1`
    FOREIGN KEY (`POST_postId`)
    REFERENCES `finedb`.`POST` (`postId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_LIKE_USER1`
    FOREIGN KEY (`USER_email`)
    REFERENCES `finedb`.`USER` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `finedb`.`COMMENT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`COMMENT` (
  `commentId` INT NOT NULL,
  `comment` TEXT NULL,
  `POST_postId` INT NOT NULL,
  `USER_email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`commentId`),
  INDEX `fk_COMMENT_POST1_idx` (`POST_postId` ASC),
  INDEX `fk_COMMENT_USER1_idx` (`USER_email` ASC),
  CONSTRAINT `fk_COMMENT_POST1`
    FOREIGN KEY (`POST_postId`)
    REFERENCES `finedb`.`POST` (`postId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_COMMENT_USER1`
    FOREIGN KEY (`USER_email`)
    REFERENCES `finedb`.`USER` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `finedb`.`BOOK_COMMENT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `finedb`.`BOOK_COMMENT` (
  `book_comment_id` INT NOT NULL,
  `book_comment` TEXT NULL,
  `ISBN` TINYINT(13) NULL,
  `USER_email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`book_comment_id`),
  INDEX `fk_BOOK_COMMENT_USER1_idx` (`USER_email` ASC),
  CONSTRAINT `fk_BOOK_COMMENT_USER1`
    FOREIGN KEY (`USER_email`)
    REFERENCES `finedb`.`USER` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
