from starlette.responses                                import JSONResponse
from cbr_shared.cbr_sites.CBR__Shared_Objects           import cbr_shared_objects
from cbr_shared.cbr_sites.CBR__Shared__Constants import COOKIE_NAME__CBR__SESSION_ID__USER, \
    COOKIE_NAME__CBR__SESSION_ID__PERSONA, HEADER_NAME__CBR__SESSION_ID__USER, HEADER_NAME__CBR__SESSION_ID__PERSONA, \
    COOKIE_NAME__CBR__SESSION_ID__ACTIVE
from osbot_fast_api.api.Fast_API_Routes                 import Fast_API_Routes
from osbot_utils.utils.Status                           import status_ok, status_error
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self

STATUS_OK__LOGGED_IN_AS_USER                       = f"Found guest  , set {COOKIE_NAME__CBR__SESSION_ID__USER} cookie to session id, so that user is now logged in as the provided guest id"
STATUS_OK__LOGGED_IN_AS_PERSONA                    = f"Found persona, set {COOKIE_NAME__CBR__SESSION_ID__PERSONA} cookie to persona id, so that user is now logged in as the provided persona id"
STATUS_OK__LOGGED_OUT_ALL                          = "Successfully logged out both guest and persona profiles"
STATUS_OK__LOGGED_OUT_GUEST                        = "Successfully logged out guest profile"
STATUS_OK__LOGGED_OUT_PERSONA                      = "Successfully logged out persona profile"

STATUS_ERROR__FOUND_GUEST_BUT_NO_ACTIVE_SESSION    = "Found guest, but there was not active session available"
STATUS_ERROR__FOUND_PERSONA_BUT_NO_ACTIVE_SESSION  = "Found persona, but there was not active session available"
STATUS_ERROR__GUEST_NOT_FOUND                      = f"Guest not found"
STATUS_ERROR__PERSONA_NOT_FOUND                    = f"Persona not found"

class Routes__Guest(Fast_API_Routes):
    tag : str = 'guest'

    @cache_on_self
    def db_guests(self):
        return cbr_shared_objects.db_guests()

    def create(self, guest_name:str=None):
        return self.db_guests().db_guest__create(guest_name)

    def data(self, guest_id:str):
        try:
            db_guest = self.db_guests().db_guest(guest_id)
            if db_guest.exists():
                return status_ok(data=db_guest.guest_data())
            else:
                return status_error(f"Guest with id {guest_id} not found")
        except Exception as error:
            return status_error(f"Error in data: {error}")

    def delete(self, guest_id:str):
        db_guest = self.db_guests().db_guest(guest_id)
        if db_guest.exists():
            if db_guest.delete():
                return status_ok("Guest deleted ok")
        return status_error(f"Error deleting guest with id: {guest_id}")


    def exists(self, guest_id:str):
        db_guest = self.db_guests().db_guest(guest_id)
        if db_guest.exists():
            return status_ok("Guest exists")
        else:
            return status_error(f"Guest with id {guest_id} not found")

    def login_as_guest(self, guest_id):
        db_guest = self.db_guests().db_guest(guest_id)
        if db_guest.exists():
            db_session = db_guest.db_session()
            if db_session.exists():
                json_response = JSONResponse(content=status_ok(message=STATUS_OK__LOGGED_IN_AS_USER))
                #json_response.set_cookie( key=COOKIE_NAME__CBR__SESSION_ID__USER  , value=db_session.session_id )           # todo: fix this to use json_response.headers.append
                #json_response.set_cookie( key=COOKIE_NAME__CBR__SESSION_ID__ACTIVE, value=db_session.session_id)            #       because FastAPI doesn't support multiple set_cookie

                session_id_user_cookie   = f"{COOKIE_NAME__CBR__SESSION_ID__USER  }={db_session.session_id}; Path=/;"  # needs to be done like this because FastAPI's bug of not supporting multiple json_response.set_cookie
                session_id_active_cookie = f"{COOKIE_NAME__CBR__SESSION_ID__ACTIVE}={db_session.session_id}; Path=/;"

                json_response.headers.append("Set-Cookie", session_id_user_cookie)
                json_response.headers.append("Set-Cookie", session_id_active_cookie)

                json_response.headers.append(HEADER_NAME__CBR__SESSION_ID__USER,db_session.session_id)
                return json_response
            return status_error(STATUS_ERROR__FOUND_GUEST_BUT_NO_ACTIVE_SESSION)
        else:
            return status_error(STATUS_ERROR__GUEST_NOT_FOUND)

    def login_as_persona(self, persona_id):
        db_guest = self.db_guests().db_guest(persona_id)
        if db_guest.exists():
            db_session = db_guest.db_session()
            if db_session.exists():
                json_response = JSONResponse(content=status_ok(message=STATUS_OK__LOGGED_IN_AS_PERSONA))
                # json_response.set_cookie(key=COOKIE_NAME__CBR__SESSION_ID__PERSONA, value=db_session.session_id)
                # json_response.set_cookie(key=COOKIE_NAME__CBR__SESSION_ID__ACTIVE, value=db_session.session_id)

                session_id_persona_cookie = f"{COOKIE_NAME__CBR__SESSION_ID__PERSONA}={db_session.session_id}; Path=/;"     # needs to be done like this because FastAPI's bug of not supporting multiple json_response.set_cookie
                session_id_active_cookie  = f"{COOKIE_NAME__CBR__SESSION_ID__ACTIVE}={db_session.session_id}; Path=/;"

                json_response.headers.append("Set-Cookie", session_id_persona_cookie)
                json_response.headers.append("Set-Cookie", session_id_active_cookie )

                json_response.headers.append(HEADER_NAME__CBR__SESSION_ID__PERSONA, db_session.session_id)
                return json_response
            return status_error(STATUS_ERROR__FOUND_PERSONA_BUT_NO_ACTIVE_SESSION)
        else:
            return status_error(STATUS_ERROR__PERSONA_NOT_FOUND)

    def logout_all(self):                               # Logs out all profiles by clearing their session cookies
        json_response             = JSONResponse(content=status_ok(message=STATUS_OK__LOGGED_OUT_ALL))
        session_id_active_cookie  = f"{COOKIE_NAME__CBR__SESSION_ID__ACTIVE }=; Path=/; Max-Age=0;"          # Create cookie deletion headers with Path set to /
        session_id_user_cookie    = f"{COOKIE_NAME__CBR__SESSION_ID__USER   }=; Path=/; Max-Age=0;"
        session_id_persona_cookie = f"{COOKIE_NAME__CBR__SESSION_ID__PERSONA}=; Path=/; Max-Age=0;"

        json_response.headers.append("Set-Cookie", session_id_active_cookie )                           # Append cookie deletion headers to the response
        json_response.headers.append("Set-Cookie", session_id_user_cookie   )
        json_response.headers.append("Set-Cookie", session_id_persona_cookie)

        return json_response

    def logout_guest(self):
        """Logs out guest profile by clearing the user session cookie"""
        json_response = JSONResponse(content=status_ok(message=STATUS_OK__LOGGED_OUT_GUEST))
        json_response.delete_cookie(key=COOKIE_NAME__CBR__SESSION_ID__USER)
        return json_response

    def logout_persona(self):
        """Logs out persona profile by clearing the persona session cookie"""
        json_response = JSONResponse(content=status_ok(message=STATUS_OK__LOGGED_OUT_PERSONA))
        json_response.delete_cookie(key=COOKIE_NAME__CBR__SESSION_ID__PERSONA)
        return json_response

    def setup_routes(self):
        self.add_route_post   (self.create           )
        self.add_route_get    (self.data             )
        self.add_route_delete (self.delete           )
        self.add_route_get    (self.exists           )
        self.add_route_post   (self.login_as_guest   )
        self.add_route_post   (self.login_as_persona )
        self.add_route_post   (self.logout_all       )
        self.add_route_post   (self.logout_guest     )
        self.add_route_post   (self.logout_persona   )
        return self