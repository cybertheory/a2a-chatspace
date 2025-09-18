import asyncio
import os
from typing import Tuple

from mautrix.appservice import AppService
from mautrix.client import Client
from mautrix.types import Event, MessageEvent, MessageType, RoomID, UserID

from llm1.llm1_bot import get_gemini_response
from llm2.llm2_bot import get_ollama_response


def _choose_model_and_strip(text: str, last_model: str) -> Tuple[str, str]:
    if not isinstance(text, str):
        return ("gemini", "")
    lowered = text.lstrip()
    if lowered.startswith("/gemini"):
        return ("gemini", lowered.split(" ", 1)[1] if " " in lowered else "")
    if lowered.startswith("/ollama") or lowered.startswith("/llama"):
        return ("ollama", lowered.split(" ", 1)[1] if " " in lowered else "")
    next_model = "ollama" if last_model == "gemini" else "gemini"
    return (next_model, text)


class LLMBridge:
    def __init__(self) -> None:
        hs_address = os.getenv("SYNAPSE_ADDRESS", "http://localhost:8008")
        domain = os.getenv("SYNAPSE_DOMAIN", "localhost")
        as_id = os.getenv("AS_ID", "autonomoussphere")
        as_token = os.getenv("AS_TOKEN", "YOUR_AS_TOKEN")
        hs_token = os.getenv("HS_TOKEN", "YOUR_HS_TOKEN")
        bot_localpart = os.getenv("AS_BOT", "_as_master")
        bind_addr = os.getenv("AS_BIND_ADDR", "0.0.0.0")
        bind_port = int(os.getenv("AS_PORT", "29333"))

        self.appservice = AppService(
            id=as_id,
            as_token=as_token,
            hs_token=hs_token,
            server=hs_address,
            appservice_host=bind_addr,
            appservice_port=bind_port,
        )
        self.bot = self.appservice.intent
        self.bot.user_id = UserID(f"@{bot_localpart}:{domain}")
        self._last_model = "ollama"

        @self.appservice.on(Event)
        async def on_event(evt: Event) -> None:
            if not isinstance(evt, MessageEvent):
                return
            if evt.content.msgtype != MessageType.TEXT:
                return
            if evt.sender == self.bot.user_id:
                return

            room_id: RoomID = evt.room_id
            body: str = evt.content.body or ""
            model, prompt = _choose_model_and_strip(body, self._last_model)
            self._last_model = model

            try:
                if model == "gemini":
                    reply = get_gemini_response(prompt)
                else:
                    reply = get_ollama_response(prompt)
            except Exception as exc:
                reply = f"Error from {model}: {exc}"

            await self.bot.send_text(room_id, reply)

    async def run(self) -> None:
        await self.appservice.start()


def run_bridge_blocking() -> None:
    bridge = LLMBridge()
    asyncio.get_event_loop().run_until_complete(bridge.run())


if __name__ == "__main__":
    run_bridge_blocking()


