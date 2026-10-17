from django.test import TestCase
LIBRARIAN = {'uid': 'lib1', 'email': 'bib@example.com', 'name': 'Bibliotecaria', 'role': 'librarian'}
STUDENT = {'uid': 'est1', 'email': 'est@example.com', 'name': 'Estudiante', 'role': 'student'}
class SessionTestCase(TestCase):
    def login_as(self, user):
        session = self.client.session
        session['user'] = user
        session.save()
