from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe

@dataclass
class Model__Session_Security(Type_Safe):
    is_admin_global: bool = False
    is_admin_site  : bool = False
    is_blocked     : bool = False
    is_customer    : bool = False
    is_guest       : bool = False
    is_malicious   : bool = False
    is_user        : bool = False
    is_user_qa     : bool = False
    is_suspended   : bool = False
    is_suspicious  : bool = False