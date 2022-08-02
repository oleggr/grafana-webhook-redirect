from typing import Optional, Union, Dict, List, Any

from enum import Enum
from pydantic import BaseModel, AnyUrl

from app.middleware.ext import url_change


class EnumedBaseModel(BaseModel):

    class Config:
        """
        Конфиг модели для включения использования Enum типа
        """
        use_enum_values = True


class State(str, Enum):
    """
    Enum статусов Legacy Alert от Grafana
    """
    ok: str = 'ok'
    paused: str = 'paused'
    alerting: str = 'alerting'
    pending: str = 'pending'
    no_data: str = 'no data'


class Status(str, Enum):
    """
    Enum статусов Alert от Grafana
    """
    firing: str = 'firing'
    resolved: str = 'resolved'


class evalMatch(EnumedBaseModel):
    """
    Модель для значений метрик в эвенте от Grafana
    """
    value: Union[str, int]
    metric: str
    tags: Optional[Union[str, Dict[Any, Any]]]

    def __str__(self):

        text = f'{self.metric}: {self.value}'

        if self.tags:

            text += ' ('

            for tag_name, tag_value in self.tags.copy().items():
                text += f'{tag_name}={tag_value}, '

            text += ')'

        text += '\n'

        return text


class Alert(EnumedBaseModel):
    """
    Модель Alert от Grafana (new Alert)
    """
    status: Status
    labels: Union[Dict[Any, Any], Dict]
    annotations: Union[Dict[Any, Any], Dict]
    startsAt: str
    endsAt: str
    valueString: str
    generatorURL: Union[AnyUrl, str]
    fingerprint: str
    silenceURL: Union[AnyUrl, str]
    dashboardURL: Optional[Union[AnyUrl, str]]
    panelURL: Optional[Union[AnyUrl, str]]

    def __init__(self, **kwargs):
        if kwargs.get("panelURL"):
            kwargs["panelURL"] = url_change(kwargs.get("panelURL"))
        if kwargs.get("dashboardURL"):
            kwargs["dashboardURL"] = url_change(kwargs.get("dashboardURL"))
        if kwargs.get("generatorURL"):
            kwargs["generatorURL"] = url_change(kwargs.get("generatorURL"))
        super().__init__(**kwargs)

    def __str__(self):

        text = '- ' + ', '.join([
                f'{key}={value}' for key, value in self.labels.items()
            ])

        if self.dashboardURL:
            text += f' <a href="{self.dashboardURL}">DASHBOARD</a>'

        if self.panelURL:
            text += f' <a href="{self.panelURL}">PANEL</a>'

        if self.silenceURL:
            text += f' <a href="{self.silenceURL}">SILENCE</a>'

        return text


class NewEvent(EnumedBaseModel):
    """
    Модель для эвента от Grafana (New Alert)
    """
    title: str
    message: Optional[str]
    receiver: str
    status: Status
    state: Optional[State]
    orgId: int
    alerts: List[Alert]
    groupLabels: Union[Dict[Any, Any], Dict]
    commonLabels: Union[Dict[Any, Any], Dict]
    commonAnnotations: Union[Dict[Any, Any], Dict]
    externalURL: AnyUrl
    version: Union[str, int]
    groupKey: str
    truncatedAlerts: int

    def to_string(self):

        text = '<b>{self.title}</b>\n'

        if self.state:
            text += 'State: {self.state}\n\n'

        if self.commonLabels:
            text += 'Common labels:\n'
            for label, value in self.commonLabels.items():
                text += f'- {label}: {value}\n'
            text += '\n'

        if self.groupLabels:
            text += 'Group labels:\n'
            for label, value in self.groupLabels.items():
                text += f'- {label}: {value}\n'
            text += '\n'

        if self.commonAnnotations:
            text += 'Annotations:\n'
            for label, value in self.commonAnnotations.items():
                text += f'- {label}: {value}\n'
            text += '\n'

        if self.alerts:

            text += 'Alerts:\n'

            for alert in self.alerts:
                text += str(alert)

        return text.format(self=self)


class OldEvent(EnumedBaseModel):
    """
    Модель для эвента от Grafana (Legacy Alert)
    """

    title: str
    ruleId: int
    ruleName: str
    state: State
    evalMatches: List[evalMatch]
    orgId: int
    dashboardId: int
    panelId: int
    tags: Union[Dict[Any, Any], Dict]
    ruleUrl: str
    imageUrl: Optional[AnyUrl]
    message: Optional[str]

    def __init__(self, **kwargs):
        if kwargs.get("ruleUrl"):
            kwargs["ruleUrl"] = url_change(kwargs.get("ruleUrl"))
        super().__init__(**kwargs)

    def to_string(self) -> str:
        """
        Приведение эвента к форме сообщения
        :return: эвент в виде str
        """
        formatted = '<b>{self.title}</b>\n' \
                    'State: {self.state}\n'

        if self.message:
            formatted += 'Message: {self.message}\n\n'

        if self.evalMatches:

            formatted += 'Metrics:\n'

            for evalMatcher in self.evalMatches:
                formatted += str(evalMatcher)

        return formatted.format(self=self)
