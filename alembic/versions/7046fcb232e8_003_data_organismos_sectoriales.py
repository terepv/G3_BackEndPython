"""003 data organismos sectoriales

Revision ID: 7046fcb232e8
Revises: cc8acf49a01c
Create Date: 2025-04-19 21:22:15.211885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7046fcb232e8'
down_revision: Union[str, None] = 'cc8acf49a01c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.organismo_sectorial;")
    op.execute('''
INSERT INTO public.organismo_sectorial (organismo_sectorial,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Servicio de Evaluación Ambiental','2025-04-04 21:45:19.649923','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Superintendencia de Electricidad y Combustibles','2025-04-04 21:45:19.649923','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Municipalidad de Santiago','2025-04-05 21:08:25.868418','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
''')
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.organismo_sectorial FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''
DELETE FROM public.organismo_sectorial WHERE organismo_sectorial IN ('Servicio de Evaluación Ambiental', 'Superintendencia de Electricidad y Combustibles');
''')
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.organismo_sectorial FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")
    
