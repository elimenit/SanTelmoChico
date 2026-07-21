#!/bin/bash
# autor o autores: Yachak,.
# aplicacion en localhost, pero esta pensada para ser desplegada.
# LOGICA 
# request -> app -> /routers -> /schemas(Validacion)
# -> /database(Read & Write Before Redis) -> 
# redis o redis + ARQ (Cola de mensajeria) -> Response

export DIR_BACKEND="$HOME/SanTelmoChico/backend"
echo "Directorio de trabajo: $DIR_BACKEND"

technology_needs() {
    sudo apt update #&& sudo apt upgrade -y
    sudo apt install postgresql redis-server
}
init_db_postgres() {
    sudo systemctl start postgresql
    sudo systemctl start redis-server
}
create_file_pount_env() {
    echo "[+] No seas pndj@ lee el codigo que no funciona"
    exit 0
    # Ejemplo de variables de entorno
    echo "ALGORITHM='HS256'" > .env
    echo "ACCESS_TOKEN_EXPIRE_MINUTES=15" >> .env
    echo "FIRST_SUPERUSER_EMAIL='admin@example.com'" >> .env
    echo "FIRST_SUPERUSER_PASSWORD='passwordSecure2026currenthard'" >> .env
    echo "SECRET_KEY='random_forest_de_auth_algoritm_cripthografy_machinel'" >> .env
    echo "DATABASE_URL='postgresql://postgres:password@localhost:5432/santelmochico'" >> .env
    echo "NAME_DB='santelmochico'" >> .env
    echo "SERVER_REDIS='localhost'" >> .env
    echo "PORT_REDIS=6379" >> .env
    echo "SMTP_SERVER='smtp.gmail.com' " >> .env
    echo "SMTP_PORT=587" >> .env
    echo "EMAIL_USER='people@gmail.com'" >> .env
    echo "EMAIL_PASSWORD='abcd efgh ijkl mnop'" >> .env
}
create_virtual_enviroment() {
    
    cd "$DIR_BACKEND"

    if [[ ! -d ".venv" ]]; then
        echo "[+] Creando entorno Virtual..."
        python3 -m venv .venv
    else
        echo "[+] Ya existe el entorno Virtual"
    fi

    source ".venv/bin/activate"
    pip3 install -r requirements.txt --retries=30
    clear
    # .venv activate 
    arq workers.email_worker.WorkerSettings & # Redis + ARG -> Cola de mensajeria
    echo "[+] Cola de mensajeria Funcionando"
    fastapi dev app.py || fastapi run app.py
}
main() {
    cd $DIR_BACKEND
    technology_needs
    init_db_postgres
    create_file_pount_env
    create_virtual_enviroment
    
}
main