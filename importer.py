import importlib.util

def path_import(name,path):
	spec = importlib.util.spec_from_file_location(name, path)
	foo = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(foo)