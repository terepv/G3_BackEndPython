"""Initial migration

Revision ID: 23133f86f05c
Revises: 
Create Date: 2025-04-19 04:27:16

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '23133f86f05c'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('''
CREATE TABLE public.comuna (
    id_comuna integer NOT NULL,
    comuna character varying NOT NULL,
    id_region integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.frecuencia (
    id_frecuencia integer NOT NULL,
    frecuencia character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.medida (
    id_medida integer NOT NULL,
    id_tipo_medida integer NOT NULL,
    nombre_corto character varying NOT NULL,
    indicador character varying NOT NULL,
    formula_calculo character varying NOT NULL,
    id_frecuencia integer NOT NULL,
    id_organismo_sectorial integer NOT NULL,
    id_plan integer NOT NULL,
    desc_medio_de_verificacion character varying NOT NULL,
    id_tipo_dato integer NOT NULL,
    reporte_unico boolean DEFAULT false NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.medio_verificacion (
    nombre_archivo character varying NOT NULL,
    fecha_subida timestamp with time zone DEFAULT now() NOT NULL,
    archivo bytea NOT NULL,
    tamano bigint NOT NULL,
    id_reporte integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.opcion (
    id_opcion integer NOT NULL,
    opcion character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.opcion_medida (
    id_opcion_medida integer NOT NULL,
    id_medida integer NOT NULL,
    id_opcion integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.organismo_sectorial (
    id_organismo_sectorial integer NOT NULL,
    organismo_sectorial character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.plan (
    id_plan integer NOT NULL,
    nombre character varying NOT NULL,
    descripcion character varying NOT NULL,
    fecha_publicacion date DEFAULT now() NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.plan_comuna (
    id_plan_comuna integer NOT NULL,
    id_plan integer NOT NULL,
    id_comuna integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.region (
    id_region integer NOT NULL,
    region character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.reporte (
    id_reporte integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying,
    id_organismo_sectorial integer NOT NULL,
    id_plan integer NOT NULL
);
''')
    op.execute('''
CREATE TABLE public.reporte_medida (
    id_reporte_medida integer NOT NULL,
    id_reporte integer NOT NULL,
    id_medida integer NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.resultado (
    id_reporte_medida integer NOT NULL,
    texto character varying,
    numerico real,
    si_no boolean,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying,
    id_opcion integer,
    id_resultado integer NOT NULL
);
''')
    op.execute('''
CREATE TABLE public.rol (
    id_rol integer NOT NULL,
    rol character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.tipo_dato (
    id_tipo_dato integer NOT NULL,
    tipo_dato character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.tipo_medida (
    id_tipo_medida integer NOT NULL,
    tipo_medida character varying NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    nombre character varying NOT NULL,
    apellido character varying NOT NULL,
    email character varying NOT NULL,
    activo boolean DEFAULT true NOT NULL,
    id_rol integer NOT NULL,
    password character varying NOT NULL,
    id_organismo_sectorial integer,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);
''')
    op.execute('''
CREATE FUNCTION public.evitar_editar_eliminados() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  RAISE EXCEPTION 'La acción no está permitida.';
END;
$$;
''')
    op.execute('''
CREATE FUNCTION public.validar_usuarios_auditoria() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF NEW.creado_por IS NULL THEN
		RAISE EXCEPTION 'El campo creado_por no puede ser NULL';
	END IF;

	IF NEW.actualizado_por IS NULL AND NOT EXISTS (
		SELECT 1 FROM public.usuario
		WHERE email = NEW.creado_por
			AND activo = true
	) THEN
		RAISE EXCEPTION 'El campo creado_por (%) no existe o no está activo', NEW.created_by;
	END IF;
	
	IF NEW.actualizado_por IS NOT NULL AND NEW.eliminado_por IS NULL THEN
		IF NOT EXISTS (
			SELECT 1 FROM public.usuario
			WHERE email = NEW.actualizado_por 
				AND activo = true
		) THEN
			RAISE EXCEPTION 'El campo actualizado_por (%) no existe o no está activo', NEW.actualizado_por;
		END IF;
	END IF;
	
	IF NEW.eliminado_por IS NOT NULL THEN
		IF NOT EXISTS (
			SELECT 1 FROM public.usuario
			WHERE email = NEW.eliminado_por AND activo = true
		) THEN
			RAISE EXCEPTION 'El campo eliminado_por (%) no existe o no está activo', NEW.eliminado_por;
		END IF;
	END IF;

	RETURN NEW;
END;
$$;
''')
    op.execute('''
CREATE FUNCTION public.validate_opcion_medida() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM medida m
        JOIN tipo_dato td ON m.id_tipo_dato = td.id_tipo_dato
        WHERE m.id_medida = NEW.id_medida
          AND td.tipo_dato != 'Selección'
    ) THEN
        -- Lanzar un error si no cumple la condición
        RAISE EXCEPTION 'Solo se pueden registrar opciones para medidas con tipo de dato "Selección".';
    END IF;

    -- Si pasa la validación, permitir la inserción
    RETURN NEW;
END;
$$;
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.frecuencia FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medio_verificacion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.organismo_sectorial FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan_comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.region FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.reporte FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.reporte_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.resultado FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.rol FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_dato FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();
''')
    op.execute('''
CREATE TRIGGER trg_validate_opcion_medida BEFORE INSERT ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validate_opcion_medida();
''')


def downgrade() -> None:
    pass
