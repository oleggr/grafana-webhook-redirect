import os
import tempfile
from typing import Optional, Union

import aiohttp
from fastapi.responses import Response

from aiologger import Logger
from aiologger.levels import LogLevel
from aiologger.formatters.base import Formatter

from async_icq.helpers import InlineKeyboardMarkup, KeyboardButton

from app.middleware.bot import notifier
from app.middleware.chrome_screen import take_screen
from app.dantic.models import OldEvent, NewEvent


log = Logger.with_default_handlers(
    name='fake-kata',
    formatter=Formatter(
        '%(asctime)s - '
        '%(name)s - '
        '%(levelname)s - '
        '%(module)s:%(funcName)s:%(lineno)d - '
        '%(message)s'
    ),
    level=LogLevel.DEBUG
)


async def event_handler(
        event: Union[OldEvent, NewEvent],
        chatId: str,
        token: Optional[str] = None
) -> Response:
    """
    Функция обработки Event от Grafana
    :param event: Event от Grafana
    :param chatId: ID чата в ICQ/Myteam
    :param token: токен бота (необязательный переметр)
    :return: fastapi.responses.Response
    """

    #  Подменяем токен бота если он был указан,
    #  в противном случае используем указанный в переменной окружения
    if token:
        notifier.token = token
    else:
        notifier.token = os.getenv('TOKEN')

    text = event.to_string()

    print(text)

    keyboard = InlineKeyboardMarkup()

    # Преобразуем эвент в текстовое сообщение
    if isinstance(event, OldEvent):

        keyboard.row(
            KeyboardButton(
                text=f'[URL] {event.ruleName}',
                url=event.ruleUrl
            )
        )
    else:

        keyboard.row(
            KeyboardButton(
                text=f'[URL] {event.externalURL}',
                url=event.externalURL
            )
        )

    if isinstance(event, OldEvent):

        if event.imageUrl:
            # Если Grafana отправляет в
            # Event ссылку на график - пытаемся его сохранить
            try:
                with tempfile.NamedTemporaryFile(
                        prefix='graphic.', suffix='.png') as upstream:
                    async with aiohttp.ClientSession() as session:
                        resp = await session.get(event.imageUrl)

                        upstream.write(
                            await resp.read()
                        )

                    await notifier.send_file(
                        chatId=chatId,
                        file_path=upstream.name,
                        caption=text,
                        inlineKeyboardMarkup=keyboard
                    )
            except Exception as error:
                await log.exception(error)  # Обрабатываем ошибку
                # если скачать график не удалось

                await notifier.send_text(
                    chatId=chatId,
                    text=text,
                    inlineKeyboardMarkup=keyboard
                )
        else:
            try:
                with tempfile.NamedTemporaryFile(
                        prefix='graphic.', suffix='.png') as upstream:

                    upstream.write(
                        take_screen(event.ruleUrl)
                    )

                    await notifier.send_file(
                        chatId=chatId,
                        file_path=upstream.name,
                        caption=text,
                        inlineKeyboardMarkup=keyboard
                    )
            except Exception as error:
                await log.exception(error)  # Обрабатываем ошибку
                # если скачать график не удалось

                await notifier.send_text(
                    chatId=chatId,
                    text=text,
                    inlineKeyboardMarkup=keyboard
                )

    else:
        try:
            with tempfile.NamedTemporaryFile(
                    prefix='graphic.', suffix='.png') as upstream:
                upstream.write(
                    take_screen(event.alerts[0].panelURL)
                )

                await notifier.send_file(
                    chatId=chatId,
                    file_path=upstream.name,
                    caption=text,
                    inlineKeyboardMarkup=keyboard
                )
        except Exception as error:
            await log.exception(error)

            # Если imageUrl не указан - отправляем обычное сообщение
            await notifier.send_text(
                chatId=chatId,
                text=text,
                inlineKeyboardMarkup=keyboard
            )

    return Response()
