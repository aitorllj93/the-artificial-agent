
import asyncio
import logging
import coloredlogs
import core.config as config
import core.registry as registry
from core.adapters import telegram

coloredlogs.install(
    fmt='%(asctime)s - %(name)s %(levelname)s %(message)s',
)

logging.basicConfig(
    level=logging.DEBUG,
)

logger = logging.getLogger()

registry.register_interpreters(config.get_value('interpreters', []))
registry.register_slash_commands(config.get_value('slashCommands', []))
registry.register_commands(config.get_value('commands', []))
registry.register_personalities(config.get_value('personalities', []))
telegram.register_schedule_jobs(config.get_value('schedules', []))


async def run(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    try:
        runner = registry.get_active_interpreter_runner()

        await runner(update, context)
    except Exception as e:
        print(e)
        logger.exception(e)


# async def main() -> None:
#     logger.info('Starting bot')
#     await telegram.connect(run)


# asyncio.run(main())
telegram.connect(run)
