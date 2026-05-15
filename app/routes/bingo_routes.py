import os
import sys

from fastapi import APIRouter
from fastapi import Request

from fastapi.responses import StreamingResponse

from fastapi.templating import Jinja2Templates

from app.services.bingo_service import BingoService
from app.services.auto_draw_service import AutoDrawService
from app.services.pdf_service import PDFService

from app.core.websocket_manager import manager
from app.core.game_state import game_state


def get_templates_path():

    if getattr(sys, "frozen", False):

        return os.path.join(
            sys._MEIPASS,
            "app",
            "templates"
        )

    return "app/templates"


router = APIRouter()

templates = Jinja2Templates(
    directory=get_templates_path()
)


@router.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.post("/draw")
async def draw_number():

    result = BingoService.draw_number()

    if result is None:

        await manager.broadcast({
            "type": "GAME_FINISHED"
        })

        return {
            "success": False
        }

    await manager.broadcast({
        "type": "DRAW_NUMBER",
        "payload": {
            "current_number": result,
            "drawn_numbers": BingoService.get_drawn_numbers()
        }
    })

    return {
        "success": True,
        "data": result
    }


@router.post("/reset")
async def reset_game():

    AutoDrawService.stop()

    BingoService.reset_game()

    await manager.broadcast({
        "type": "RESET_GAME"
    })

    return {
        "success": True
    }


@router.post("/auto/start")
async def start_auto_draw():

    await AutoDrawService.start()

    await manager.broadcast({
        "type": "AUTO_STARTED"
    })

    return {
        "success": True
    }


@router.post("/auto/pause")
async def pause_auto_draw():

    AutoDrawService.pause()

    await manager.broadcast({
        "type": "AUTO_PAUSED"
    })

    return {
        "success": True
    }


@router.post("/auto/resume")
async def resume_auto_draw():

    AutoDrawService.resume()

    await manager.broadcast({
        "type": "AUTO_RESUMED"
    })

    return {
        "success": True
    }


@router.post("/auto/interval/{seconds}")
async def change_auto_interval(seconds: int):

    allowed_values = [3, 5, 10]

    if seconds not in allowed_values:

        return {
            "success": False,
            "message": "Valor inválido"
        }

    game_state["interval_seconds"] = seconds

    return {
        "success": True,
        "interval": seconds
    }


@router.get("/cards/download")
async def download_cards_pdf(quantity: int = 4):

    if quantity < 4 or quantity % 4 != 0:

        quantity = 4

    print(f"\nQuantidade recebida: {quantity}\n")

    pdf_buffer = PDFService.generate_cards_pdf(
        quantity=quantity
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                "attachment; filename=cartelas_bingo.pdf"
        }
    )