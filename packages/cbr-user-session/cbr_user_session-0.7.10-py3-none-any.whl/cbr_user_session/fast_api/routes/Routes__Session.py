from starlette.requests                                         import Request
from cbr_shared.cbr_backend.session.S3_DB__Session              import S3_DB__Session
from cbr_shared.cbr_backend.session.decorators.with_db_session  import with_db_session
from cbr_user_session.user_session.User_Session__Utils          import User_Session__Utils
from osbot_fast_api.api.Fast_API_Routes                         import Fast_API_Routes

class Routes__Session(Fast_API_Routes):
    tag                : str                 = 'session'
    user_session_utils : User_Session__Utils

    @with_db_session
    def current_session(self, request: Request):
        db_session : S3_DB__Session = request.state.db_session
        return db_session.session_config().json()

    def session_details(self, session_id):
        return self.user_session_utils.session__details(session_id)

    def session_exists(self, session_id):
        return self.user_session_utils.session__exists(session_id)

    def session_user_id(self, session_id):
        return self.user_session_utils.session__user_id(session_id)

    def setup_routes(self):
        self.add_route_get(self.current_session )
        self.add_route_get(self.session_details )
        self.add_route_get(self.session_exists  )
        self.add_route_get(self.session_user_id )