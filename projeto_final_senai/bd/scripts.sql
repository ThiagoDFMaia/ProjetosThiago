-- mysql workbench forward engineering

set @old_unique_checks=@@unique_checks, unique_checks=0;
set @old_foreign_key_checks=@@foreign_key_checks, foreign_key_checks=0;
set @old_sql_mode=@@sql_mode, sql_mode='only_full_group_by,strict_trans_tables,no_zero_in_date,no_zero_date,error_for_division_by_zero,no_engine_substitution';

-- -----------------------------------------------------
-- schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- schema clinica
-- -----------------------------------------------------

-- -----------------------------------------------------
-- schema clinica
-- -----------------------------------------------------
create schema if not exists `clinica` default character set utf8mb4 collate utf8mb4_0900_ai_ci ;
use `clinica` ;

-- -----------------------------------------------------
-- table `clinica`.`especialidade`
-- -----------------------------------------------------
create table if not exists `clinica`.`especialidade` (
  `codespecialidade` int not null auto_increment,
  `descricao` varchar(50) not null,
  primary key (`codespecialidade`))
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`pessoa`
-- -----------------------------------------------------
create table if not exists `clinica`.`pessoa` (
  `id` int not null auto_increment,
  `nome` varchar(100) not null,
  `endereco` varchar(100) not null,
  `cep` varchar(100) not null,
  `uf` char(2) not null,
  `cidade` varchar(30) not null,
  `complemento` varchar(50) null default null,
  `numero` varchar(15) null default null,
  `telefone_01` varchar(12) not null,
  `telefone_02` varchar(12) null default null,
  `telefone_03` varchar(12) null default null,
  `rg` varchar(12) not null,
  `cpf` varchar(11) not null,
  primary key (`id`))
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`medico`
-- -----------------------------------------------------
create table if not exists `clinica`.`medico` (
  `codmedico` int not null auto_increment,
  `crm` varchar(15) not null,
  `fk_pessoa_id` int not null,
  `flgativo` bit(1) not null,
  primary key (`codmedico`),
  index `fk_medico_2` (`fk_pessoa_id` asc) visible,
  constraint `fk_medico_2`
    foreign key (`fk_pessoa_id`)
    references `clinica`.`pessoa` (`id`)
    on delete cascade)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`clinica`
-- -----------------------------------------------------
create table if not exists `clinica`.`clinica` (
  `codclinica` int not null auto_increment,
  `fk_especialidade_codespecialidade` int not null,
  `fk_medico_codmedico` int not null,
  `flgativo` bit(1) not null,
  primary key (`codclinica`),
  index `fk_clinica_2` (`fk_especialidade_codespecialidade` asc) visible,
  index `fk_clinica_3` (`fk_medico_codmedico` asc) visible,
  constraint `fk_clinica_2`
    foreign key (`fk_especialidade_codespecialidade`)
    references `clinica`.`especialidade` (`codespecialidade`)
    on delete cascade,
  constraint `fk_clinica_3`
    foreign key (`fk_medico_codmedico`)
    references `clinica`.`medico` (`codmedico`)
    on delete cascade)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`escala`
-- -----------------------------------------------------
create table if not exists `clinica`.`escala` (
  `id` int not null auto_increment,
  `data` date not null,
  `quantvagasmanha` smallint not null,
  `quantvagastarde` smallint not null,
  `quantvagasnoite` smallint not null,
  `fk_clinica_codclinica` int not null,
  `flaativo` bit(1) not null,
  primary key (`id`),
  index `fk_escala_2` (`fk_clinica_codclinica` asc) visible,
  constraint `fk_escala_2`
    foreign key (`fk_clinica_codclinica`)
    references `clinica`.`clinica` (`codclinica`)
    on delete cascade)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`convenio`
-- -----------------------------------------------------
create table if not exists `clinica`.`convenio` (
  `id` int not null auto_increment,
  `cnpj` varchar(15) not null,
  `descricao` varchar(50) not null,
  primary key (`id`),
  unique index `cnpj` (`cnpj` asc) visible)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`paciente`
-- -----------------------------------------------------
create table if not exists `clinica`.`paciente` (
  `id` int not null auto_increment,
  `tipoconvenio` char(2) not null,
  `fk_pessoa_id` int not null,
  `fk_convenio_id` int null,
  primary key (`id`),
  index `fk_paciente_2` (`fk_pessoa_id` asc) visible,
  index `fk_paciente_3` (`fk_convenio_id` asc) visible,
  constraint `fk_paciente_2`
    foreign key (`fk_pessoa_id`)
    references `clinica`.`pessoa` (`id`)
    on delete cascade,
  constraint `fk_paciente_3`
    foreign key (`fk_convenio_id`)
    references `clinica`.`convenio` (`id`))
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`agendamento`
-- -----------------------------------------------------
create table if not exists `clinica`.`agendamento` (
  `codigo` int not null auto_increment,
  `dataagenda` date not null,
  `datacadastro` date not null,
  `flgsituacao` char(2) not null comment '01- agendado\n02- cancelado\n03- presenca\n04- falta',
  `fk_escala_id` int not null,
  `fk_paciente_id` int null default null,
  primary key (`codigo`),
  index `fk_agendamento_2` (`fk_escala_id` asc) visible,
  index `fk_agendamento_3` (`fk_paciente_id` asc) visible,
  constraint `fk_agendamento_2`
    foreign key (`fk_escala_id`)
    references `clinica`.`escala` (`id`)
    on delete cascade,
  constraint `fk_agendamento_3`
    foreign key (`fk_paciente_id`)
    references `clinica`.`paciente` (`id`)
    on delete cascade)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`setor`
-- -----------------------------------------------------
create table if not exists `clinica`.`setor` (
  `id` int not null auto_increment,
  `descricao` varchar(100) not null,
  primary key (`id`))
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`usuario`
-- -----------------------------------------------------
create table if not exists `clinica`.`usuario` (
  `id` int not null auto_increment,
  `login` varchar(10) not null,
  `senha` varchar(8) not null,
  `tipo` char(2) not null,
  `flgativo` bit(1) not null,
  `fk_pessoa_id` int not null,
  `fk_setor_id` int not null,
  primary key (`id`),
  index `fk_usuario_2` (`fk_pessoa_id` asc) visible,
  index `fk_usuario_3` (`fk_setor_id` asc) visible,
  constraint `fk_usuario_2`
    foreign key (`fk_pessoa_id`)
    references `clinica`.`pessoa` (`id`)
    on delete cascade,
  constraint `fk_usuario_3`
    foreign key (`fk_setor_id`)
    references `clinica`.`setor` (`id`)
    on delete cascade)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`permissao`
-- -----------------------------------------------------
create table if not exists `clinica`.`permissao` (
  `fk_usuario_id` int null default null,
  `id` int not null,
  `descricao` varchar(100) null default null,
  primary key (`id`),
  index `fk_permissao_1` (`fk_usuario_id` asc) visible,
  constraint `fk_permissao_1`
    foreign key (`fk_usuario_id`)
    references `clinica`.`usuario` (`id`)
    on delete cascade)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- table `clinica`.`prontuario`
-- -----------------------------------------------------
create table if not exists `clinica`.`prontuario` (
  `numprontuario` int not null auto_increment,
  `fk_paciente_id` int not null,
  primary key (`numprontuario`),
  index `fk_prontuario_2` (`fk_paciente_id` asc) visible,
  constraint `fk_prontuario_2`
    foreign key (`fk_paciente_id`)
    references `clinica`.`paciente` (`id`)
    on delete cascade)
engine = innodb
default character set = utf8mb4
collate = utf8mb4_0900_ai_ci;


set sql_mode=@old_sql_mode;
set foreign_key_checks=@old_foreign_key_checks;
set unique_checks=@old_unique_checks;
