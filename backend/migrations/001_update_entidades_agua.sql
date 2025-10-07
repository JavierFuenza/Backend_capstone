-- Migración: Actualizar tabla entidades_agua
-- Fecha: 2025-10-07
-- Descripción: Cambiar columna 'subtipo' a 'tipo' y actualizar VARCHAR(50) a VARCHAR(100)

-- 1. Eliminar la restricción única existente
ALTER TABLE entidades_agua DROP CONSTRAINT IF EXISTS uq_nombre_subtipo;

-- 2. Renombrar la columna subtipo a tipo
ALTER TABLE entidades_agua RENAME COLUMN subtipo TO tipo;

-- 3. Modificar el tipo de dato de VARCHAR(50) a VARCHAR(100)
ALTER TABLE entidades_agua ALTER COLUMN tipo TYPE VARCHAR(100);

-- 4. Crear la nueva restricción única con los nombres correctos
ALTER TABLE entidades_agua ADD CONSTRAINT uq_nombre_tipo UNIQUE (nombre, tipo);

-- Verificar la estructura de la tabla
-- SELECT column_name, data_type, character_maximum_length, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'entidades_agua';
