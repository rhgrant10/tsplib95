# -*- coding: utf-8 -*-
from . import bisep
from . import exceptions
from . import utils


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


class NumberT(Transformer):
    def parse(self, text):
        for func in (int, float):
            try:
                return func(text)
            except ValueError:
                pass
        error = f'could not convert text to number: {text}'
        raise exceptions.ParsingError(error)


class ContainerT(Transformer):
    def __init__(self, *, value=None, sep=None, terminal=None,
                 size=None, filter_empty=True):
        self.child_tf = value or Transformer()
        self.sep = bisep.from_value(sep)
        self.terminal = terminal
        self.size = size
        self.filter_empty = filter_empty

    def parse(self, text):
        # start without unpredictable whitespace
        text = text.strip()

        # if we have a terminal, make sure it's there and remove it
        if self.terminal:
            if not text.endswith(self.terminal):
                raise exceptions.ParsingError(f'must end with {self.terminal}')
            text = text[:-len(self.terminal)].strip()

        # split the whole text into multiple texts
        try:
            texts = self.split_items(text)
        except Exception as e:
            message = 'could not split the text'
            raise exceptions.ParsingError.ammend(e, message)

        # filter out the empties, or don't; it's configurable
        if self.filter_empty:
            texts = list(filter(None, texts))

        # if specified, ensure the terminal terminates the list
        if self.terminal is not None:
            try:
                index = texts.index(self.terminal)
            except ValueError:
                error = f'items did not end with terminal: {repr(self.terminal)}'
                raise exceptions.ParsingError(error)

            if index < len(texts) - 1:
                extra = texts[index + 1:]
                error = (f'found {len(extra)} extra items after terminal '
                         f'{repr(self.terminal)}, first is {repr(extra[0])}')
                raise exceptions.ParsingError(error)

        # parse the texts into items, catching all errors by index
        items = []
        errors = []
        for i, text in enumerate(texts):
            try:
                item = self.parse_item(text)
            except Exception as e:
                errors.append(f'item.{i}=>{repr(e)}')
            else:
                items.append(item)

        # join and report any errors
        if errors:
            error = utils.friendly_join(errors, limit=3)
            raise exceptions.ParsingError(error)

        # if the size is specified, make sure its right
        if self.size and len(items) != self.size:
            error = f'expected {self.size} items, found {len(items)}'
            raise exceptions.ParsingError(error)

        # finally, pack the items into a container and return it
        return self.pack(items)

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
        errors = []
        for tf in self.transformers:
            try:
                return tf.parse(text)
            except Exception as e:
                errors.append(f'{tf.__class__.__qualname__}=>{repr(e)}')
        raise exceptions.ParsingError('no transformer in the union could '
                                      'parse the text, resulting in the '
                                      'following errors: '
                                      f'{utils.friendly_join(errors)}')

    def render(self, value):
        errors = []
        for tf in self.transformers:
            try:
                return tf.render(value)
            except Exception as e:
                errors.append(f'{tf.__class__.__qualname__}=>{repr(e)}')
        raise exceptions.ParsingError('no transformer in the union could '
                                      'render the value, resulting in the '
                                      'following errors: '
                                      f'{utils.friendly_join(errors)}')
