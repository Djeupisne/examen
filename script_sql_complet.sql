-- ============================================================================
-- TRAVAUX PRATIQUES ADMINISTRATION SQL SERVER
-- Filière : LICENCE 3 IRT - Option DA
-- Professeur : M. N'SOUGAN
-- Année : 2025-2026
-- ============================================================================

-- ============================================================================
-- PARTIE I : GESTION DE BASES DE DONNÉES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Question 1 : Créer la base de données bdGesStock
-- ----------------------------------------------------------------------------
-- Création du dossier C:\DONNEES\GesStock (à exécuter dans l'invite de commandes Windows)
-- Commande : mkdir C:\DONNEES\GesStock

USE master;
GO

-- Vérifier si la base existe déjà et la supprimer si nécessaire
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'bdGesStock')
BEGIN
    ALTER DATABASE bdGesStock SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE bdGesStock;
END
GO

-- Création de la base de données avec les paramètres spécifiés
CREATE DATABASE bdGesStock
ON PRIMARY 
(
    NAME = bdGesStock,
    FILENAME = 'C:\DONNEES\GesStock\bdGesStock.mdf',
    SIZE = 250MB,
    MAXSIZE = 1GB,
    FILEGROWTH = 50MB
)
LOG ON 
(
    NAME = bdGesStock_log,
    FILENAME = 'C:\DONNEES\GesStock\bdGesStock_log.ldf',
    SIZE = 80MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 5%
);
GO

-- ----------------------------------------------------------------------------
-- Question 2 : Ajouter les groupes de fichiers gfProda, gfProdb, gfProdc, gfCateg
-- ----------------------------------------------------------------------------
ALTER DATABASE bdGesStock ADD FILEGROUP gfProda;
ALTER DATABASE bdGesStock ADD FILEGROUP gfProdb;
ALTER DATABASE bdGesStock ADD FILEGROUP gfProdc;
ALTER DATABASE bdGesStock ADD FILEGROUP gfCateg;
GO

-- ----------------------------------------------------------------------------
-- Question 3 : Ajouter les fichiers aux groupes de fichiers
-- ----------------------------------------------------------------------------
ALTER DATABASE bdGesStock 
ADD FILE 
(
    NAME = Proda1,
    FILENAME = 'C:\DONNEES\GesStock\Proda1.ndf'
) TO FILEGROUP gfProda;

ALTER DATABASE bdGesStock 
ADD FILE 
(
    NAME = Prodb1,
    FILENAME = 'C:\DONNEES\GesStock\Prodb1.ndf'
) TO FILEGROUP gfProdb;

ALTER DATABASE bdGesStock 
ADD FILE 
(
    NAME = Prodc1,
    FILENAME = 'C:\DONNEES\GesStock\Prodc1.ndf'
) TO FILEGROUP gfProdc;

ALTER DATABASE bdGesStock 
ADD FILE 
(
    NAME = Categ1,
    FILENAME = 'C:\DONNEES\GesStock\Categ1.ndf'
) TO FILEGROUP gfCateg;

ALTER DATABASE bdGesStock 
ADD FILE 
(
    NAME = Categ2,
    FILENAME = 'C:\DONNEES\GesStock\Categ2.ndf'
) TO FILEGROUP gfCateg;
GO

-- ----------------------------------------------------------------------------
-- Question 4 : Afficher l'aperçu de la base de données avec sp_helpdb
-- ----------------------------------------------------------------------------
EXEC sp_helpdb bdGesStock;
GO

-- ----------------------------------------------------------------------------
-- Question 5 : Créer la table CATEGORIE dans le groupe de fichiers gfCateg
-- ----------------------------------------------------------------------------
USE bdGesStock;
GO

CREATE TABLE CATEGORIE 
(
    CodeCateg CHAR(2) NOT NULL PRIMARY KEY,
    NomCateg VARCHAR(50)
) ON gfCateg;
GO

-- ----------------------------------------------------------------------------
-- Question 6 : Afficher l'aperçu de la structure de la table CATEGORIE
-- ----------------------------------------------------------------------------
EXEC sp_help 'CATEGORIE';
GO

-- ----------------------------------------------------------------------------
-- Question 7 : Insérer deux catégories
-- ----------------------------------------------------------------------------
INSERT INTO CATEGORIE (CodeCateg, NomCateg) VALUES ('AG', 'Alimentation Générale');
INSERT INTO CATEGORIE (CodeCateg, NomCateg) VALUES ('EM', 'Electro Ménager');
GO

-- ----------------------------------------------------------------------------
-- Question 8 : Créer la table PRODUIT partitionnée selon codeCateg
-- ----------------------------------------------------------------------------
-- Étape 1 : Créer la fonction de partition
CREATE PARTITION FUNCTION pf_CodeCateg (CHAR(2))
AS RANGE LEFT FOR VALUES ('EL');
GO

-- Étape 2 : Créer le schéma de partition
CREATE PARTITION SCHEME ps_CodeCateg
AS PARTITION pf_CodeCateg
TO (gfProda, gfProdb, gfProdc);
GO

-- Étape 3 : Créer la table PRODUIT partitionnée
CREATE TABLE PRODUIT 
(
    Id INT IDENTITY(1,1) NOT NULL,
    Libelle VARCHAR(100),
    PU DECIMAL(18,2),
    codeCateg CHAR(2)
) ON ps_CodeCateg(codeCateg);
GO

-- ----------------------------------------------------------------------------
-- Question 9 : Insérer des produits pour chaque catégorie (au moins 5 chacun)
-- ----------------------------------------------------------------------------
-- Produits pour la catégorie AG (Alimentation Générale)
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Riz 5kg', 3500, 'AG');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Huile végétale 1L', 1200, 'AG');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Sucre 1kg', 800, 'AG');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Pâtes alimentaires 500g', 600, 'AG');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Conserve de tomate', 450, 'AG');

-- Produits pour la catégorie EM (Electro Ménager)
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Réfrigérateur', 150000, 'EM');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Machine à laver', 120000, 'EM');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Micro-ondes', 45000, 'EM');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Fer à repasser', 15000, 'EM');
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Mixeur électrique', 25000, 'EM');
GO

-- ----------------------------------------------------------------------------
-- Question 10 : Afficher pour chaque fichier de données le nombre de pages allouées et restantes
-- ----------------------------------------------------------------------------
SELECT 
    df.name AS NomFichier,
    df.physical_name AS CheminPhysique,
    df.size AS PagesTotales,
    fu.unallocated_extent_page_count AS PagesRestantes,
    (df.size - fu.unallocated_extent_page_count) AS PagesAllouees
FROM sys.database_files df
CROSS JOIN sys.dm_db_file_space_usage fu
WHERE df.type = 0; -- Type 0 = fichiers de données (ROWS)
GO

-- ============================================================================
-- PARTIE II : GESTION DE LA SÉCURITÉ DES ACCÈS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Question 1 : Créer la connexion Root avec mot de passe root
-- ----------------------------------------------------------------------------
USE master;
GO

-- Vérifier si le login existe déjà et le supprimer
IF EXISTS (SELECT name FROM sys.server_principals WHERE name = 'Root')
BEGIN
    DROP LOGIN Root;
END
GO

CREATE LOGIN Root 
WITH PASSWORD = 'root',
DEFAULT_DATABASE = bdGesStock,
CHECK_POLICY = OFF; -- L'utilisateur ne changera pas son mot de passe
GO

-- ----------------------------------------------------------------------------
-- Question 2 : Créer la connexion Jacques avec mot de passe root (changement obligatoire)
-- ----------------------------------------------------------------------------
IF EXISTS (SELECT name FROM sys.server_principals WHERE name = 'Jacques')
BEGIN
    DROP LOGIN Jacques;
END
GO

CREATE LOGIN Jacques 
WITH PASSWORD = 'root',
DEFAULT_DATABASE = bdGesStock,
MUST_CHANGE_PASSWORD = ON; -- Changement obligatoire à la première connexion
GO

-- ----------------------------------------------------------------------------
-- Question 3 : Test de connexion avec Jacques
-- ----------------------------------------------------------------------------
-- Observation : Lors de la première connexion, Jacques doit changer son mot de passe.
-- Sans avoir changé son mot de passe, il ne pourra pas accéder aux ressources.
-- De plus, même après changement de mot de passe, Jacques n'aura pas accès à la base
-- car aucun utilisateur de base de données n'a encore été créé pour lui.
GO

-- ----------------------------------------------------------------------------
-- Question 4 : Activer le compte guest sur bdGesStock
-- ----------------------------------------------------------------------------
USE bdGesStock;
GO

-- Activer le compte guest
GRANT CONNECT TO GUEST;
GO

-- Observation : 
-- - Avec la connexion Root : Root peut se connecter mais ne peut pas accéder à la base
--   car il n'a pas d'utilisateur mappé dans la base (sauf si dbo est utilisé).
-- - Le compte guest permet à tout login de se connecter à la base, mais avec des
--   permissions très limitées.
GO

-- ----------------------------------------------------------------------------
-- Question 5 : Se reconnecter avec Jacques et tester l'accès à bdGesStock
-- ----------------------------------------------------------------------------
-- Observation : Après avoir changé son mot de passe, Jacques peut se connecter au serveur
-- mais ne peut PAS utiliser la base de données bdGesStock car il n'a pas d'utilisateur
-- mappé dans cette base de données.
GO

-- ----------------------------------------------------------------------------
-- Question 6 : Faire une requête SELECT sur PRODUIT avec Jacques
-- ----------------------------------------------------------------------------
-- Observation : La requête échoue avec un message d'erreur indiquant que Jacques
-- n'a pas accès à la base de données ou à la table PRODUIT.
-- Erreur typique : "The user does not have permission to perform this action."
GO

-- ----------------------------------------------------------------------------
-- Question 7 : Créer des utilisateurs de base de données pour chaque login
-- ----------------------------------------------------------------------------
USE bdGesStock;
GO

-- Créer l'utilisateur pour le login Root
IF EXISTS (SELECT name FROM sys.database_principals WHERE name = 'Root')
BEGIN
    DROP USER Root;
END
CREATE USER Root FOR LOGIN Root;
GO

-- Créer l'utilisateur pour le login Jacques
IF EXISTS (SELECT name FROM sys.database_principals WHERE name = 'Jacques')
BEGIN
    DROP USER Jacques;
END
CREATE USER Jacques FOR LOGIN Jacques;
GO

-- ----------------------------------------------------------------------------
-- Question 8 : Se reconnecter avec Jacques et tester l'accès
-- ----------------------------------------------------------------------------
-- Observation : Maintenant que Jacques a un utilisateur mappé dans la base,
-- il peut se connecter à la base de données bdGesStock. Cependant, il ne peut
-- toujours pas accéder aux tables car il n'a aucune permission.
GO

-- ----------------------------------------------------------------------------
-- Question 9 : Faire une requête SELECT sur PRODUIT avec Jacques
-- ----------------------------------------------------------------------------
-- Observation : La requête échoue toujours car Jacques n'a pas la permission SELECT
-- sur la table PRODUIT.
-- Erreur : "SELECT permission denied on object 'PRODUIT'"
GO

-- ----------------------------------------------------------------------------
-- Question 10 : Donner l'autorisation SELECT sur PRODUIT à Jacques
-- ----------------------------------------------------------------------------
GRANT SELECT ON PRODUIT TO Jacques;
GO

-- ----------------------------------------------------------------------------
-- Question 11 : Faire une requête SELECT sur PRODUIT avec Jacques
-- ----------------------------------------------------------------------------
-- Observation : Cette fois, la requête réussit ! Jacques peut maintenant lire
-- les données de la table PRODUIT.
GO

-- ----------------------------------------------------------------------------
-- Question 12 : Accorder DELETE, UPDATE, INSERT à Jacques avec GRANT OPTION
-- ----------------------------------------------------------------------------
GRANT DELETE, UPDATE, INSERT ON PRODUIT TO Jacques WITH GRANT OPTION;
GO
-- WITH GRANT OPTION permet à Jacques de donner ces droits à d'autres utilisateurs

-- ----------------------------------------------------------------------------
-- Question 13 : Insérer un nouveau produit depuis la session de Jacques
-- ----------------------------------------------------------------------------
-- Dans la session de Jacques :
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Produit test Jacques', 1000, 'AG');
GO
-- Observation : L'insertion réussit car Jacques a la permission INSERT

-- ----------------------------------------------------------------------------
-- Question 14 : Jacques essaie de donner INSERT à Root
-- ----------------------------------------------------------------------------
-- Dans la session de Jacques :
GRANT INSERT ON PRODUIT TO Root;
GO
-- Observation : Cela devrait réussir car Jacques a reçu INSERT WITH GRANT OPTION
-- Cependant, si cela échoue, c'est parce que Jacques ne peut pas donner de 
-- permissions à un utilisateur qui a potentiellement plus de privilèges que lui.

-- ----------------------------------------------------------------------------
-- Question 15 : Donner SELECT à Jacques sur toutes les tables du schéma dbo
-- ----------------------------------------------------------------------------
GRANT SELECT ON SCHEMA::dbo TO Jacques;
GO

-- ----------------------------------------------------------------------------
-- Question 16 : Enlever à Jacques le droit SELECT sur CATEGORIE
-- ----------------------------------------------------------------------------
DENY SELECT ON CATEGORIE TO Jacques;
GO

-- ----------------------------------------------------------------------------
-- Question 17 : Essayer de faire SELECT sur CATEGORIE avec Jacques
-- ----------------------------------------------------------------------------
-- Observation : La requête échoue avec une erreur de permission.
-- DENY a priorité sur GRANT, donc même si Jacques a SELECT sur le schéma dbo,
-- le DENY spécifique sur CATEGORIE bloque l'accès.
GO

-- ----------------------------------------------------------------------------
-- Question 18 : Que faut-il faire pour régulariser cela ?
-- ----------------------------------------------------------------------------
-- Réponse : Il faut retirer le DENY sur CATEGORIE pour que Jacques puisse
-- accéder à cette table. Le DENY annule le GRANT au niveau du schéma.
-- Solution : Utiliser REVOKE pour supprimer le DENY.
GO

-- ----------------------------------------------------------------------------
-- Question 19 : Écrire l'instruction T-SQL pour résoudre le problème
-- ----------------------------------------------------------------------------
-- Il faut utiliser REVOKE pour supprimer le DENY
REVOKE SELECT ON CATEGORIE TO Jacques;
GO

-- Maintenant, Jacques hérite du SELECT du schéma dbo et peut accéder à CATEGORIE
-- Test : SELECT * FROM CATEGORIE; -- Cela devrait fonctionner maintenant
GO

-- ----------------------------------------------------------------------------
-- Question 20 : Accorder CREATE TABLE et CREATE VIEW à Root
-- ----------------------------------------------------------------------------
USE bdGesStock;
GO

GRANT CREATE TABLE, CREATE VIEW TO Root;
GO
-- Root peut maintenant créer des tables et des vues dans la base bdGesStock

-- ============================================================================
-- FIN DU SCRIPT
-- ============================================================================
