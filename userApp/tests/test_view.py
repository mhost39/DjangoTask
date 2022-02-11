from django.urls import reverse, resolve



class TestView:

    def test_organization(self):
        path = reverse('organizations')
        assert resolve(path).view_name == 'organization'   
