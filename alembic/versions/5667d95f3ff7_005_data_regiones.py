"""005 data regiones

Revision ID: 5667d95f3ff7
Revises: 850c776a830d
Create Date: 2025-04-19 21:35:06.098924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5667d95f3ff7'
down_revision: Union[str, None] = '850c776a830d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.region;")
    op.execute("""INSERT INTO public.region (region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Región de Arica y Parinacota','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Tarapacá','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Antofagasta','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Atacama','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Coquimbo','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Valparaíso','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región del Libertador General Bernardo O’Higgins','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región del Maule','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Ñuble','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región del Biobío','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL);""")
    op.execute("""INSERT INTO public.region (region,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Región de La Araucanía','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Los Ríos','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Los Lagos','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Aysén del General Carlos Ibáñez del Campo','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región de Magallanes y de la Antártica Chilena','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Región Metropolitana de Santiago','2025-04-04 20:43:52.597629','hpinilla@gmail.com',NULL,NULL,NULL,NULL);""")
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.region FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DELETE FROM public.region;""")
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.region FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")
