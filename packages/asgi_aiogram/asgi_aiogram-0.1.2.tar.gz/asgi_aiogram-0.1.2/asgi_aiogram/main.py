from asyncio import create_task
from logging import getLogger
from typing import Any

from aiogram import Dispatcher
from aiogram.types import Update

from asgi_aiogram.responses import ok, error
from asgi_aiogram.asgi import read_body
from asgi_aiogram.strategy.base import BaseStrategy
from asgi_aiogram.types import ScopeType


class ASGIAiogram:
    def __init__(self,
        dispatcher: Dispatcher,
        strategy: BaseStrategy,
        handle_as_tasks: bool = True,
        handle_signals: bool = True,
        **kwargs: Any
    ):
        self.dispatcher = dispatcher
        self.handle_as_tasks = handle_as_tasks
        self.handle_signals = handle_signals
        self.strategy = strategy
        self.kwargs = {
            "dispatcher": self.dispatcher,
            **self.dispatcher.workflow_data,
            **kwargs,
        }
        self.kwargs.pop("bot", None)
        self.logger = getLogger("asgi_aiogram")
        self.task_list = set()

    async def post(self, scope: ScopeType, receive, send):
        if await self.strategy.verify_path(scope["path"]):
            bot = await self.strategy.resolve_bot(scope)
            if bot is None:
                return
            try:
                cor = self.dispatcher.feed_update(
                    bot=bot,
                    update=Update.model_validate_json(await read_body(receive)),
                )
                if self.handle_as_tasks:
                    handle_update_task = create_task(cor)
                    self.task_list.add(handle_update_task)
                    handle_update_task.add_done_callback(self.task_list.discard)
                else:
                    await cor
                    # if isinstance(response, TelegramMethod):
                    #     form = bot.session.build_form_data(bot, response)
                    #     form.add_field(
                    #         name="method",
                    #         value=response.__api_method__
                    #     )
                    #     await answer(send, form)
                await ok(send)
                return
            except Exception as e:
                self.logger.error(e)
                await error(send)
            return
        self.logger.warning("unknown path: %s", scope['path'])

    async def get(self, scope: ScopeType, receive, send):
        pass

    async def lifespan(self, scope: ScopeType, receive, send):
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                try:
                    await self.dispatcher.emit_startup(
                        **self.kwargs,
                        bots=self.strategy.bots,
                        bot=self.strategy.bot,
                    )
                    await self.strategy.startup()
                except Exception as e:
                    self.logger.error(e)
                    await send({'type': 'lifespan.startup.failed'})
                else:
                    await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                try:
                    try:
                        await self.dispatcher.emit_shutdown(
                            **self.kwargs,
                            bots=self.strategy.bots,
                            bot=self.strategy.bot
                        )
                    finally:
                        await self.strategy.shutdown()
                except Exception as e:
                    self.logger.error(e)
                    await send({'type': 'lifespan.shutdown.failed'})
                    return
                else:
                    await send({'type': 'lifespan.shutdown.complete'})
                    return

            else:
                self.logger.warning("unknown lifespan type: %s", message['type'])

    async def http(self, scope: ScopeType, receive, send):
        if scope["method"] == "POST":
            return await self.post(scope, receive, send)
        if scope["method"] == "GET":
            return await self.get(scope, receive, send)
        self.logger.info("unsupported method: %s", scope['type'])



    async def __call__(self, scope: ScopeType, receive, send):
        if scope['type'] == 'http':
            return await self.http(scope, receive, send)
        if scope['type'] == 'lifespan':
            return await self.lifespan(scope, receive, send)
        self.logger.warning("unknown event type:", scope['type'])