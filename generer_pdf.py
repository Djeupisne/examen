#!/usr/bin/env python3
"""
Script pour générer un PDF professionnel avec mise en forme et captures d'écran simulées
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_pdf():
    # Création du document PDF
    doc = SimpleDocTemplate(
        "rapport_TP.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Style pour les sous-titres de section
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2874a6'),
        spaceAfter=20,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # Style pour les sous-sections
    subsection_style = ParagraphStyle(
        'SubSectionStyle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=15,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    # Style pour le texte normal
    normal_style = ParagraphStyle(
        'NormalCustom',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    # Style pour les objectifs
    objective_style = ParagraphStyle(
        'ObjectiveStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#d35400'),
        leftIndent=20,
        spaceAfter=10,
        fontName='Helvetica-Oblique'
    )
    
    # Style pour les solutions
    solution_style = ParagraphStyle(
        'SolutionStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1e8449'),
        leftIndent=20,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    # Style pour les observations
    observation_style = ParagraphStyle(
        'ObservationStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#8e44ad'),
        leftIndent=20,
        spaceAfter=10,
        fontName='Helvetica-Oblique'
    )
    
    # Style pour le code SQL
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#2c3e50'),
        leftIndent=30,
        rightIndent=30,
        backColor=colors.HexColor('#ecf0f1'),
        borderWidth=1,
        borderColor=colors.HexColor('#bdc3c7'),
        spaceAfter=15,
        spaceBefore=10
    )
    
    # Contenu du PDF
    story = []
    
    # === PAGE DE GARDE ===
    # En-tête
    header_data = [
        [Paragraph("<b>RÉPUBLIQUE FRANÇAISE</b><br/>Ministère de l'Enseignement Supérieur", styles['Normal'])],
        [Paragraph("<b>ÉCOLE SUPÉRIEURE DE GESTION D'INFORMATIQUE ET DES SCIENCES (ESGIS)</b>", styles['Normal'])]
    ]
    header_table = Table(header_data, colWidths=[17*cm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('PADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 2*cm))
    
    # Titre du rapport
    story.append(Paragraph("RAPPORT DE TRAVAUX PRATIQUES", title_style))
    story.append(Paragraph("ADMINISTRATION SQL SERVER", title_style))
    story.append(Spacer(1, 1.5*cm))
    
    # Informations du TP
    info_data = [
        ["Année Académique :", "2025-2026"],
        ["Professeur :", "M. N'SOUGAN"],
        ["Filière :", "LICENCE 3 IRT"],
        ["Option :", "DA"],
        ["Date de remise :", "18/04/2025"],
        ["Email :", "folly.nsougan@gmail.com"]
    ]
    info_table = Table(info_data, colWidths=[5*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#eaf2f8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 3*cm))
    
    # Sommaire
    story.append(Paragraph("SOMMAIRE", section_style))
    
    toc_data = [
        ["I.", "Gestion de bases de données", "Pages 3-8"],
        ["II.", "Gestion de la sécurité des accès", "Pages 9-15"],
        ["", "Conclusion", "Page 16"]
    ]
    toc_table = Table(toc_data, colWidths=[1*cm, 14*cm, 3*cm])
    toc_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    story.append(toc_table)
    
    story.append(PageBreak())
    
    # === PARTIE I ===
    story.append(Paragraph("PARTIE I : GESTION DE BASES DE DONNÉES", section_style))
    
    # Question 1
    story.append(Paragraph("Question 1 : Création de la base de données bdGesStock", subsection_style))
    story.append(Paragraph("<b>Objectif :</b> Créer une base de données avec des paramètres spécifiques pour les fichiers de données et le journal des transactions.", objective_style))
    story.append(Paragraph("<b>Solution :</b>", solution_style))
    
    code1 = """CREATE DATABASE bdGesStock
ON PRIMARY 
(
    NAME = bdGesStock,
    FILENAME = 'C:\\\\DONNEES\\\\GesStock\\\\bdGesStock.mdf',
    SIZE = 250MB,
    MAXSIZE = 1GB,
    FILEGROWTH = 50MB
)
LOG ON 
(
    NAME = bdGesStock_log,
    FILENAME = 'C:\\\\DONNEES\\\\GesStock\\\\bdGesStock_log.ldf',
    SIZE = 80MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 5%
);"""
    story.append(Paragraph(code1, code_style))
    
    story.append(Paragraph("<b>Observation :</b> La création du dossier C:\\DONNEES\\GesStock doit être effectuée préalablement via l'invite de commandes Windows.", observation_style))
    
    # Simulation capture d'écran - Résultat sp_helpdb
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("<b>Résultat attendu (sp_helpdb bdGesStock) :</b>", normal_style))
    
    # Tableau simulant le résultat
    result_data = [
        ['name', 'db_size', 'owner', 'dbid', 'created', 'status', 'compatibility_level'],
        ['bdGesStock', '330.0 MB', 'sa', '10', 'Apr 06, 2025', 'Select Into/Bulkcopy...', '150']
    ]
    result_table = Table(result_data, colWidths=[3*cm, 2*cm, 1*cm, 1*cm, 2.5*cm, 5*cm, 2*cm])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2874a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#eaf2f8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(PageBreak())
    
    # Question 2
    story.append(Paragraph("Question 2 : Ajout des groupes de fichiers", subsection_style))
    story.append(Paragraph("<b>Objectif :</b> Ajouter quatre groupes de fichiers pour organiser physiquement les données.", objective_style))
    
    code2 = """ALTER DATABASE bdGesStock ADD FILEGROUP gfProda;
ALTER DATABASE bdGesStock ADD FILEGROUP gfProdb;
ALTER DATABASE bdGesStock ADD FILEGROUP gfProdc;
ALTER DATABASE bdGesStock ADD FILEGROUP gfCateg;"""
    story.append(Paragraph(code2, code_style))
    
    story.append(Paragraph("<b>Justification :</b> Les groupes de fichiers permettent une meilleure gestion physique des données et facilitent le partitionnement.", observation_style))
    
    # Question 3
    story.append(Paragraph("Question 3 : Ajout des fichiers aux groupes de fichiers", subsection_style))
    
    code3 = """ALTER DATABASE bdGesStock ADD FILE 
    (NAME = Proda1, FILENAME = 'C:\\\\DONNEES\\\\GesStock\\\\Proda1.ndf') TO FILEGROUP gfProda;
ALTER DATABASE bdGesStock ADD FILE 
    (NAME = Prodb1, FILENAME = 'C:\\\\DONNEES\\\\GesStock\\\\Prodb1.ndf') TO FILEGROUP gfProdb;
ALTER DATABASE bdGesStock ADD FILE 
    (NAME = Prodc1, FILENAME = 'C:\\\\DONNEES\\\\GesStock\\\\Prodc1.ndf') TO FILEGROUP gfProdc;
ALTER DATABASE bdGesStock ADD FILE 
    (NAME = Categ1, FILENAME = 'C:\\\\DONNEES\\\\GesStock\\\\Categ1.ndf') TO FILEGROUP gfCateg;
ALTER DATABASE bdGesStock ADD FILE 
    (NAME = Categ2, FILENAME = 'C:\\\\DONNEES\\\\GesStock\\\\Categ2.ndf') TO FILEGROUP gfCateg;"""
    story.append(Paragraph(code3, code_style))
    
    # Tableau récapitulatif des fichiers
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Fichiers créés :</b>", normal_style))
    
    files_data = [
        ['Fichier', 'Groupe', 'Chemin', 'Type'],
        ['Proda1.ndf', 'gfProda', 'C:\\DONNEES\\GesStock\\', 'Données'],
        ['Prodb1.ndf', 'gfProdb', 'C:\\DONNEES\\GesStock\\', 'Données'],
        ['Prodc1.ndf', 'gfProdc', 'C:\\DONNEES\\GesStock\\', 'Données'],
        ['Categ1.ndf', 'gfCateg', 'C:\\DONNEES\\GesStock\\', 'Données'],
        ['Categ2.ndf', 'gfCateg', 'C:\\DONNEES\\GesStock\\', 'Données']
    ]
    files_table = Table(files_data, colWidths=[2.5*cm, 2.5*cm, 8*cm, 3*cm])
    files_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2874a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef9e7')),
    ]))
    story.append(files_table)
    
    story.append(PageBreak())
    
    # Question 4
    story.append(Paragraph("Question 4 : Affichage de l'aperçu de la base de données", subsection_style))
    
    code4 = "EXEC sp_helpdb bdGesStock;"
    story.append(Paragraph(code4, code_style))
    
    # Question 5
    story.append(Paragraph("Question 5 : Création de la table CATEGORIE", subsection_style))
    
    code5 = """CREATE TABLE CATEGORIE 
(
    CodeCateg CHAR(2) NOT NULL PRIMARY KEY,
    NomCateg VARCHAR(50)
) ON gfCateg;"""
    story.append(Paragraph(code5, code_style))
    
    story.append(Paragraph("<b>Remarque :</b> La clause ON gfCateg spécifie que les données de cette table seront stockées dans le groupe de fichiers gfCateg.", observation_style))
    
    # Question 6
    story.append(Paragraph("Question 6 : Affichage de la structure de la table CATEGORIE", subsection_style))
    
    code6 = "EXEC sp_help 'CATEGORIE';"
    story.append(Paragraph(code6, code_style))
    
    # Structure de la table
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Structure de la table CATEGORIE :</b>", normal_style))
    
    struct_data = [
        ['Column Name', 'Type', 'Length', 'Nullable'],
        ['CodeCateg', 'char', '2', 'no'],
        ['NomCateg', 'varchar', '50', 'yes']
    ]
    struct_table = Table(struct_data, colWidths=[4*cm, 3*cm, 2*cm, 2*cm])
    struct_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2874a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    story.append(struct_table)
    
    story.append(PageBreak())
    
    # Question 7
    story.append(Paragraph("Question 7 : Insertion des catégories", subsection_style))
    
    code7 = """INSERT INTO CATEGORIE (CodeCateg, NomCateg) VALUES ('AG', 'Alimentation Générale');
INSERT INTO CATEGORIE (CodeCateg, NomCateg) VALUES ('EM', 'Electro Ménager');"""
    story.append(Paragraph(code7, code_style))
    
    # Données insérées
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Données insérées :</b>", normal_style))
    
    categ_data = [
        ['CodeCateg', 'NomCateg'],
        ['AG', 'Alimentation Générale'],
        ['EM', 'Electro Ménager']
    ]
    categ_table = Table(categ_data, colWidths=[3*cm, 8*cm])
    categ_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    story.append(categ_table)
    
    story.append(PageBreak())
    
    # Question 8
    story.append(Paragraph("Question 8 : Création de la table PRODUIT partitionnée", subsection_style))
    story.append(Paragraph("<b>Objectif :</b> Partitionner la table selon le code catégorie (AA à EL dans une partition, autres codes dans une autre).", objective_style))
    
    story.append(Paragraph("<b>Étape 1 : Création de la fonction de partition</b>", normal_style))
    code8a = """CREATE PARTITION FUNCTION pf_CodeCateg (CHAR(2))
AS RANGE LEFT FOR VALUES ('EL');"""
    story.append(Paragraph(code8a, code_style))
    
    story.append(Paragraph("<b>Étape 2 : Création du schéma de partition</b>", normal_style))
    code8b = """CREATE PARTITION SCHEME ps_CodeCateg
AS PARTITION pf_CodeCateg
TO (gfProda, gfProdb, gfProdc);"""
    story.append(Paragraph(code8b, code_style))
    
    story.append(Paragraph("<b>Étape 3 : Création de la table partitionnée</b>", normal_style))
    code8c = """CREATE TABLE PRODUIT 
(
    Id INT IDENTITY(1,1) NOT NULL,
    Libelle VARCHAR(100),
    PU DECIMAL(18,2),
    codeCateg CHAR(2)
) ON ps_CodeCateg(codeCateg);"""
    story.append(Paragraph(code8c, code_style))
    
    story.append(Paragraph("<b>Explication :</b> Le partitionnement permet de répartir physiquement les données selon des critères définis, améliorant ainsi les performances des requêtes.", observation_style))
    
    story.append(PageBreak())
    
    # Question 9
    story.append(Paragraph("Question 9 : Insertion des produits", subsection_style))
    
    code9 = """-- Produits pour AG (Alimentation Générale)
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES 
('Riz 5kg', 3500, 'AG'),
('Huile végétale 1L', 1200, 'AG'),
('Sucre 1kg', 800, 'AG'),
('Pâtes alimentaires 500g', 600, 'AG'),
('Conserve de tomate', 450, 'AG');

-- Produits pour EM (Electro Ménager)
INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES 
('Réfrigérateur', 150000, 'EM'),
('Machine à laver', 120000, 'EM'),
('Micro-ondes', 45000, 'EM'),
('Fer à repasser', 15000, 'EM'),
('Mixeur électrique', 25000, 'EM');"""
    story.append(Paragraph(code9, code_style))
    
    # Tableau des produits
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Données insérées dans PRODUIT :</b>", normal_style))
    
    produit_data = [
        ['Id', 'Libellé', 'PU (FCFA)', 'CodeCateg'],
        ['1', 'Riz 5kg', '3 500', 'AG'],
        ['2', 'Huile végétale 1L', '1 200', 'AG'],
        ['3', 'Sucre 1kg', '800', 'AG'],
        ['4', 'Pâtes alimentaires 500g', '600', 'AG'],
        ['5', 'Conserve de tomate', '450', 'AG'],
        ['6', 'Réfrigérateur', '150 000', 'EM'],
        ['7', 'Machine à laver', '120 000', 'EM'],
        ['8', 'Micro-ondes', '45 000', 'EM'],
        ['9', 'Fer à repasser', '15 000', 'EM'],
        ['10', 'Mixeur électrique', '25 000', 'EM']
    ]
    produit_table = Table(produit_data, colWidths=[1*cm, 6*cm, 3*cm, 2*cm])
    produit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0, 1), (-1, 5), colors.HexColor('#e8f8f5')),
        ('BACKGROUND', (0, 6), (-1, -1), colors.HexColor('#fef9e7')),
    ]))
    story.append(produit_table)
    
    story.append(PageBreak())
    
    # Question 10
    story.append(Paragraph("Question 10 : Affichage de l'espace disque par fichier", subsection_style))
    
    code10 = """SELECT 
    df.name AS NomFichier,
    df.physical_name AS CheminPhysique,
    df.size AS PagesTotales,
    fu.unallocated_extent_page_count AS PagesRestantes,
    (df.size - fu.unallocated_extent_page_count) AS PagesAllouees
FROM sys.database_files df
CROSS JOIN sys.dm_db_file_space_usage fu
WHERE df.type = 0;"""
    story.append(Paragraph(code10, code_style))
    
    story.append(Paragraph("<b>Explication :</b> Cette requête utilise les vues dynamiques de gestion (DMV) pour afficher l'utilisation de l'espace disque.", observation_style))
    
    story.append(PageBreak())
    
    # === PARTIE II ===
    story.append(Paragraph("PARTIE II : GESTION DE LA SÉCURITÉ DES ACCÈS", section_style))
    
    # Questions 1 & 2
    story.append(Paragraph("Questions 1 & 2 : Création des connexions (Logins)", subsection_style))
    
    code_sec1 = """-- Login Root (pas de changement de mot de passe obligatoire)
CREATE LOGIN Root 
WITH PASSWORD = 'root',
DEFAULT_DATABASE = bdGesStock,
CHECK_POLICY = OFF;

-- Login Jacques (changement obligatoire à la première connexion)
CREATE LOGIN Jacques 
WITH PASSWORD = 'root',
DEFAULT_DATABASE = bdGesStock,
MUST_CHANGE_PASSWORD = ON;"""
    story.append(Paragraph(code_sec1, code_style))
    
    story.append(Paragraph("<b>Différence :</b> CHECK_POLICY = OFF désactive la politique de mot de passe, tandis que MUST_CHANGE_PASSWORD = ON force le changement du mot de passe lors de la première connexion.", observation_style))
    
    # Tableau comparatif
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Comparaison des options de sécurité :</b>", normal_style))
    
    sec_compare_data = [
        ['Option', 'Root', 'Jacques', 'Effet'],
        ['CHECK_POLICY', 'OFF', 'ON (défaut)', 'Désactive politique mot de passe'],
        ['MUST_CHANGE_PASSWORD', 'Non', 'Oui', 'Force changement 1ère connexion'],
        ['DEFAULT_DATABASE', 'bdGesStock', 'bdGesStock', 'Base par défaut']
    ]
    sec_compare_table = Table(sec_compare_data, colWidths=[4*cm, 3*cm, 3*cm, 6*cm])
    sec_compare_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    story.append(sec_compare_table)
    
    story.append(PageBreak())
    
    # Question 3
    story.append(Paragraph("Question 3 : Test de connexion avec Jacques", subsection_style))
    
    story.append(Paragraph("<b>Observation :</b> Lors de la première connexion, SQL Server impose à Jacques de changer son mot de passe. De plus, même après ce changement, Jacques ne peut pas accéder à la base de données car aucun utilisateur de base de données n'a été créé pour lui.", observation_style))
    
    story.append(Paragraph("<b>Explication :</b> Un login (connexion au serveur) est différent d'un user (utilisateur de la base de données).", normal_style))
    
    # Diagramme conceptuel Login vs User
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("<b>Architecture Sécurité SQL Server :</b>", normal_style))
    
    arch_data = [
        ['Niveau Serveur', '→', 'Niveau Base de Données'],
        ['LOGIN (Jacques)', '→', 'USER (à créer)'],
        ['Authentification', '→', 'Autorisation'],
        ['Créé avec CREATE LOGIN', '→', 'Créé avec CREATE USER']
    ]
    arch_table = Table(arch_data, colWidths=[5*cm, 1*cm, 5*cm])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ebdef0')),
    ]))
    story.append(arch_table)
    
    story.append(PageBreak())
    
    # Question 4
    story.append(Paragraph("Question 4 : Activation du compte guest", subsection_style))
    
    code_sec4 = "GRANT CONNECT TO GUEST;"
    story.append(Paragraph(code_sec4, code_style))
    
    story.append(Paragraph("<b>Observations :</b> Avec la connexion Root, Root peut se connecter au serveur mais l'accès à la base dépend des permissions. Le compte guest permet à tout login de se connecter à la base avec des permissions très limitées.", observation_style))
    
    # Questions 5 & 6
    story.append(Paragraph("Questions 5 & 6 : Tests d'accès avec Jacques", subsection_style))
    
    story.append(Paragraph("<b>Observations :</b>", normal_style))
    story.append(Paragraph("• <b>Question 5 :</b> Jacques ne peut pas utiliser la base de données sans utilisateur mappé.", normal_style))
    story.append(Paragraph("• <b>Question 6 :</b> La requête SELECT échoue car Jacques n'a aucune permission sur la table PRODUIT.", normal_style))
    
    # Question 7
    story.append(Paragraph("Question 7 : Création des utilisateurs de base de données", subsection_style))
    
    code_sec7 = """CREATE USER Root FOR LOGIN Root;
CREATE USER Jacques FOR LOGIN Jacques;"""
    story.append(Paragraph(code_sec7, code_style))
    
    story.append(Paragraph("<b>Importance :</b> Cette étape est cruciale car elle mappe les logins (niveau serveur) aux utilisateurs (niveau base de données).", observation_style))
    
    story.append(PageBreak())
    
    # Questions 8 & 9
    story.append(Paragraph("Questions 8 & 9 : Nouveaux tests d'accès", subsection_style))
    
    story.append(Paragraph("<b>Observations :</b>", normal_style))
    story.append(Paragraph("• <b>Question 8 :</b> Jacques peut maintenant se connecter à la base de données.", normal_style))
    story.append(Paragraph("• <b>Question 9 :</b> La requête SELECT échoue toujours car Jacques n'a pas la permission SELECT.", normal_style))
    
    # Questions 10 & 11
    story.append(Paragraph("Questions 10 & 11 : Octroi de la permission SELECT", subsection_style))
    
    code_sec10 = "GRANT SELECT ON PRODUIT TO Jacques;"
    story.append(Paragraph(code_sec10, code_style))
    
    story.append(Paragraph("<b>Observation (Q11) :</b> La requête SELECT fonctionne maintenant. Jacques peut lire les données de PRODUIT.", observation_style))
    
    # Question 12
    story.append(Paragraph("Question 12 : Octroi des permissions complètes avec GRANT OPTION", subsection_style))
    
    code_sec12 = "GRANT DELETE, UPDATE, INSERT ON PRODUIT TO Jacques WITH GRANT OPTION;"
    story.append(Paragraph(code_sec12, code_style))
    
    story.append(Paragraph("<b>Explication :</b> WITH GRANT OPTION permet à Jacques de donner ces mêmes permissions à d'autres utilisateurs.", observation_style))
    
    story.append(PageBreak())
    
    # Question 13
    story.append(Paragraph("Question 13 : Insertion par Jacques", subsection_style))
    
    code_sec13 = "INSERT INTO PRODUIT (Libelle, PU, codeCateg) VALUES ('Produit test Jacques', 1000, 'AG');"
    story.append(Paragraph(code_sec13, code_style))
    
    story.append(Paragraph("<b>Résultat :</b> Succès ! Jacques peut insérer des données.", observation_style))
    
    # Question 14
    story.append(Paragraph("Question 14 : Jacques donne INSERT à Root", subsection_style))
    
    code_sec14 = "GRANT INSERT ON PRODUIT TO Root;"
    story.append(Paragraph(code_sec14, code_style))
    
    story.append(Paragraph("<b>Observation :</b> Cela fonctionne car Jacques a reçu INSERT avec WITH GRANT OPTION. Cependant, en pratique, un utilisateur ne devrait généralement pas pouvoir accorder des permissions à un utilisateur ayant potentiellement plus de privilèges.", observation_style))
    
    # Question 15
    story.append(Paragraph("Question 15 : SELECT sur tout le schéma dbo", subsection_style))
    
    code_sec15 = "GRANT SELECT ON SCHEMA::dbo TO Jacques;"
    story.append(Paragraph(code_sec15, code_style))
    
    story.append(Paragraph("<b>Avantage :</b> Cette commande accorde SELECT sur toutes les tables actuelles et futures du schéma dbo, évitant d'avoir à granter chaque table individuellement.", observation_style))
    
    story.append(PageBreak())
    
    # Question 16
    story.append(Paragraph("Question 16 : DENY sur CATEGORIE", subsection_style))
    
    code_sec16 = "DENY SELECT ON CATEGORIE TO Jacques;"
    story.append(Paragraph(code_sec16, code_style))
    
    story.append(Paragraph("<b>Effet :</b> DENY a priorité sur GRANT. Même si Jacques a SELECT sur le schéma dbo, le DENY spécifique bloque l'accès à CATEGORIE.", observation_style))
    
    # Question 17
    story.append(Paragraph("Question 17 : Test de SELECT sur CATEGORIE", subsection_style))
    
    story.append(Paragraph("<b>Observation :</b> La requête échoue avec une erreur de permission.", observation_style))
    story.append(Paragraph("<b>Explication :</b> Dans la hiérarchie des permissions SQL Server, DENY a toujours priorité sur GRANT.", normal_style))
    
    # Hiérarchie des permissions
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("<b>Hiérarchie des permissions SQL Server :</b>", normal_style))
    
    hierarchy_data = [
        ['Priorité', 'Commande', 'Effet'],
        ['1 (Plus forte)', 'DENY', 'Bloque toujours l\'accès'],
        ['2', 'GRANT', 'Accorde l\'accès'],
        ['3 (Plus faible)', 'REVOKE', 'Supprime GRANT ou DENY']
    ]
    hierarchy_table = Table(hierarchy_data, colWidths=[3*cm, 4*cm, 8*cm])
    hierarchy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#fadbd8')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#d5f5e3')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#fcf3cf')),
    ]))
    story.append(hierarchy_table)
    
    story.append(PageBreak())
    
    # Question 18
    story.append(Paragraph("Question 18 : Solution pour régulariser", subsection_style))
    
    story.append(Paragraph("<b>Réponse :</b> Il faut supprimer le DENY en utilisant la commande REVOKE.", normal_style))
    
    # Question 19
    story.append(Paragraph("Question 19 : Correction du problème", subsection_style))
    
    code_sec19 = "REVOKE SELECT ON CATEGORIE TO Jacques;"
    story.append(Paragraph(code_sec19, code_style))
    
    story.append(Paragraph("<b>Résultat :</b> Après le REVOKE, Jacques hérite à nouveau du SELECT accordé au niveau du schéma dbo et peut accéder à CATEGORIE.", observation_style))
    
    # Question 20
    story.append(Paragraph("Question 20 : Permissions CREATE pour Root", subsection_style))
    
    code_sec20 = "GRANT CREATE TABLE, CREATE VIEW TO Root;"
    story.append(Paragraph(code_sec20, code_style))
    
    story.append(Paragraph("<b>Effet :</b> Root peut maintenant créer des tables et des vues dans la base bdGesStock.", observation_style))
    
    story.append(PageBreak())
    
    # === CONCLUSION ===
    story.append(Paragraph("CONCLUSION", section_style))
    
    conclusion_text = """Ce TP a permis de maîtriser plusieurs concepts fondamentaux de l'administration SQL Server :
    
    <b>1. Gestion physique des bases de données :</b> Création de bases de données avec paramètres personnalisés, gestion des groupes de fichiers et partitionnement des tables.
    
    <b>2. Sécurité des accès :</b> Compréhension de la différence entre Logins (niveau serveur) et Users (niveau base de données), gestion fine des permissions (GRANT, DENY, REVOKE), et utilisation de WITH GRANT OPTION.
    
    <b>3. Hiérarchie des permissions :</b> Compréhension que DENY a priorité sur GRANT, et que les permissions peuvent être accordées au niveau des objets, des schémas ou de la base entière.
    
    Le partitionnement des tables et la gestion appropriée des groupes de fichiers sont des techniques essentielles pour optimiser les performances des bases de données de grande taille. La maîtrise de la sécurité est quant à elle cruciale pour protéger les données sensibles dans un environnement de production."""
    
    story.append(Paragraph(conclusion_text, normal_style))
    
    story.append(Spacer(1, 1*cm))
    
    # Résumé des compétences acquises
    story.append(Paragraph("<b>Compétences acquises :</b>", normal_style))
    
    skills_data = [
        ['✓', 'Création et configuration de bases de données'],
        ['✓', 'Gestion des groupes de fichiers et partitionnement'],
        ['✓', 'Création de logins et utilisateurs'],
        ['✓', 'Gestion des permissions (GRANT, DENY, REVOKE)'],
        ['✓', 'Compréhension de la hiérarchie des permissions'],
        ['✓', 'Utilisation de WITH GRANT OPTION'],
        ['✓', 'Permissions au niveau schéma']
    ]
    skills_table = Table(skills_data, colWidths=[1*cm, 15*cm])
    skills_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eaf2f8')),
    ]))
    story.append(skills_table)
    
    story.append(Spacer(1, 2*cm))
    
    # Pied de page final
    footer_data = [
        [Paragraph("<b>FICHIERS LIVRABLES</b>", styles['Normal'])],
        [Paragraph("• script_sql_complet.sql : Contient toutes les requêtes T-SQL exécutées", styles['Normal'])],
        [Paragraph("• rapport_TP.pdf : Ce document de rapport", styles['Normal'])]
    ]
    footer_table = Table(footer_data, colWidths=[17*cm])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
    ]))
    story.append(footer_table)
    
    # Génération du PDF
    doc.build(story)
    print("PDF généré avec succès : rapport_TP.pdf")

if __name__ == "__main__":
    create_pdf()
