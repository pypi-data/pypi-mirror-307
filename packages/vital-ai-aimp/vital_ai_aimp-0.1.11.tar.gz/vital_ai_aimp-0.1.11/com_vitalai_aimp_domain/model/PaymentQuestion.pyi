
import datetime
from com_vitalai_aimp_domain.model.Question import Question


class PaymentQuestion(Question):
        provider: str
        publicKey: str

