# Redis 
Para almacenamiento en memoria RAM para un servicio altamente optimizado

**Para integrar Redis eficientemente, necesitas implementar el patrón Cache-Aside junto con una estrategia de Invalidación de Caché.**

La lógica se divide en dos partes:

- En las lecturas (get_all): Interceptar la petición antes de ir a la base de datos. Si los datos están en Redis, devolverlos inmediatamente (deserializándolos). Si no están, ir a la base de datos, guardar el resultado en Redis (serializado a JSON) y devolverlos.

- En las escrituras (add, update, remove): Eliminar las claves guardadas en Redis para forzar que el próximo GET obtenga datos frescos directamente de la base de datos.

# Ver las consultas Sql de la base de datos 
El engine de SQLModel deberia tener la siguiente forma:
̣̣
```python3
engine = create_engine(DATABASE_URL, echo=True)
```
## Redis + ARG
Para poder usar contraseñas de aplicacion 
1) Activar 2 paso de verificacion 
2) Crear un nombre a la aplicacion (myaccount.google.com/apppasswords)
3) Copiar y pegar en el .env (setup.sh)