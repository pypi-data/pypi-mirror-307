from cbr_shared.cbr_backend.guests.Guests__Create__Many import Guests__Create__Many
from cbr_shared.cbr_sites.CBR__Shared_Objects       import cbr_shared_objects
from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Status                       import status_ok


class Routes__Guests(Fast_API_Routes):
    tag : str = 'guests'

    @cache_on_self
    def db_guests(self):
        return cbr_shared_objects.db_guests()

    def create_demo_guests(self):
       return Guests__Create__Many().create_demo_guests()

    def delete_all_guests(self):
        deleted_guests_ids = []
        for guest_id in self.ids():
            db_guest = self.db_guests().db_guest(guest_id)
            if db_guest.delete():
                deleted_guests_ids.append(guest_id)
        message = f"Deleted guests: {deleted_guests_ids} "
        return status_ok(message)


    def data(self):
        return self.db_guests().db_guests__data()

    def ids(self):
        return self.db_guests().db_guests__ids()

    def setup_routes(self):
        self.add_route_post  (self.create_demo_guests)
        self.add_route_delete(self.delete_all_guests )
        self.add_route_get   (self.data              )
        self.add_route_get   (self.ids               )
        return self