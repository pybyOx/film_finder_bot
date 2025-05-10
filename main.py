from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from database.models import create_models
from database.models import delete_user

if __name__ == "__main__":
    create_models()
    delete_user(395578226)
    set_default_commands(bot)
    bot.infinity_polling()

