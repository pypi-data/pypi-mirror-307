
import datetime
from vital_ai_vitalsigns.model.VITAL_Node import VITAL_Node


class HaleyChatAgentThought(VITAL_Node):
        bridgeHaleyMessageURI: str
        haleyChatAgentThoughtTypeURI: str
        haleyChatInteractionURI: str
        haleyChatMessageHistoryURI: str
        haleyChatReferenceMessageURI: str
        haleyChatThoughtText: str
        haleyChatThoughtTitle: str
        chatIncrementalMessage: bool
        chatPartialMessage: bool
        haleyChatThoughtComplete: bool

