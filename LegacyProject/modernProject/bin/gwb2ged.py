#!/usr/bin/env python3
"""
gwb2ged - Convertit une base de données GeneWeb en fichier GEDCOM

Usage:
    gwb2ged input_dir output.ged
    gwb2ged --help

Options:
    -h, --help      Afficher l'aide
    -v, --verbose   Mode verbeux
    --source NAME   Nom du logiciel source (défaut: AWKWARD LEGACY)
"""

import sys
import os
import argparse
from pathlib import Path

# Ajouter le chemin des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from gedcom_exporter import GedcomExporter


def convert_gwb_to_gedcom(input_dir: str, output_file: str, verbose: bool = False, source: str = "AWKWARD LEGACY"):
    """
    Convertir une base GeneWeb en fichier GEDCOM

    Args:
        input_dir: Répertoire contenant la base GeneWeb
        output_file: Fichier GEDCOM de sortie
        verbose: Afficher les détails
        source: Nom du logiciel source
    """
    # Vérifier que le répertoire d'entrée existe
    if not os.path.exists(input_dir):
        print(f"❌ Erreur: Le répertoire {input_dir} n'existe pas")
        return 1

    persons_file = os.path.join(input_dir, "persons.txt")
    families_file = os.path.join(input_dir, "families.txt")

    # Vérifier que les fichiers existent
    if not os.path.exists(persons_file):
        print(f"❌ Erreur: Le fichier {persons_file} n'existe pas")
        return 1

    if not os.path.exists(families_file):
        print(f"❌ Erreur: Le fichier {families_file} n'existe pas")
        return 1

    if verbose:
        print(f"📖 Lecture de la base GeneWeb: {input_dir}/")

    # Charger les personnes
    persons = []
    try:
        with open(persons_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split('|')
                if len(parts) >= 11:
                    person = {
                        'id': parts[0],
                        'first_name': parts[1],
                        'last_name': parts[2],
                        'gender': parts[3] if parts[3] else None,
                        'birth_date': parts[4] if parts[4] else None,
                        'birth_place': parts[5] if parts[5] else None,
                        'death_date': parts[6] if parts[6] else None,
                        'death_place': parts[7] if parts[7] else None,
                        'father_id': parts[8] if parts[8] else None,
                        'mother_id': parts[9] if parts[9] else None,
                        'occupation': parts[10] if parts[10] else None
                    }
                    persons.append(person)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de persons.txt: {e}")
        return 1

    # Charger les familles
    families = []
    try:
        with open(families_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split('|')
                if len(parts) >= 7:
                    family = {
                        'id': parts[0],
                        'father_id': parts[1] if parts[1] else None,
                        'mother_id': parts[2] if parts[2] else None,
                        'children_ids': parts[3].split(',') if parts[3] else [],
                        'marriage_date': parts[4] if parts[4] else None,
                        'marriage_place': parts[5] if parts[5] else None,
                        'divorce_date': parts[6] if parts[6] else None
                    }
                    families.append(family)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de families.txt: {e}")
        return 1

    if verbose:
        print(f"✅ Chargement terminé: {len(persons)} personnes, {len(families)} familles")

    # Exporter en GEDCOM
    if verbose:
        print(f"\n💾 Export vers: {output_file}")

    try:
        exporter = GedcomExporter(source=source)
        exporter.export_to_file(persons, families, output_file)
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        return 1

    print(f"\n✅ Conversion terminée avec succès!")
    print(f"   Fichier créé: {output_file}")
    print(f"   - {len(persons)} personnes")
    print(f"   - {len(families)} familles")

    # Afficher la taille du fichier
    file_size = os.path.getsize(output_file)
    if file_size < 1024:
        size_str = f"{file_size} bytes"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size / 1024:.1f} KB"
    else:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"

    print(f"   Taille: {size_str}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Convertit une base de données GeneWeb en fichier GEDCOM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  gwb2ged output_db family.ged
  gwb2ged output_db family.ged --verbose
  gwb2ged ~/geneweb/bases/ancestry ~/exports/ancestry.ged --source "MyApp"

Format d'entrée:
  Le répertoire d'entrée doit contenir:
  - persons.txt: Liste des personnes au format pipe-separated
  - families.txt: Liste des familles au format pipe-separated

Format de sortie:
  Fichier GEDCOM 5.5.1 compatible avec:
  - Family Tree Maker
  - Ancestry.com
  - MyHeritage
  - GeneWeb
  - Et autres logiciels de généalogie

Pour plus d'informations: https://github.com/geneweb/geneweb
        """
    )

    parser.add_argument(
        'input_dir',
        help='Répertoire contenant la base GeneWeb'
    )

    parser.add_argument(
        'output_file',
        help='Fichier GEDCOM de sortie (.ged)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux'
    )

    parser.add_argument(
        '--source',
        default="AWKWARD LEGACY",
        help='Nom du logiciel source (défaut: AWKWARD LEGACY)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  gwb2ged - GeneWeb to GEDCOM Converter")
    print("  AWKWARD LEGACY - Version 1.0.0")
    print("=" * 60)
    print()

    exit_code = convert_gwb_to_gedcom(
        args.input_dir,
        args.output_file,
        verbose=args.verbose,
        source=args.source
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
