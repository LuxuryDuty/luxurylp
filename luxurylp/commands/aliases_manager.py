from typing import List, Dict

import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from luxurylp import const
from luxurylp.logger import logger, logger_decorator
from luxurylp.database import Database, Alias
from luxurylp.utils import edit_message

user = Blueprint(
    name='aliases_manager_blueprint'
)


def add_alias(database: Database, name: str, command_from: str, command_to: str) -> Alias:
    new_alias = Alias(**{
        'name': name,
        'command_from': command_from,
        'command_to': command_to
    })
    database.aliases.append(new_alias)
    database.save()
    return new_alias


def remove_alias(database: Database, alias: Alias) -> None:
    database.aliases.remove(alias)
    database.save()


def show_aliases(database: Database) -> str:
    if len(database.aliases):
        message = '📃 Ваши алиасы:\n'
        index = 1
        for alias in database.aliases:
            message += f"{index}. {alias.name} ({alias.command_from} -> !л {alias.command_to})\n"
            index += 1
        return message
    else:
        return "⚠ У вас нет алиасов"


def delete_last_space(value: str) -> str:
    if value[-1] == ' ':
        return value[:-1]
    return value


@user.on.message_handler(
    FromMe(),
    text="<prefix:service_prefix> +алиас <alias_name>\n<command_from>\n<command_to>"
)
@logger_decorator
async def add_alias_wrapper(message: Message, alias_name: str, command_from: str, command_to: str, *args, **kwargs):
    db = Database.get_current()
    logger.info(f"Создание алиаса\n")
    alias_name = delete_last_space(alias_name)
    command_from = delete_last_space(command_from)
    command_to = delete_last_space(command_to)

    for alias in db.aliases:
        if alias_name == alias.name:
            await edit_message(
                message,
                f"⚠ Алиас <<{alias_name}>> уже существует"
            )
            return

    new_alias = add_alias(db, alias_name, command_from, command_to)
    await edit_message(
        message,
        f"✅ Новый алиас <<{alias_name}>> создан\n"
        f"Команды: {new_alias.command_from} -> !л {command_to}"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> алиасы")
@logger_decorator
async def show_aliases_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    logger.info(f"Просмотр алиасов\n")
    await edit_message(
        message,
        show_aliases(db)
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -алиас <alias_name>")
@logger_decorator
async def remove_alias_wrapper(message: Message, alias_name: str, **kwargs):
    db = Database.get_current()
    logger.info(f"Удаление алиаса\n")
    alias_name = delete_last_space(alias_name)
    for alias in db.aliases:
        if alias_name == alias.name:
            remove_alias(db, alias)
            await edit_message(
                message,
                f"✅ Алиас <<{alias_name}>> удален"
            )
            return

    await edit_message(
        message,
        f'⚠ Алиас <<{alias_name}>> не найден'
    )





def generate_aliases_pack_description(pack: List[Alias]) -> str:
    message = ""
    index = 1
    for alias in pack:
        message += f"{index}. {alias.name} ({alias.command_from} -> !л {alias.command_to})\n"
        index += 1
    return message


def check_name_duplicates(db: Database, pack: List[Alias]) -> bool:
    current_alias_names = [alias.name for alias in db.aliases]
    for alias in pack:
        if alias.name in current_alias_names:
            return False
    return True


