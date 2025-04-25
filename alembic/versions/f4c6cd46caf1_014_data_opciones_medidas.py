"""014 data opciones medidas

Revision ID: f4c6cd46caf1
Revises: de32bf7b8c23
Create Date: 2025-04-19 22:47:30.219835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4c6cd46caf1'
down_revision: Union[str, None] = 'de32bf7b8c23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.opcion_medida;")
    op.execute('''INSERT INTO public.opcion_medida (id_medida,id_opcion,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 (3,1,'2025-04-04 21:50:52.837067','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 (3,2,'2025-04-04 21:50:52.837067','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.opcion_medida WHERE id_medida = 3 AND id_opcion IN (1,2);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
