import collections
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, OrderedDict, Collection, Any

from brigadier import Command, RedirectModifier

S = TypeVar('S')


# the class ouroboros keeps growing
class CommandNode(ABC, Generic[S]):
    @abstractmethod
    def is_valid_input(self, input: str) -> bool:
        return False

    @abstractmethod
    def get_name(self) -> str:
        return ""

    @abstractmethod
    def get_usage_text(self) -> str:
        return ""

    @abstractmethod
    def parse(self, reader: StringReader, contextBuilder: CommandContextBuilder[S]) -> None:
        return

    @abstractmethod
    async def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder) -> Suggestions :
        return None

    @abstractmethod
    def create_builder(self) -> ArgumentBuilder[S, Any]:
        return None

    @abstractmethod
    def get_sorted_key(self) -> str:
        return ""

    @abstractmethod
    def get_examples(self) -> Collection[str]:
        return []



class LiteralCommandNode(CommandNode):
    pass


class ArgumentCommandNode(CommandNode):
    pass


class RootCommandNode(CommandNode):
    pass


class CommandNode(ABC, Generic[S]):
    def __init__(self, command: Command[S], requirement: Callable[[S], bool], redirect: CommandNode[S],
                 modifier: RedirectModifier[S], forks: bool,
                 children: OrderedDict[str, CommandNode[S]] = collections.OrderedDict,
                 literals: OrderedDict[str, LiteralCommandNode[S]] = collections.OrderedDict,
                 arguments: OrderedDict[str, ArgumentCommandNode[S]] = collections.OrderedDict):
        self.command = command
        self.requirement = requirement
        self.redirect = redirect
        self.modifier = modifier
        self.forks = forks
        self.children = children
        self.literals = literals
        self.arguments = arguments

    def get_children(self) -> Collection[CommandNode[S]]:
        return self.children.values()  # this is a subclass of Collection so it's ok but pycharm doesn't think so

    def get_child(self, name: str) -> CommandNode[S]:
        return self.children[name]

    def can_use(self, source: S) -> bool:
        return self.requirement(source)

    def add_child(self, node: CommandNode[S]) -> None:
        if isinstance(node, RootCommandNode):
            raise TypeError('Cannot add a RootCommandNode as a child to any other CommandNode')
        name = node.getName()
        if name in self.children:
            # We've found something to merge onto
            child = self.children[name]
            if node.command is not None:
                child.command = node.command
            for grandchild in node.children:
                child.add_child(grandchild)
        else:
            self.children[name] = node
            if isinstance(node, LiteralCommandNode):
                self.literals[name] = node
            elif isinstance(node, ArgumentCommandNode):
                self.arguments[name] = node
        # Note: Mojang has a cursed stream sort thing here but it's bad and useless

    @abstractmethod
    def is_valid_input(self, input: str) -> bool:
        return False

    @abstractmethod
    def get_name(self) -> str:
        return ""

    @abstractmethod
    def get_usage_text(self) -> str:
        return ""

    @abstractmethod
    def parse(self, reader: StringReader, contextBuilder: CommandContextBuilder[S]) -> None:
        return

    @abstractmethod
    async def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder) -> Suggestions:
        return None

    @abstractmethod
    def create_builder(self) -> ArgumentBuilder[S, Any]:
        return None

    @abstractmethod
    def get_sorted_key(self) -> str:
        return ""

    @abstractmethod
    def get_examples(self) -> Collection[str]:
        return []
