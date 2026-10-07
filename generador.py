import random
import uuid
from datetime import date, timedelta

# Listas de datos base para generar combinaciones
nombres = ["Carlos", "Laura", "Pedro", "Ana", "Luis", "Carmen", "Jorge", "Marta", "Diego", "Sofia", "Miguel", "Lucia", "Juan", "Elena", "Andres", "Valeria", "Gabriel", "Isabella", "Fernando", "Camila", "Ricardo", "Paula"]
apellidos = ["Gomez", "Perez", "Rodriguez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Diaz", "Torres", "Ramirez"]
nacionalidades = ["Chilena", "Mexicana", "Española", "Argentina", "Colombiana", "Peruana"]
idiomas_posibles = ["Español", "Ingles", "Frances", "Japones", "Portugues", "Italiano"]
producciones = ["El misterio final", "Aventuras espaciales", "La gran ciudad", "Héroes oscuros", "Cuentos de la cripta", "Guerreros mágicos"]
tipos_produccion = ["profesional", "independiente"]
roles = ["principal", "secundario", "extra", "narrador"]
generos_posibles = ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Aventura", "Fantasía"]

def generar_datos():
    cql_statements = []
    
    # Declarar el keyspace inicial
    cql_statements.append("USE actors;\n")
    
    # Generar 25 actores (cumpliendo el mínimo de 20 solicitado)
    for _ in range(25):
        actor_id = uuid.uuid4()
        nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
        nacionalidad = random.choice(nacionalidades)
        
        # Calcular fecha de nacimiento y edad (entre 18 y 65 años)
        dias_aleatorios = random.randint(18 * 365, 65 * 365)
        fecha_nac = date.today() - timedelta(days=dias_aleatorios)
        edad = (date.today() - fecha_nac).days // 365
        fecha_nac_str = fecha_nac.strftime('%Y-%m-%d')
        
        patrimonio = random.randint(50000, 5000000)
        
        # Crear colección de idiomas con formato CQL: {'idioma1', 'idioma2'}
        idiomas = random.sample(idiomas_posibles, random.randint(1, 3))
        idiomas_cql = "{" + ", ".join([f"'{i}'" for i in idiomas]) + "}"
        
        # 1. Inserción en tabla principal: actors_by_id
        cql_statements.append(
            f"INSERT INTO actors_by_id (id, nombre, nacionalidad, fecha_nacimiento, edad, patrimonio, idiomas) "
            f"VALUES ({actor_id}, '{nombre}', '{nacionalidad}', '{fecha_nac_str}', {edad}, {patrimonio}, {idiomas_cql});"
        )
        
        # 2. Inserción desnormalizada: actors_by_nationality
        cql_statements.append(
            f"INSERT INTO actors_by_nationality (nacionalidad, edad, id, nombre, patrimonio, idiomas) "
            f"VALUES ('{nacionalidad}', {edad}, {actor_id}, '{nombre}', {patrimonio}, {idiomas_cql});"
        )
        
        # 3. Generar entre 1 y 4 personajes para este actor
        num_personajes = random.randint(1, 4)
        for i in range(num_personajes):
            personaje_nombre = f"Personaje_{random.randint(1, 1000)}"
            produccion = random.choice(producciones)
            tipo_prod = random.choice(tipos_produccion)
            rol = random.choice(roles)
            apariciones = random.randint(1, 200)
            
            # Crear colección de géneros con formato CQL
            generos = random.sample(generos_posibles, random.randint(1, 3))
            generos_cql = "{" + ", ".join([f"'{g}'" for g in generos]) + "}"
            
            # Inserción en tabla de personajes: characters_by_actor
            cql_statements.append(
                f"INSERT INTO characters_by_actor (actor_id, rol, apariciones, personaje_nombre, produccion, tipo_produccion, generos) "
                f"VALUES ({actor_id}, '{rol}', {apariciones}, '{personaje_nombre}', '{produccion}', '{tipo_prod}', {generos_cql});"
            )

    return cql_statements

if __name__ == "__main__":
    consultas = generar_datos()
    
    # Escribir todas las sentencias en el archivo datos.cql
    with open("datos.cql", "w", encoding="utf-8") as f:
        for consulta in consultas:
            f.write(consulta + "\n")
            
    print("Archivo 'datos.cql' generado con éxito. Listo para cargar en Cassandra.")