--
-- Create model Disciplina
--
CREATE TABLE `core_disciplina` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`nome` varchar(200) NOT NULL,
	`codigo` varchar(20) NOT NULL UNIQUE
);

--
-- Create model Aluno
--
CREATE TABLE `core_aluno` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`matricula` varchar(20) NOT NULL UNIQUE,
	`user_id` integer NOT NULL UNIQUE
);

--
-- Create model Professor
--
CREATE TABLE `core_professor` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`matricula` varchar(20) NOT NULL UNIQUE,
	`user_id` integer NOT NULL UNIQUE
);

--
-- Create model Turma
--
CREATE TABLE `core_turma` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`codigo` varchar(20) NOT NULL UNIQUE,
	`ano` integer NOT NULL,
	`semestre` integer NOT NULL,
	`disciplina_id` bigint NOT NULL,
	`professor_id` bigint NULL
);

CREATE TABLE `core_turma_alunos` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`turma_id` bigint NOT NULL,
	`aluno_id` bigint NOT NULL
);

--
-- Create model Avaliacao
--
CREATE TABLE `core_avaliacao` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`titulo` varchar(100) NOT NULL,
	`descricao` longtext NULL,
	`peso` numeric(4, 2) NOT NULL,
	`turma_id` bigint NOT NULL
);

--
-- Create model Nota
--
CREATE TABLE `core_nota` (
	`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`valor` numeric(4, 2) NOT NULL,
	`aluno_id` bigint NOT NULL,
	`avaliacao_id` bigint NOT NULL
);
ALTER TABLE `core_aluno` ADD CONSTRAINT `core_aluno_user_id_41778bae_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `core_professor` ADD CONSTRAINT `core_professor_user_id_4dcd1d23_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `core_turma` ADD CONSTRAINT `core_turma_disciplina_id_4b9d4c06_fk_core_disciplina_id` FOREIGN KEY (`disciplina_id`) REFERENCES `core_disciplina` (`id`);
ALTER TABLE `core_turma` ADD CONSTRAINT `core_turma_professor_id_cc72ef42_fk_core_professor_id` FOREIGN KEY (`professor_id`) REFERENCES `core_professor` (`id`);
ALTER TABLE `core_turma_alunos` ADD CONSTRAINT `core_turma_alunos_turma_id_aluno_id_4e5520c6_uniq` UNIQUE (`turma_id`, `aluno_id`);
ALTER TABLE `core_turma_alunos` ADD CONSTRAINT `core_turma_alunos_turma_id_ac49e001_fk_core_turma_id` FOREIGN KEY (`turma_id`) REFERENCES `core_turma` (`id`);
ALTER TABLE `core_turma_alunos` ADD CONSTRAINT `core_turma_alunos_aluno_id_e9c39527_fk_core_aluno_id` FOREIGN KEY (`aluno_id`) REFERENCES `core_aluno` (`id`);
ALTER TABLE `core_avaliacao` ADD CONSTRAINT `core_avaliacao_turma_id_02e5473d_fk_core_turma_id` FOREIGN KEY (`turma_id`) REFERENCES `core_turma` (`id`);
ALTER TABLE `core_nota` ADD CONSTRAINT `core_nota_aluno_id_avaliacao_id_c50deb53_uniq` UNIQUE (`aluno_id`, `avaliacao_id`);
ALTER TABLE `core_nota` ADD CONSTRAINT `core_nota_aluno_id_952ad411_fk_core_aluno_id` FOREIGN KEY (`aluno_id`) REFERENCES `core_aluno` (`id`);
ALTER TABLE `core_nota` ADD CONSTRAINT `core_nota_avaliacao_id_3d0c1dd1_fk_core_avaliacao_id` FOREIGN KEY (`avaliacao_id`) REFERENCES `core_avaliacao` (`id`);