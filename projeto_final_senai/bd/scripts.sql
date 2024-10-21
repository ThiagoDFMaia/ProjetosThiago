
drop database clinica;
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema clinica
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema clinica
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `clinica` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `clinica` ;

-- -----------------------------------------------------
-- Table `clinica`.`pessoa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`pessoa` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(100) NOT NULL,
  `cep` VARCHAR(100) NOT NULL,
  `uf` CHAR(2) NOT NULL,
  `cidade` VARCHAR(30) NOT NULL,
  `complemento` VARCHAR(50) NULL DEFAULT NULL,
  `numero` VARCHAR(15) NULL DEFAULT NULL,
  `telefone_01` VARCHAR(12) NOT NULL,
  `telefone_02` VARCHAR(12) NULL DEFAULT NULL,
  `telefone_03` VARCHAR(12) NULL DEFAULT NULL,
  `rg` VARCHAR(12) NOT NULL,
  `cpf` VARCHAR(11) NOT NULL,
  `data_nas` DATE NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 24
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`convenio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`convenio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cnpj` VARCHAR(15) NOT NULL,
  `descricao` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `cnpj` (`cnpj` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`paciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`paciente` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tipoconvenio` ENUM('individual', 'coletivo', 'publico') NULL DEFAULT NULL,
  `fk_pessoa_id` INT NOT NULL,
  `fk_convenio_id` INT NULL DEFAULT NULL,
  `flgconvenio` BIT(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `fk_pessoa_id_UNIQUE` (`fk_pessoa_id` ASC) VISIBLE,
  INDEX `fk_paciente_2` (`fk_pessoa_id` ASC) VISIBLE,
  INDEX `fk_paciente_3` (`fk_convenio_id` ASC) VISIBLE,
  CONSTRAINT `fk_paciente_2`
    FOREIGN KEY (`fk_pessoa_id`)
    REFERENCES `clinica`.`pessoa` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_paciente_3`
    FOREIGN KEY (`fk_convenio_id`)
    REFERENCES `clinica`.`convenio` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`especialidade`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`especialidade` (
  `codespecialidade` INT NOT NULL AUTO_INCREMENT,
  `descricao` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`codespecialidade`))
ENGINE = InnoDB
AUTO_INCREMENT = 81
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`medico`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`medico` (
  `codmedico` INT NOT NULL AUTO_INCREMENT,
  `crm` VARCHAR(15) NOT NULL,
  `fk_pessoa_id` INT NOT NULL,
  `flgativo` BIT(1) NOT NULL,
  `codespecialidade` INT NOT NULL,
  PRIMARY KEY (`codmedico`),
  UNIQUE INDEX `fk_pessoa_id_UNIQUE` (`fk_pessoa_id` ASC) VISIBLE,
  INDEX `fk_medico_2` (`fk_pessoa_id` ASC) VISIBLE,
  INDEX `fk_medico_especialidade1_idx` (`codespecialidade` ASC) VISIBLE,
  CONSTRAINT `fk_medico_2`
    FOREIGN KEY (`fk_pessoa_id`)
    REFERENCES `clinica`.`pessoa` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_medico_especialidade1`
    FOREIGN KEY (`codespecialidade`)
    REFERENCES `clinica`.`especialidade` (`codespecialidade`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`escala`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`escala` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `data` DATE NOT NULL,
  `quantvagasmanha` SMALLINT NOT NULL,
  `quantvagastarde` SMALLINT NOT NULL,
  `quantvagasnoite` SMALLINT NOT NULL,
  `flaativo` BIT(1) NOT NULL,
  `codmedico` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_escala_medico1_idx` (`codmedico` ASC) VISIBLE,
  CONSTRAINT `fk_escala_medico1`
    FOREIGN KEY (`codmedico`)
    REFERENCES `clinica`.`medico` (`codmedico`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`agendamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`agendamento` (
  `codigo` INT NOT NULL AUTO_INCREMENT,
  `dataagenda` DATE NOT NULL,
  `datacadastro` DATE NOT NULL,
  `flgsituacao` CHAR(2) NOT NULL COMMENT '01- agendado\\\\\\\\\\\\\\\\n02- cancelado\\\\\\\\\\\\\\\\n03- presenca\\\\\\\\\\\\\\\\n04- falta',
  `fk_paciente_id` INT NULL DEFAULT NULL,
  `escala_id` INT NOT NULL,
  `horaagendamento` TIME NOT NULL,
  `turno` ENUM('manhã', 'tarde', 'noite') NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_agendamento_3` (`fk_paciente_id` ASC) VISIBLE,
  INDEX `fk_agendamento_escala1_idx` (`escala_id` ASC) VISIBLE,
  CONSTRAINT `fk_agendamento_3`
    FOREIGN KEY (`fk_paciente_id`)
    REFERENCES `clinica`.`paciente` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_agendamento_escala1`
    FOREIGN KEY (`escala_id`)
    REFERENCES `clinica`.`escala` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`setor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`setor` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `descricao` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(10) NOT NULL,
  `senha` VARCHAR(8) NOT NULL,
  `tipo` CHAR(2) NOT NULL,
  `flgativo` BIT(1) NOT NULL,
  `fk_pessoa_id` INT NOT NULL,
  `fk_setor_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `fk_pessoa_id_UNIQUE` (`fk_pessoa_id` ASC) VISIBLE,
  INDEX `fk_usuario_2` (`fk_pessoa_id` ASC) VISIBLE,
  INDEX `fk_usuario_3` (`fk_setor_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_2`
    FOREIGN KEY (`fk_pessoa_id`)
    REFERENCES `clinica`.`pessoa` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_usuario_3`
    FOREIGN KEY (`fk_setor_id`)
    REFERENCES `clinica`.`setor` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`permissao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`permissao` (
  `fk_usuario_id` INT NULL DEFAULT NULL,
  `id` INT NOT NULL,
  `descricao` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_permissao_1` (`fk_usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_permissao_1`
    FOREIGN KEY (`fk_usuario_id`)
    REFERENCES `clinica`.`usuario` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `clinica`.`prontuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinica`.`prontuario` (
  `numprontuario` INT NOT NULL AUTO_INCREMENT,
  `fk_paciente_id` INT NOT NULL,
  PRIMARY KEY (`numprontuario`),
  INDEX `fk_prontuario_2` (`fk_paciente_id` ASC) VISIBLE,
  CONSTRAINT `fk_prontuario_2`
    FOREIGN KEY (`fk_paciente_id`)
    REFERENCES `clinica`.`paciente` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


ALTER TABLE especialidade AUTO_INCREMENT = 1;
ALTER TABLE paciente AUTO_INCREMENT = 1;
ALTER TABLE agendamento AUTO_INCREMENT = 1;
ALTER TABLE pessoa AUTO_INCREMENT = 1;
ALTER TABLE medico AUTO_INCREMENT = 1;
ALTER TABLE escala AUTO_INCREMENT = 1;
ALTER TABLE convenio AUTO_INCREMENT = 1;