"""CONFIGURACIÓN DEL LOGGER PARA FALLOS
"""
import os
import logging
import aiosmtplib
from email.message import EmailMessage
from arq import Retry
from config.redis_config import redis_settings
from utils.constants import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD

os.makedirs("logs", exist_ok=True)

worker_logger = logging.getLogger("WorkerLogger")
worker_logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler("logs/redis.log", encoding="utf-8")
file_handler.setLevel(logging.ERROR)

formato_log = logging.Formatter('%(asctime)s - DATA: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formato_log)

if not worker_logger.handlers:
    worker_logger.addHandler(file_handler)

async def send_welcome_email(ctx: dict, user_email: str):
    "Envia el mail de bienvenida, auqe sigo pensndo que se puede reutilizar de "
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = user_email
    message["Subject"] = "¡Bienvenido a nuestra plataforma!"
    
    body = "Hola,\n\n¡Gracias por crear tu cuenta!\n\nSaludos,\nEl Equipo"
    message.set_content(body)
    
    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=int(SMTP_PORT),
            username=EMAIL_USER,
            password=EMAIL_PASSWORD,
            start_tls=True,
        )
        print(f"✅ Email enviado con éxito a: {user_email}")
        
    except Exception as e:
        intento_actual = ctx['job_try']
        motivo_fallo = str(e)
        
        worker_logger.error(f"{user_email} (Intento {intento_actual}) - MOTIVO_FALLO: {motivo_fallo}")
        
        print(f"❌ Error al enviar a {user_email} guardado en log. Reintentando en 60s...")
        
        # reintento en 60seconds
        raise Retry(defer=60) 

class WorkerSettings:
    functions = [send_welcome_email]
    redis_settings = redis_settings
    # 15 intentos -> 15(60)-> 15 min
    max_tries = 15