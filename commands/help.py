from signalbot import Command, Context, triggered

HELP_TEXT = (
    "/plate [LICENSE PLATE] - Check if a plate is monitored\n"
    "Juntos 215-218-9079\n"
    "/help - Show this message\n"
    "Fuck ICE GO BIRDS \U0001F985"
)


class HelpCommand(Command):
    @triggered("/help")
    async def handle(self, c: Context) -> None:
        await c.send(HELP_TEXT)