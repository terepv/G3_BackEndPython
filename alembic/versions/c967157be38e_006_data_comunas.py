"""006 data comunas

Revision ID: c967157be38e
Revises: 5667d95f3ff7
Create Date: 2025-04-19 21:36:35.167890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c967157be38e'
down_revision: Union[str, None] = '5667d95f3ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.comuna;")
    op.execute("""
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Arica',1,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Camarones',1,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Putre',1,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('General Lagos',1,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Iquique',2,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Alto Hospicio',2,'2025-04-04 21:32:49.671911','hpinilla@gmail.coma',NULL,NULL,NULL,NULL),
	 ('Pozo Almonte',2,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Camiña',2,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Colchane',2,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Huara',2,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Pica',2,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Antofagasta',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Mejillones',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Sierra Gorda',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Taltal',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Calama',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Ollagüe',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Pedro de Atacama',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Tocopilla',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('María Elena',3,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Copiapó',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Caldera',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Tierra Amarilla',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chañaral',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Diego de Almagro',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Vallenar',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Alto del Carmen',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Freirina',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Huasco',4,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Serena',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Coquimbo',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Andacollo',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Higuera',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Paihuano',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Vicuña',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Illapel',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Canela',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Los Vilos',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Salamanca',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Ovalle',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Combarbalá',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Monte Patria',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Punitaqui',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Río Hurtado',5,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Concepción',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Hualpén',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Talcahuano',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Penco',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chiguayante',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Pedro de la Paz',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Coronel',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lota',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Arauco',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Curanilahue',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Los Álamos',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lebu',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Tirúa',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cabrero',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Laja',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Mulchén',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Nacimiento',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Negrete',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Rosendo',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Santa Juana',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Yumbel',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Antuco',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Alto Biobío',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quilleco',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quilaco',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Santa Bárbara',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Cañete',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Contulmo',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Hualqui',10,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Temuco',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Carahue',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cunco',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Curarrehue',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Freire',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Galvarino',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Gorbea',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Loncoche',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Melipeuco',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Nueva Imperial',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Valparaíso',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Viña del Mar',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Concón',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quintero',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puchuncaví',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Juan Fernández',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Casablanca',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('El Quisco',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('El Tabo',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Antonio',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Algarrobo',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cartagena',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Santo Domingo',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Sebastián',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Los Andes',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Calle Larga',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Rinconada',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('San Esteban',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Llay Llay',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Villa Alemana',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Olmué',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Limache',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quilpué',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Calera',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Cruz',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Nogales',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Felipe',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Catemu',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Panquehue',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Putaendo',6,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Padre Las Casas',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Perquenco',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pitrufquén',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pucón',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Saavedra',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Villarrica',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Victoria',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Angol',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Collipulli',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Curacautín',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Ercilla',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lonquimay',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Los Sauces',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lumaco',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Talca',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Constitución',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Curepto',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Empedrado',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Maule',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pelarco',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pencahue',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Clemente',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Rafael',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Teno',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cauquenes',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chanco',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pelluhue',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Curicó',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Hualañé',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Molina',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Rancagua',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Codegua',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Coinco',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Coltauco',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Doñihue',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Graneros',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Las Cabras',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Machalí',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Malloa',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Mostazal',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Olivar',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Peumo',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pichidegua',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quinta de Tilcoco',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Rengo',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Requínoa',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Vicente de Tagua Tagua',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Pichilemu',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Rauco',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Sagrada Familia',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Villa Alegre',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Yerbas Buenas',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Estrella',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Litueche',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Marchigüe',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Navidad',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Peralillo',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Pumanque',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Fernando',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chépica',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chimbarongo',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lolol',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Nancagua',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Palmilla',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Placilla',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Santa Cruz',7,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Linares',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Colbún',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Longaví',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Parral',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Retiro',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Javier',8,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chillán',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chillán Viejo',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Bulnes',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cobquecura',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Coihueco',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('El Carmen',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Ninhue',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pemuco',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pinto',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quillón',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quirihue',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Ránquil',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Carlos',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Fabián',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Ignacio',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Yungay',9,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Renaico',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Traiguén',11,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Valdivia',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Corral',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lanco',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Los Lagos',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Máfil',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Mariquina',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Paillaco',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Panguipulli',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Futrono',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Unión',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Río Bueno',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San José de la Mariquina',12,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puerto Montt',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puerto Varas',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Calbuco',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cochamó',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Fresia',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Frutillar',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Los Muermos',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Maullín',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Osorno',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puyehue',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Purranque',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Río Negro',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Juan de la Costa',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Pablo',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Ancud',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Castro',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chonchi',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Curaco de Vélez',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Dalcahue',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puqueldón',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Queilén',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quellón',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quinchao',13,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Coyhaique',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lago Verde',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Aisén',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cisnes',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Guaitecas',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cochrane',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('O''Higgins',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Tortel',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Chile Chico',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Río Ibáñez',14,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Punta Arenas',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puerto Natales',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Porvenir',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puerto Williams',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Timaukel',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Natales',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Torres del Paine',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Río Verde',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Laguna Blanca',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Gregorio',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Estancia Río de los Ciervos',15,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Santiago',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Cerrillos',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Cerro Navia',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Conchalí',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('El Bosque',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Estación Central',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Huechuraba',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Independencia',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Cisterna',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Florida',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('La Granja',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('La Pintana',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Las Condes',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lo Barnechea',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lo Espejo',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lo Prado',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Macul',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Maipú',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Ñuñoa',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pedro Aguirre Cerda',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Peñalolén',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Providencia',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pudahuel',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quilicura',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Quinta Normal',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Recoleta',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Renca',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Bernardo',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Joaquín',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Miguel',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San Ramón',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Vitacura',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Puente Alto',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Pirque',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Colina',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Lampa',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Buin',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Paine',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Melipilla',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Alhué',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Curacaví',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
INSERT INTO public.comuna (comuna,id_region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('María Pinto',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('San José de Maipo',16,'2025-04-04 21:32:49.671911','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('nombre comuna',1,'2025-04-05 18:48:40.543049','hpinilla@gmail.com','2025-04-05 19:16:38.401578','hpinilla@gmail.com','2025-04-05 19:26:56.843556','hpinilla@gmail.com');
""")
    op.execute("""CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();""")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DELETE FROM public.comuna;""")
    op.execute("""CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();""")
