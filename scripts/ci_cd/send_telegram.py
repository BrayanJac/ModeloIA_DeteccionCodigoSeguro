import os
import sys
import argparse
import requests
from typing import Optional


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
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error enviando mensaje a Telegram: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Envía notificaciones a Telegram')
    parser.add_argument('--bot-token', type=str, help='Token del bot de Telegram (o usa TELEGRAM_BOT_TOKEN)')
    parser.add_argument('--chat-id', type=str, help='ID del chat (o usa TELEGRAM_CHAT_ID)')
    parser.add_argument('--message', type=str, required=True, help='Mensaje a enviar')
    parser.add_argument('--event', type=str, required=True, 
                       choices=['analysis_start', 'analysis_result', 'vulnerability_rejected', 
                               'merge_test', 'test_result', 'deploy_success', 'deploy_failed'],
                       help='Tipo de evento')
    parser.add_argument('--pr-number', type=str, help='Número del PR')
    parser.add_argument('--repo', type=str, help='Nombre del repositorio')
    parser.add_argument('--status', type=str, help='Estado (success/failure)')
    parser.add_argument('--details', type=str, help='Detalles adicionales')
    
    args = parser.parse_args()
    
    # Obtener token y chat_id de argumentos o variables de entorno
    bot_token = args.bot_token or os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = args.chat_id or os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("ERROR: Se requieren TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID")
        sys.exit(1)
    
    # Construir mensaje según el evento
    event_emojis = {
        'analysis_start': '🔍',
        'analysis_result': '📊',
        'vulnerability_rejected': '🚫',
        'merge_test': '🔀',
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
            f"**Evento:** Inicio del análisis de seguridad",
            f"**PR:** #{args.pr_number}" if args.pr_number else "",
            f"**Repositorio:** {args.repo}" if args.repo else "",
            "",
            "Iniciando análisis de código con modelo de Machine Learning..."
        ])
    
    elif args.event == 'analysis_result':
        status_emoji = "✅" if args.status == "success" else "❌"
        message_lines.extend([
            f"**Evento:** Resultado del análisis de seguridad",
            f"**PR:** #{args.pr_number}" if args.pr_number else "",
            f"**Repositorio:** {args.repo}" if args.repo else "",
            f"**Estado:** {status_emoji} {args.status.upper()}" if args.status else "",
            ""
        ])
        if args.details:
            message_lines.append(f"**Detalles:** {args.details}")
    
    elif args.event == 'vulnerability_rejected':
        message_lines.extend([
            f"**Evento:** Rechazo por vulnerabilidad detectada",
            f"**PR:** #{args.pr_number}" if args.pr_number else "",
            f"**Repositorio:** {args.repo}" if args.repo else "",
            "",
            "❌ El Pull Request ha sido bloqueado debido a código vulnerable.",
            ""
        ])
        if args.details:
            message_lines.append(f"**Detalles:** {args.details}")
    
    elif args.event == 'merge_test':
        message_lines.extend([
            f"**Evento:** Merge a rama test",
            f"**PR:** #{args.pr_number}" if args.pr_number else "",
            f"**Repositorio:** {args.repo}" if args.repo else "",
            "",
            "✅ El código ha sido mergeado a la rama test."
        ])
    
    elif args.event == 'test_result':
        status_emoji = "✅" if args.status == "success" else "❌"
        message_lines.extend([
            f"**Evento:** Resultado de pruebas",
            f"**Repositorio:** {args.repo}" if args.repo else "",
            f"**Estado:** {status_emoji} {args.status.upper()}" if args.status else "",
            ""
        ])
        if args.status == "failure":
            message_lines.extend([
                "❌ Las pruebas han fallado. El merge está bloqueado.",
                ""
            ])
            if args.details:
                message_lines.append(f"**Detalles:** {args.details}")
        else:
            message_lines.append("✅ Todas las pruebas han pasado exitosamente.")
    
    elif args.event == 'deploy_success':
        message_lines.extend([
            f"**Evento:** Despliegue exitoso",
            f"**Repositorio:** {args.repo}" if args.repo else "",
            "",
            "🚀 La aplicación ha sido desplegada exitosamente en producción."
        ])
    
    elif args.event == 'deploy_failed':
        message_lines.extend([
            f"**Evento:** Despliegue fallido",
            f"**Repositorio:** {args.repo}" if args.repo else "",
            "",
            "❌ El despliegue ha fallado."
        ])
        if args.details:
            message_lines.append(f"**Detalles:** {args.details}")
    
    # Filtrar líneas vacías
    message_lines = [line for line in message_lines if line]
    message = "\n".join(message_lines)
    
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
