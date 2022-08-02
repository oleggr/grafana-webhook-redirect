from typing import Union

from fastapi import APIRouter, Request, Path

from app.dantic.models import OldEvent, NewEvent
from app.middleware.handler import event_handler


router = APIRouter()


@router.post('/{token}/{chatId}')
async def grafana_events(
        request: Request,
        # event: Union[OldEvent, NewEvent],
        token: str = Path(
            ...,
            title='Токен от бота'
        ),
        chatId: str = Path(
            ...,
            title='ID чата',
            description='ID чата в ICQ/Myteam, '
                        'куда должно быть отправленно сообщение'
        ),
):
    """
    Метод для получения webhook от Grafana с указанием bot_token в path
    """

    tmp = await request.json()

    event = OldEvent(
        title       = tmp['title'],
        ruleId      = tmp['ruleId'],
        ruleName    = tmp['ruleName'],
        state       = tmp['state'],
        evalMatches = tmp['evalMatches'],
        orgId       = tmp['orgId'],
        dashboardId = tmp['dashboardId'],
        panelId     = tmp['panelId'],
        tags        = tmp['tags'],
        ruleUrl     = tmp['ruleUrl'],
        imageUrl    = tmp['imageUrl'],
        message     = tmp['message'],
    )

    return await event_handler(event, chatId, token)
