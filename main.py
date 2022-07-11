#blackdragonx61 / Mali

import ast
from pathlib import Path

PATH_BUILTINS = 'builtins'
PATH_OUT = 'out'

data : dict[str, dict] = {}

def collect() -> bool:
    if not Path(PATH_BUILTINS).is_dir():
        print(f'Cannot find: {PATH_BUILTINS}')
        return False

    for p in Path('builtins').glob('*.py'):
        with p.open() as f:
            d = ast.literal_eval(f.read())

            if type(d) is not dict:
                print(f"Failed to read: {p.name}")
                continue

            data[p.name.replace("dict.", "")] = d

    return True

def out() -> None:
    p = Path(PATH_OUT)
    if not p.is_dir():
        p.mkdir(parents=True, exist_ok=True)

    for n, d in data.items():
        with open(f'{PATH_OUT}/{n}', 'w') as f:
            f.write(
                '__author__ = "blackdragonx61 / Mali"\n'
                '__unpacker__ = "xP3NG3Rx"\n'
                '__skeleton__ = "Takuma"\n\n'
            )

            if 'var' in d:
                for vars in d['var']:
                    if all (t in vars for t in ('name', 'type', 'value')):
                        if vars['type'] == 'str':
                            vars['value'] = '"' + vars['value'] + '"'
                        f.write('{} : {} = {}\n'.format(vars['name'], vars['type'], vars['value']))
                f.write('\n')
            
            if 'func' in d:
                for funcs in d['func']:
                    if 'name' in funcs:
                        f.write('def {}() -> None:\n\tpass\n\n'.format(funcs['name']))

if __name__ == "__main__":
    if collect():
        out()
        print("Finished.")