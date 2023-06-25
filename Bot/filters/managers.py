import typing

from aiogram.dispatcher.filters import BoundFilter

from Bot.config import Config


class ManagerFilter(BoundFilter):
    key = 'is_manager'

    def __init__(self, is_manager: typing.Optional[bool] = None):
        self.is_manager = is_manager

    async def check(self, obj):
        if self.is_manager is None:
            return False
        config: Config = obj.bot.get('config')
        return (obj.from_user.id in config.tg_bot.manager_ids) == self.is_manager
