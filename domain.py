class Patient:
    """
    Clase que representa un paciente en el sistema.

    Attributes:
        id (str): Identificador único del paciente
        name (str): Nombre completo del paciente 
        current_city (str): Ciudad actual de residencia del paciente
    """

    def __init__(self, id, name, current_city):
        """
        Constructor de la clase Patient.

        Args:
            id (str): Identificador único del paciente
            name (str): Nombre completo del paciente
            current_city (str): Ciudad actual de residencia del paciente
        """
        self.id = id
        self.name = name
        self.current_city = current_city

    def __dict__(self):
        """
        Convierte el objeto Patient a un diccionario.

        Returns:
            dict: Diccionario con los datos del paciente
        """
        return {
            "patient_id": self.id,
            "name": self.name,
            "current_city": self.current_city
        }