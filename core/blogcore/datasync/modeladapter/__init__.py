import logging

logger = logging.getLogger('geekblog')
_ADAPTERS = {}


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


def register(model, adapter_class, conn_options):    # only register non-proxy model
    try:
        if model in _ADAPTERS:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)

        _ADAPTERS[model] = adapter_class(conn_options)
    except AlreadyRegistered, e:
        logger.exception('register adapter FAILED, model: %s, adapter_class: %s' % (model, adapter_class))


def get_adapter(model):
    if model._meta.proxy:     # only support one level proxy class
        model = model.__bases__[0]    # only get first parent class, ignore multi-inherited
    if model not in _ADAPTERS:
        raise NotRegistered('The model %s is not registered' % model.__name__)
    return _ADAPTERS[model]
