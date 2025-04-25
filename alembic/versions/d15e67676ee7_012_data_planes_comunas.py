"""012 data planes comunas

Revision ID: d15e67676ee7
Revises: 16824aeabebe
Create Date: 2025-04-19 22:39:47.042840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd15e67676ee7'
down_revision: Union[str, None] = '16824aeabebe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.plan_comuna;")
    op.execute('''INSERT INTO public.plan_comuna (id_plan,id_comuna,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 (1,86,'2025-04-04 21:36:58.170734','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 (1,87,'2025-04-04 21:36:58.170734','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 (1,88,'2025-04-04 21:36:58.170734','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan_comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.plan_comuna WHERE id_plan = 1 AND id_comuna IN (86,87,88);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.plan_comuna FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
