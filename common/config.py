import imp
import inspect
import os
import sys
from contextlib import contextmanager
from copy import deepcopy


class Options:
    """
    Hierarchical class container for plain options.
    Non-plain options types (module type and class type)
    represents as another `Options` container.
    """

    @staticmethod
    def from_filesystem(path):
        if not os.path.exists(path) and not os.path.exists(path + '.py'):
            raise RuntimeError('Configuration %s was not found.' % (path,))

        if os.path.isdir(path):
            load_method = imp.load_package
        else:
            load_method = imp.load_source
            path += '.py'

        # configuration files may be changed in a production environment
        # so we need to ensure, they will be correctly reloaded after uwsgi/gunicorn restarting,
        # by disabling bytecode writing for these files only
        dont_write_bytecode = sys.dont_write_bytecode
        sys.dont_write_bytecode = True

        module_name = os.path.splitext(os.path.basename(path))[0]

        try:
            data = load_method(module_name, path)
            del sys.modules[module_name]
        except Exception as e:
            raise RuntimeError('Error loading configuration "%s": %r' % (path, e))

        sys.dont_write_bytecode = dont_write_bytecode

        parent_layer_name = data.__dict__.pop('PARENT_CONFIGURATION_LAYER', None)
        options = Options.from_object(data)
        setattr(options, '_name', module_name)
        if parent_layer_name:
            path = os.path.join(os.path.dirname(path), parent_layer_name)
            parent_options = Options.from_filesystem(path)
            options = parent_options.copy_with(**options._options)

        return options

    @staticmethod
    def from_object(obj):
        if not (inspect.isclass(obj) or inspect.ismodule(obj)):
            raise RuntimeError('Param object should be a container for plain options.')

        config_modules = getattr(obj, '__config_modules__', [])

        options = {}
        for key, value in inspect.getmembers(obj):
            if key.startswith('_'):
                continue

            is_config_module = False
            if inspect.ismodule(value):
                if value not in config_modules:
                    continue
                is_config_module = True

            if is_config_module or inspect.isclass(value):
                value = Options.from_object(value)

            options[key] = value

        return Options(**options)

    def copy_with(self, **additional_options):
        options = Options(**deepcopy(self._options))
        options.update(Options(**additional_options))
        return options

    def update(self, options_obj):
        for key, value in options_obj._options.items():
            if key not in self._options:
                self._options[key] = value
            else:
                old_value = self._options[key]
                if isinstance(old_value, Options) and isinstance(value, Options):
                    old_value.update(value)
                else:
                    self._options[key] = value

    def __init__(self, **options):
        self._options = options

    def __getattr__(self, name):
        if name in self.__dict__ or name.startswith('_'):
            return super(Options, self).__getattr__(name)

        return self._options[name]

    def __dir__(self):
        return self._options.keys()

    def __deepcopy__(self, memo):
        return Options(**deepcopy(self._options))

    @contextmanager
    def override(self, **options):
        """
        with config.override(
            foo='test',
            db=Options(host='test', user='test'),
            amqp=config.amqp.copy_with(user='test'),
        ):
            <new config values>
        <old config values>
        """

        old_values = {
            key: self._options[key]
            for key in options
            if key in self._options
        }
        self._options.update(options)

        try:
            yield
        finally:
            self._options.update(old_values)
            for key in set(options.keys()) - set(old_values.keys()):
                del self._options[key]
