"""011 data planes

Revision ID: 16824aeabebe
Revises: bb8a13e92836
Create Date: 2025-04-19 22:29:33.868646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16824aeabebe'
down_revision: Union[str, None] = 'bb8a13e92836'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.plan;")
    op.execute('''INSERT INTO public."plan" (nombre,descripcion,fecha_publicacion,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('PPDA CQP','Plan de Prevención y Descontaminación Atmosférica para las comunas de Concón, Quintero y Puchuncaví','2025-01-24','2025-04-04 21:38:50.504328','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.plan WHERE nombre = 'PPDA CQP';''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
