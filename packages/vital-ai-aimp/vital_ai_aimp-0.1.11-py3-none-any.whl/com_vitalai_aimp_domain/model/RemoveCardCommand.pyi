
import datetime
from com_vitalai_aimp_domain.model.UserCommandMessage import UserCommandMessage


class RemoveCardCommand(UserCommandMessage):
        cardURI: str

