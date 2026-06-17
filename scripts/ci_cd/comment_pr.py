import os
import sys
import argparse
import requests
from typing import Optional


def add_pr_comment(
    repo_owner: str,
    repo_name: str,
    pr_number: int,
    body: str,
    github_token: str
) -> Optional[dict]:
    """
    Agrega un comentario a un Pull Request en GitHub.
    
    Args:
        repo_owner: Propietario del repositorio
        repo_name: Nombre del repositorio
        pr_number: Número del Pull Request
        body: Contenido del comentario
        github_token: Token de GitHub con permisos
    
    Returns:
        Diccionario con la respuesta de la API o None si falla
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'body': body
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error agregando comentario al PR: {e}")
        if response:
            print(f"Response: {response.text}")
        return None


def add_pr_label(
    repo_owner: str,
    repo_name: str,
    pr_number: int,
    label: str,
    github_token: str
) -> bool:
    """
    Agrega una etiqueta a un Pull Request en GitHub.
    
    Args:
        repo_owner: Propietario del repositorio
        repo_name: Nombre del repositorio
        pr_number: Número del Pull Request
        label: Nombre de la etiqueta
        github_token: Token de GitHub con permisos
    
    Returns:
        True si se agregó exitosamente, False en caso contrario
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/labels"
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    payload = [label]
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error agregando etiqueta al PR: {e}")
        if response:
            print(f"Response: {response.text}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Comenta y etiqueta Pull Requests en GitHub')
    parser.add_argument('--repo-owner', type=str, required=True, help='Propietario del repositorio')
    parser.add_argument('--repo-name', type=str, required=True, help='Nombre del repositorio')
    parser.add_argument('--pr-number', type=int, required=True, help='Número del PR')
    parser.add_argument('--comment-file', type=str, help='Archivo con el comentario (Markdown)')
    parser.add_argument('--comment-text', type=str, help='Texto del comentario directamente')
    parser.add_argument('--label', type=str, help='Etiqueta a agregar (fixing-required, tests-failed)')
    parser.add_argument('--github-token', type=str, help='Token de GitHub (o usa GITHUB_TOKEN)')
    
    args = parser.parse_args()
    
    # Obtener token de argumento o variable de entorno
    github_token = args.github_token or os.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: Se requiere GITHUB_TOKEN")
        sys.exit(1)
    
    comment_body = None
    if args.comment_file:
        if not os.path.exists(args.comment_file):
            print(f"ERROR: Archivo de comentario no encontrado: {args.comment_file}")
            sys.exit(1)
        with open(args.comment_file, 'r', encoding='utf-8') as f:
            comment_body = f.read()
    elif args.comment_text:
        comment_body = args.comment_text

    if not comment_body and not args.label:
        print("ERROR: Se requiere --comment-file, --comment-text o --label")
        sys.exit(1)

    if comment_body:
        print(f"Agregando comentario al PR #{args.pr_number}...")
        comment_result = add_pr_comment(
            args.repo_owner,
            args.repo_name,
            args.pr_number,
            comment_body,
            github_token
        )
        
        if comment_result:
            print("✅ Comentario agregado exitosamente")
        else:
            print("❌ Error agregando comentario")
            sys.exit(1)
    
    # Agregar etiqueta si se especificó
    if args.label:
        print(f"Agregando etiqueta '{args.label}' al PR...")
        label_result = add_pr_label(
            args.repo_owner,
            args.repo_name,
            args.pr_number,
            args.label,
            github_token
        )
        
        if label_result:
            print(f"✅ Etiqueta '{args.label}' agregada exitosamente")
        else:
            print(f"❌ Error agregando etiqueta '{args.label}'")
            sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
