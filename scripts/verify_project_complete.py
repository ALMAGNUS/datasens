#!/usr/bin/env python3
"""
Script de vérification complet - DataSens E1/v1/v2/v3
Vérifie : JSON valide, linting Python, structure, imports, syntaxe
Objectif : Être "parfait major de promo"
"""
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import ast

# Couleurs pour terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    # Éviter les emojis pour compatibilité Windows
    text_clean = text.replace('🔍', '[CHECK]').replace('🎉', '[SUCCESS]').replace('✗', '[ERROR]')
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text_clean:^80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}[OK]{Colors.END} {text}")

def print_error(text: str):
    print(f"{Colors.RED}[ERROR]{Colors.END} {text}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}[WARN]{Colors.END} {text}")

def print_info(text: str):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {text}")

# ============================================================
# 1. VÉRIFICATION JSON (Notebooks valides)
# ============================================================
def check_json_validity(notebook_path: Path) -> Tuple[bool, str]:
    """Vérifie que le notebook est un JSON valide"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "JSON valide"
    except json.JSONDecodeError as e:
        return False, f"JSON invalide : {e}"
    except Exception as e:
        return False, f"Erreur lecture : {e}"

# ============================================================
# 2. VÉRIFICATION SYNTAXE PYTHON (ast.parse)
# ============================================================
def check_python_syntax(notebook_path: Path) -> Tuple[bool, List[str]]:
    """Vérifie la syntaxe Python de toutes les cellules code"""
    errors = []
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        for i, cell in enumerate(nb.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if source.strip():
                    try:
                        ast.parse(source)
                    except SyntaxError as e:
                        errors.append(f"Cellule {i+1} : {e}")
    except Exception as e:
        errors.append(f"Erreur lecture notebook : {e}")
    
    return len(errors) == 0, errors

# ============================================================
# 3. VÉRIFICATION STRUCTURE NOTEBOOKS
# ============================================================
def check_notebook_structure(notebook_path: Path) -> Tuple[bool, List[str]]:
    """Vérifie la structure minimale d'un notebook"""
    errors = []
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Vérifier clés essentielles
        if 'cells' not in nb:
            errors.append("Clé 'cells' manquante")
        if not isinstance(nb.get('cells'), list):
            errors.append("'cells' doit être une liste")
        if len(nb.get('cells', [])) == 0:
            errors.append("Notebook vide (aucune cellule)")
        
        # Vérifier que chaque cellule a cell_type
        for i, cell in enumerate(nb.get('cells', [])):
            if 'cell_type' not in cell:
                errors.append(f"Cellule {i+1} : 'cell_type' manquant")
            if cell.get('cell_type') not in ['code', 'markdown', 'raw']:
                errors.append(f"Cellule {i+1} : 'cell_type' invalide")
            if 'source' not in cell:
                errors.append(f"Cellule {i+1} : 'source' manquant")
    
    except Exception as e:
        errors.append(f"Erreur vérification structure : {e}")
    
    return len(errors) == 0, errors

# ============================================================
# 4. VÉRIFICATION LINTING (Ruff)
# ============================================================
def check_linting(file_path: Path) -> Tuple[bool, str]:
    """Vérifie le linting avec Ruff (si disponible)"""
    try:
        result = subprocess.run(
            ['ruff', 'check', str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, "Pas d'erreurs de linting"
        else:
            return False, result.stdout + result.stderr
    except FileNotFoundError:
        return None, "Ruff non installé (optionnel)"
    except subprocess.TimeoutExpired:
        return False, "Timeout linting (>30s)"
    except Exception as e:
        return False, f"Erreur linting : {e}"

# ============================================================
# 5. VÉRIFICATION STRUCTURE PROJET
# ============================================================
def check_project_structure(root: Path) -> Tuple[bool, List[str]]:
    """Vérifie la structure du projet"""
    errors = []
    expected_dirs = [
        'notebooks',
        'docs',
        'scripts',
        'config',
        'data'
    ]
    
    for dir_name in expected_dirs:
        dir_path = root / dir_name
        if not dir_path.exists():
            errors.append(f"Dossier '{dir_name}' manquant")
        elif not dir_path.is_dir():
            errors.append(f"'{dir_name}' n'est pas un dossier")
    
    # Vérifier notebooks par version
    for version in ['datasens_E1_v1', 'datasens_E1_v2', 'datasens_E1_v3']:
        nb_dir = root / 'notebooks' / version
        if not nb_dir.exists():
            errors.append(f"Notebooks '{version}' manquant")
        else:
            # Vérifier notebooks essentiels
            essential = ['01_setup_env.ipynb', '02_schema_create.ipynb',
                        '03_ingest_sources.ipynb', '04_crud_tests.ipynb',
                        '05_snapshot_and_readme.ipynb']
            for nb_file in essential:
                if not (nb_dir / nb_file).exists():
                    errors.append(f"Notebook manquant : {version}/{nb_file}")
    
    return len(errors) == 0, errors

# ============================================================
# 6. VÉRIFICATION IMPORTS PYTHON
# ============================================================
def check_imports(notebook_path: Path) -> Tuple[bool, List[str]]:
    """Vérifie que les imports sont syntaxiquement corrects"""
    errors = []
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        for i, cell in enumerate(nb.get('cells', [])):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                # Extraire les imports
                for line in source.split('\n'):
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        try:
                            ast.parse(line)
                        except SyntaxError as e:
                            errors.append(f"Cellule {i+1}, ligne import : {e}")
    
    except Exception as e:
        errors.append(f"Erreur vérification imports : {e}")
    
    return len(errors) == 0, errors

# ============================================================
# 7. VÉRIFICATION FICHIERS ESSENTIELS
# ============================================================
def check_essential_files(root: Path) -> Tuple[bool, List[str]]:
    """Vérifie la présence des fichiers essentiels"""
    errors = []
    essential_files = [
        'README.md',
        '.env.example',
        'requirements.txt',
        '.gitignore',
        'docker-compose.yml',
        'Dockerfile',
        'docs/GUIDE_TECHNIQUE_E1.md',
        'docs/datasens_MPD.sql',
    ]
    
    for file_path in essential_files:
        full_path = root / file_path
        if not full_path.exists():
            errors.append(f"Fichier manquant : {file_path}")
    
    return len(errors) == 0, errors

# ============================================================
# MAIN
# ============================================================
def main():
    print_header("VERIFICATION COMPLETE - DATASENS E1/v1/v2/v3")
    
    # Détection racine projet
    root = Path(__file__).parent.parent
    print_info(f"Racine projet : {root}")
    
    results = {
        'json': {'ok': 0, 'errors': 0, 'total': 0},
        'syntax': {'ok': 0, 'errors': 0, 'total': 0},
        'structure_nb': {'ok': 0, 'errors': 0, 'total': 0},
        'structure_proj': {'ok': 0, 'errors': 0},
        'files': {'ok': 0, 'errors': 0},
        'linting': {'ok': 0, 'errors': 0, 'warnings': 0, 'total': 0}
    }
    
    # ============================================================
    # 1. Vérification structure projet
    # ============================================================
    print_header("1. STRUCTURE DU PROJET")
    ok, errors = check_project_structure(root)
    if ok:
        print_success("Structure projet correcte")
        results['structure_proj']['ok'] = 1
    else:
        for err in errors:
            print_error(err)
        results['structure_proj']['errors'] = len(errors)
    
    # ============================================================
    # 2. Vérification fichiers essentiels
    # ============================================================
    print_header("2. FICHIERS ESSENTIELS")
    ok, errors = check_essential_files(root)
    if ok:
        print_success("Tous les fichiers essentiels présents")
        results['files']['ok'] = 1
    else:
        for err in errors:
            print_error(err)
        results['files']['errors'] = len(errors)
    
    # ============================================================
    # 3. Vérification notebooks (v1/v2/v3)
    # ============================================================
    print_header("3. VÉRIFICATION NOTEBOOKS (v1/v2/v3)")
    
    versions = ['datasens_E1_v1', 'datasens_E1_v2', 'datasens_E1_v3']
    notebooks_to_check = []
    
    for version in versions:
        nb_dir = root / 'notebooks' / version
        if nb_dir.exists():
            for nb_file in nb_dir.glob('*.ipynb'):
                notebooks_to_check.append(nb_file)
    
    print_info(f"{len(notebooks_to_check)} notebook(s) à vérifier\n")
    
    for nb_path in notebooks_to_check:
        rel_path = nb_path.relative_to(root)
        print(f"\n[NOTEBOOK] {rel_path}")
        
        # JSON valide
        ok, msg = check_json_validity(nb_path)
        results['json']['total'] += 1
        if ok:
            print_success(f"JSON valide")
            results['json']['ok'] += 1
        else:
            print_error(msg)
            results['json']['errors'] += 1
            continue  # Si JSON invalide, on skip le reste
        
        # Structure notebook
        ok, errors = check_notebook_structure(nb_path)
        results['structure_nb']['total'] += 1
        if ok:
            print_success("Structure notebook correcte")
            results['structure_nb']['ok'] += 1
        else:
            for err in errors:
                print_error(f"Structure : {err}")
            results['structure_nb']['errors'] += 1
        
        # Syntaxe Python
        ok, errors = check_python_syntax(nb_path)
        results['syntax']['total'] += 1
        if ok:
            print_success("Syntaxe Python correcte")
            results['syntax']['ok'] += 1
        else:
            for err in errors:
                print_error(f"Syntaxe : {err}")
            results['syntax']['errors'] += 1
        
        # Imports Python
        ok, errors = check_imports(nb_path)
        if ok:
            print_success("Imports Python valides")
        else:
            for err in errors:
                print_error(f"Import : {err}")
        
        # Linting (optionnel)
        lint_result, lint_msg = check_linting(nb_path)
        results['linting']['total'] += 1
        if lint_result is True:
            print_success(f"Linting : {lint_msg}")
            results['linting']['ok'] += 1
        elif lint_result is False:
            print_warning(f"Linting : {lint_msg}")
            results['linting']['warnings'] += 1
        else:
            print_info(f"Linting : {lint_msg}")
    
    # ============================================================
    # RÉSUMÉ FINAL
    # ============================================================
    print_header("📊 RÉSUMÉ FINAL")
    
    total_checks = (
        results['json']['total'] +
        results['syntax']['total'] +
        results['structure_nb']['total'] +
        results['structure_proj']['ok'] +
        results['files']['ok'] +
        results['linting']['total']
    )
    
    total_ok = (
        results['json']['ok'] +
        results['syntax']['ok'] +
        results['structure_nb']['ok'] +
        results['structure_proj']['ok'] +
        results['files']['ok'] +
        results['linting']['ok']
    )
    
    total_errors = (
        results['json']['errors'] +
        results['syntax']['errors'] +
        results['structure_nb']['errors'] +
        results['structure_proj']['errors'] +
        results['files']['errors']
    )
    
    print(f"\n{Colors.BOLD}Resultats :{Colors.END}")
    print(f"  [OK] JSON valide           : {results['json']['ok']}/{results['json']['total']}")
    print(f"  [OK] Syntaxe Python        : {results['syntax']['ok']}/{results['syntax']['total']}")
    print(f"  [OK] Structure notebook    : {results['structure_nb']['ok']}/{results['structure_nb']['total']}")
    print(f"  [OK] Structure projet      : {results['structure_proj']['ok']}/1")
    print(f"  [OK] Fichiers essentiels   : {results['files']['ok']}/1")
    print(f"  [OK] Linting (optionnel)   : {results['linting']['ok']}/{results['linting']['total']}")
    
    if total_errors == 0:
        print(f"\n{Colors.BOLD}{Colors.GREEN}[SUCCESS] PROJET PARFAIT - MAJOR DE PROMO !{Colors.END}")
        print(f"{Colors.GREEN}[OK] Tous les checks passent ({total_ok}/{total_checks}){Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}[ERROR] {total_errors} erreur(s) detectee(s){Colors.END}")
        print(f"{Colors.YELLOW}[WARN] Corrigez les erreurs avant le commit{Colors.END}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())

