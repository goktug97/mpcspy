import ast
import sys
import types

def check(node_or_string, allowed_modules={}, allowed_functions=[],
        verbose=True):
    def exception_handler(
            exception_type, exception, traceback, debug_hook=sys.excepthook):
        if verbose:
            debug_hook(exception_type, exception, traceback)
        else:
            print(f'{exception_type.__name__}: {exception}')
    sys.excepthook = exception_handler
    aliases = {}
    if isinstance(node_or_string, str):
        node_or_string = ast.parse(node_or_string, mode='exec')
    if isinstance(node_or_string, ast.Module):
        node_or_string = node_or_string.body
    def _convert(node):
        if hasattr(node, 'values'):
            for value in node.values:
                _convert(value)
        if hasattr(node, 'elts'):
            for value in node.elts:
                _convert(value)
        if hasattr(node, 'body'):
            for exp in node.body:
                _convert(exp)

        if isinstance(node, ast.Expr):
            _convert(node.value)
            return
        elif isinstance(node, ast.Constant):
            return
        elif isinstance(node, (ast.Str, ast.Bytes)):
            return
        elif isinstance(node, ast.Num):
            return
        elif isinstance(node, ast.Tuple):
            return
        elif isinstance(node, ast.List):
            return
        elif isinstance(node, ast.Set):
            return
        elif isinstance(node, ast.Dict):
            return
        elif isinstance(node, ast.NameConstant):
            return
        elif isinstance(node, ast.BinOp):
            _convert(node.right)
            _convert(node.left)
            return
        elif isinstance(node, ast.For):
            _convert(node.iter)
            return
        elif isinstance(node, ast.While):
            _convert(node.test)
            return
        elif isinstance(node, ast.Compare):
            for exp in node.comparators:
                _convert(exp)
            _convert(node.left)
            return
        elif isinstance(node, ast.FunctionDef):
            for arg in node.args.defaults:
                _convert(arg)
            return
        elif isinstance(node, ast.Return):
            _convert(node.value)
            return
        elif isinstance(node, ast.Pass):
            return
        elif isinstance(node, ast.ClassDef):
            for base in node.bases:
                _convert(base)
            return
        elif isinstance(node, ast.AnnAssign):
            if node.target.id in aliases.keys():
                raise ValueError(
                        'Module to module assign is not allowed')
            _convert(node.value)
            return
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if target.id in aliases.keys():
                    raise ValueError(
                            'Module to module assign is not allowed')
            _convert(node.value)
            return
        elif isinstance(node, ast.Name):
            return
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if not (alias.name in allowed_modules):
                    raise ValueError(f'{alias.name} is not allowed.')
                if alias.asname is not None:
                    aliases[alias.asname] = alias.name
                else:
                    aliases[alias.name] = alias.name
            return
        elif isinstance(node, ast.Attribute):
            if node.value.id in aliases.keys():
                funcs = allowed_modules[aliases[node.value.id]]
                if funcs == '':
                    return
                elif node.attr in funcs:
                    return
            else:
                if node.attr in allowed_functions:
                    return
            raise ValueError(f'{node.attr} is not allowed.')
        elif isinstance(node, ast.Call):
            for arg in node.args:
                _convert(arg)
            if hasattr(node.func, 'id'):
                if node.func.id in allowed_functions:
                    return
                raise ValueError(f'{node.func.id} is not allowed.')
            elif hasattr(node.func, 'attr'):
                if node.func.value.id in aliases.keys():
                    funcs = allowed_modules[aliases[node.func.value.id]]
                    if funcs == '':
                        return
                    if node.func.attr in funcs:
                        return
                else:
                    if node.func.attr in allowed_functions:
                        return
                raise ValueError(f'{node.func.attr} is not allowed.')
        raise ValueError(f'malformed node or string: {node}')
    return [_convert(node) for node in node_or_string]

def read_config(config_file, allowed_modules, allowed_functions,
        verbose=False):
    config = types.ModuleType('config', 'Config')
    with open(config_file) as f:
        code = f.read()
        check(code, allowed_modules=allowed_modules,
                allowed_functions=allowed_functions,
                verbose=verbose)
        code = compile(code, "config", "exec")
        exec(code, config.__dict__)
    return config


