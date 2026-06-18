import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request


def github_request(repo: str, token: str, method: str, path: str, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        return exc.code, {"error": body}


def protection_payload(required_checks):
    return {
        "required_status_checks": {
            "strict": True,
            "contexts": required_checks,
        } if required_checks else None,
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 0,
            "require_last_push_approval": False,
            "bypass_pull_request_allowances": {
                "users": [],
                "teams": [],
                "apps": [],
            },
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": False,
        "lock_branch": False,
        "allow_fork_syncing": True,
    }


def verify(repo: str, token: str, branches):
    ok = True
    for branch, checks in branches.items():
        status, data = github_request(repo, token, "GET", f"/branches/{branch}/protection")
        if status != 200:
            print(f"{branch}: NOT PROTECTED ({status})")
            ok = False
            continue

        actual_checks = (data.get("required_status_checks") or {}).get("contexts") or []
        enforce_admins = bool((data.get("enforce_admins") or {}).get("enabled"))
        force_pushes = bool((data.get("allow_force_pushes") or {}).get("enabled"))
        deletions = bool((data.get("allow_deletions") or {}).get("enabled"))
        pr_required = bool(data.get("required_pull_request_reviews"))

        branch_ok = (
            pr_required
            and enforce_admins
            and not force_pushes
            and not deletions
            and all(check in actual_checks for check in checks)
        )
        ok = ok and branch_ok
        print(
            f"{branch}: {'OK' if branch_ok else 'INCOMPLETE'} | "
            f"checks={actual_checks} | pr_required={pr_required} | "
            f"enforce_admins={enforce_admins} | force_pushes={force_pushes} | deletions={deletions}"
        )

    return ok


def get_git_credential_token():
    try:
        result = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            text=True,
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    values = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    return values.get("password") or values.get("oauth_token")


def main():
    parser = argparse.ArgumentParser(description="Configura proteccion de ramas para el proyecto.")
    parser.add_argument("--repo", default="BrayanJac/ModeloIA_DeteccionCodigoSeguro")
    parser.add_argument(
        "--token",
        default=os.environ.get("GH_ADMIN_TOKEN") or os.environ.get("GITHUB_TOKEN") or get_git_credential_token(),
    )
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    if not args.token:
        print("ERROR: configura GH_ADMIN_TOKEN con permisos de administrador del repositorio.")
        sys.exit(1)

    branches = {
        "dev": [],
        "test": ["Analyze Code with ML Model"],
        "main": ["Unit Tests", "Integration Tests"],
    }

    if args.verify_only:
        sys.exit(0 if verify(args.repo, args.token, branches) else 1)

    for branch, checks in branches.items():
        status, data = github_request(
            args.repo,
            args.token,
            "PUT",
            f"/branches/{branch}/protection",
            protection_payload(checks),
        )
        if status not in (200, 201):
            print(f"ERROR configurando {branch}: HTTP {status}")
            print((data or {}).get("error", data))
            sys.exit(1)
        print(f"{branch}: proteccion aplicada")

    sys.exit(0 if verify(args.repo, args.token, branches) else 1)


if __name__ == "__main__":
    main()
