"""010 data opcion

Revision ID: bb8a13e92836
Revises: cd0cdd5ef74e
Create Date: 2025-04-19 22:20:59.194150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb8a13e92836'
down_revision: Union[str, None] = 'cd0cdd5ef74e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.opcion;")
    op.execute('''INSERT INTO public.opcion (opcion,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Si','2025-04-04 21:51:39.379777','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('No','2025-04-04 21:51:39.379777','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.opcion WHERE opcion IN ('Si','No');''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.opcion FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
