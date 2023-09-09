CREATE DATABASE IF NOT EXISTS `crud_python_db`;

CREATE TABLE IF NOT EXISTS `sales` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `price` INT NULL,
  PRIMARY KEY (`id`));

INSERT INTO `sales` (`id`, `name`, `price`) VALUES (1, 'Coca-Cola', 5);
