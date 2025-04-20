"""009 data tipo dato

Revision ID: cd0cdd5ef74e
Revises: 0155c7ec244f
Create Date: 2025-04-19 22:14:40.719630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd0cdd5ef74e'
down_revision: Union[str, None] = '0155c7ec244f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.tipo_dato;")
    op.execute('''INSERT INTO public.tipo_dato (tipo_dato,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Texto','2025-04-04 21:50:09.742606','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Si/No','2025-04-04 21:50:09.742606','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Numérico','2025-04-04 21:50:09.742606','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Selección','2025-04-04 21:50:09.742606','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_dato FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.tipo_dato WHERE tipo_dato IN ('Texto','Si/No','Numérico','Selección'¿);''')
    op.execute('''CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.tipo_dato FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();''')
