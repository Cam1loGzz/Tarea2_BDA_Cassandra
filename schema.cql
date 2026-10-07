-- 1. Crear el keyspace y usarlo
CREATE KEYSPACE IF NOT EXISTS actors
WITH replication = {
  'class': 'NetworkTopologyStrategy', 
  'datacenter1': 3
};

USE actors;

-- 2. Tabla para buscar por identificador
CREATE TABLE IF NOT EXISTS actors_by_id (
    id uuid PRIMARY KEY,
    nombre text,
    nacionalidad text,
    fecha_nacimiento date,
    edad int,
    patrimonio bigint,
    idiomas set<text>
);

-- 3. Tabla para buscar por nacionalidad ordenado por edad
CREATE TABLE IF NOT EXISTS actors_by_nationality (
    nacionalidad text,
    edad int,
    id uuid,
    nombre text,
    patrimonio bigint,
    idiomas set<text>,
    PRIMARY KEY ((nacionalidad), edad, id)
) WITH CLUSTERING ORDER BY (edad ASC, id ASC);

-- 4. Tabla para buscar personajes de un actor
CREATE TABLE IF NOT EXISTS characters_by_actor (
    actor_id uuid,
    rol text,
    apariciones int,
    personaje_nombre text,
    produccion text,
    tipo_produccion text,
    generos set<text>,
    PRIMARY KEY ((actor_id), rol, apariciones, personaje_nombre)
) WITH CLUSTERING ORDER BY (rol ASC, apariciones DESC, personaje_nombre ASC);