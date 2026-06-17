import os
import sys
import argparse
import re
import requests
from typing import Optional, Tuple


def normalize_bot_token(token: str) -> str:
    """Elimina espacios y prefijos comunes al copiar el token."""
    token = token.strip().strip('"').strip("'")
    if token.lower().startswith('bot '):
        token = token[4:].strip()
    return token


def normalize_chat_id(chat_id: str) -> str:
    """Normaliza el chat/user id de Telegram."""
    chat_id = chat_id.strip().strip('"').strip("'")
    if chat_id.startswith('@'):
        chat_id = chat_id[1:]
    return chat_id


def validate_credentials(bot_token: str, chat_id: str) -> Tuple[bool, str]:
    """
    Valida token y chat_id antes de enviar.
    Un 404 en sendMessage casi siempre indica token de bot inválido.
    """
    if not bot_token:
        return False, "TELEGRAM_BOT_TOKEN está vacío. Configura el secret en GitHub (Settings → Secrets → Actions)."

    if not chat_id:
        return False, "TELEGRAM_CHAT_ID está vacío. Configura el secret en GitHub (Settings → Secrets → Actions)."

    if ':' not in bot_token:
        return False, (
            "TELEGRAM_BOT_TOKEN no tiene formato válido. "
            "Debe ser algo como '123456789:AAH...' (obténlo con @BotFather). "
            "Verifica que no hayas pegado el chat ID o el username del bot."
        )

    if chat_id.startswith('-') or chat_id.isdigit() or re.fullmatch(r'-?\d+', chat_id):
        pass
    elif re.fullmatch(r'[A-Za-z0-9_]+', chat_id):
        return False, (
            f"TELEGRAM_CHAT_ID parece un username ('{chat_id}'), no un ID numérico. "
            "Usa tu user ID numérico (ej. 123456789). Puedes obtenerlo con @userinfobot."
        )
    else:
        return False, (
            "TELEGRAM_CHAT_ID no parece válido. "
            "Debe ser un número entero (ej. 123456789)."
        )

    try:
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getMe",
            timeout=10
        )
        data = response.json()
    except requests.exceptions.RequestException as e:
        return False, f"No se pudo conectar con la API de Telegram: {e}"

    if not data.get('ok'):
        error_code = data.get('error_code', response.status_code)
        description = data.get('description', 'Error desconocido')
        if error_code == 404 or response.status_code == 404:
            return False, (
                "Token de bot inválido (404 Not Found). "
                "Regenera el token con @BotFather (/token) y actualiza el secret TELEGRAM_BOT_TOKEN. "
                "Asegúrate de no incluir espacios ni el prefijo 'Bot '."
            )
        return False, f"Token de bot rechazado por Telegram ({error_code}): {description}"

    bot_username = data['result'].get('username', 'unknown')
    print(f"✅ Bot verificado: @{bot_username}")

    try:
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getChat",
            params={'chat_id': chat_id},
            timeout=10
        )
        data = response.json()
    except requests.exceptions.RequestException as e:
        return False, f"No se pudo validar el chat ID: {e}"

    if not data.get('ok'):
        description = data.get('description', 'Error desconocido')
        return False, (
            f"Chat ID inválido o bot sin acceso: {description}. "
            "Abre Telegram, busca tu bot y envíale /start antes de probar."
        )

    print(f"✅ Chat verificado: id={data['result'].get('id')}")
    return True, ""


def send_telegram_message(
    bot_token: str,
    chat_id: str,
    message: str,
    parse_mode: str = 'Markdown'
) -> bool:
    """
    Envía un mensaje a través de la API de Telegram.
    
    Args:
        bot_token: Token del bot de Telegram
        chat_id: ID del chat donde enviar el mensaje
        message: Contenido del mensaje
        parse_mode: Modo de parseo (Markdown o HTML)
    
    Returns:
        True si el mensaje se envió exitosamente, False en caso contrario
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': parse_mode
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 400:
            # Reintentar sin parse_mode si falla el formato Markdown
            payload_no_format = {'chat_id': chat_id, 'text': message}
            retry = requests.post(url, json=payload_no_format, timeout=10)
            retry.raise_for_status()
            return True
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        detail = e.response.text if e.response is not None else str(e)
        status = e.response.status_code if e.response is not None else None
        if status == 404:
            print(
                "Error enviando mensaje a Telegram: token de bot inválido (404). "
                "Verifica TELEGRAM_BOT_TOKEN en GitHub Secrets."
            )
        else:
            print(f"Error enviando mensaje a Telegram ({status}): {detail}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error enviando mensaje a Telegram: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Envía notificaciones a Telegram')
    parser.add_argument('--bot-token', type=str, help='Token del bot de Telegram (o usa TELEGRAM_BOT_TOKEN)')
    parser.add_argument('--chat-id', type=str, help='ID del chat (o usa TELEGRAM_CHAT_ID)')
    parser.add_argument('--message', type=str, help='Mensaje personalizado (opcional; el contenido se genera según --event)')
    parser.add_argument('--dry-run', action='store_true', help='Muestra el mensaje sin enviarlo')
    parser.add_argument('--validate-only', action='store_true', help='Solo valida token y chat ID')
    parser.add_argument('--event', type=str,
                       choices=['analysis_start', 'analysis_result', 'vulnerability_rejected', 
                               'merge_test', 'merge_main', 'test_result', 'deploy_success', 'deploy_failed'],
                       help='Tipo de evento')
    parser.add_argument('--pr-number', type=str, help='Número del PR')
    parser.add_argument('--repo', type=str, help='Nombre del repositorio')
    parser.add_argument('--status', type=str, help='Estado (success/failure)')
    parser.add_argument('--details', type=str, help='Detalles adicionales')
    
    args = parser.parse_args()
    
    # Obtener token y chat_id de argumentos o variables de entorno
    bot_token = normalize_bot_token(args.bot_token or os.environ.get('TELEGRAM_BOT_TOKEN', ''))
    chat_id = normalize_chat_id(args.chat_id or os.environ.get('TELEGRAM_CHAT_ID', ''))

    if args.dry_run:
        bot_token = bot_token or '123456789:DRY_RUN_TOKEN'
        chat_id = chat_id or '123456789'
    else:
        valid, error_message = validate_credentials(bot_token, chat_id)
        if not valid:
            print(f"ERROR: {error_message}")
            sys.exit(1)

    if args.validate_only:
        print("✅ Credenciales de Telegram válidas")
        sys.exit(0)

    if not args.event:
        print("ERROR: Se requiere --event (excepto con --validate-only)")
        sys.exit(1)
    
    # Construir mensaje según el evento
    event_emojis = {
        'analysis_start': '🔍',
        'analysis_result': '📊',
        'vulnerability_rejected': '🚫',
        'merge_test': '🔀',
        'merge_main': '🔀',
        'test_result': '🧪',
        'deploy_success': '🚀',
        'deploy_failed': '❌'
    }
    
    emoji = event_emojis.get(args.event, 'ℹ️')
    
    message_lines = [
        f"{emoji} *Pipeline CI/CD Seguro con IA*",
        ""
    ]
    
    if args.event == 'analysis_start':
        message_lines.extend([
            "*Evento:* Inicio del análisis de seguridad",
            f"*PR:* #{args.pr_number}" if args.pr_number else "",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            "",
            "Iniciando análisis de código con modelo de Machine Learning..."
        ])
    
    elif args.event == 'analysis_result':
        status_emoji = "✅" if args.status == "success" else "❌"
        message_lines.extend([
            "*Evento:* Resultado del análisis de seguridad",
            f"*PR:* #{args.pr_number}" if args.pr_number else "",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            f"*Estado:* {status_emoji} {args.status.upper()}" if args.status else "",
            ""
        ])
        if args.details:
            message_lines.append(f"*Detalles:* {args.details}")
    
    elif args.event == 'vulnerability_rejected':
        message_lines.extend([
            "*Evento:* Rechazo por vulnerabilidad detectada",
            f"*PR:* #{args.pr_number}" if args.pr_number else "",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            "",
            "❌ El Pull Request ha sido bloqueado debido a código vulnerable.",
            ""
        ])
        if args.details:
            message_lines.append(f"*Detalles:* {args.details}")
    
    elif args.event == 'merge_test':
        message_lines.extend([
            "*Evento:* Merge a rama test",
            f"*PR:* #{args.pr_number}" if args.pr_number else "",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            "",
            "✅ El código ha sido mergeado a la rama test."
        ])

    elif args.event == 'merge_main':
        message_lines.extend([
            "*Evento:* Merge a rama main",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            "",
            "✅ El código ha sido mergeado a la rama main."
        ])
    
    elif args.event == 'test_result':
        status_emoji = "✅" if args.status == "success" else "❌"
        message_lines.extend([
            "*Evento:* Resultado de pruebas",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            f"*Estado:* {status_emoji} {args.status.upper()}" if args.status else "",
            ""
        ])
        if args.status == "failure":
            message_lines.extend([
                "❌ Las pruebas han fallado. El merge está bloqueado.",
                ""
            ])
            if args.details:
                message_lines.append(f"*Detalles:* {args.details}")
        else:
            message_lines.append("✅ Todas las pruebas han pasado exitosamente.")
            if args.details:
                message_lines.append(f"*Detalles:* {args.details}")
    
    elif args.event == 'deploy_success':
        message_lines.extend([
            "*Evento:* Despliegue exitoso",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            "",
            "🚀 La aplicación ha sido desplegada exitosamente en producción."
        ])
    
    elif args.event == 'deploy_failed':
        message_lines.extend([
            "*Evento:* Despliegue fallido",
            f"*Repositorio:* {args.repo}" if args.repo else "",
            "",
            "❌ El despliegue ha fallado."
        ])
        if args.details:
            message_lines.append(f"*Detalles:* {args.details}")
    
    # Filtrar líneas vacías
    message_lines = [line for line in message_lines if line]
    message = args.message if args.message else "\n".join(message_lines)
    
    if args.dry_run:
        print("--- Mensaje (dry-run) ---")
        print(message)
        print("-------------------------")
        sys.exit(0)
    
    # Enviar mensaje
    success = send_telegram_message(bot_token, chat_id, message)
    
    if success:
        print("✅ Mensaje enviado a Telegram exitosamente")
        sys.exit(0)
    else:
        print("❌ Error enviando mensaje a Telegram")
        sys.exit(1)


if __name__ == '__main__':
    main()
