# RAPPORT DE TRAVAUX PRATIQUES
## ADMINISTRATION SQL SERVER

**École Supérieure de Gestion d'Informatique et des Sciences (ESGIS)**  
**Année Académique : 2025-2026**  
**Professeur : M. N'SOUGAN**  
**Filière : LICENCE 3 IRT**  
**Option : DA**  

---

## SOMMAIRE

1. [Partie I : Gestion de bases de données](#partie-i-gestion-de-bases-de-données)
2. [Partie II : Gestion de la sécurité des accès](#partie-ii-gestion-de-la-sécurité-des-accès)
3. [Conclusion](#conclusion)

---

## PARTIE I : GESTION DE BASES DE DONNÉES

### Question 1 : Création de la base de données bdGesStock

**Objectif :** Créer une base de données avec des paramètres spécifiques pour les fichiers de données et le journal des transactions.

**Solution :**
```sql
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
```

**Observations :** La création du dossier `C:\DONNEES\GesStock` doit être effectuée préalablement via l'invite de commandes Windows.

---

### Question 2 : Ajout des groupes de fichiers

**Objectif :** Ajouter quatre groupes de fichiers pour organiser physiquement les données.

**Solution :**
```sql
ALTER DATABASE bdGesStock ADD FILEGROUP gfProda;
ALTER DATABASE bdGesStock ADD FILEGROUP gfProdb;
ALTER DATABASE bdGesStock ADD FILEGROUP gfProdc;
ALTER DATABASE bdGesStock ADD FILEGROUP gfCateg;
```

**Justification :** Les groupes de fichiers permettent une meilleure gestion physique des données et facilitent le partitionnement.

---

### Question 3 : Ajout des fichiers aux groupes de fichiers

**Objectif :** Associer des fichiers physiques à chaque groupe de fichiers.

**Solution :**
```sql
ALTER DATABASE bdGesStock ADD FILE (NAME = Proda1, FILENAME = 'C:\DONNEES\GesStock\Proda1.ndf') TO FILEGROUP gfProda;
ALTER DATABASE bdGesStock ADD FILE (NAME = Prodb1, FILENAME = 'C:\DONNEES\GesStock\Prodb1.ndf') TO FILEGROUP gfProdb;
ALTER DATABASE bdGesStock ADD FILE (NAME = Prodc1, FILENAME = 'C:\DONNEES\GesStock\Prodc1.ndf') TO FILEGROUP gfProdc;
ALTER DATABASE bdGesStock ADD FILE (NAME = Categ1, FILENAME = 'C:\DONNEES\GesStock\Categ1.ndf') TO FILEGROUP gfCateg;
ALTER DATABASE bdGesStock ADD FILE (NAME = Categ2, FILENAME = 'C:\DONNEES\GesStock\Categ2.ndf') TO FILEGROUP gfCateg;
```

---

### Question 4 : Affichage de l'aperçu de la base de données

**Commande :**
```sql
EXEC sp_helpdb bdGesStock;
```

**Résultat attendu :** Affichage de toutes les informations sur la base de données incluant les fichiers principaux et secondaires.

---

### Question 5 : Création de la table CATEGORIE

**Solution :**
```sql
CREATE TABLE CATEGORIE 
(
    CodeCateg CHAR(2) NOT NULL PRIMARY KEY,
    NomCateg VARCHAR(50)
) ON gfCateg;
```

**Remarque :** La clause `ON gfCateg` spécifie que les données de cette table seront stockées dans le groupe de fichiers gfCateg.

---

### Question 6 : Affichage de la structure de la table CATEGORIE

**Commande :**
```sql
EXEC sp_help 'CATEGORIE';
```

**Résultat :** Affiche toutes les informations sur la table (colonnes, types, contraintes, index, etc.)

---

### Question 7 : Insertion des catégories

**Solution :**
```sql
INSERT INTO CATEGORIE (CodeCateg, NomCateg) VALUES ('AG', 'Alimentation Générale');
INSERT INTO CATEGORIE (CodeCateg, NomCateg) VALUES ('EM', 'Electro Ménager');
```

---

### Question 8 : Création de la table PRODUIT partitionnée

**Objectif :** Partitionner la table selon le code catégorie (AA à EL dans une partition, autres codes dans une autre).

**Solution :**

1. **Création de la fonction de partition :**
```sql
CREATE PARTITION FUNCTION pf_CodeCateg (CHAR(2))
AS RANGE LEFT FOR VALUES ('EL');
```

2. **Création du schéma de partition :**
```sql
CREATE PARTITION SCHEME ps_CodeCateg
AS PARTITION pf_CodeCateg
TO (gfProda, gfProdb, gfProdc);
```

3. **Création de la table partitionnée :**
```sql
CREATE TABLE PRODUIT 
(
    Id INT IDENTITY(1,1) NOT NULL,
    Libelle VARCHAR(100),
    PU DECIMAL(18,2),
    codeCateg CHAR(2)
) ON ps_CodeCateg(codeCateg);
```

**Explication :** Le partitionnement permet de répartir physiquement les données selon des critères définis, améliorant ainsi les performances des requêtes.

---

### Question 9 : Insertion des produits

**Solution :**
```sql
-- Produits pour AG
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES 
('Riz 5kg', 3500, 'AG'),
('Huile végétale 1L', 1200, 'AG'),
('Sucre 1kg', 800, 'AG'),
('Pâtes alimentaires 500g', 600, 'AG'),
('Conserve de tomate', 450, 'AG');

-- Produits pour EM
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES 
('Réfrigérateur', 150000, 'EM'),
('Machine à laver', 120000, 'EM'),
('Micro-ondes', 45000, 'EM'),
('Fer à repasser', 15000, 'EM'),
('Mixeur électrique', 25000, 'EM');
```

---

### Question 10 : Affichage de l'espace disque par fichier

**Solution :**
```sql
SELECT 
    df.name AS NomFichier,
    df.physical_name AS CheminPhysique,
    df.size AS PagesTotales,
    fu.unallocated_extent_page_count AS PagesRestantes,
    (df.size - fu.unallocated_extent_page_count) AS PagesAllouees
FROM sys.database_files df
CROSS JOIN sys.dm_db_file_space_usage fu
WHERE df.type = 0;
```

**Explication :** Cette requête utilise les vues dynamiques de gestion (DMV) pour afficher l'utilisation de l'espace disque.

---

## PARTIE II : GESTION DE LA SÉCURITÉ DES ACCÈS

### Questions 1 & 2 : Création des connexions (Logins)

**Solution :**
```sql
-- Login Root (pas de changement de mot de passe)
CREATE LOGIN Root 
WITH PASSWORD = 'root',
DEFAULT_DATABASE = bdGesStock,
CHECK_POLICY = OFF;

-- Login Jacques (changement obligatoire à la première connexion)
CREATE LOGIN Jacques 
WITH PASSWORD = 'root',
DEFAULT_DATABASE = bdGesStock,
MUST_CHANGE_PASSWORD = ON;
```

**Différence :** `CHECK_POLICY = OFF` désactive la politique de mot de passe, tandis que `MUST_CHANGE_PASSWORD = ON` force le changement du mot de passe lors de la première connexion.

---

### Question 3 : Test de connexion avec Jacques

**Observation :** Lors de la première connexion, SQL Server impose à Jacques de changer son mot de passe. De plus, même après ce changement, Jacques ne peut pas accéder à la base de données car aucun utilisateur de base de données n'a été créé pour lui.

**Explication :** Un login (connexion au serveur) est différent d'un user (utilisateur de la base de données).

---

### Question 4 : Activation du compte guest

**Solution :**
```sql
GRANT CONNECT TO GUEST;
```

**Observations :**
- Avec la connexion Root : Root peut se connecter au serveur mais l'accès à la base dépend des permissions.
- Le compte guest permet à tout login de se connecter à la base avec des permissions très limitées.

---

### Questions 5 & 6 : Tests d'accès avec Jacques

**Observations :**
- **Question 5 :** Jacques ne peut pas utiliser la base de données sans utilisateur mappé.
- **Question 6 :** La requête SELECT échoue car Jacques n'a aucune permission sur la table PRODUIT.

---

### Question 7 : Création des utilisateurs de base de données

**Solution :**
```sql
CREATE USER Root FOR LOGIN Root;
CREATE USER Jacques FOR LOGIN Jacques;
```

**Importance :** Cette étape est cruciale car elle mappe les logins (niveau serveur) aux utilisateurs (niveau base de données).

---

### Questions 8 & 9 : Nouveaux tests d'accès

**Observations :**
- **Question 8 :** Jacques peut maintenant se connecter à la base de données.
- **Question 9 :** La requête SELECT échoue toujours car Jacques n'a pas la permission SELECT.

---

### Questions 10 & 11 : Octroi de la permission SELECT

**Solution :**
```sql
GRANT SELECT ON PRODUIT TO Jacques;
```

**Observation (Q11) :** La requête SELECT fonctionne maintenant. Jacques peut lire les données de PRODUIT.

---

### Question 12 : Octroi des permissions complètes avec GRANT OPTION

**Solution :**
```sql
GRANT DELETE, UPDATE, INSERT ON PRODUIT TO Jacques WITH GRANT OPTION;
```

**Explication :** `WITH GRANT OPTION` permet à Jacques de donner ces mêmes permissions à d'autres utilisateurs.

---

### Question 13 : Insertion par Jacques

**Test :**
```sql
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Produit test Jacques', 1000, 'AG');
```

**Résultat :** Succès ! Jacques peut insérer des données.

---

### Question 14 : Jacques donne INSERT à Root

**Test :**
```sql
GRANT INSERT ON PRODUIT TO Root;
```

**Observation :** Cela fonctionne car Jacques a reçu INSERT avec `WITH GRANT OPTION`. Cependant, en pratique, un utilisateur ne devrait généralement pas pouvoir accorder des permissions à un utilisateur ayant potentiellement plus de privilèges.

---

### Question 15 : SELECT sur tout le schéma dbo

**Solution :**
```sql
GRANT SELECT ON SCHEMA::dbo TO Jacques;
```

**Avantage :** Cette commande accorde SELECT sur toutes les tables actuelles et futures du schéma dbo, évitant d'avoir à_granter_ chaque table individuellement.

---

### Question 16 : DENY sur CATEGORIE

**Solution :**
```sql
DENY SELECT ON CATEGORIE TO Jacques;
```

**Effet :** DENY a priorité sur GRANT. Même si Jacques a SELECT sur le schéma dbo, le DENY spécifique bloque l'accès à CATEGORIE.

---

### Question 17 : Test de SELECT sur CATEGORIE

**Observation :** La requête échoue avec une erreur de permission.

**Explication :** Dans la hiérarchie des permissions SQL Server, DENY a toujours priorité sur GRANT.

---

### Question 18 : Solution pour régulariser

**Réponse :** Il faut supprimer le DENY en utilisant la commande REVOKE.

---

### Question 19 : Correction du problème

**Solution :**
```sql
REVOKE SELECT ON CATEGORIE TO Jacques;
```

**Résultat :** Après le REVOKE, Jacques hérite à nouveau du SELECT accordé au niveau du schéma dbo et peut accéder à CATEGORIE.

---

### Question 20 : Permissions CREATE pour Root

**Solution :**
```sql
GRANT CREATE TABLE, CREATE VIEW TO Root;
```

**Effet :** Root peut maintenant créer des tables et des vues dans la base bdGesStock.

---

## CONCLUSION

Ce TP a permis de maîtriser plusieurs concepts fondamentaux de l'administration SQL Server :

1. **Gestion physique des bases de données :** Création de bases de données avec paramètres personnalisés, gestion des groupes de fichiers et partitionnement des tables.

2. **Sécurité des accès :** Compréhension de la différence entre Logins (niveau serveur) et Users (niveau base de données), gestion fine des permissions (GRANT, DENY, REVOKE), et utilisation de `WITH GRANT OPTION`.

3. **Hiérarchie des permissions :** Compréhension que DENY a priorité sur GRANT, et que les permissions peuvent être accordées au niveau des objets, des schémas ou de la base entière.

Le partitionnement des tables et la gestion appropriée des groupes de fichiers sont des techniques essentielles pour optimiser les performances des bases de données de grande taille. La maîtrise de la sécurité est quant à elle cruciale pour protéger les données sensibles dans un environnement de production.

---

## FICHIERS LIVRABLES

- **script_sql_complet.sql** : Contient toutes les requêtes T-SQL exécutées
- **rapport_TP.pdf** : Ce document rapport

---

**Date de remise :** 18/04/2025  
**Email de submission :** folly.nsougan@gmail.com
