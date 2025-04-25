"""007 data frecuencia

Revision ID: f3fbf4e3679c
Revises: c967157be38e
Create Date: 2025-04-19 22:07:17.049934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3fbf4e3679c'
down_revision: Union[str, None] = 'c967157be38e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.frecuencia;")
    op.execute('''INSERT INTO public.frecuencia (frecuencia,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Anual','2025-04-04 21:44:11.44453','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Única','2025-04-04 21:44:11.44453','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.frecuencia FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.frecuencia WHERE frecuencia IN ('Anual', 'Única');''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.frecuencia FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
