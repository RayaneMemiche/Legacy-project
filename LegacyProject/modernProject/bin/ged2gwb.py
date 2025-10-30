#!/usr/bin/env python3
"""
ged2gwb - Convertit un fichier GEDCOM en base de données GeneWeb

Usage:
    ged2gwb input.ged output_dir
    ged2gwb --help

Options:
    -h, --help      Afficher l'aide
    -v, --verbose   Mode verbeux
    --stats         Afficher les statistiques après conversion
"""

import sys
import os
import argparse
from pathlib import Path

# Ajouter le chemin des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from gedcom_parser import GedcomParser, GedcomPerson, GedcomFamily


def convert_gedcom_to_gwb(input_file: str, output_dir: str, verbose: bool = False, show_stats: bool = False):
    """
    Convertir un fichier GEDCOM en base GeneWeb

    Args:
        input_file: Chemin vers le fichier GEDCOM
        output_dir: Répertoire de sortie pour la base GeneWeb
        verbose: Afficher les détails
        show_stats: Afficher les statistiques
    """
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(input_file):
        print(f"❌ Erreur: Le fichier {input_file} n'existe pas")
        return 1

    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    if verbose:
        print(f"📖 Lecture du fichier GEDCOM: {input_file}")

    # Parser le fichier GEDCOM
    parser = GedcomParser()
    try:
        persons, families = parser.parse_file(input_file)
    except Exception as e:
        print(f"❌ Erreur lors du parsing: {e}")
        return 1

    if verbose:
        print(f"✅ Parsing terminé: {len(persons)} personnes, {len(families)} familles")

    # Afficher les statistiques si demandé
    if show_stats or verbose:
        stats = parser.get_statistics()
        print("\n📊 Statistiques:")
        print(f"  Total personnes: {stats['total_persons']}")
        print(f"  Total familles: {stats['total_families']}")
        print(f"  Hommes: {stats['males']}")
        print(f"  Femmes: {stats['females']}")
        print(f"  Avec date de naissance: {stats['with_birth_date']}")
        print(f"  Avec date de décès: {stats['with_death_date']}")
        print(f"  Vivants: {stats['living']}")

    # Convertir en format GeneWeb et sauvegarder
    if verbose:
        print(f"\n💾 Sauvegarde dans: {output_dir}/")

    # Sauvegarder les personnes
    persons_file = os.path.join(output_dir, "persons.txt")
    with open(persons_file, 'w', encoding='utf-8') as f:
        for person_id, person in persons.items():
            line = f"{person.id}|{person.first_name}|{person.last_name}|{person.gender or ''}|"
            line += f"{person.birth_date or ''}|{person.birth_place or ''}|"
            line += f"{person.death_date or ''}|{person.death_place or ''}|"
            line += f"{person.father_id or ''}|{person.mother_id or ''}|"
            line += f"{person.occupation or ''}\n"
            f.write(line)

    # Sauvegarder les familles
    families_file = os.path.join(output_dir, "families.txt")
    with open(families_file, 'w', encoding='utf-8') as f:
        for family_id, family in families.items():
            line = f"{family.id}|{family.husband_id or ''}|{family.wife_id or ''}|"
            line += f"{','.join(family.children_ids)}|"
            line += f"{family.marriage_date or ''}|{family.marriage_place or ''}|"
            line += f"{family.divorce_date or ''}\n"
            f.write(line)

    print(f"\n✅ Conversion terminée avec succès!")
    print(f"   Fichiers créés dans: {output_dir}/")
    print(f"   - persons.txt ({len(persons)} entrées)")
    print(f"   - families.txt ({len(families)} entrées)")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Convertit un fichier GEDCOM en base de données GeneWeb",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  ged2gwb family.ged output_db
  ged2gwb family.ged output_db --verbose --stats
  ged2gwb ~/Downloads/ancestry.ged ~/geneweb/bases/ancestry

Format de sortie:
  Le répertoire de sortie contiendra:
  - persons.txt: Liste des personnes au format pipe-separated
  - families.txt: Liste des familles au format pipe-separated

Pour plus d'informations: https://github.com/geneweb/geneweb
        """
    )

    parser.add_argument(
        'input_file',
        help='Fichier GEDCOM d\'entrée (.ged)'
    )

    parser.add_argument(
        'output_dir',
        help='Répertoire de sortie pour la base GeneWeb'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Afficher les statistiques après conversion'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  ged2gwb - GEDCOM to GeneWeb Converter")
    print("  AWKWARD LEGACY - Version 1.0.0")
    print("=" * 60)
    print()

    exit_code = convert_gedcom_to_gwb(
        args.input_file,
        args.output_dir,
        verbose=args.verbose,
        show_stats=args.stats
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
