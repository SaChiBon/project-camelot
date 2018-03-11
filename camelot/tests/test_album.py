from django.test import TestCase
from django.test.client import RequestFactory
from django.shortcuts import reverse

from django.contrib.auth.models import User

from ..controllers.albumcontroller import albumcontroller
from ..controllers.utilities import get_profile_from_uid
from ..view.album import *

# we should probably split up the controller tests from the view tests

class AlbumTests(TestCase):
    # this setUp code needs to be made universal
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'user@test.com',
            'password': 'secret'}
        self.u = User.objects.create_user(**self.credentials)
        self.u.save()

        # send login data
        response = self.client.post('', self.credentials, follow=True)

        self.factory = RequestFactory()
        self.albumcontrol = albumcontroller(self.u.id)

    def test_get_profile_from_uid(self):
        profile = get_profile_from_uid(self.u.id)
        self.assertEqual(profile.user, self.u)
        self.assertEqual(self.u.profile, profile)

    def test_create_controller_duplicate_name(self):
        self.albumcontrol.create_album("test title", "test description")
        self.assertRaises(AlreadyExistsException, self.albumcontrol.create_album, "test title", "test description2")

    def test_create_view(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse("create_album"))
        request.user = self.u
        request.session = {}

        # Test my_view() as if it were deployed at /customer/details
        response = create_album(request)

        self.assertEqual(response.status_code, 200)

    def test_return_albums_controller(self):
        # can't count on tests running in order
        self.albumcontrol.create_album("a test title", "test description")
        albums = self.albumcontrol.return_albums()

        # there's probably some string compare assert for this
        assert albums[0].name == "a test title"
        assert albums[0].description == "test description"

    def test_return_album(self):
        newalbum = self.albumcontrol.create_album("return album test", "lalala")
        testalbum = self.albumcontrol.return_album(newalbum.id)
        assert newalbum == testalbum

    # the following tests are for functionality that hasn't been written yet
    # just defining the future path
    def test_add_image_to_album_controller(self):
        import shutil

        myalbum = self.albumcontrol.create_album("image add test", "lalala")

        try:
            # double check that our test is sending the right type for fi and that django will sent in rb mode
            with open('camelot/tests/resources/testimage.jpg', 'rb') as fi:
                self.albumcontrol.add_photo_to_album(myalbum.id, "generic description", fi)
                # need to add checks for file existence and db existence

        # clean up
        except:
            shutil.rmtree("userphotos")
            raise
        shutil.rmtree("userphotos")
        # example (for view):
        #c = Client()
        #with open('wishlist.doc') as fp:
        #    c.post('/customers/wishes/', {'name': 'fred', 'attachment': fp})

    def test_get_images_for_album(self):
        # implemented
        pass

    def test_remove_image_from_album(self):
        pass

    def test_download_album(self):
        pass

    def test_add_contributor_to_album(self):
        pass

    def test_remove_contributor_from_album(self):
        pass

    def test_get_album_contributors(self):
        pass

    def test_user_can_access(self):
        pass

    def test_user_cant_access(self):
        pass

class AlbumViewTests(TestCase):
    def test_album_view(self):
        # implemented
        pass