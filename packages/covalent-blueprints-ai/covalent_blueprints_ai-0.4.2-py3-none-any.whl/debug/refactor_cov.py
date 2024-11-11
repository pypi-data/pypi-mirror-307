# %%

import covalent as ct
import covalent_cloud as cc
from pydantic import BaseModel

print(cc.__version__)
print(ct.__version__)

cpu_executor = cc.CloudExecutor()  # does not matter


@ct.electron(executor=cpu_executor)
def run():

    class LLMResponse(BaseModel):
        """empty class; adding attrs does not help"""

    return LLMResponse()
    # return LLMResponse  # ALSO ERROR
    # return BaseModel    # OK
    # return BaseModel()  # OK


# ERROR during wrapping with lattice.
@ct.lattice(executor=cpu_executor, workflow_executor=cpu_executor)
def main():
    return run()

# %%
# dispatch_id = cc.dispatch(main)()
# dispatch_id

# %%
# result = cc.get_result(dispatch_id, wait=True)
# result.result.load()
# local_folder = result.result.value


