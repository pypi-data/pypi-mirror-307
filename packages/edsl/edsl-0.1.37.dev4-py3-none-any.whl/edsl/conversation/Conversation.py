from collections import UserList
import asyncio
import inspect
from typing import Optional, Callable
from edsl import Agent, QuestionFreeText, Results, AgentList, ScenarioList, Scenario
from edsl.questions import QuestionBase
from edsl.results.Result import Result

from edsl.data import Cache

from edsl.conversation.next_speaker_utilities import (
    default_turn_taking_generator,
    speaker_closure,
)


class AgentStatement:
    def __init__(self, statement: Result):
        self.statement = statement

    @property
    def agent_name(self):
        return self.statement["agent"]["name"]

    def to_dict(self):
        return self.statement.to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(Result.from_dict(data))

    @property
    def text(self):
        return self.statement["answer"]["dialogue"]


class AgentStatements(UserList):
    def __init__(self, data=None):
        super().__init__(data)

    @property
    def transcript(self):
        return [{s.agent_name: s.text} for s in self.data]

    def to_dict(self):
        return [d.to_dict() for d in self.data]

    @classmethod
    def from_dict(cls, data):
        return cls([AgentStatement.from_dict(d) for d in data])


class Conversation:
    """A conversation between a list of agents. The first agent in the list is the first speaker.
    After that, order is determined by the next_speaker function.
    The question asked to each agent is determined by the next_statement_question.
    """

    def __init__(
        self,
        agent_list: AgentList,
        max_turns: int = 20,
        stopping_function: Optional[Callable] = None,
        next_statement_question: Optional[QuestionBase] = None,
        next_speaker_generator: Optional[Callable] = None,
        verbose: bool = False,
        conversation_index: Optional[int] = None,
        cache=None,
    ):
        if cache is None:
            self.cache = Cache()
        else:
            self.cache = cache

        self.agent_list = agent_list
        self.verbose = verbose
        self.agent_statements = []
        self._conversation_index = conversation_index

        self.agent_statements = AgentStatements()

        self.max_turns = max_turns

        if next_statement_question is None:
            self.next_statement_question = QuestionFreeText(
                question_text="You are {{ agent_name }}. This is the converstaion so far: {{ conversation }}. What do you say next?",
                question_name="dialogue",
            )

        # Determine how the next speaker is chosen
        if next_speaker_generator is None:
            func = default_turn_taking_generator
        else:
            func = next_speaker_generator

        self.next_speaker = speaker_closure(
            agent_list=self.agent_list, generator_function=func
        )

        # Determine when the conversation ends
        if stopping_function is None:
            self.stopping_function = lambda agent_statements: False
        else:
            self.stopping_function = stopping_function

    async def continue_conversation(self, **kwargs) -> bool:
        if len(self.agent_statements) >= self.max_turns:
            return False

        if inspect.iscoroutinefunction(self.stopping_function):
            should_stop = await self.stopping_function(self.agent_statements, **kwargs)
        else:
            should_stop = self.stopping_function(self.agent_statements, **kwargs)

        return not should_stop

    def add_index(self, index) -> None:
        self._conversation_index = index

    @property
    def conversation_index(self):
        return self._conversation_index

    def to_dict(self):
        return {
            "agent_list": self.agent_list.to_dict(),
            "max_turns": self.max_turns,
            "verbose": self.verbose,
            "agent_statements": [d.to_dict() for d in self.agent_statements],
            "conversation_index": self.conversation_index,
        }

    @classmethod
    def from_dict(cls, data):
        agent_list = AgentList.from_dict(data["agent_list"])
        max_turns = data["max_turns"]
        verbose = data["verbose"]
        agent_statements = (AgentStatements.from_dict(data["agent_statements"]),)
        conversation_index = data["conversation_index"]
        return cls(
            agent_list=agent_list,
            max_turns=max_turns,
            verbose=verbose,
            results_data=agent_statements,
            conversation_index=conversation_index,
        )

    def to_results(self):
        return Results(data=[s.statement for s in self.agent_statements])

    def summarize(self):
        d = {
            "num_agents": len(self.agent_list),
            "max_turns": self.max_turns,
            "conversation_index": self.conversation_index,
            "transcript": self.to_results().select("agent_name", "dialogue").to_list(),
            "number_of_agent_statements": len(self.agent_statements),
        }
        return Scenario(d)

    async def get_next_statement(self, *, index, speaker, conversation):
        q = self.next_statement_question
        assert q.parameters == {"agent_name", "conversation"}, q.parameters
        results = await q.run_async(
            index=index,
            conversation=conversation,
            conversation_index=self.conversation_index,
            agent_name=speaker.name,
            agent=speaker,
            just_answer=False,
            cache=self.cache,
            model=speaker.model,
        )
        return results[0]

    def converse(self):
        return asyncio.run(self._converse())

    async def _converse(self):
        i = 0
        while await self.continue_conversation():
            speaker = self.next_speaker()

            next_statement = AgentStatement(
                statement=await self.get_next_statement(
                    index=i,
                    speaker=speaker,
                    conversation=self.agent_statements.transcript,
                )
            )
            self.agent_statements.append(next_statement)
            if self.verbose:
                print(f"'{speaker.name}':{next_statement.text}")
                print("\n")
            i += 1


class ConversationList:
    """A collection of conversations to be run in parallel."""

    def __init__(self, conversations: list[Conversation], cache=None):
        self.conversations = conversations
        for i, conversation in enumerate(self.conversations):
            conversation.add_index(i)

        if cache is None:
            self.cache = Cache()
        else:
            self.cache = cache

        for c in self.conversations:
            c.cache = self.cache

    async def run_conversations(self):
        await asyncio.gather(*[c._converse() for c in self.conversations])

    def run(self) -> None:
        """Run all conversations in parallel"""
        asyncio.run(self.run_conversations())

    def to_dict(self) -> dict:
        return {"conversations": c.to_dict() for c in self.conversations}

    @classmethod
    def from_dict(cls, data):
        conversations = [Conversation.from_dict(d) for d in data["conversations"]]
        return cls(conversations)

    def to_results(self) -> Results:
        """Return the results of all conversations as a single Results"""
        first_convo = self.conversations[0]
        results = first_convo.to_results()
        for conv in self.conversations[1:]:
            results += conv.to_results()
        return results

    def summarize(self) -> ScenarioList:
        return ScenarioList([c.summarize() for c in self.conversations])
