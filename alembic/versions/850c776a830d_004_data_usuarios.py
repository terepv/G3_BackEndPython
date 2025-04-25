"""004 data usuarios

Revision ID: 850c776a830d
Revises: 7046fcb232e8
Create Date: 2025-04-19 21:32:07.857037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '850c776a830d'
down_revision: Union[str, None] = '7046fcb232e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.usuario;")
    op.execute("""INSERT INTO public.usuario (nombre,apellido,email,activo,id_rol,"password",id_organismo_sectorial,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 ('Hamid','Pinilla','hpinilla@gmail.com',true,1,'$2b$12$1OJJ5ybGfWXgzYVaHQUrT.tLxj6LeOOpTdnNfxTbT7C7MpQc2Bqci',NULL,'2025-04-05 09:22:17.575321','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 ('Jorge','Bernal','jbernal@gmail.com',true,3,'$2b$12$EwSlmFayPCrPTVXXeNM/kuNKYb6CGT5irZP75ZpQNNTcwRJNfSmdq',1,'2025-04-05 09:22:17.575321','hpinilla@gmail.com',NULL,NULL,NULL,NULL);
    """)
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DELETE FROM public.usuario WHERE email IN ('hpinilla@gmail.com','jbernal@gmail.com');""")
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")
