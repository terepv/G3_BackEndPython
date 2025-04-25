"""013 data medidas

Revision ID: de32bf7b8c23
Revises: d15e67676ee7
Create Date: 2025-04-19 22:42:46.193179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de32bf7b8c23'
down_revision: Union[str, None] = 'd15e67676ee7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_validar_usuarios_auditoria ON public.medida;")
    op.execute('''INSERT INTO public.medida (id_tipo_medida,nombre_corto,indicador,formula_calculo,id_frecuencia,id_organismo_sectorial,id_plan,desc_medio_de_verificacion,id_tipo_dato,reporte_unico,fecha_creacion,creado_por,fecha_actualizacion,actualizado_por,fecha_eliminacion,eliminado_por) VALUES
	 (1,'RCA que contenga obligación de compensar emisiones','Número de RCA aprobadas en el año t que contengan obligaciones de compensar emisiones atmosféricas','Suma del número de RCA aprobadas que contengan obligación de compensar emisiones atmosféricas',1,1,1,'Registro de las RCA aprobadas identificando el titular, la RCA, las emisiones y el monto a compensar',1,false,'2025-04-04 21:48:45.197036','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 (1,'Condiciones del sistema de recuperación y/o eliminación de vapores de estanques Deposito techo fijo','Cumplimiento de las condiciones indicadas en el literal A para depósitos de techo fijo y Cronograma de implementación gradual calificado por la SEC cuando corresponda','([N° de tanques del artículo 33 literal A) al cual se han implementado las medidas comprometidas en el año t]/[N° de tanques del artículo 33 literal A) programadas para el año t])*100',1,2,1,'a) Informe de Avance de Implementación de las medidas del Artículo 33 del Plan. b) En caso de solicitar más plazo, Oficio de envío de la Resolución que califica el Cronograma de implementación gradual para el plazo de cumplimiento',1,false,'2025-04-04 21:48:45.197036','hpinilla@gmail.com',NULL,NULL,NULL,NULL),
	 (1,'Requisitos del sistema de almacenamiento intermedio','Instrucciones de SEC, para cumplir con el sistema de almacenamiento intermedio u otro con el mismo objetivo, conforme al artículo 5 del DS N°160/2008.','Si/No',2,2,1,'Oficialización de la Instrucción de SEC para cumplir con el sistema indicado en el artículo 33 del Plan.',4,false,'2025-04-04 21:48:45.197036','hpinilla@gmail.com',NULL,NULL,NULL,NULL);''')
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('''DELETE FROM public.medida WHERE id_tipo_medida = 1 AND nombre_corto IN ('RCA que contenga obligación de compensar emisiones','Condiciones del sistema de recuperación y/o eliminación de vapores de estanques Deposito techo fijo','Requisitos del sistema de almacenamiento intermedio');''')
    op.execute("CREATE TRIGGER trg_validar_usuarios_auditoria BEFORE INSERT OR UPDATE ON public.medida FOR EACH ROW EXECUTE FUNCTION public.validar_usuarios_auditoria();")
