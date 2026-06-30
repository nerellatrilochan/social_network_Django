import factory
import datetime

from posts_auth.adapters.dtos import UserProfileDTO


class UserProfileDTOFactory(factory.Factory):

    class Meta:
        model = UserProfileDTO

    user_id = factory.Sequence(lambda n: "user_{0}".format(n + 1))
    cover_page_url = factory.Sequence(lambda n: "name_{0}".format(n + 1))
    state_of_residence = factory.Sequence(
        lambda n: "my_profile_{0}".format(n + 1))
    i_want_to_receive_updates_directly_on_whatsapp = "yes"
    pincode = "534313"
    age_group = factory.Sequence(lambda n: "age_group{0}".format(n + 1))
    accepted_tnc = True
    last_name = factory.Sequence(lambda n: "last_name_{0}".format(n + 1))
    occupation = factory.Sequence(lambda n: "occupation_{0}".format(n + 1))
    name = factory.Sequence(lambda n: "name_{0}".format(n + 1))
    gender = "MALE"
    dob = datetime.date(2020, 12, 28)
    profile_pic_url = factory.Sequence(
        lambda n: "my_profile_{0}".format(n + 1))
    phone_number = "98765431"
    is_phone_number_verified = False
    country_code = "91"
    email = factory.Sequence(lambda n: "my_email_{0}".format(n + 1))
    is_email_verified = False
    language_preference = "ENGLISH"
    age = 20

