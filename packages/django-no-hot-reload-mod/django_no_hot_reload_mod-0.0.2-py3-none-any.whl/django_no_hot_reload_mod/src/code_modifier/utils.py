import textwrap
from importlib import import_module

# LIVE CODE with no hot reloads

"""

TODO 

# generate url -> endpoint
# show current code  url -> endpoint -> in the form please

"""

test_code = """
@require_POST
def _(request):
    import random
    vv = random.randint(-10, 0)
    print("CHANGsES") 
    # print("sss:")
    if vv == -6:
        return JsonResponse({"CHANGES": vv})
    return JsonResponse({"CHANGES": f", {vv}"})
"""


def change_code(app: str, view: str, code_block: str):

    print(" --- Trying to change code --- ")
    module = import_module(app)
    funcs = getattr(module, 'views', {})
    view = getattr(funcs, view, None)

    # function defined args breaks -> in code args ( in def )
    # new_code = textwrap.dedent(base64.standard_b64decode(code_block_bytes).decode())

    code_block = textwrap.dedent(code_block)
    # assert dis.dis(view)

    to_eval = ['view']
    iterator_view = view
    while hasattr(iterator_view, '__wrapped__'):
        iterator_view = iterator_view.__wrapped__
        to_eval.append('__wrapped__')

    to_eval.append("__code__ = compile(code_block, '<string>', 'exec').co_consts[0]")
    exec('.'.join(to_eval))
