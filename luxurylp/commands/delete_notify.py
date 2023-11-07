from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from luxurylp.logger import logger_decorator
from luxurylp.database import Database
from luxurylp.rules import DeleteNotifyRule
from luxurylp.utils import edit_message

user = Blueprint(
    name='delete_notify_blueprint'
)


@user.on.message_handler(DeleteNotifyRule())
@logger_decorator
async def delete_notify_wrapper(message: Message):
    await message.api.messages.delete(message_ids=[message.id])


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -уведы")
@logger_decorator
async def activate_delete_all_notify_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.delete_all_notify = True
    db.save()
    await edit_message(
        message,
        "✅ Удаление уведомлений включено"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +уведы")
@logger_decorator
async def deactivate_delete_all_notify_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.delete_all_notify = False
    db.save()
    await edit_message(
        message,
        "✅ Удаление уведомлений отключено"
    )
