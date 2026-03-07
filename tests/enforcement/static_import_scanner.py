
import os
import ast
from typing import Set

def list_py_files(root: str):
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith('.py') and not f.startswith('test_'):
                yield os.path.join(dirpath, f)

def module_name_from_path(root: str, path: str) -> str:
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    if parts[-1] == '__init__.py':
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace('.py', '')
    return '.'.join(['core'] + parts)

def parse_imports(py_path: str) -> Set[str]:
    with open(py_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=py_path)
    imports: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports

def reduce_to_core(imports: Set[str]) -> Set[str]:
    out = set()
    for imp in imports:
        if imp == 'core' or imp.startswith('core.'):
            out.add(imp)
    return out


def project_submodule_name(full_core_module: str) -> str:
    return full_core_module.split('core.', 1)[1] if full_core_module.startswith('core.') else ''


def build_dependency_edges(core_root: str):
    edges = set()
    modules = set()
    for py in list_py_files(core_root):
        src = module_name_from_path(core_root, py)
        modules.add(src)
        imports = reduce_to_core(parse_imports(py))
        for imp in imports:
            edges.add((src, imp))
            modules.add(imp)
    return modules, edges
