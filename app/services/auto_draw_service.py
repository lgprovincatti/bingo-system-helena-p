import asyncio

from app.core.game_state import game_state

from app.services.bingo_service import BingoService

from app.core.websocket_manager import manager


class AutoDrawService:

    @classmethod
    async def start(cls):

        if game_state["automatic_mode"]:
            return

        game_state["automatic_mode"] = True

        game_state["paused"] = False

        asyncio.create_task(
            cls.auto_draw_loop()
        )

    @classmethod
    async def auto_draw_loop(cls):

        while game_state["automatic_mode"]:

            if game_state["game_finished"]:
                break

            if not game_state["paused"]:

                result = BingoService.draw_number()

                if result is None:

                    game_state["automatic_mode"] = False

                    await manager.broadcast({
                        "type": "GAME_FINISHED"
                    })

                    break

                await manager.broadcast({
                    "type": "DRAW_NUMBER",
                    "payload": {
                        "current_number": result,
                        "drawn_numbers": BingoService.get_drawn_numbers()
                    }
                })

            await asyncio.sleep(
                game_state["interval_seconds"]
            )

    @classmethod
    def pause(cls):

        game_state["paused"] = True

    @classmethod
    def resume(cls):

        game_state["paused"] = False

    @classmethod
    def stop(cls):

        game_state["automatic_mode"] = False

        game_state["paused"] = False