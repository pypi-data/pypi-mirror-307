from fastapi                            import Request, HTTPException
from osbot_utils.base_classes.Type_Safe import Type_Safe

class CBR__Fast_API__Security_Demands(Type_Safe):

    def demand_admin(self, request: Request):
        if request and hasattr(request.state, 'request'):
            pass

        self.raise_exception('admin')

    def raise_exception(self, missing_role):
        kwargs = dict(status_code = 401,
                      detail      = f"Unauthorized! Only {missing_role}(s) can access this route")
        raise HTTPException(**kwargs)