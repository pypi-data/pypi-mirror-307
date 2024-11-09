from collections.abc import Callable
import asyncio
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from msgraph.generated.models.chat_message import (
    ChatMessage
)
from .flow import FlowComponent
from ..interfaces.AzureGraph import AzureGraph
from ..exceptions import ComponentError, DataNotFound, ConfigError


class MSTeamsMessages(AzureGraph, FlowComponent):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.channel_id: str = kwargs.pop('channel_id', None)
        self.team_id: str = kwargs.pop('team_id', None)
        self.chat_id: str = kwargs.pop('chat_id', None)
        self.chat_name: str = kwargs.pop('chat_name', None)
        self.start_time: str = kwargs.pop('start_time', None)
        self.end_time: str = kwargs.pop('end_time', None)
        self.as_dataframe: bool = kwargs.get('as_dataframe', False)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        await super().start(**kwargs)
        self.processing_credentials()
        if not self.team_id:
            raise ConfigError(
                "Must Provide a *team_id* Attribute."
            )
        # Processing Channel and Team:
        self.team_id = self.mask_replacement(self.team_id)
        self.channel_id = self.mask_replacement(self.channel_id)
        self.chat_id = self.mask_replacement(self.chat_id)
        # Processing the start time and end time:
        if self.start_time:
            self.start_time = self.mask_replacement(self.start_time)
            if isinstance(self.start_time, str):
                # convert to datetime with Z
                self.start_time = datetime.strptime(
                    self.start_time, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
        else:
            # 72 hours ago
            self.start_time = (datetime.utcnow() - timedelta(hours=72)).isoformat() + 'Z'
        if self.end_time:
            self.end_time = self.mask_replacement(self.end_time)
            if isinstance(self.end_time, str):
                # convert to datetime with Z
                self.end_time = datetime.strptime(
                    self.end_time, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
        else:
            self.end_time = datetime.utcnow().isoformat() + 'Z'  # Current time
        return True

    def _process_messages(self, messages: list) -> list:
        msgs = []
        for message in messages:
            if isinstance(message, ChatMessage):
                # extracting info from message:
                user = {}
                if message.from_:
                    usr = message.from_.user
                    user = {
                        "sender_id": usr.id,
                        "sender_name": usr.display_name
                    }
                content = message.body.content
                soup = BeautifulSoup(content, 'html.parser')
                stripped_content = soup.get_text()
                msg = {
                    "message_id": message.id,
                    # "attachments": message.attachments,
                    **user,
                    "chat_id": message.chat_id,
                    "created_date": message.created_date_time,
                    "policy_violation": message.policy_violation,
                    "content": content,
                    "text": stripped_content,
                }
                msgs.append(msg)
            else:
                msg = {}
                sender_name = message.get('from', {}).get('user', {}).get('displayName', 'Unknown')
                content = message.get('body', {}).get('content', '')
                created_time = message.get('createdDateTime', '')
                print(f"[{created_time}] {sender_name}: {content}")
                msg = {
                    "sender_name": sender_name,
                    "content": content,
                    "created_time": created_time
                }
                msgs.append(msg)
        return msgs

    async def run(self):
        async with self.open() as client:
            try:
                if self.chat_name is not None:
                    # Find chat id by name:
                    chat = await client.find_chat_by_name(self.chat_name)
                    messages = await client.get_chat_messages(
                        chat_id=chat.id,
                        start_time=self.start_time,
                        end_time=self.end_time
                    )
                elif self.chat_id is not None:
                    # Using the chat Id for extracting chat messages:
                    messages = await client.get_chat_messages(
                        chat_id=self.chat_id,
                        start_time=self.start_time,
                        end_time=self.end_time
                    )
                elif self.channel_id is not None:
                    messages = await client.get_msteams_channel_messages(
                        team_id=self.team_id,
                        channel_id=self.channel_id,
                        start_time=self.start_time,
                        end_time=self.end_time
                    )
                    if not messages:
                        raise DataNotFound(
                            f"Found no messages on MS Team {self.team_id}:{self.channel_id}"
                        )
                # Processing the messages:
                msgs = self._process_messages(messages)
                df = pd.DataFrame(msgs)
                if self.as_dataframe is True:
                    # return only the dataframe:
                    self._result = df
                    return self._result
                self._result = {
                    "data": df,
                    "messages": msgs,
                    "raw_messages": messages
                }
                self.add_metric('NUM_MESSAGES', len(messages))
                return self._result
            except Exception as exc:
                self._logger.error(
                    f"Error getting Teams Channel Messages: {exc}"
                )
                raise ComponentError(
                    f"Error getting Teams Channel Messages: {exc}"
                )
