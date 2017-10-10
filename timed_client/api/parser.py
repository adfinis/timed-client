#!/usr/bin/env python3

"""API client models for Timed"""
import collections

MODEL_REGISTRY = {}

def model_for(modelname):
    """Decorator to register custom model classes"""

    def wrapper(fn):
        MODEL_REGISTRY[modelname] = fn
        return fn

    return wrapper


class APIModel():
    def __init__(self, res, type, id, attributes, relationships={}):
        self.type = type
        self.id   = id
        self._res = res

        for k, v in attributes.items():
            kname = k.replace('-', '_')
            setattr(self, kname, v)

        for rtype, rcontent in relationships.items():
            data  = rcontent['data']
            rname = rtype.replace('-', '_')
            #print("%s%s - reading relationships: %s" % (type,id, rname))

            if isinstance(data, dict):
                # single object
                setattr(self, rname, res.stored(**data))
            elif isinstance(data, list):
                setattr(self, rname,
                        [
                           res.stored(**rdata)
                           for rdata
                           in data
                        ])
            elif data is None:
                # Yes that's possible as well
                setattr(self, rname, None)

    def api_client(self):
        return self._res.client

class APIResult(list):
    def __init__(self, client, data, included=[], meta=None):
        # We process lists and single-object results the same way.
        self._deferred = []
        self.client = client
        self._store = collections.defaultdict(dict)

        self._parse_included_list(included)

        for rec in data:
            self.append(self.model(**rec))

    def model(self, **kwargs):
        "Build a model instance for the given record data"

        subcls = MODEL_REGISTRY.get(kwargs['type'], APIModel)

        obj = subcls(self, **kwargs)
        self._store_model(obj)
        return obj

    @classmethod
    def from_resp(cls, client, data, included=[], meta=None):
        if isinstance(data, dict):
            # Single instance. handle like a list, but
            # then only return the (singular) result
            res = cls(client, [data], included)
            assert len(res) == 1
            return res[0]
        else:
            return cls(client, data, included)

    def stored(self, type, id):
        try:
            res = self._store[type][id]
        except KeyError:
            res = self.model(type=type, id=id, attributes={})
            self._store[type][id] = res
        return res

    def _store_model(self, model):
        self._store[model.type][model.id] = model

    def _parse_included_list(self, included):
        for inc in included:
            obj = self.model(**inc)

    def __repr__(self):
        return "APIResult%s" % str([x for x in self])
