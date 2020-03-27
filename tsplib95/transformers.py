# -*- coding: utf-8 -*-
from . import bisep
from . import exceptions


class Transformer:
    def parse(self, text):
        return text

    def render(self, value):
        if value is None:
            return ''
        return str(value)

    def validate(self, value):
        pass


class FuncT(Transformer):
    def __init__(self, *, func, **kwargs):
        super().__init__(**kwargs)
        self.func = func

    def parse(self, text):
        return self.func(text)


class ContainerT(Transformer):
    def __init__(self, *, value=None, sep=None, terminal=None,
                 size=None, filter_empty=True):
        self.child_tf = value or Transformer()
        self.sep = bisep.from_value(sep)
        self.terminal = terminal
        self.size = size
        self.filter_empty = filter_empty

    def parse(self, text):
        text = text.strip()

        # if we have a terminal, make sure it's there and remove it
        if self.terminal:
            if not text.endswith(self.terminal):
                raise exceptions.ParsingError(f'must end with {self.terminal}')
            text = text[:-len(self.terminal)].strip()

        # filter empties, or create an always filter
        if self.filter_empty:
            predicate = None
        else:
            def predicate(x):
                return True

        # split and filter
        texts = list(filter(predicate, self.split_items(text)))

        # parse each subitem
        items = [self.parse_item(text) for text in texts]

        # if size is specified, make sure its right
        if self.size and len(items) != self.size:
            raise exceptions.ParsingError(f'expected {self.size} items, '
                                          f'found {len(items)}')

        # pack them into a container and return it
        container = self.pack(items)
        return container

    def render(self, container):
        # unpack the items from the container and render them
        items = self.unpack(container)
        rendered = list(self.render_item(i) for i in items)

        # if there is a terminal, append it
        if self.terminal:
            rendered.append(self.terminal)

        # return the rendered items joined together
        return self.join_items(rendered)

    def parse_item(self, text):
        return self.child_tf.parse(text)

    def render_item(self, item):
        return self.child_tf.render(item)

    def split_items(self, text):
        return self.sep.split(text)

    def join_items(self, items):
        return self.sep.join(items)

    def pack(self, items):
        raise NotImplementedError()

    def unpack(self, container):
        raise NotImplementedError()


class ListT(ContainerT):
    def pack(self, items):
        return list(items)

    def unpack(self, container):
        return list(container)


class MapT(ContainerT):
    def __init__(self, *, kv_sep=None, key=None, **kwargs):
        super().__init__(**kwargs)
        self.key_tf = key or Transformer()
        self.kv_sep = bisep.from_value(kv_sep)

    def parse_item(self, text):
        # split the text into a key and value
        try:
            key, value = self.kv_sep.split(text, maxsplit=1)
        except ValueError:
            raise exceptions.ParsingError('expected key-value pair')

        # parse each and return a parsed key-value tuple
        return self.parse_key(key), self.parse_value(value)

    def render_item(self, item):
        # render the key and value
        k, v = item
        key = self.render_key(k)
        value = self.render_value(v)

        # return them joined
        return self.kv_sep.join([key, value])

    def parse_key(self, text):
        return self.key_tf.parse(text)

    def render_key(self, key):
        return self.key_tf.render(key)

    def parse_value(self, text):
        return self.child_tf.parse(text)

    def render_value(self, value):
        return self.child_tf.render(value)

    def pack(self, items):
        return {k: v for k, v in items}

    def unpack(self, container):
        return container.items()


class UnionT(Transformer):
    def __init__(self, *tfs, **kwargs):
        super().__init__(**kwargs)
        self.transformers = tfs

    def parse(self, text):
        for tf in self.transformers:
            try:
                return tf.parse(text)
            except Exception:
                pass
        raise exceptions.ParsingError('no transformer in the union '
                                      f'could parse the text: {text}')

    def render(self, value):
        for tf in self.transformers:
            try:
                return tf.render(value)
            except Exception:
                pass
        raise exceptions.ParsingError('no transformer in the union '
                                      f'could render the value: {value}')


class NumberT(UnionT):

    def __init__(self):
        super().__init__(FuncT(func=int), FuncT(func=float))
