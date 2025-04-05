--
-- PostgreSQL database cluster dump
--

-- Started on 2025-04-05 20:06:56

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-05 20:06:56

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-04-05 20:06:56

--
-- PostgreSQL database dump complete
--

--
-- Database "PPDA" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-05 20:06:56

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5120 (class 1262 OID 16388)
-- Name: PPDA; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "PPDA" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es-MX';


ALTER DATABASE "PPDA" OWNER TO postgres;

\connect "PPDA"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 261 (class 1255 OID 17052)
-- Name: evitar_editar_eliminados(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.evitar_editar_eliminados() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  RAISE EXCEPTION 'La acción no está permitida.';
END;
$$;


ALTER FUNCTION public.evitar_editar_eliminados() OWNER TO postgres;

--
-- TOC entry 262 (class 1255 OID 16989)
-- Name: validar_usuarios_auditoria(); Type: FUNCTION; Schema: public; Owner: postgres
--

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


ALTER FUNCTION public.validar_usuarios_auditoria() OWNER TO postgres;

--
-- TOC entry 249 (class 1255 OID 16684)
-- Name: validate_opcion_medida(); Type: FUNCTION; Schema: public; Owner: postgres
--

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


ALTER FUNCTION public.validate_opcion_medida() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16685)
-- Name: comuna; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.comuna OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16690)
-- Name: comuna_id_comuna_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.comuna ALTER COLUMN id_comuna ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.comuna_id_comuna_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16691)
-- Name: frecuencia; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.frecuencia OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16696)
-- Name: frecuencia_id_frecuencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.frecuencia ALTER COLUMN id_frecuencia ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.frecuencia_id_frecuencia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 16697)
-- Name: medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.medida OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16703)
-- Name: medida_id_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.medida ALTER COLUMN id_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.medida_id_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 223 (class 1259 OID 16704)
-- Name: medio_verificacion; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.medio_verificacion OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16716)
-- Name: opcion; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.opcion OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16721)
-- Name: opcion_id_opcion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.opcion ALTER COLUMN id_opcion ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.opcion_id_opcion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 226 (class 1259 OID 16722)
-- Name: opcion_medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.opcion_medida OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16725)
-- Name: opciones_medida_id_opcion_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.opcion_medida ALTER COLUMN id_opcion_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.opciones_medida_id_opcion_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 228 (class 1259 OID 16726)
-- Name: organismo_sectorial; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.organismo_sectorial OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16731)
-- Name: organismo_sectorial_id_organismo_sectorial_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.organismo_sectorial ALTER COLUMN id_organismo_sectorial ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.organismo_sectorial_id_organismo_sectorial_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 16736)
-- Name: plan; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.plan OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16742)
-- Name: plan_comuna; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.plan_comuna OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16745)
-- Name: plan_comuna_id_plan_comuna_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.plan_comuna ALTER COLUMN id_plan_comuna ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.plan_comuna_id_plan_comuna_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 233 (class 1259 OID 16746)
-- Name: plan_id_plan_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.plan ALTER COLUMN id_plan ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.plan_id_plan_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 234 (class 1259 OID 16747)
-- Name: region; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.region OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16752)
-- Name: region_id_region_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.region ALTER COLUMN id_region ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.region_id_region_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 236 (class 1259 OID 16753)
-- Name: reporte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reporte (
    id_reporte integer NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);


ALTER TABLE public.reporte OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16757)
-- Name: reporte_id_reporte_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.reporte ALTER COLUMN id_reporte ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.reporte_id_reporte_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 248 (class 1259 OID 17054)
-- Name: reporte_medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.reporte_medida OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 17053)
-- Name: reporte_medida_id_reporte_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.reporte_medida ALTER COLUMN id_reporte_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.reporte_medida_id_reporte_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 238 (class 1259 OID 16758)
-- Name: resultado; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resultado (
    id_reporte_medida integer NOT NULL,
    texto character varying,
    numerico real,
    si_no boolean,
    seleccion character varying,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying,
    CONSTRAINT resultado_chk_al_menos_un_campo_no_nulo CHECK (((texto IS NOT NULL) OR (numerico IS NOT NULL) OR (si_no IS NOT NULL) OR (seleccion IS NOT NULL)))
);


ALTER TABLE public.resultado OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 16782)
-- Name: rol; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.rol OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16770)
-- Name: tipo_dato; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.tipo_dato OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 16775)
-- Name: tipo_dato_medida_id_tipo_dato_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tipo_dato ALTER COLUMN id_tipo_dato ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipo_dato_medida_id_tipo_dato_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 241 (class 1259 OID 16776)
-- Name: tipo_medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.tipo_medida OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 16781)
-- Name: tipo_medida_id_tipo_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tipo_medida ALTER COLUMN id_tipo_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipo_medida_id_tipo_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 244 (class 1259 OID 16787)
-- Name: tipo_usuario_id_tipo_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.rol ALTER COLUMN id_rol ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipo_usuario_id_tipo_usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 245 (class 1259 OID 16788)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 16794)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario ALTER COLUMN id_usuario ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuario_id_usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 5083 (class 0 OID 16685)
-- Dependencies: 217
-- Data for Name: comuna; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comuna (id_comuna, comuna, id_region, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Arica	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
2	Camarones	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
3	Putre	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
4	General Lagos	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
5	Iquique	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
6	Alto Hospicio	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
7	Pozo Almonte	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
8	Camiña	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
9	Colchane	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
10	Huara	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
11	Pica	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
12	Antofagasta	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
13	Mejillones	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
14	Sierra Gorda	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
15	Taltal	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
16	Calama	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
17	Ollagüe	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
18	San Pedro de Atacama	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
19	Tocopilla	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
20	María Elena	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
21	Copiapó	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
22	Caldera	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
23	Tierra Amarilla	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
24	Chañaral	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
25	Diego de Almagro	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
26	Vallenar	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
27	Alto del Carmen	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
28	Freirina	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
29	Huasco	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
30	La Serena	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
31	Coquimbo	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
32	Andacollo	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
33	La Higuera	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
34	Paihuano	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
35	Vicuña	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
36	Illapel	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
37	Canela	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
38	Los Vilos	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
39	Salamanca	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
40	Ovalle	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
41	Combarbalá	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
42	Monte Patria	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
43	Punitaqui	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
44	Río Hurtado	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
303	Concepción	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
304	Hualpén	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
305	Talcahuano	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
306	Penco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
307	Chiguayante	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
308	San Pedro de la Paz	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
309	Coronel	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
310	Lota	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
311	Arauco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
312	Curanilahue	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
313	Los Álamos	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
314	Lebu	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
315	Tirúa	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
316	Cabrero	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
317	Laja	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
318	Mulchén	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
319	Nacimiento	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
320	Negrete	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
321	San Rosendo	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
322	Santa Juana	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
323	Yumbel	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
324	Antuco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
325	Alto Biobío	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
326	Quilleco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
327	Quilaco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
328	Santa Bárbara	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
329	Cañete	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
330	Contulmo	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
331	Hualqui	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
332	Temuco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
333	Carahue	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
334	Cunco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
335	Curarrehue	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
336	Freire	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
337	Galvarino	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
338	Gorbea	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
339	Loncoche	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
340	Melipeuco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
341	Nueva Imperial	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
84	Valparaíso	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
85	Viña del Mar	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
86	Concón	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
87	Quintero	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
88	Puchuncaví	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
89	Juan Fernández	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
90	Casablanca	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
91	El Quisco	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
92	El Tabo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
93	San Antonio	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
94	Algarrobo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
95	Cartagena	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
96	Santo Domingo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
97	San Sebastián	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
98	Los Andes	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
99	Calle Larga	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
100	Rinconada	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
101	San Esteban	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
102	Llay Llay	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
103	Villa Alemana	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
104	Olmué	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
105	Limache	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
106	Quilpué	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
107	La Calera	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
108	La Cruz	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
109	Nogales	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
110	San Felipe	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
111	Catemu	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
112	Panquehue	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
113	Putaendo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
342	Padre Las Casas	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
343	Perquenco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
344	Pitrufquén	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
345	Pucón	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
346	Saavedra	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
347	Villarrica	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
348	Victoria	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
349	Angol	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
350	Collipulli	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
351	Curacautín	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
352	Ercilla	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
353	Lonquimay	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
354	Los Sauces	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
355	Lumaco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
231	Talca	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
232	Constitución	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
233	Curepto	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
234	Empedrado	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
235	Maule	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
236	Pelarco	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
237	Pencahue	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
238	San Clemente	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
239	San Rafael	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
240	Teno	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
241	Cauquenes	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
242	Chanco	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
243	Pelluhue	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
244	Curicó	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
245	Hualañé	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
246	Molina	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
145	Rancagua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
146	Codegua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
147	Coinco	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
148	Coltauco	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
149	Doñihue	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
150	Graneros	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
151	Las Cabras	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
152	Machalí	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
153	Malloa	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
154	Mostazal	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
155	Olivar	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
156	Peumo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
157	Pichidegua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
158	Quinta de Tilcoco	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
159	Rengo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
160	Requínoa	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
161	San Vicente de Tagua Tagua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
162	Pichilemu	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
247	Rauco	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
248	Sagrada Familia	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
249	Villa Alegre	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
250	Yerbas Buenas	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
163	La Estrella	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
164	Litueche	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
165	Marchigüe	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
166	Navidad	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
167	Peralillo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
168	Pumanque	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
169	San Fernando	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
170	Chépica	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
171	Chimbarongo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
172	Lolol	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
173	Nancagua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
174	Palmilla	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
175	Placilla	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
176	Santa Cruz	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
251	Linares	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
252	Colbún	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
253	Longaví	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
254	Parral	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
255	Retiro	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
256	San Javier	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
257	Chillán	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
258	Chillán Viejo	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
259	Bulnes	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
260	Cobquecura	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
261	Coihueco	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
262	El Carmen	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
263	Ninhue	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
264	Pemuco	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
265	Pinto	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
266	Quillón	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
267	Quirihue	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
268	Ránquil	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
269	San Carlos	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
270	San Fabián	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
271	San Ignacio	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
272	Yungay	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
356	Renaico	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
357	Traiguén	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
363	Valdivia	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
364	Corral	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
365	Lanco	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
366	Los Lagos	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
367	Máfil	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
368	Mariquina	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
369	Paillaco	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
370	Panguipulli	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
371	Futrono	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
372	La Unión	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
373	Río Bueno	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
374	San José de la Mariquina	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
375	Puerto Montt	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
376	Puerto Varas	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
377	Calbuco	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
378	Cochamó	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
379	Fresia	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
380	Frutillar	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
381	Los Muermos	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
382	Maullín	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
383	Osorno	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
384	Puyehue	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
385	Purranque	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
386	Río Negro	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
387	San Juan de la Costa	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
388	San Pablo	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
389	Ancud	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
390	Castro	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
391	Chonchi	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
392	Curaco de Vélez	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
393	Dalcahue	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
394	Puqueldón	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
395	Queilén	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
396	Quellón	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
397	Quinchao	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
398	Coyhaique	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
399	Lago Verde	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
400	Aisén	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
401	Cisnes	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
402	Guaitecas	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
403	Cochrane	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
404	O’Higgins	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
405	Tortel	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
406	Chile Chico	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
407	Río Ibáñez	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
408	Punta Arenas	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
409	Puerto Natales	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
410	Porvenir	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
411	Puerto Williams	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
412	Timaukel	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
413	Natales	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
414	Torres del Paine	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
415	Río Verde	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
416	Laguna Blanca	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
417	San Gregorio	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
418	Estancia Río de los Ciervos	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
419	Santiago	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
420	Cerrillos	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
421	Cerro Navia	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
422	Conchalí	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
423	El Bosque	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
424	Estación Central	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
425	Huechuraba	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
426	Independencia	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
427	La Cisterna	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
428	La Florida	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
429	La Granja	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
430	La Pintana	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
431	Las Condes	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
432	Lo Barnechea	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
433	Lo Espejo	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
434	Lo Prado	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
435	Macul	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
436	Maipú	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
437	Ñuñoa	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
438	Pedro Aguirre Cerda	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
439	Peñalolén	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
440	Providencia	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
441	Pudahuel	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
442	Quilicura	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
443	Quinta Normal	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
444	Recoleta	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
445	Renca	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
446	San Bernardo	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
447	San Joaquín	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
448	San Miguel	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
449	San Ramón	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
450	Vitacura	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
451	Puente Alto	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
452	Pirque	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
453	Colina	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
454	Lampa	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
455	Buin	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
456	Paine	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
457	Melipilla	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
458	Alhué	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
459	Curacaví	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
460	María Pinto	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
461	San José de Maipo	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
462	nombre comuna	1	2025-04-05 18:48:40.543049	hpinilla@gmail.com	2025-04-05 19:16:38.401578	hpinilla@gmail.com	2025-04-05 19:26:56.843556	hpinilla@gmail.com
\.


--
-- TOC entry 5085 (class 0 OID 16691)
-- Dependencies: 219
-- Data for Name: frecuencia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.frecuencia (id_frecuencia, frecuencia, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Anual	2025-04-04 21:44:11.44453	hpinilla@gmail.com	\N	\N	\N	\N
2	Única	2025-04-04 21:44:11.44453	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5087 (class 0 OID 16697)
-- Dependencies: 221
-- Data for Name: medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medida (id_medida, id_tipo_medida, nombre_corto, indicador, formula_calculo, id_frecuencia, id_organismo_sectorial, id_plan, desc_medio_de_verificacion, id_tipo_dato, reporte_unico, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	1	RCA que contenga obligación de compensar emisiones	Número de RCA aprobadas en el año t que contengan obligaciones de compensar emisiones atmosféricas	Suma del número de RCA aprobadas que contengan obligación de compensar emisiones atmosféricas	1	1	1	Registro de las RCA aprobadas identificando el titular, la RCA, las emisiones y el monto a compensar	1	f	2025-04-04 21:48:45.197036	hpinilla@gmail.com	\N	\N	\N	\N
2	1	Condiciones del sistema de recuperación y/o eliminación de vapores de estanques Deposito techo fijo	Cumplimiento de las condiciones indicadas en el literal A para depósitos de techo fijo y Cronograma de implementación gradual calificado por la SEC cuando corresponda	([N° de tanques del artículo 33 literal A) al cual se han implementado las medidas comprometidas en el año t]/[N° de tanques del artículo 33 literal A) programadas para el año t])*100	1	2	1	a) Informe de Avance de Implementación de las medidas del Artículo 33 del Plan. b) En caso de solicitar más plazo, Oficio de envío de la Resolución que califica el Cronograma de implementación gradual para el plazo de cumplimiento	1	f	2025-04-04 21:48:45.197036	hpinilla@gmail.com	\N	\N	\N	\N
3	1	Requisitos del sistema de almacenamiento intermedio	Instrucciones de SEC, para cumplir con el sistema de almacenamiento intermedio u otro con el mismo objetivo, conforme al artículo 5 del DS N°160/2008.	Si/No	2	2	1	Oficialización de la Instrucción de SEC para cumplir con el sistema indicado en el artículo 33 del Plan.	4	f	2025-04-04 21:48:45.197036	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5089 (class 0 OID 16704)
-- Dependencies: 223
-- Data for Name: medio_verificacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medio_verificacion (nombre_archivo, fecha_subida, archivo, tamano, id_reporte, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
\.


--
-- TOC entry 5090 (class 0 OID 16716)
-- Dependencies: 224
-- Data for Name: opcion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opcion (id_opcion, opcion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
4	Si	2025-04-04 21:51:39.379777	hpinilla@gmail.com	\N	\N	\N	\N
5	No	2025-04-04 21:51:39.379777	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5092 (class 0 OID 16722)
-- Dependencies: 226
-- Data for Name: opcion_medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opcion_medida (id_opcion_medida, id_medida, id_opcion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
4	3	4	2025-04-04 21:50:52.837067	hpinilla@gmail.com	\N	\N	\N	\N
5	3	5	2025-04-04 21:50:52.837067	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5094 (class 0 OID 16726)
-- Dependencies: 228
-- Data for Name: organismo_sectorial; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organismo_sectorial (id_organismo_sectorial, organismo_sectorial, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Servicio de Evaluación Ambiental	2025-04-04 21:45:19.649923	hpinilla@gmail.com	\N	\N	\N	\N
2	Superintendencia de Electricidad y Combustibles	2025-04-04 21:45:19.649923	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5096 (class 0 OID 16736)
-- Dependencies: 230
-- Data for Name: plan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plan (id_plan, nombre, descripcion, fecha_publicacion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	PPDA CQP	Plan de Prevención y Descontaminación Atmosférica para las comunas de Concón, Quintero y Puchuncaví	2025-01-24	2025-04-04 21:38:50.504328	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5097 (class 0 OID 16742)
-- Dependencies: 231
-- Data for Name: plan_comuna; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plan_comuna (id_plan_comuna, id_plan, id_comuna, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	1	86	2025-04-04 21:36:58.170734	hpinilla@gmail.com	\N	\N	\N	\N
2	1	87	2025-04-04 21:36:58.170734	hpinilla@gmail.com	\N	\N	\N	\N
3	1	88	2025-04-04 21:36:58.170734	hpinilla@gmail.com	\N	\N	\N	\N
12	1	1	2025-04-05 11:01:28.322013	hpinilla@gmail.com	\N	\N	2025-04-05 11:07:01.961695	hpinilla@gmail.com
\.


--
-- TOC entry 5100 (class 0 OID 16747)
-- Dependencies: 234
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.region (id_region, region, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Región de Arica y Parinacota	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
2	Región de Tarapacá	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
3	Región de Antofagasta	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
4	Región de Atacama	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
5	Región de Coquimbo	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
6	Región de Valparaíso	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
7	Región del Libertador General Bernardo O’Higgins	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
8	Región del Maule	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
9	Región de Ñuble	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
10	Región del Biobío	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
11	Región de La Araucanía	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
12	Región de Los Ríos	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
13	Región de Los Lagos	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
14	Región de Aysén del General Carlos Ibáñez del Campo	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
15	Región de Magallanes y de la Antártica Chilena	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
16	Región Metropolitana de Santiago	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5102 (class 0 OID 16753)
-- Dependencies: 236
-- Data for Name: reporte; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reporte (id_reporte, fecha_registro, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
2	2025-03-23 01:27:21.256095	2025-04-04 21:57:31.809002	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5114 (class 0 OID 17054)
-- Dependencies: 248
-- Data for Name: reporte_medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reporte_medida (id_reporte_medida, id_reporte, id_medida, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
\.


--
-- TOC entry 5104 (class 0 OID 16758)
-- Dependencies: 238
-- Data for Name: resultado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resultado (id_reporte_medida, texto, numerico, si_no, seleccion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
\.


--
-- TOC entry 5109 (class 0 OID 16782)
-- Dependencies: 243
-- Data for Name: rol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rol (id_rol, rol, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
2	Fiscalizador	2025-04-04 22:31:14.939052	hpinilla@gmail.com	\N	\N	\N	\N
1	Administrador	2025-04-04 22:31:14.939052	hpinilla@gmail.com	\N	\N	\N	\N
3	Organismo Sectorial	2025-04-04 22:31:14.939052	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5105 (class 0 OID 16770)
-- Dependencies: 239
-- Data for Name: tipo_dato; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipo_dato (id_tipo_dato, tipo_dato, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
2	Texto	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
3	Si/No	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
1	Numérico	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
4	Selección	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5107 (class 0 OID 16776)
-- Dependencies: 241
-- Data for Name: tipo_medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipo_medida (id_tipo_medida, tipo_medida, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Medida Regulatoria	2025-04-04 21:47:01.37056	hpinilla@gmail.com	\N	\N	\N	\N
3	Medidas No Regulatorias	2025-04-04 21:47:01.37056	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5111 (class 0 OID 16788)
-- Dependencies: 245
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, nombre, apellido, email, activo, id_rol, password, id_organismo_sectorial, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Hamid	Pinilla	hpinilla@gmail.com	t	1	$2b$12$1OJJ5ybGfWXgzYVaHQUrT.tLxj6LeOOpTdnNfxTbT7C7MpQc2Bqci	\N	2025-04-05 09:22:17.575321	hpinilla@gmail.com	\N	\N	\N	\N
7	Jorge	Bernal	jbernal@gmail.com	t	2	$2b$12$EwSlmFayPCrPTVXXeNM/kuNKYb6CGT5irZP75ZpQNNTcwRJNfSmdq	\N	2025-04-05 09:22:17.575321	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5122 (class 0 OID 0)
-- Dependencies: 218
-- Name: comuna_id_comuna_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comuna_id_comuna_seq', 462, true);


--
-- TOC entry 5123 (class 0 OID 0)
-- Dependencies: 220
-- Name: frecuencia_id_frecuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.frecuencia_id_frecuencia_seq', 7, true);


--
-- TOC entry 5124 (class 0 OID 0)
-- Dependencies: 222
-- Name: medida_id_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medida_id_medida_seq', 11, true);


--
-- TOC entry 5125 (class 0 OID 0)
-- Dependencies: 225
-- Name: opcion_id_opcion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opcion_id_opcion_seq', 5, true);


--
-- TOC entry 5126 (class 0 OID 0)
-- Dependencies: 227
-- Name: opciones_medida_id_opcion_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opciones_medida_id_opcion_medida_seq', 5, true);


--
-- TOC entry 5127 (class 0 OID 0)
-- Dependencies: 229
-- Name: organismo_sectorial_id_organismo_sectorial_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organismo_sectorial_id_organismo_sectorial_seq', 7, true);


--
-- TOC entry 5128 (class 0 OID 0)
-- Dependencies: 232
-- Name: plan_comuna_id_plan_comuna_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plan_comuna_id_plan_comuna_seq', 12, true);


--
-- TOC entry 5129 (class 0 OID 0)
-- Dependencies: 233
-- Name: plan_id_plan_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plan_id_plan_seq', 12, true);


--
-- TOC entry 5130 (class 0 OID 0)
-- Dependencies: 235
-- Name: region_id_region_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.region_id_region_seq', 16, true);


--
-- TOC entry 5131 (class 0 OID 0)
-- Dependencies: 237
-- Name: reporte_id_reporte_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reporte_id_reporte_seq', 3, true);


--
-- TOC entry 5132 (class 0 OID 0)
-- Dependencies: 247
-- Name: reporte_medida_id_reporte_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reporte_medida_id_reporte_medida_seq', 1, false);


--
-- TOC entry 5133 (class 0 OID 0)
-- Dependencies: 240
-- Name: tipo_dato_medida_id_tipo_dato_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_dato_medida_id_tipo_dato_medida_seq', 4, true);


--
-- TOC entry 5134 (class 0 OID 0)
-- Dependencies: 242
-- Name: tipo_medida_id_tipo_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_medida_id_tipo_medida_seq', 4, true);


--
-- TOC entry 5135 (class 0 OID 0)
-- Dependencies: 244
-- Name: tipo_usuario_id_tipo_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_usuario_id_tipo_usuario_seq', 3, true);


--
-- TOC entry 5136 (class 0 OID 0)
-- Dependencies: 246
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 7, true);


--
-- TOC entry 4847 (class 2606 OID 16800)
-- Name: comuna comuna_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comuna
    ADD CONSTRAINT comuna_pk PRIMARY KEY (id_comuna);


--
-- TOC entry 4849 (class 2606 OID 16802)
-- Name: comuna comuna_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comuna
    ADD CONSTRAINT comuna_un UNIQUE (comuna);


--
-- TOC entry 4851 (class 2606 OID 16804)
-- Name: frecuencia frecuencia_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frecuencia
    ADD CONSTRAINT frecuencia_pk PRIMARY KEY (id_frecuencia);


--
-- TOC entry 4853 (class 2606 OID 16806)
-- Name: frecuencia frecuencia_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frecuencia
    ADD CONSTRAINT frecuencia_un UNIQUE (frecuencia);


--
-- TOC entry 4855 (class 2606 OID 16808)
-- Name: medida medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_pk PRIMARY KEY (id_medida);


--
-- TOC entry 4857 (class 2606 OID 16810)
-- Name: medio_verificacion medio_verificacion_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medio_verificacion
    ADD CONSTRAINT medio_verificacion_pk PRIMARY KEY (id_reporte);


--
-- TOC entry 4859 (class 2606 OID 16814)
-- Name: opcion opcion_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion
    ADD CONSTRAINT opcion_pk PRIMARY KEY (id_opcion);


--
-- TOC entry 4861 (class 2606 OID 16816)
-- Name: opcion opcion_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion
    ADD CONSTRAINT opcion_un UNIQUE (opcion);


--
-- TOC entry 4863 (class 2606 OID 16818)
-- Name: opcion_medida opciones_medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opciones_medida_pk PRIMARY KEY (id_opcion_medida);


--
-- TOC entry 4865 (class 2606 OID 16820)
-- Name: opcion_medida opciones_medida_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opciones_medida_un UNIQUE (id_medida, id_opcion);


--
-- TOC entry 4867 (class 2606 OID 16822)
-- Name: organismo_sectorial organismo_sectorial_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organismo_sectorial
    ADD CONSTRAINT organismo_sectorial_pk PRIMARY KEY (id_organismo_sectorial);


--
-- TOC entry 4869 (class 2606 OID 16824)
-- Name: organismo_sectorial organismo_sectorial_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organismo_sectorial
    ADD CONSTRAINT organismo_sectorial_un UNIQUE (organismo_sectorial);


--
-- TOC entry 4873 (class 2606 OID 16830)
-- Name: plan_comuna plan_comuna_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_pk PRIMARY KEY (id_plan_comuna);


--
-- TOC entry 4875 (class 2606 OID 17092)
-- Name: plan_comuna plan_comuna_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_unique UNIQUE (id_plan, id_comuna);


--
-- TOC entry 4871 (class 2606 OID 16832)
-- Name: plan plan_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT plan_pk PRIMARY KEY (id_plan);


--
-- TOC entry 4877 (class 2606 OID 16834)
-- Name: region region_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_pk PRIMARY KEY (id_region);


--
-- TOC entry 4879 (class 2606 OID 16836)
-- Name: region region_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_un UNIQUE (region);


--
-- TOC entry 4901 (class 2606 OID 17066)
-- Name: reporte_medida reporte_medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_pk PRIMARY KEY (id_reporte_medida);


--
-- TOC entry 4903 (class 2606 OID 17064)
-- Name: reporte_medida reporte_medida_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_unique UNIQUE (id_reporte, id_medida);


--
-- TOC entry 4881 (class 2606 OID 16838)
-- Name: reporte reporte_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pk PRIMARY KEY (id_reporte);


--
-- TOC entry 4883 (class 2606 OID 16840)
-- Name: resultado resultado_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resultado
    ADD CONSTRAINT resultado_pk PRIMARY KEY (id_reporte_medida);


--
-- TOC entry 4893 (class 2606 OID 16854)
-- Name: rol rol_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pk PRIMARY KEY (id_rol);


--
-- TOC entry 4895 (class 2606 OID 16856)
-- Name: rol rol_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_un UNIQUE (rol);


--
-- TOC entry 4885 (class 2606 OID 16846)
-- Name: tipo_dato tipo_dato_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_dato
    ADD CONSTRAINT tipo_dato_pk PRIMARY KEY (id_tipo_dato);


--
-- TOC entry 4887 (class 2606 OID 16848)
-- Name: tipo_dato tipo_dato_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_dato
    ADD CONSTRAINT tipo_dato_un UNIQUE (tipo_dato);


--
-- TOC entry 4889 (class 2606 OID 16850)
-- Name: tipo_medida tipo_medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_medida
    ADD CONSTRAINT tipo_medida_pk PRIMARY KEY (id_tipo_medida);


--
-- TOC entry 4891 (class 2606 OID 16852)
-- Name: tipo_medida tipo_medida_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_medida
    ADD CONSTRAINT tipo_medida_un UNIQUE (tipo_medida);


--
-- TOC entry 4897 (class 2606 OID 16858)
-- Name: usuario usuario_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pk PRIMARY KEY (id_usuario);


--
-- TOC entry 4899 (class 2606 OID 16864)
-- Name: usuario usuario_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_un UNIQUE (email);


--
-- TOC entry 4920 (class 2620 OID 16996)
-- Name: comuna trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4921 (class 2620 OID 17010)
-- Name: frecuencia trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.frecuencia FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4922 (class 2620 OID 17022)
-- Name: medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4923 (class 2620 OID 17046)
-- Name: medio_verificacion trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medio_verificacion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4924 (class 2620 OID 17036)
-- Name: opcion trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4925 (class 2620 OID 17032)
-- Name: opcion_medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4927 (class 2620 OID 17014)
-- Name: organismo_sectorial trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.organismo_sectorial FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4928 (class 2620 OID 17006)
-- Name: plan trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4929 (class 2620 OID 17002)
-- Name: plan_comuna trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan_comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4930 (class 2620 OID 16991)
-- Name: region trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.region FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4931 (class 2620 OID 17042)
-- Name: reporte trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.reporte FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4937 (class 2620 OID 17061)
-- Name: reporte_medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.reporte_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4932 (class 2620 OID 17050)
-- Name: resultado trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.resultado FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4935 (class 2620 OID 17086)
-- Name: rol trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.rol FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4933 (class 2620 OID 17026)
-- Name: tipo_dato trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_dato FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4934 (class 2620 OID 17018)
-- Name: tipo_medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4936 (class 2620 OID 17090)
-- Name: usuario trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4926 (class 2620 OID 16865)
-- Name: opcion_medida trg_validate_opcion_medida; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validate_opcion_medida BEFORE INSERT ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validate_opcion_medida();


--
-- TOC entry 4904 (class 2606 OID 16866)
-- Name: comuna comuna_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comuna
    ADD CONSTRAINT comuna_fk FOREIGN KEY (id_region) REFERENCES public.region(id_region);


--
-- TOC entry 4905 (class 2606 OID 16871)
-- Name: medida medida_fk_frecuencia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_frecuencia FOREIGN KEY (id_frecuencia) REFERENCES public.frecuencia(id_frecuencia);


--
-- TOC entry 4906 (class 2606 OID 16876)
-- Name: medida medida_fk_organismo_sectorial; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_organismo_sectorial FOREIGN KEY (id_organismo_sectorial) REFERENCES public.organismo_sectorial(id_organismo_sectorial);


--
-- TOC entry 4907 (class 2606 OID 16881)
-- Name: medida medida_fk_plan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_plan FOREIGN KEY (id_plan) REFERENCES public.plan(id_plan);


--
-- TOC entry 4908 (class 2606 OID 16886)
-- Name: medida medida_fk_tipo_dato; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_tipo_dato FOREIGN KEY (id_tipo_dato) REFERENCES public.tipo_dato(id_tipo_dato);


--
-- TOC entry 4909 (class 2606 OID 16891)
-- Name: medida medida_fk_tipo_medida; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_tipo_medida FOREIGN KEY (id_tipo_medida) REFERENCES public.tipo_medida(id_tipo_medida);


--
-- TOC entry 4910 (class 2606 OID 16896)
-- Name: medio_verificacion medio_verificacion_fk_reporte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medio_verificacion
    ADD CONSTRAINT medio_verificacion_fk_reporte FOREIGN KEY (id_reporte) REFERENCES public.reporte(id_reporte);


--
-- TOC entry 4911 (class 2606 OID 16906)
-- Name: opcion_medida opcion_medida_fk_medida; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opcion_medida_fk_medida FOREIGN KEY (id_medida) REFERENCES public.medida(id_medida);


--
-- TOC entry 4912 (class 2606 OID 16911)
-- Name: opcion_medida opcion_medida_fk_opcion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opcion_medida_fk_opcion FOREIGN KEY (id_opcion) REFERENCES public.opcion(id_opcion);


--
-- TOC entry 4913 (class 2606 OID 16926)
-- Name: plan_comuna plan_comuna_fk_comuna; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_fk_comuna FOREIGN KEY (id_comuna) REFERENCES public.comuna(id_comuna);


--
-- TOC entry 4914 (class 2606 OID 16931)
-- Name: plan_comuna plan_comuna_fk_plan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_fk_plan FOREIGN KEY (id_plan) REFERENCES public.plan(id_plan);


--
-- TOC entry 4918 (class 2606 OID 17079)
-- Name: reporte_medida reporte_medida_medida_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_medida_fk FOREIGN KEY (id_medida) REFERENCES public.medida(id_medida);


--
-- TOC entry 4919 (class 2606 OID 17074)
-- Name: reporte_medida reporte_medida_reporte_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_reporte_fk FOREIGN KEY (id_reporte) REFERENCES public.reporte(id_reporte);


--
-- TOC entry 4915 (class 2606 OID 17067)
-- Name: resultado resultado_reporte_medida_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resultado
    ADD CONSTRAINT resultado_reporte_medida_fk FOREIGN KEY (id_reporte_medida) REFERENCES public.reporte_medida(id_reporte_medida);


--
-- TOC entry 4916 (class 2606 OID 16961)
-- Name: usuario usuario_fk_rol; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_fk_rol FOREIGN KEY (id_rol) REFERENCES public.rol(id_rol);


--
-- TOC entry 4917 (class 2606 OID 16979)
-- Name: usuario usuario_organismo_sectorial_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_organismo_sectorial_fk FOREIGN KEY (id_organismo_sectorial) REFERENCES public.organismo_sectorial(id_organismo_sectorial);


--
-- TOC entry 5121 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


-- Completed on 2025-04-05 20:06:57

--
-- PostgreSQL database dump complete
--

--
-- Database "PPDA2" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-05 20:06:57

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5120 (class 1262 OID 17948)
-- Name: PPDA2; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "PPDA2" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es-MX';


ALTER DATABASE "PPDA2" OWNER TO postgres;

\connect "PPDA2"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 249 (class 1255 OID 17949)
-- Name: evitar_editar_eliminados(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.evitar_editar_eliminados() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  RAISE EXCEPTION 'La acción no está permitida.';
END;
$$;


ALTER FUNCTION public.evitar_editar_eliminados() OWNER TO postgres;

--
-- TOC entry 250 (class 1255 OID 17950)
-- Name: validar_usuarios_auditoria(); Type: FUNCTION; Schema: public; Owner: postgres
--

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


ALTER FUNCTION public.validar_usuarios_auditoria() OWNER TO postgres;

--
-- TOC entry 251 (class 1255 OID 17951)
-- Name: validate_opcion_medida(); Type: FUNCTION; Schema: public; Owner: postgres
--

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


ALTER FUNCTION public.validate_opcion_medida() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 17952)
-- Name: comuna; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.comuna OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17958)
-- Name: comuna_id_comuna_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.comuna ALTER COLUMN id_comuna ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.comuna_id_comuna_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 17959)
-- Name: frecuencia; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.frecuencia OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17965)
-- Name: frecuencia_id_frecuencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.frecuencia ALTER COLUMN id_frecuencia ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.frecuencia_id_frecuencia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 17966)
-- Name: medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.medida OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17973)
-- Name: medida_id_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.medida ALTER COLUMN id_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.medida_id_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 223 (class 1259 OID 17974)
-- Name: medio_verificacion; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.medio_verificacion OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 17981)
-- Name: opcion; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.opcion OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17987)
-- Name: opcion_id_opcion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.opcion ALTER COLUMN id_opcion ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.opcion_id_opcion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 226 (class 1259 OID 17988)
-- Name: opcion_medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.opcion_medida OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17994)
-- Name: opciones_medida_id_opcion_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.opcion_medida ALTER COLUMN id_opcion_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.opciones_medida_id_opcion_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 228 (class 1259 OID 17995)
-- Name: organismo_sectorial; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.organismo_sectorial OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 18001)
-- Name: organismo_sectorial_id_organismo_sectorial_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.organismo_sectorial ALTER COLUMN id_organismo_sectorial ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.organismo_sectorial_id_organismo_sectorial_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 18002)
-- Name: plan; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.plan OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 18009)
-- Name: plan_comuna; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.plan_comuna OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 18015)
-- Name: plan_comuna_id_plan_comuna_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.plan_comuna ALTER COLUMN id_plan_comuna ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.plan_comuna_id_plan_comuna_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 233 (class 1259 OID 18016)
-- Name: plan_id_plan_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.plan ALTER COLUMN id_plan ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.plan_id_plan_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 234 (class 1259 OID 18017)
-- Name: region; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.region OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 18023)
-- Name: region_id_region_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.region ALTER COLUMN id_region ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.region_id_region_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 236 (class 1259 OID 18024)
-- Name: reporte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reporte (
    id_reporte integer NOT NULL,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying
);


ALTER TABLE public.reporte OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 18031)
-- Name: reporte_id_reporte_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.reporte ALTER COLUMN id_reporte ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.reporte_id_reporte_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 238 (class 1259 OID 18032)
-- Name: reporte_medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.reporte_medida OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 18038)
-- Name: reporte_medida_id_reporte_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.reporte_medida ALTER COLUMN id_reporte_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.reporte_medida_id_reporte_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 240 (class 1259 OID 18039)
-- Name: resultado; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resultado (
    id_reporte_medida integer NOT NULL,
    texto character varying,
    numerico real,
    si_no boolean,
    seleccion character varying,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    creado_por character varying NOT NULL,
    fecha_actualizacion timestamp without time zone,
    actualizado_por character varying,
    fecha_eliminacion timestamp without time zone,
    eliminado_por character varying,
    CONSTRAINT resultado_chk_al_menos_un_campo_no_nulo CHECK (((texto IS NOT NULL) OR (numerico IS NOT NULL) OR (si_no IS NOT NULL) OR (seleccion IS NOT NULL)))
);


ALTER TABLE public.resultado OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 18046)
-- Name: rol; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.rol OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 18052)
-- Name: tipo_dato; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.tipo_dato OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 18058)
-- Name: tipo_dato_medida_id_tipo_dato_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tipo_dato ALTER COLUMN id_tipo_dato ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipo_dato_medida_id_tipo_dato_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 244 (class 1259 OID 18059)
-- Name: tipo_medida; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.tipo_medida OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 18065)
-- Name: tipo_medida_id_tipo_medida_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tipo_medida ALTER COLUMN id_tipo_medida ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipo_medida_id_tipo_medida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 246 (class 1259 OID 18066)
-- Name: tipo_usuario_id_tipo_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.rol ALTER COLUMN id_rol ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipo_usuario_id_tipo_usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 247 (class 1259 OID 18067)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 18074)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario ALTER COLUMN id_usuario ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuario_id_usuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 5083 (class 0 OID 17952)
-- Dependencies: 217
-- Data for Name: comuna; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comuna (id_comuna, comuna, id_region, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Arica	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
2	Camarones	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
3	Putre	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
4	General Lagos	1	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
5	Iquique	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
6	Alto Hospicio	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
7	Pozo Almonte	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
8	Camiña	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
9	Colchane	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
10	Huara	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
11	Pica	2	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
12	Antofagasta	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
13	Mejillones	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
14	Sierra Gorda	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
15	Taltal	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
16	Calama	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
17	Ollagüe	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
18	San Pedro de Atacama	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
19	Tocopilla	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
20	María Elena	3	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
21	Copiapó	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
22	Caldera	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
23	Tierra Amarilla	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
24	Chañaral	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
25	Diego de Almagro	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
26	Vallenar	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
27	Alto del Carmen	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
28	Freirina	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
29	Huasco	4	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
30	La Serena	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
31	Coquimbo	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
32	Andacollo	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
33	La Higuera	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
34	Paihuano	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
35	Vicuña	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
36	Illapel	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
37	Canela	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
38	Los Vilos	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
39	Salamanca	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
40	Ovalle	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
41	Combarbalá	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
42	Monte Patria	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
43	Punitaqui	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
44	Río Hurtado	5	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
303	Concepción	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
304	Hualpén	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
305	Talcahuano	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
306	Penco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
307	Chiguayante	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
308	San Pedro de la Paz	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
309	Coronel	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
310	Lota	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
311	Arauco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
312	Curanilahue	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
313	Los Álamos	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
314	Lebu	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
315	Tirúa	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
316	Cabrero	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
317	Laja	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
318	Mulchén	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
319	Nacimiento	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
320	Negrete	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
321	San Rosendo	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
322	Santa Juana	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
323	Yumbel	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
324	Antuco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
325	Alto Biobío	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
326	Quilleco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
327	Quilaco	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
328	Santa Bárbara	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
329	Cañete	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
330	Contulmo	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
331	Hualqui	10	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
332	Temuco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
333	Carahue	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
334	Cunco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
335	Curarrehue	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
336	Freire	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
337	Galvarino	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
338	Gorbea	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
339	Loncoche	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
340	Melipeuco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
341	Nueva Imperial	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
84	Valparaíso	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
85	Viña del Mar	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
86	Concón	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
87	Quintero	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
88	Puchuncaví	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
89	Juan Fernández	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
90	Casablanca	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
91	El Quisco	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
92	El Tabo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
93	San Antonio	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
94	Algarrobo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
95	Cartagena	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
96	Santo Domingo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
97	San Sebastián	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
98	Los Andes	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
99	Calle Larga	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
100	Rinconada	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
101	San Esteban	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
102	Llay Llay	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
103	Villa Alemana	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
104	Olmué	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
105	Limache	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
106	Quilpué	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
107	La Calera	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
108	La Cruz	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
109	Nogales	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
110	San Felipe	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
111	Catemu	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
112	Panquehue	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
113	Putaendo	6	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
342	Padre Las Casas	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
343	Perquenco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
344	Pitrufquén	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
345	Pucón	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
346	Saavedra	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
347	Villarrica	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
348	Victoria	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
349	Angol	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
350	Collipulli	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
351	Curacautín	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
352	Ercilla	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
353	Lonquimay	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
354	Los Sauces	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
355	Lumaco	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
231	Talca	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
232	Constitución	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
233	Curepto	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
234	Empedrado	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
235	Maule	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
236	Pelarco	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
237	Pencahue	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
238	San Clemente	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
239	San Rafael	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
240	Teno	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
241	Cauquenes	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
242	Chanco	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
243	Pelluhue	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
244	Curicó	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
245	Hualañé	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
246	Molina	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
145	Rancagua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
146	Codegua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
147	Coinco	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
148	Coltauco	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
149	Doñihue	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
150	Graneros	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
151	Las Cabras	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
152	Machalí	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
153	Malloa	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
154	Mostazal	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
155	Olivar	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
156	Peumo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
157	Pichidegua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
158	Quinta de Tilcoco	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
159	Rengo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
160	Requínoa	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
161	San Vicente de Tagua Tagua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
162	Pichilemu	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
247	Rauco	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
248	Sagrada Familia	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
249	Villa Alegre	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
250	Yerbas Buenas	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
163	La Estrella	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
164	Litueche	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
165	Marchigüe	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
166	Navidad	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
167	Peralillo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
168	Pumanque	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
169	San Fernando	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
170	Chépica	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
171	Chimbarongo	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
172	Lolol	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
173	Nancagua	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
174	Palmilla	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
175	Placilla	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
176	Santa Cruz	7	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
251	Linares	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
252	Colbún	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
253	Longaví	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
254	Parral	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
255	Retiro	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
256	San Javier	8	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
257	Chillán	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
258	Chillán Viejo	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
259	Bulnes	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
260	Cobquecura	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
261	Coihueco	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
262	El Carmen	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
263	Ninhue	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
264	Pemuco	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
265	Pinto	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
266	Quillón	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
267	Quirihue	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
268	Ránquil	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
269	San Carlos	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
270	San Fabián	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
271	San Ignacio	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
272	Yungay	9	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
356	Renaico	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
357	Traiguén	11	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
363	Valdivia	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
364	Corral	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
365	Lanco	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
366	Los Lagos	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
367	Máfil	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
368	Mariquina	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
369	Paillaco	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
370	Panguipulli	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
371	Futrono	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
372	La Unión	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
373	Río Bueno	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
374	San José de la Mariquina	12	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
375	Puerto Montt	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
376	Puerto Varas	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
377	Calbuco	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
378	Cochamó	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
379	Fresia	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
380	Frutillar	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
381	Los Muermos	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
382	Maullín	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
383	Osorno	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
384	Puyehue	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
385	Purranque	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
386	Río Negro	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
387	San Juan de la Costa	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
388	San Pablo	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
389	Ancud	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
390	Castro	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
391	Chonchi	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
392	Curaco de Vélez	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
393	Dalcahue	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
394	Puqueldón	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
395	Queilén	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
396	Quellón	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
397	Quinchao	13	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
398	Coyhaique	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
399	Lago Verde	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
400	Aisén	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
401	Cisnes	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
402	Guaitecas	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
403	Cochrane	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
404	O’Higgins	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
405	Tortel	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
406	Chile Chico	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
407	Río Ibáñez	14	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
408	Punta Arenas	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
409	Puerto Natales	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
410	Porvenir	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
411	Puerto Williams	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
412	Timaukel	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
413	Natales	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
414	Torres del Paine	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
415	Río Verde	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
416	Laguna Blanca	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
417	San Gregorio	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
418	Estancia Río de los Ciervos	15	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
419	Santiago	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
420	Cerrillos	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
421	Cerro Navia	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
422	Conchalí	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
423	El Bosque	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
424	Estación Central	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
425	Huechuraba	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
426	Independencia	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
427	La Cisterna	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
428	La Florida	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
429	La Granja	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
430	La Pintana	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
431	Las Condes	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
432	Lo Barnechea	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
433	Lo Espejo	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
434	Lo Prado	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
435	Macul	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
436	Maipú	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
437	Ñuñoa	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
438	Pedro Aguirre Cerda	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
439	Peñalolén	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
440	Providencia	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
441	Pudahuel	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
442	Quilicura	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
443	Quinta Normal	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
444	Recoleta	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
445	Renca	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
446	San Bernardo	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
447	San Joaquín	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
448	San Miguel	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
449	San Ramón	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
450	Vitacura	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
451	Puente Alto	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
452	Pirque	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
453	Colina	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
454	Lampa	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
455	Buin	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
456	Paine	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
457	Melipilla	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
458	Alhué	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
459	Curacaví	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
460	María Pinto	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
461	San José de Maipo	16	2025-04-04 21:32:49.671911	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5085 (class 0 OID 17959)
-- Dependencies: 219
-- Data for Name: frecuencia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.frecuencia (id_frecuencia, frecuencia, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Anual	2025-04-04 21:44:11.44453	hpinilla@gmail.com	\N	\N	\N	\N
2	Única	2025-04-04 21:44:11.44453	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5087 (class 0 OID 17966)
-- Dependencies: 221
-- Data for Name: medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medida (id_medida, id_tipo_medida, nombre_corto, indicador, formula_calculo, id_frecuencia, id_organismo_sectorial, id_plan, desc_medio_de_verificacion, id_tipo_dato, reporte_unico, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	1	RCA que contenga obligación de compensar emisiones	Número de RCA aprobadas en el año t que contengan obligaciones de compensar emisiones atmosféricas	Suma del número de RCA aprobadas que contengan obligación de compensar emisiones atmosféricas	1	1	1	Registro de las RCA aprobadas identificando el titular, la RCA, las emisiones y el monto a compensar	1	f	2025-04-04 21:48:45.197036	hpinilla@gmail.com	\N	\N	\N	\N
2	1	Condiciones del sistema de recuperación y/o eliminación de vapores de estanques Deposito techo fijo	Cumplimiento de las condiciones indicadas en el literal A para depósitos de techo fijo y Cronograma de implementación gradual calificado por la SEC cuando corresponda	([N° de tanques del artículo 33 literal A) al cual se han implementado las medidas comprometidas en el año t]/[N° de tanques del artículo 33 literal A) programadas para el año t])*100	1	2	1	a) Informe de Avance de Implementación de las medidas del Artículo 33 del Plan. b) En caso de solicitar más plazo, Oficio de envío de la Resolución que califica el Cronograma de implementación gradual para el plazo de cumplimiento	1	f	2025-04-04 21:48:45.197036	hpinilla@gmail.com	\N	\N	\N	\N
3	1	Requisitos del sistema de almacenamiento intermedio	Instrucciones de SEC, para cumplir con el sistema de almacenamiento intermedio u otro con el mismo objetivo, conforme al artículo 5 del DS N°160/2008.	Si/No	2	2	1	Oficialización de la Instrucción de SEC para cumplir con el sistema indicado en el artículo 33 del Plan.	4	f	2025-04-04 21:48:45.197036	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5089 (class 0 OID 17974)
-- Dependencies: 223
-- Data for Name: medio_verificacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medio_verificacion (nombre_archivo, fecha_subida, archivo, tamano, id_reporte, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
\.


--
-- TOC entry 5090 (class 0 OID 17981)
-- Dependencies: 224
-- Data for Name: opcion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opcion (id_opcion, opcion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
4	Si	2025-04-04 21:51:39.379777	hpinilla@gmail.com	\N	\N	\N	\N
5	No	2025-04-04 21:51:39.379777	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5092 (class 0 OID 17988)
-- Dependencies: 226
-- Data for Name: opcion_medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opcion_medida (id_opcion_medida, id_medida, id_opcion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
4	3	4	2025-04-04 21:50:52.837067	hpinilla@gmail.com	\N	\N	\N	\N
5	3	5	2025-04-04 21:50:52.837067	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5094 (class 0 OID 17995)
-- Dependencies: 228
-- Data for Name: organismo_sectorial; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organismo_sectorial (id_organismo_sectorial, organismo_sectorial, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Servicio de Evaluación Ambiental	2025-04-04 21:45:19.649923	hpinilla@gmail.com	\N	\N	\N	\N
2	Superintendencia de Electricidad y Combustibles	2025-04-04 21:45:19.649923	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5096 (class 0 OID 18002)
-- Dependencies: 230
-- Data for Name: plan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plan (id_plan, nombre, descripcion, fecha_publicacion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	PPDA CQP	Plan de Prevención y Descontaminación Atmosférica para las comunas de Concón, Quintero y Puchuncaví	2025-01-24	2025-04-04 21:38:50.504328	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5097 (class 0 OID 18009)
-- Dependencies: 231
-- Data for Name: plan_comuna; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plan_comuna (id_plan_comuna, id_plan, id_comuna, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	1	86	2025-04-04 21:36:58.170734	hpinilla@gmail.com	\N	\N	\N	\N
2	1	87	2025-04-04 21:36:58.170734	hpinilla@gmail.com	\N	\N	\N	\N
3	1	88	2025-04-04 21:36:58.170734	hpinilla@gmail.com	\N	\N	\N	\N
12	1	1	2025-04-05 11:01:28.322013	hpinilla@gmail.com	\N	\N	2025-04-05 11:07:01.961695	hpinilla@gmail.com
\.


--
-- TOC entry 5100 (class 0 OID 18017)
-- Dependencies: 234
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.region (id_region, region, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Región de Arica y Parinacota	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
2	Región de Tarapacá	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
3	Región de Antofagasta	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
4	Región de Atacama	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
5	Región de Coquimbo	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
6	Región de Valparaíso	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
7	Región del Libertador General Bernardo O’Higgins	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
8	Región del Maule	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
9	Región de Ñuble	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
10	Región del Biobío	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
11	Región de La Araucanía	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
12	Región de Los Ríos	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
13	Región de Los Lagos	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
14	Región de Aysén del General Carlos Ibáñez del Campo	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
15	Región de Magallanes y de la Antártica Chilena	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
16	Región Metropolitana de Santiago	2025-04-04 20:43:52.597629	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5102 (class 0 OID 18024)
-- Dependencies: 236
-- Data for Name: reporte; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reporte (id_reporte, fecha_registro, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
2	2025-03-23 01:27:21.256095	2025-04-04 21:57:31.809002	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5104 (class 0 OID 18032)
-- Dependencies: 238
-- Data for Name: reporte_medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reporte_medida (id_reporte_medida, id_reporte, id_medida, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
\.


--
-- TOC entry 5106 (class 0 OID 18039)
-- Dependencies: 240
-- Data for Name: resultado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resultado (id_reporte_medida, texto, numerico, si_no, seleccion, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
\.


--
-- TOC entry 5107 (class 0 OID 18046)
-- Dependencies: 241
-- Data for Name: rol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rol (id_rol, rol, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
2	Fiscalizador	2025-04-04 22:31:14.939052	hpinilla@gmail.com	\N	\N	\N	\N
1	Administrador	2025-04-04 22:31:14.939052	hpinilla@gmail.com	\N	\N	\N	\N
3	Organismo Sectorial	2025-04-04 22:31:14.939052	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5108 (class 0 OID 18052)
-- Dependencies: 242
-- Data for Name: tipo_dato; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipo_dato (id_tipo_dato, tipo_dato, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
2	Texto	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
3	Si/No	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
1	Numérico	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
4	Selección	2025-04-04 21:50:09.742606	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5110 (class 0 OID 18059)
-- Dependencies: 244
-- Data for Name: tipo_medida; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipo_medida (id_tipo_medida, tipo_medida, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Medida Regulatoria	2025-04-04 21:47:01.37056	hpinilla@gmail.com	\N	\N	\N	\N
3	Medidas No Regulatorias	2025-04-04 21:47:01.37056	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5113 (class 0 OID 18067)
-- Dependencies: 247
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, nombre, apellido, email, activo, id_rol, password, id_organismo_sectorial, fecha_creacion, creado_por, fecha_actualizacion, actualizado_por, fecha_eliminacion, eliminado_por) FROM stdin;
1	Hamid	Pinilla	hpinilla@gmail.com	t	1	$2b$12$1OJJ5ybGfWXgzYVaHQUrT.tLxj6LeOOpTdnNfxTbT7C7MpQc2Bqci	\N	2025-04-05 09:22:17.575321	hpinilla@gmail.com	\N	\N	\N	\N
7	Jorge	Bernal	jbernal@gmail.com	t	2	$2b$12$EwSlmFayPCrPTVXXeNM/kuNKYb6CGT5irZP75ZpQNNTcwRJNfSmdq	\N	2025-04-05 09:22:17.575321	hpinilla@gmail.com	\N	\N	\N	\N
\.


--
-- TOC entry 5122 (class 0 OID 0)
-- Dependencies: 218
-- Name: comuna_id_comuna_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comuna_id_comuna_seq', 461, true);


--
-- TOC entry 5123 (class 0 OID 0)
-- Dependencies: 220
-- Name: frecuencia_id_frecuencia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.frecuencia_id_frecuencia_seq', 7, true);


--
-- TOC entry 5124 (class 0 OID 0)
-- Dependencies: 222
-- Name: medida_id_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medida_id_medida_seq', 11, true);


--
-- TOC entry 5125 (class 0 OID 0)
-- Dependencies: 225
-- Name: opcion_id_opcion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opcion_id_opcion_seq', 5, true);


--
-- TOC entry 5126 (class 0 OID 0)
-- Dependencies: 227
-- Name: opciones_medida_id_opcion_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opciones_medida_id_opcion_medida_seq', 5, true);


--
-- TOC entry 5127 (class 0 OID 0)
-- Dependencies: 229
-- Name: organismo_sectorial_id_organismo_sectorial_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organismo_sectorial_id_organismo_sectorial_seq', 7, true);


--
-- TOC entry 5128 (class 0 OID 0)
-- Dependencies: 232
-- Name: plan_comuna_id_plan_comuna_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plan_comuna_id_plan_comuna_seq', 12, true);


--
-- TOC entry 5129 (class 0 OID 0)
-- Dependencies: 233
-- Name: plan_id_plan_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plan_id_plan_seq', 12, true);


--
-- TOC entry 5130 (class 0 OID 0)
-- Dependencies: 235
-- Name: region_id_region_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.region_id_region_seq', 16, true);


--
-- TOC entry 5131 (class 0 OID 0)
-- Dependencies: 237
-- Name: reporte_id_reporte_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reporte_id_reporte_seq', 3, true);


--
-- TOC entry 5132 (class 0 OID 0)
-- Dependencies: 239
-- Name: reporte_medida_id_reporte_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reporte_medida_id_reporte_medida_seq', 1, false);


--
-- TOC entry 5133 (class 0 OID 0)
-- Dependencies: 243
-- Name: tipo_dato_medida_id_tipo_dato_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_dato_medida_id_tipo_dato_medida_seq', 4, true);


--
-- TOC entry 5134 (class 0 OID 0)
-- Dependencies: 245
-- Name: tipo_medida_id_tipo_medida_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_medida_id_tipo_medida_seq', 4, true);


--
-- TOC entry 5135 (class 0 OID 0)
-- Dependencies: 246
-- Name: tipo_usuario_id_tipo_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_usuario_id_tipo_usuario_seq', 3, true);


--
-- TOC entry 5136 (class 0 OID 0)
-- Dependencies: 248
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 7, true);


--
-- TOC entry 4847 (class 2606 OID 18076)
-- Name: comuna comuna_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comuna
    ADD CONSTRAINT comuna_pk PRIMARY KEY (id_comuna);


--
-- TOC entry 4849 (class 2606 OID 18078)
-- Name: comuna comuna_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comuna
    ADD CONSTRAINT comuna_un UNIQUE (comuna);


--
-- TOC entry 4851 (class 2606 OID 18080)
-- Name: frecuencia frecuencia_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frecuencia
    ADD CONSTRAINT frecuencia_pk PRIMARY KEY (id_frecuencia);


--
-- TOC entry 4853 (class 2606 OID 18082)
-- Name: frecuencia frecuencia_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frecuencia
    ADD CONSTRAINT frecuencia_un UNIQUE (frecuencia);


--
-- TOC entry 4855 (class 2606 OID 18084)
-- Name: medida medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_pk PRIMARY KEY (id_medida);


--
-- TOC entry 4857 (class 2606 OID 18086)
-- Name: medio_verificacion medio_verificacion_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medio_verificacion
    ADD CONSTRAINT medio_verificacion_pk PRIMARY KEY (id_reporte);


--
-- TOC entry 4859 (class 2606 OID 18088)
-- Name: opcion opcion_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion
    ADD CONSTRAINT opcion_pk PRIMARY KEY (id_opcion);


--
-- TOC entry 4861 (class 2606 OID 18090)
-- Name: opcion opcion_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion
    ADD CONSTRAINT opcion_un UNIQUE (opcion);


--
-- TOC entry 4863 (class 2606 OID 18092)
-- Name: opcion_medida opciones_medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opciones_medida_pk PRIMARY KEY (id_opcion_medida);


--
-- TOC entry 4865 (class 2606 OID 18094)
-- Name: opcion_medida opciones_medida_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opciones_medida_un UNIQUE (id_medida, id_opcion);


--
-- TOC entry 4867 (class 2606 OID 18096)
-- Name: organismo_sectorial organismo_sectorial_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organismo_sectorial
    ADD CONSTRAINT organismo_sectorial_pk PRIMARY KEY (id_organismo_sectorial);


--
-- TOC entry 4869 (class 2606 OID 18098)
-- Name: organismo_sectorial organismo_sectorial_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organismo_sectorial
    ADD CONSTRAINT organismo_sectorial_un UNIQUE (organismo_sectorial);


--
-- TOC entry 4873 (class 2606 OID 18100)
-- Name: plan_comuna plan_comuna_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_pk PRIMARY KEY (id_plan_comuna);


--
-- TOC entry 4875 (class 2606 OID 18102)
-- Name: plan_comuna plan_comuna_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_unique UNIQUE (id_plan, id_comuna);


--
-- TOC entry 4871 (class 2606 OID 18104)
-- Name: plan plan_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT plan_pk PRIMARY KEY (id_plan);


--
-- TOC entry 4877 (class 2606 OID 18106)
-- Name: region region_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_pk PRIMARY KEY (id_region);


--
-- TOC entry 4879 (class 2606 OID 18108)
-- Name: region region_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_un UNIQUE (region);


--
-- TOC entry 4883 (class 2606 OID 18110)
-- Name: reporte_medida reporte_medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_pk PRIMARY KEY (id_reporte_medida);


--
-- TOC entry 4885 (class 2606 OID 18112)
-- Name: reporte_medida reporte_medida_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_unique UNIQUE (id_reporte, id_medida);


--
-- TOC entry 4881 (class 2606 OID 18114)
-- Name: reporte reporte_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pk PRIMARY KEY (id_reporte);


--
-- TOC entry 4887 (class 2606 OID 18116)
-- Name: resultado resultado_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resultado
    ADD CONSTRAINT resultado_pk PRIMARY KEY (id_reporte_medida);


--
-- TOC entry 4889 (class 2606 OID 18118)
-- Name: rol rol_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pk PRIMARY KEY (id_rol);


--
-- TOC entry 4891 (class 2606 OID 18120)
-- Name: rol rol_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_un UNIQUE (rol);


--
-- TOC entry 4893 (class 2606 OID 18122)
-- Name: tipo_dato tipo_dato_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_dato
    ADD CONSTRAINT tipo_dato_pk PRIMARY KEY (id_tipo_dato);


--
-- TOC entry 4895 (class 2606 OID 18124)
-- Name: tipo_dato tipo_dato_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_dato
    ADD CONSTRAINT tipo_dato_un UNIQUE (tipo_dato);


--
-- TOC entry 4897 (class 2606 OID 18126)
-- Name: tipo_medida tipo_medida_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_medida
    ADD CONSTRAINT tipo_medida_pk PRIMARY KEY (id_tipo_medida);


--
-- TOC entry 4899 (class 2606 OID 18128)
-- Name: tipo_medida tipo_medida_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_medida
    ADD CONSTRAINT tipo_medida_un UNIQUE (tipo_medida);


--
-- TOC entry 4901 (class 2606 OID 18130)
-- Name: usuario usuario_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pk PRIMARY KEY (id_usuario);


--
-- TOC entry 4903 (class 2606 OID 18132)
-- Name: usuario usuario_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_un UNIQUE (email);


--
-- TOC entry 4920 (class 2620 OID 18133)
-- Name: comuna trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4921 (class 2620 OID 18134)
-- Name: frecuencia trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.frecuencia FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4922 (class 2620 OID 18135)
-- Name: medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4923 (class 2620 OID 18136)
-- Name: medio_verificacion trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medio_verificacion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4924 (class 2620 OID 18137)
-- Name: opcion trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4925 (class 2620 OID 18138)
-- Name: opcion_medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4927 (class 2620 OID 18139)
-- Name: organismo_sectorial trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.organismo_sectorial FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4928 (class 2620 OID 18140)
-- Name: plan trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4929 (class 2620 OID 18141)
-- Name: plan_comuna trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan_comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4930 (class 2620 OID 18142)
-- Name: region trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.region FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4931 (class 2620 OID 18143)
-- Name: reporte trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.reporte FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4932 (class 2620 OID 18144)
-- Name: reporte_medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.reporte_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4933 (class 2620 OID 18145)
-- Name: resultado trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.resultado FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4934 (class 2620 OID 18146)
-- Name: rol trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.rol FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4935 (class 2620 OID 18147)
-- Name: tipo_dato trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_dato FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4936 (class 2620 OID 18148)
-- Name: tipo_medida trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4937 (class 2620 OID 18149)
-- Name: usuario trg_validar_usuarios_auditoria; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();


--
-- TOC entry 4926 (class 2620 OID 18150)
-- Name: opcion_medida trg_validate_opcion_medida; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_validate_opcion_medida BEFORE INSERT ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validate_opcion_medida();


--
-- TOC entry 4904 (class 2606 OID 18151)
-- Name: comuna comuna_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comuna
    ADD CONSTRAINT comuna_fk FOREIGN KEY (id_region) REFERENCES public.region(id_region);


--
-- TOC entry 4905 (class 2606 OID 18156)
-- Name: medida medida_fk_frecuencia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_frecuencia FOREIGN KEY (id_frecuencia) REFERENCES public.frecuencia(id_frecuencia);


--
-- TOC entry 4906 (class 2606 OID 18161)
-- Name: medida medida_fk_organismo_sectorial; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_organismo_sectorial FOREIGN KEY (id_organismo_sectorial) REFERENCES public.organismo_sectorial(id_organismo_sectorial);


--
-- TOC entry 4907 (class 2606 OID 18166)
-- Name: medida medida_fk_plan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_plan FOREIGN KEY (id_plan) REFERENCES public.plan(id_plan);


--
-- TOC entry 4908 (class 2606 OID 18171)
-- Name: medida medida_fk_tipo_dato; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_tipo_dato FOREIGN KEY (id_tipo_dato) REFERENCES public.tipo_dato(id_tipo_dato);


--
-- TOC entry 4909 (class 2606 OID 18176)
-- Name: medida medida_fk_tipo_medida; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medida
    ADD CONSTRAINT medida_fk_tipo_medida FOREIGN KEY (id_tipo_medida) REFERENCES public.tipo_medida(id_tipo_medida);


--
-- TOC entry 4910 (class 2606 OID 18181)
-- Name: medio_verificacion medio_verificacion_fk_reporte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medio_verificacion
    ADD CONSTRAINT medio_verificacion_fk_reporte FOREIGN KEY (id_reporte) REFERENCES public.reporte(id_reporte);


--
-- TOC entry 4911 (class 2606 OID 18186)
-- Name: opcion_medida opcion_medida_fk_medida; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opcion_medida_fk_medida FOREIGN KEY (id_medida) REFERENCES public.medida(id_medida);


--
-- TOC entry 4912 (class 2606 OID 18191)
-- Name: opcion_medida opcion_medida_fk_opcion; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opcion_medida
    ADD CONSTRAINT opcion_medida_fk_opcion FOREIGN KEY (id_opcion) REFERENCES public.opcion(id_opcion);


--
-- TOC entry 4913 (class 2606 OID 18196)
-- Name: plan_comuna plan_comuna_fk_comuna; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_fk_comuna FOREIGN KEY (id_comuna) REFERENCES public.comuna(id_comuna);


--
-- TOC entry 4914 (class 2606 OID 18201)
-- Name: plan_comuna plan_comuna_fk_plan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_comuna
    ADD CONSTRAINT plan_comuna_fk_plan FOREIGN KEY (id_plan) REFERENCES public.plan(id_plan);


--
-- TOC entry 4915 (class 2606 OID 18206)
-- Name: reporte_medida reporte_medida_medida_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_medida_fk FOREIGN KEY (id_medida) REFERENCES public.medida(id_medida);


--
-- TOC entry 4916 (class 2606 OID 18211)
-- Name: reporte_medida reporte_medida_reporte_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reporte_medida
    ADD CONSTRAINT reporte_medida_reporte_fk FOREIGN KEY (id_reporte) REFERENCES public.reporte(id_reporte);


--
-- TOC entry 4917 (class 2606 OID 18216)
-- Name: resultado resultado_reporte_medida_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resultado
    ADD CONSTRAINT resultado_reporte_medida_fk FOREIGN KEY (id_reporte_medida) REFERENCES public.reporte_medida(id_reporte_medida);


--
-- TOC entry 4918 (class 2606 OID 18221)
-- Name: usuario usuario_fk_rol; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_fk_rol FOREIGN KEY (id_rol) REFERENCES public.rol(id_rol);


--
-- TOC entry 4919 (class 2606 OID 18226)
-- Name: usuario usuario_organismo_sectorial_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_organismo_sectorial_fk FOREIGN KEY (id_organismo_sectorial) REFERENCES public.organismo_sectorial(id_organismo_sectorial);


--
-- TOC entry 5121 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


-- Completed on 2025-04-05 20:06:57

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-05 20:06:57

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-04-05 20:06:57

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-04-05 20:06:57

--
-- PostgreSQL database cluster dump complete
--

