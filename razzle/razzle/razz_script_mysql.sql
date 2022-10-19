-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema razz
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `razz` ;

-- -----------------------------------------------------
-- Schema razz
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `razz` DEFAULT CHARACTER SET utf8 ;
USE `razz` ;

-- -----------------------------------------------------
-- Table `razz`.`categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `razz`.`categories` ;

CREATE TABLE IF NOT EXISTS `razz`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `razz`.`products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `razz`.`products` ;

CREATE TABLE IF NOT EXISTS `razz`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `price` DECIMAL(5,2) NULL DEFAULT NULL,
  `quantity` INT NULL DEFAULT NULL,
  `image_url` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `razz`.`categorizations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `razz`.`categorizations` ;

CREATE TABLE IF NOT EXISTS `razz`.`categorizations` (
  `products_id` INT NOT NULL,
  `categories_id` INT NOT NULL,
  PRIMARY KEY (`products_id`, `categories_id`),
  INDEX `fk_categorizations_category1_idx` (`categories_id` ASC) INVISIBLE,
  INDEX `fk_categorizations_product1_idx` (`products_id` ASC) VISIBLE,
  CONSTRAINT `fk_categorizations_category1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `razz`.`categories` (`id`),
  CONSTRAINT `fk_categorizations_product1_idx`
    FOREIGN KEY (`products_id`)
    REFERENCES `razz`.`products` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `razz`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `razz`.`users` ;

CREATE TABLE IF NOT EXISTS `razz`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `admin` TINYINT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(255) NULL DEFAULT NULL,
  `state` VARCHAR(45) NULL DEFAULT NULL,
  `zip` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `razz`.`orders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `razz`.`orders` ;

CREATE TABLE IF NOT EXISTS `razz`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `total_price` DECIMAL(6,2) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_orders_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `razz`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
