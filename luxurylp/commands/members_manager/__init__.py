from luxurylp.commands.members_manager import ignored
from luxurylp.commands.members_manager import ignored_global
from luxurylp.commands.members_manager import muted
from luxurylp.commands.members_manager import trusted

users_bp = (
    ignored.user,
    ignored_global.user,
    muted.user,
    trusted.user,
)
