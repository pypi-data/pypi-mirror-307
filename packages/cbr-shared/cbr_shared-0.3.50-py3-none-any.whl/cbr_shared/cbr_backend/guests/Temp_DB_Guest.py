from cbr_shared.cbr_backend.guests.S3_DB__Guest     import S3_DB__Guest
from cbr_shared.cbr_sites.CBR__Shared_Objects       import cbr_shared_objects
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_utils.helpers.Random_Guid import Random_Guid


class Temp_DB_Guest(Type_Safe):
    guest_name: str = None
    guest_id  : Random_Guid

    @cache_on_self
    def db_guest(self):
        return self.db_guests().db_guest(guest_id=self.guest_id)

    @cache_on_self
    def db_guests(self):
        return cbr_shared_objects.db_guests()

    def __enter__(self) -> S3_DB__Guest:
        self.create()
        return self.db_guest()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def create(self):
        self.db_guest().create(guest_name=self.guest_name)
        return self.db_guest()

    def delete(self):
        self.db_guest().delete()
        return self