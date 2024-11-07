from .ebest import EBest
from .ls import LS, LSV
from .kis import Kis, KisV

class APIFactory:
    @staticmethod
    def create_api(api_type):
        api_type = api_type.upper()
        if api_type == "EBEST":
            return EBest()
        elif api_type == "LS":
            return LS()
        elif api_type == "LSV":
            return LSV()
        elif api_type == "KIS":
            return Kis()
        elif api_type == "KISV":
            return KisV()
        else:
            raise ValueError("Unsupported api type")