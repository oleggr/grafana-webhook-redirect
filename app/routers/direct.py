from typing import Union

from fastapi import APIRouter, Request, Path

from app.dantic.models import OldEvent, NewEvent


router = APIRouter()


@router.post('/{chatId}')
async def grafana_events(
        request: Request,
        event: Union[OldEvent, NewEvent],
        chatId: str = Path(
            ...,
            title='ID чата',
            description='ID чата в ICQ/Myteam, '
                        'куда должно быть отправленно сообщение'
        ),
):
    """
    Метод для получения webhook от Grafana без указания bot_token в path
    """

    return await request.app.event_handler(event, chatId)
