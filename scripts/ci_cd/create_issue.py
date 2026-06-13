import os
import sys
import argparse
import requests
import json
from typing import Optional


def create_github_issue(
    repo_owner: str,
    repo_name: str,
    title: str,
    body: str,
    labels: list,
    github_token: str
) -> Optional[dict]:
    """
    Crea una issue en GitHub usando la API.
    
    Args:
        repo_owner: Propietario del repositorio
        repo_name: Nombre del repositorio
        title: Título de la issue
        body: Cuerpo de la issue
        labels: Lista de etiquetas
        github_token: Token de GitHub con permisos
    
    Returns:
        Diccionario con la respuesta de la API o None si falla
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'title': title,
        'body': body,
        'labels': labels
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creando issue en GitHub: {e}")
        if response:
            print(f"Response: {response.text}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Crea una issue automática en GitHub')
    parser.add_argument('--repo-owner', type=str, required=True, help='Propietario del repositorio')
    parser.add_argument('--repo-name', type=str, required=True, help='Nombre del repositorio')
    parser.add_argument('--pr-number', type=str, required=True, help='Número del PR asociado')
    parser.add_argument('--vulnerability-type', type=str, help='Tipo de vulnerabilidad detectada')
    parser.add_argument('--probability', type=str, help='Probabilidad de vulnerabilidad')
    parser.add_argument('--files', type=str, help='Archivos afectados (separados por coma)')
    parser.add_argument('--github-token', type=str, help='Token de GitHub (o usa GITHUB_TOKEN)')
    
    args = parser.parse_args()
    
    # Obtener token de argumento o variable de entorno
    github_token = args.github_token or os.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("ERROR: Se requiere GITHUB_TOKEN")
        sys.exit(1)
    
    # Construir título de la issue
    title = f"🔒 Vulnerabilidad de seguridad detectada - PR #{args.pr_number}"
    
    # Construir cuerpo de la issue
    body_lines = [
        "## 🚨 Vulnerabilidad de Seguridad Detectada",
        "",
        f"**Pull Request:** #{args.pr_number}",
        f"**Repositorio:** {args.repo_owner}/{args.repo_name}",
        "",
        "### 📋 Detalles de la Vulnerabilidad",
        ""
    ]
    
    if args.vulnerability_type:
        body_lines.extend([
            f"**Tipo de vulnerabilidad:** {args.vulnerability_type}",
            ""
        ])
    
    if args.probability:
        body_lines.extend([
            f"**Probabilidad de vulnerabilidad:** {args.probability}",
            ""
        ])
    
    if args.files:
        body_lines.extend([
            "### 📁 Archivos Afectados",
            ""
        ])
        files_list = args.files.split(',')
        for file in files_list:
            body_lines.append(f"- `{file.strip()}`")
        body_lines.append("")
    
    body_lines.extend([
        "### 🔧 Acciones Requeridas",
        "",
        "- [ ] Revisar el código vulnerable",
        "- [ ] Implementar las correcciones necesarias",
        "- [ ] Validar que las correcciones no introducen nuevos problemas",
        "- [ ] Actualizar el Pull Request con las correcciones",
        "",
        "### 📝 Notas",
        "",
        "Esta issue fue creada automáticamente por el pipeline CI/CD de seguridad.",
        "El modelo de Machine Learning detectó código que podría ser vulnerable.",
        "",
        "---",
        "",
        "*Etiqueta: fixing-required*"
    ])
    
    body = "\n".join(body_lines)
    
    # Etiquetas
    labels = ['fixing-required', 'security', 'automated']
    
    # Crear la issue
    print(f"Creando issue en {args.repo_owner}/{args.repo_name}...")
    result = create_github_issue(
        args.repo_owner,
        args.repo_name,
        title,
        body,
        labels,
        github_token
    )
    
    if result:
        issue_number = result.get('number')
        issue_url = result.get('html_url')
        print(f"✅ Issue creada exitosamente: #{issue_number}")
        print(f"🔗 URL: {issue_url}")
        
        # Guardar el número de issue para uso posterior
        os.makedirs('reports', exist_ok=True)
        with open('reports/issue_number.txt', 'w') as f:
            f.write(str(issue_number))
        
        sys.exit(0)
    else:
        print("❌ Error creando la issue")
        sys.exit(1)


if __name__ == '__main__':
    main()
