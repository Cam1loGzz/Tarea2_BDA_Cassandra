import subprocess
import json

def ejecutar_cql(query):
    cmd = ["docker", "exec", "-i", "cassandra1", "cqlsh", "-e", f"USE actors; {query}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return res.stdout

def main():
    print("Obteniendo actores actuales desde Cassandra...")
    salida_json = ejecutar_cql("SELECT json id, nombre, nacionalidad, edad, patrimonio FROM actors_by_id;")
    
    lineas = salida_json.strip().split("\n")
    actores = []
    for l in lineas:
        l = l.strip()
        if l.startswith('{"'):
            actores.append(json.loads(l))

    print(f"Procesando {len(actores)} actores...")
    sentencias_cql = ["USE actors;"]

    for actor in actores:
        actor_id = actor["id"]
        nacionalidad = actor["nacionalidad"]
        edad = int(actor["edad"])
        patrimonio_actual = int(actor["patrimonio"])
        nuevo_patrimonio = int(round(patrimonio_actual * 1.32))
        
        # Actualizacion en actors_by_id
        sentencias_cql.append(
            f"UPDATE actors_by_id SET patrimonio = {nuevo_patrimonio} WHERE id = {actor_id};"
        )
        
        # Actualizacion en actors_by_nationality
        sentencias_cql.append(
            f"UPDATE actors_by_nationality SET patrimonio = {nuevo_patrimonio} "
            f"WHERE nacionalidad = '{nacionalidad}' AND edad = {edad} AND id = {actor_id};"
        )

        if edad < 40:
            rol = "principal"
            apariciones = 3
        else:
            rol = "secundario"
            apariciones = 1
            
        nombre_personaje = "Corredor"
        produccion = "Sansa Ball Race"
        tipo_prod = "profesional"
        generos = "{'Animacion', 'Carreras'}"

        # Nueva particion
        sentencias_cql.append(
            f"INSERT INTO characters_by_actor (actor_id, rol, apariciones, personaje_nombre, produccion, tipo_produccion, generos) "
            f"VALUES ({actor_id}, '{rol}', {apariciones}, '{nombre_personaje}', '{produccion}', '{tipo_prod}', {generos});"
        )

    with open("actualizacion.cql", "w", encoding="utf-8") as f:
        f.write("\n".join(sentencias_cql) + "\n")
        
    print("Archivo 'actualizacion.cql' generado exitosamente.")
    print("Aplicando actualizaciones al clúster de Cassandra...")
    
    # Aplicar todas las sentencias en Cassandra
    cmd_apply = ["docker", "exec", "-i", "cassandra1", "cqlsh"]
    with open("actualizacion.cql", "r", encoding="utf-8") as f:
        subprocess.run(cmd_apply, stdin=f, check=True)
        
    print("Actualizacion completada")

if __name__ == "__main__":
    main()