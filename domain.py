class Comuna:
    """
    Clase que representa una comuna en el sistema.

    Attributes:
        id (str): Identificador único de la comuna
        nombre_comuna (str): Nombre de la columna 
        id_region (int): Id de la región
    """

    def __init__(self, id, nombre_comuna, id_region):
        """
        Constructor de la clase Patient.

        Args:
            id (str): Identificador único del paciente
            name (str): Nombre completo del paciente
            current_city (str): Ciudad actual de residencia del paciente
        """
        self.id = id
        self.nombre_comuna = nombre_comuna
        self.id_region= id_region

    def __dict__(self):
        """
        Convierte el objeto Comuna a un diccionario.

        Returns:
            dict: Diccionario con los datos de la comuna
        """
        return {
            "id_comuna": self.id,
            "nombre_comuna": self.nombre_comuna,
            "id_region": self.id_region
        }