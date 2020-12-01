from typing import TypeVar, Mapping, Any, List, Generic, Type, overload

from brigadier import Command, RedirectModifier, ImmutableStringReader
from brigadier.tree import CommandNode

S = TypeVar('S')
T = TypeVar('T')
V = TypeVar('V')


# necessary for type hint linting to understand that the class exists >:(
class StringRange:
    pass


class StringRange:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @staticmethod
    def at(pos: int) -> StringRange:
        return StringRange(pos, pos)

    @staticmethod
    def between(start: int, end: int) -> StringRange:
        return StringRange(start, end)

    @staticmethod
    def encompassing(a: StringRange, b: StringRange) -> StringRange:
        return StringRange(min(a.start, b.start), max(a.end, b.end))

    @overload
    def get(self, reader: ImmutableStringReader) -> str:
        return reader.get_string()[self.start, self.end]

    @overload
    def get(self, string: str) -> str:
        return string[self.start, self.end]

    def is_empty(self):
        return self.start == self.end

    def __len__(self):
        return self.end - self.start

    def __str__(self):
        return 'StringRange{start=' + self.start + ', end=' + self.end + '}'

    def __hash__(self):
        return hash(self.start, self.end)


class ParsedArgument(Generic[S, T]):  # TODO: impl
    def __init__(self, start: int, end: int, result: T):
        self.range = StringRange.between(start, end)
        self.result = result


class ParsedCommandNode(Generic[S]):
    pass


# necessary for type hint linting to understand that the class exists >:(
class CommandContext(Generic[S]):
    pass


class CommandContext(Generic[S]):
    def __init__(self, source: S, input: str, arguments: Mapping[str, ParsedArgument[S, Any]], command: Command[S],
                 root_node: CommandNode[S], nodes: List[ParsedCommandNode[S]], range: StringRange,
                 child: CommandContext[S], modifier: RedirectModifier[S], forks: bool):
        self.source = source
        self.input = input
        self.arguments = arguments
        self.command = command
        self.root_node = root_node
        self.nodes = nodes
        self.range = range
        self.child = child
        self.modifier = modifier
        self.forks = forks

    def copy_for(self, source: S) -> CommandContext[S]:
        if source == self.source:
            return self
        return CommandContext(self.source, self.input, self.arguments, self.command, self.root_node, self.nodes,
                              self.range, self.child, self.modifier, self.forks)

    def get_last_child(self) -> CommandContext[S]:
        result = self
        while result.child is not None:
            result = result.child
        return result

    def get_argument(self, name: str, clazz: Type[V]) -> V:  # TODO: how does this work with type hints?
        if name not in self.arguments:
            raise KeyError('No such argument \'' + name + '\' exists on this command')

        argument = self.arguments[name]

        result = argument.result

        if isinstance(result, clazz):
            return result
        raise TypeError('Argument ' + name + ' is defined as ' + str(type(result)) + ', not ' + str(clazz))

    def has_nodes(self) -> bool:
        return len(self.nodes) != 0

    def __hash__(self):
        result = hash(self.source)
        result = 31 * result + hash(self.arguments)
        result = 31 * result + hash(self.command) if self.command is not None else 0
        result = 31 * result + hash(self.root_node)
        result = 31 * result + hash(self.nodes)
        result = 31 * result + hash(self.child) if self.child is not None else 0
        return result
