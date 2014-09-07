import os
import tempfile
import unittest

from fluenttest import test_case

import flaskr


class TestCase(test_case.TestCase, unittest.TestCase):

    @classmethod
    def arrange(cls):
        cls._db_fd, cls._db_path = tempfile.mkstemp()

        flaskr.init_db()
        cls.app = flaskr.app.test_client()

    @classmethod
    def destroy(cls):
        os.close(cls._db_fd)
        os.unlink(cls._db_path)

    @classmethod
    def get(cls, url):
        cls.response = cls.app.get(url, follow_redirects=True)

    @classmethod
    def post(cls, url, **data):
        cls.response = cls.app.post(url, data=data, follow_redirects=True)

    @property
    def response_body(self):
        return self.response.data.decode()


class TestLoginWithEmptyDatabase(TestCase):

    @classmethod
    def act(cls):
        cls.post('/login', username='admin', password='default')

    def test_logged_in_message_shown(self):
        assert 'You were logged in' in self.response_body

    def test_empty_db_message_shown(self):
        assert 'No entries here so far' in self.response_body


class TestLoginWithInvalidUsername(TestCase):

    @classmethod
    def act(cls):
        cls.post('/login', username='xadmin', password='default')

    def test_invalid_username_shown(self):
        assert 'Invalid username' in self.response_body


class TestLoginWithInvalidPassword(TestCase):

    @classmethod
    def act(cls):
        cls.post('/login', username='admin', password='xdefault')

    def test_invalid_password_shown(self):
        assert 'Invalid password' in self.response_body


class TestLogout(TestCase):

    @classmethod
    def arrange(cls):
        super(TestLogout, cls).arrange()
        cls.post('/login', username='admin', password='default')

    @classmethod
    def act(cls):
        cls.get('/logout')

    def test_logged_out_message_shown(self):
        assert 'You were logged out' in self.response_body


class TestAddingFirstMessage(TestCase):

    @classmethod
    def arrange(cls):
        super(TestAddingFirstMessage, cls).arrange()
        cls.post('/login', username='admin', password='default')

    @classmethod
    def act(cls):
        cls.post('/add', title='<Hello>',
                 text='<strong>HTML</strong> allowed here')

    def test_empty_db_message_is_not_shown(self):
        assert 'No entries here so far' not in self.response_body

    def test_title_is_html_encoded(self):
        assert '&lt;Hello&gt;' in self.response_body

    def test_body_allows_embedded_html(self):
        assert '<strong>HTML</strong> allowed here' in self.response_body


if __name__ == '__main__':
    unittest.main(verbosity=3)
