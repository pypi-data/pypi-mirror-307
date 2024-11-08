from typing import Optional
from typing_extensions import Annotated
import sys
import os
import importlib

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from certified.fast import BiscuitAuthz

def fail_auth(req: Request, biscuit: Optional[str]) -> bool:
    raise HTTPException(status_code=501,
                        detail='setup_security not called.')
    return False

def local_auth(req: Request, biscuit: Optional[str]) -> bool:
    """ Implement local authorization mode --
    passing only traffic originating from localhost
    or a UNIX socket.  This ignores the biscuit contents.
    """
    if req.client is None: # UNIX socket...
        return True
    if req.client.host.startswith("127."): # IPv4
        return True
    if req.client.host.replace(":0",":") \
                 .replace(":0",":").lstrip(":") == "1": # IPv6
        return True
    return False

# place-holders until setup_security is called.
_create_token = lambda req: None # Don't generate tokens.
_Authz = fail_auth

token_scheme = HTTPBearer(
    bearerFormat="biscuit",
    scheme_name="Biscuit token for authorization",
    description="Optional - may be obtained from /token",
    auto_error=False,
)

def run_auth(req: Request,
             credentials: Annotated[Optional[
                                 HTTPAuthorizationCredentials],
                             Depends(token_scheme)] = None,
            ) -> bool:

    # Expects a header of the form:
    # "Authorization: bearer b64-encoded biscuit"
    if credentials is None:
        # Will create a token with user=client
        # if no biscuit has been provided.
        biscuit = create_token(req)
    else:
        if credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=401,
                                detail='header format should be Authorization: bearer b64-token')
        biscuit = credentials.credentials

    try:
        return _Authz(req, biscuit)
    except KeyError as e:
        if str(e) == "'transport'":
            return True
        raise

# functions exported by this module:
def create_token(req: Request) -> Optional[str]:
    return _create_token(req)

Authz = Depends(run_auth)

def setup_security(policyfn: str) -> None:
    """ Import the policyfn and run it to create
    authz, an instance of the authz class.

    Then populate Authz and create_token from it.
    """
    global _Authz, _create_token

    if policyfn == "local":
        _Authz = local_auth
        return
    mod_name, fn_name = policyfn.split(':')

    sys.path.insert(0, os.getcwd())
    mod = importlib.import_module(mod_name)
    # TODO: allow reloading policy fn.
    #importlib.reload(mymodule)
    authorizor_fn = getattr(mod, fn_name)
    sys.path.pop(0)

    authz = authorizor_fn()
    _Authz = BiscuitAuthz("psik_api",
                          authz.get_pubkey,
                          authz) # type: ignore[assignment]
    _create_token = authz.create_token
