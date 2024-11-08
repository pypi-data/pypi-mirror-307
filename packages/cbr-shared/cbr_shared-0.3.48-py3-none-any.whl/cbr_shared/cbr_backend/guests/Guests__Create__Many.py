from cbr_shared.cbr_sites.CBR__Shared_Objects            import cbr_shared_objects
from cbr_shared.schemas.data_models.Model__User__Profile import Model__User__Profile
from osbot_utils.base_classes.Type_Safe                  import Type_Safe
from osbot_utils.utils.Files                             import path_combine
from osbot_utils.utils.Toml                              import toml_file_load


class Guests__Create__Many(Type_Safe):

    def db_guests(self):
        return cbr_shared_objects.db_guests()

    def guests_to_create_data(self):
        guest_file = path_combine(__file__, '../guests-to-create.toml')
        return toml_file_load(guest_file)

    def create_demo_guests(self):
        guest_data = self.guests_to_create_data()
        return self.create_many(guest_data)

    def create_many(self, guest_data):
        guests_created = []
        guests_skipped = []
        for guest, guest_json in guest_data.items():
            user_profile_json   = guest_json.get('user_profile')
            user_profile        = Model__User__Profile.from_json(user_profile_json)
            guest_id            = guest_json.get('guest_id')
            db_guest = self.db_guests().db_guest(guest_id=guest_id)
            if db_guest.not_exists():
                db_guest.create()
                db_guest.db_user().user_profile__update(user_profile)
                guests_created.append(guest_id)
            else:
                guests_skipped.append(guest_id)
        result = dict(guests_created=guests_created, guests_skipped=guests_skipped)
        return result