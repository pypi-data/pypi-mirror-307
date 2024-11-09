"""
Type annotations for lexv2-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_lexv2_runtime.type_defs import ActiveContextTimeToLiveTypeDef

    data: ActiveContextTimeToLiveTypeDef = ...
    ```
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ConfirmationStateType,
    DialogActionTypeType,
    IntentStateType,
    InterpretationSourceType,
    MessageContentTypeType,
    SentimentTypeType,
    ShapeType,
    StyleTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActiveContextOutputTypeDef",
    "ActiveContextTimeToLiveTypeDef",
    "ActiveContextTypeDef",
    "ActiveContextUnionTypeDef",
    "BlobTypeDef",
    "ButtonTypeDef",
    "ConfidenceScoreTypeDef",
    "DeleteSessionRequestRequestTypeDef",
    "DeleteSessionResponseTypeDef",
    "DialogActionOutputTypeDef",
    "DialogActionTypeDef",
    "DialogActionUnionTypeDef",
    "ElicitSubSlotOutputTypeDef",
    "ElicitSubSlotTypeDef",
    "ElicitSubSlotUnionTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "ImageResponseCardOutputTypeDef",
    "ImageResponseCardTypeDef",
    "ImageResponseCardUnionTypeDef",
    "IntentOutputTypeDef",
    "IntentTypeDef",
    "IntentUnionTypeDef",
    "InterpretationTypeDef",
    "MessageOutputTypeDef",
    "MessageTypeDef",
    "MessageUnionTypeDef",
    "PutSessionRequestRequestTypeDef",
    "PutSessionResponseTypeDef",
    "RecognizeTextRequestRequestTypeDef",
    "RecognizeTextResponseTypeDef",
    "RecognizeUtteranceRequestRequestTypeDef",
    "RecognizeUtteranceResponseTypeDef",
    "RecognizedBotMemberTypeDef",
    "ResponseMetadataTypeDef",
    "RuntimeHintDetailsOutputTypeDef",
    "RuntimeHintDetailsTypeDef",
    "RuntimeHintDetailsUnionTypeDef",
    "RuntimeHintValueTypeDef",
    "RuntimeHintsOutputTypeDef",
    "RuntimeHintsTypeDef",
    "RuntimeHintsUnionTypeDef",
    "SentimentResponseTypeDef",
    "SentimentScoreTypeDef",
    "SessionStateOutputTypeDef",
    "SessionStateTypeDef",
    "SlotOutputTypeDef",
    "SlotTypeDef",
    "SlotUnionTypeDef",
    "ValueOutputTypeDef",
    "ValueTypeDef",
    "ValueUnionTypeDef",
)

class ActiveContextTimeToLiveTypeDef(TypedDict):
    timeToLiveInSeconds: int
    turnsToLive: int

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ButtonTypeDef(TypedDict):
    text: str
    value: str

class ConfidenceScoreTypeDef(TypedDict):
    score: NotRequired[float]

class DeleteSessionRequestRequestTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str
    sessionId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ElicitSubSlotOutputTypeDef(TypedDict):
    name: str
    subSlotToElicit: NotRequired[Dict[str, Any]]

class ElicitSubSlotTypeDef(TypedDict):
    name: str
    subSlotToElicit: NotRequired[Mapping[str, Any]]

class GetSessionRequestRequestTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str
    sessionId: str

class RecognizedBotMemberTypeDef(TypedDict):
    botId: str
    botName: NotRequired[str]

class RuntimeHintValueTypeDef(TypedDict):
    phrase: str

class SentimentScoreTypeDef(TypedDict):
    positive: NotRequired[float]
    negative: NotRequired[float]
    neutral: NotRequired[float]
    mixed: NotRequired[float]

class ValueOutputTypeDef(TypedDict):
    interpretedValue: str
    originalValue: NotRequired[str]
    resolvedValues: NotRequired[List[str]]

class ValueTypeDef(TypedDict):
    interpretedValue: str
    originalValue: NotRequired[str]
    resolvedValues: NotRequired[Sequence[str]]

class ActiveContextOutputTypeDef(TypedDict):
    name: str
    timeToLive: ActiveContextTimeToLiveTypeDef
    contextAttributes: Dict[str, str]

class ActiveContextTypeDef(TypedDict):
    name: str
    timeToLive: ActiveContextTimeToLiveTypeDef
    contextAttributes: Mapping[str, str]

class RecognizeUtteranceRequestRequestTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str
    sessionId: str
    requestContentType: str
    sessionState: NotRequired[str]
    requestAttributes: NotRequired[str]
    responseContentType: NotRequired[str]
    inputStream: NotRequired[BlobTypeDef]

class ImageResponseCardOutputTypeDef(TypedDict):
    title: str
    subtitle: NotRequired[str]
    imageUrl: NotRequired[str]
    buttons: NotRequired[List[ButtonTypeDef]]

class ImageResponseCardTypeDef(TypedDict):
    title: str
    subtitle: NotRequired[str]
    imageUrl: NotRequired[str]
    buttons: NotRequired[Sequence[ButtonTypeDef]]

class DeleteSessionResponseTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutSessionResponseTypeDef(TypedDict):
    contentType: str
    messages: str
    sessionState: str
    requestAttributes: str
    sessionId: str
    audioStream: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class RecognizeUtteranceResponseTypeDef(TypedDict):
    inputMode: str
    contentType: str
    messages: str
    interpretations: str
    sessionState: str
    requestAttributes: str
    sessionId: str
    inputTranscript: str
    audioStream: StreamingBody
    recognizedBotMember: str
    ResponseMetadata: ResponseMetadataTypeDef

DialogActionOutputTypeDef = TypedDict(
    "DialogActionOutputTypeDef",
    {
        "type": DialogActionTypeType,
        "slotToElicit": NotRequired[str],
        "slotElicitationStyle": NotRequired[StyleTypeType],
        "subSlotToElicit": NotRequired[ElicitSubSlotOutputTypeDef],
    },
)
ElicitSubSlotUnionTypeDef = Union[ElicitSubSlotTypeDef, ElicitSubSlotOutputTypeDef]

class RuntimeHintDetailsOutputTypeDef(TypedDict):
    runtimeHintValues: NotRequired[List[RuntimeHintValueTypeDef]]
    subSlotHints: NotRequired[Dict[str, Dict[str, Any]]]

class RuntimeHintDetailsTypeDef(TypedDict):
    runtimeHintValues: NotRequired[Sequence[RuntimeHintValueTypeDef]]
    subSlotHints: NotRequired[Mapping[str, Mapping[str, Any]]]

class SentimentResponseTypeDef(TypedDict):
    sentiment: NotRequired[SentimentTypeType]
    sentimentScore: NotRequired[SentimentScoreTypeDef]

class SlotOutputTypeDef(TypedDict):
    value: NotRequired[ValueOutputTypeDef]
    shape: NotRequired[ShapeType]
    values: NotRequired[List[Dict[str, Any]]]
    subSlots: NotRequired[Dict[str, Dict[str, Any]]]

ValueUnionTypeDef = Union[ValueTypeDef, ValueOutputTypeDef]
ActiveContextUnionTypeDef = Union[ActiveContextTypeDef, ActiveContextOutputTypeDef]

class MessageOutputTypeDef(TypedDict):
    contentType: MessageContentTypeType
    content: NotRequired[str]
    imageResponseCard: NotRequired[ImageResponseCardOutputTypeDef]

ImageResponseCardUnionTypeDef = Union[ImageResponseCardTypeDef, ImageResponseCardOutputTypeDef]
DialogActionTypeDef = TypedDict(
    "DialogActionTypeDef",
    {
        "type": DialogActionTypeType,
        "slotToElicit": NotRequired[str],
        "slotElicitationStyle": NotRequired[StyleTypeType],
        "subSlotToElicit": NotRequired[ElicitSubSlotUnionTypeDef],
    },
)

class RuntimeHintsOutputTypeDef(TypedDict):
    slotHints: NotRequired[Dict[str, Dict[str, RuntimeHintDetailsOutputTypeDef]]]

RuntimeHintDetailsUnionTypeDef = Union[RuntimeHintDetailsTypeDef, RuntimeHintDetailsOutputTypeDef]

class IntentOutputTypeDef(TypedDict):
    name: str
    slots: NotRequired[Dict[str, SlotOutputTypeDef]]
    state: NotRequired[IntentStateType]
    confirmationState: NotRequired[ConfirmationStateType]

class SlotTypeDef(TypedDict):
    value: NotRequired[ValueUnionTypeDef]
    shape: NotRequired[ShapeType]
    values: NotRequired[Sequence[Mapping[str, Any]]]
    subSlots: NotRequired[Mapping[str, Mapping[str, Any]]]

class MessageTypeDef(TypedDict):
    contentType: MessageContentTypeType
    content: NotRequired[str]
    imageResponseCard: NotRequired[ImageResponseCardUnionTypeDef]

DialogActionUnionTypeDef = Union[DialogActionTypeDef, DialogActionOutputTypeDef]

class RuntimeHintsTypeDef(TypedDict):
    slotHints: NotRequired[Mapping[str, Mapping[str, RuntimeHintDetailsUnionTypeDef]]]

class InterpretationTypeDef(TypedDict):
    nluConfidence: NotRequired[ConfidenceScoreTypeDef]
    sentimentResponse: NotRequired[SentimentResponseTypeDef]
    intent: NotRequired[IntentOutputTypeDef]
    interpretationSource: NotRequired[InterpretationSourceType]

class SessionStateOutputTypeDef(TypedDict):
    dialogAction: NotRequired[DialogActionOutputTypeDef]
    intent: NotRequired[IntentOutputTypeDef]
    activeContexts: NotRequired[List[ActiveContextOutputTypeDef]]
    sessionAttributes: NotRequired[Dict[str, str]]
    originatingRequestId: NotRequired[str]
    runtimeHints: NotRequired[RuntimeHintsOutputTypeDef]

SlotUnionTypeDef = Union[SlotTypeDef, SlotOutputTypeDef]
MessageUnionTypeDef = Union[MessageTypeDef, MessageOutputTypeDef]
RuntimeHintsUnionTypeDef = Union[RuntimeHintsTypeDef, RuntimeHintsOutputTypeDef]

class GetSessionResponseTypeDef(TypedDict):
    sessionId: str
    messages: List[MessageOutputTypeDef]
    interpretations: List[InterpretationTypeDef]
    sessionState: SessionStateOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RecognizeTextResponseTypeDef(TypedDict):
    messages: List[MessageOutputTypeDef]
    sessionState: SessionStateOutputTypeDef
    interpretations: List[InterpretationTypeDef]
    requestAttributes: Dict[str, str]
    sessionId: str
    recognizedBotMember: RecognizedBotMemberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class IntentTypeDef(TypedDict):
    name: str
    slots: NotRequired[Mapping[str, SlotUnionTypeDef]]
    state: NotRequired[IntentStateType]
    confirmationState: NotRequired[ConfirmationStateType]

IntentUnionTypeDef = Union[IntentTypeDef, IntentOutputTypeDef]

class SessionStateTypeDef(TypedDict):
    dialogAction: NotRequired[DialogActionUnionTypeDef]
    intent: NotRequired[IntentUnionTypeDef]
    activeContexts: NotRequired[Sequence[ActiveContextUnionTypeDef]]
    sessionAttributes: NotRequired[Mapping[str, str]]
    originatingRequestId: NotRequired[str]
    runtimeHints: NotRequired[RuntimeHintsUnionTypeDef]

class PutSessionRequestRequestTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str
    sessionId: str
    sessionState: SessionStateTypeDef
    messages: NotRequired[Sequence[MessageUnionTypeDef]]
    requestAttributes: NotRequired[Mapping[str, str]]
    responseContentType: NotRequired[str]

class RecognizeTextRequestRequestTypeDef(TypedDict):
    botId: str
    botAliasId: str
    localeId: str
    sessionId: str
    text: str
    sessionState: NotRequired[SessionStateTypeDef]
    requestAttributes: NotRequired[Mapping[str, str]]
