"""
Main API for Vega-lite spec generation
"""

try:
    import traitlets as T
except ImportError:
    from IPython.utils import traitlets as T

from .utils import parse_shorthand


class BaseObject(T.HasTraits):
    
    def __contains__(self, key):
        value = getattr(self, key)
        return (value is not None) and (not (not isinstance(value, bool) and not value))


class Data(BaseObject):

    formatType = T.Enum(['json','csv'], default_value='json')
    url = T.Unicode('', allow_none=True)
    data = T.List([], allow_none=True)

class Scale(BaseObject):
    pass

class Axis(BaseObject):
    pass

class Band(BaseObject):
    pass

class Legend(BaseObject):
    pass

class SortItems(BaseObject):
    name = T.Unicode(allow_none=True)
    aggregate = T.Enum(['avg','sum','min','max','count'], allow_none=True)
    reverse = T.Bool(False)

class Position(BaseObject):

    name = T.Unicode('')
    type = T.Enum(['N','O','Q','T'], allow_none=True)
    aggregate = T.Enum(['avg','sum','median','min','max','count'], default_value=None)
    timeUnit = T.Enum(['year','month','day','date','hours','minutes','seconds'], allow_none=True)
    bin = T.Union([T.Bool(),T.Int()], default_value=False)
    scale = T.Instance(Scale, allow_none=True)
    axis = T.Instance(Axis, allow_none=True)
    band = T.Instance(Band, allow_none=True)
    sort = T.List(T.Instance(SortItems), allow_none=True)

class Index(BaseObject):

    name = T.Unicode('')
    type = T.Enum(['N','O','Q','T'], allow_none=True)
    timeUnit = T.Enum(['year','month','day','date','hours','minutes','seconds'], allow_none=True)
    bin = T.Union([T.Bool(),T.Int()], default_value=False)
    aggregate = T.Enum(['count'], allow_none=True)
    padding = T.CFloat(0.1)
    sort = T.List(T.Instance(SortItems), allow_none=True)
    axis = T.Instance(Axis, allow_none=True)
    height = T.CInt(150)

class Size(BaseObject):
    name = T.Unicode('')
    type = T.Enum(['N','O','Q','T'])
    aggregate = T.Enum(['avg','sum','median','min','max','count'])
    timeUnit = T.Enum(['year','month','day','date','hours','minutes','seconds'], allow_none=True)
    bin = T.Union([T.Bool(),T.Int()], default_value=False)
    scale = T.Instance(Scale, allow_none=True)
    legend = T.Instance(Legend, allow_none=True)
    value = T.CInt(30)
    sort = T.List(T.Instance(SortItems), allow_none=True)

class Color(BaseObject):
    name = T.Unicode('')
    type = T.Enum(['N','O','Q','T'])
    aggregate = T.Enum(['avg','sum','median','min','max','count'])
    timeUnit = T.Enum(['year','month','day','date','hours','minutes','seconds'], allow_none=True)
    bin = T.Union([T.Bool(),T.Int()], default_value=False)
    scale = T.Instance(Scale, allow_none=True)
    legend = T.Instance(Legend, allow_none=True)
    value = T.Unicode('#4682b4')
    opacity = T.Float(1.0)
    sort = T.List(T.Instance(SortItems), allow_none=True)

class Shape(BaseObject):
    name = T.Unicode('')
    type = T.Enum(['N','O','Q','T'])
    aggregate = T.Enum(['count'], allow_none=True)
    timeUnit = T.Enum(['year','month','day','date','hours','minutes','seconds'], allow_none=True)
    bin = T.Union([T.Bool(),T.Int()], default_value=False)
    legend = T.Instance(Legend, allow_none=True)
    value = T.Enum(['circle','square','cross','diamond','triangle-up','triangle-down'], default_value='circle')
    filled = T.Bool(False)
    sort = T.List(T.Instance(SortItems), allow_none=True)

class Encoding(BaseObject):

    x = T.Union([T.Instance(Position),T.Unicode()], allow_none=True)
    y = T.Union([T.Instance(Position),T.Unicode()], allow_none=True)
    row = T.Union([T.Instance(Index),T.Unicode()], allow_none=True)
    col = T.Union([T.Instance(Index),T.Unicode()], allow_none=True)
    size = T.Instance(Size, allow_none=True)
    color = T.Instance(Color, allow_none=True)
    shape = T.Instance(Shape, allow_none=True)

    def _x_changed(self, name, old, new):
        if isinstance(new, str):
            result = parse_shorthand(new)
            self.x = Position(**result)

    def _y_changed(self, name, old, new):
        if isinstance(new, str):
            result = parse_shorthand(new)
            self.y = Position(**result)

    def _row_changed(self, name, old, new):
        if isinstance(new, str):
            result = parse_shorthand(new)
            self.row = Index(**result)

    def _col_changed(self, name, old, new):
        if isinstance(new, str):
            result = parse_shorthand(new)
            self.col = Index(**result)


class Viz(BaseObject):

    marktype = T.Enum(['point','tick','bar','line',
                     'area','circle','square','text'], default_value='point')
    _data = T.Instance(Data, allow_none=True)
    data = T.Any()
    encoding = T.Instance(Encoding)
    # _encoding = T.Union([T.Instance(Encoding),T.Dict])

    # def __encoding_changed(self, name, old, new):
    #     if isinstance(new, dict):
    #         self._encoding = Encoding(**new)

    def __init__(self, data, **kwargs):
        kwargs['data'] = data
        super(Viz,self).__init__(self, **kwargs)

    def encode(self, **kwargs):
        self.encoding = Encoding(**kwargs)
        return self

    def mark(self, mt):
        self.marktype = mt
        return self

    def mark_point(self):
        return self.mark('point')

    def mark_tick(self):
        return self.mark('tick')

    def mark_bar(self):
        return self.mark('bar')

    def mark_line(self):
        return self.mark('line')

    def mark_area(self):
        return self.mark('area')

    def mark_circle(self):
        return self.mark('circle')

    def mark_square(self):
        return self.mark('square')

    def mark_text(self):
        return self.mark('text')