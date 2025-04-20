"""002 data roles

Revision ID: cc8acf49a01c
Revises: 23133f86f05c
Create Date: 2025-04-19 21:05:53.292947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc8acf49a01c'
down_revision: Union[str, None] = '23133f86f05c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.rol;")
    op.execute('''INSERT INTO public.rol (rol,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Fiscalizador','2025-04-04 22:31:14.939052','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Administrador','2025-04-04 22:31:14.939052','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Organismo Sectorial','2025-04-04 22:31:14.939052','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
''')
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.rol FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.rol WHERE rol IN ('Fiscalizador', 'Administrador', 'Organismo Sectorial');''')
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.rol FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")
