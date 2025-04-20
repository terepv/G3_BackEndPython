"""008 data tipo medida

Revision ID: 0155c7ec244f
Revises: f3fbf4e3679c
Create Date: 2025-04-19 22:10:45.526266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0155c7ec244f'
down_revision: Union[str, None] = 'f3fbf4e3679c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.tipo_medida;")
    op.execute('''INSERT INTO public.tipo_medida (tipo_medida,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Medida Regulatoria','2025-04-04 21:47:01.37056','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Medidas No Regulatorias','2025-04-04 21:47:01.37056','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
    

def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.tipo_medida WHERE tipo_medida IN ('Medida Regulatoria','Medidas No Regulatorias');''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
