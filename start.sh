#!/bin/bash

main() {
    trap '' SIGINT
    echo "Unica forma de salir es escribiendo 'salir'"

    while true; do
        read -p "Ingrese un comando: >" input
        bash ./backend/setup.sh
        cd frontend && pnpm run dev

        if [[ $input == "salir" ]]; then
            exit 0
        fi
    done

    echo "[-] Corriendo script del Backend."
$()
}
main