import re
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

from config import Config

Config.SQLALCHEMY_DATABASE_URI = "sqlite://"
Config.SECRET_KEY = "test-key-for-authentication"

from app import create_app, db
from app.models import User


class AuthenticationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True, API_KEY="fake", API_FROM="sender@example.com",
                               APP_BASE_URL="https://example.com")
        self.client = self.app.test_client()

    def post(self, path, fields=None, form_path=None):
        html = self.client.get(form_path or path).text
        token = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html).group(1)
        return self.client.post(path, data={**(fields or {}), "csrf_token": token})

    @patch("app.email_service.requests.post")
    def test_signup_confirmation_login_and_logout(self, send):
        send.return_value.status_code = 202
        response = self.post("/auth/register", {
            "name": "Taissa", "username": "teste", "email": "teste@example.com",
            "password": "senha-teste", "password2": "senha-teste",
        })
        self.assertEqual(response.status_code, 302)
        payload = send.call_args.kwargs["json"]
        self.assertEqual(payload["personalizations"], [{"to": [{"email": "teste@example.com"}]}])
        link = re.search(r"https://example.com/auth/confirm/\S+", payload["content"][0]["value"]).group()
        path = urlsplit(link).path
        with self.app.app_context():
            user = db.session.scalar(db.select(User))
            self.assertNotEqual(user.password_hash, "senha-teste")
            self.assertTrue(user.verify_password("senha-teste"))
            self.assertFalse(user.confirmed)
        self.assertIn("/auth/login", self.client.get(path).location)
        login = self.post("/auth/login", {"email": "teste@example.com", "password": "senha-teste"})
        self.assertEqual(login.location, path)
        self.assertIn("/auth/unconfirmed", self.client.get("/").location)
        self.assertEqual(self.client.post(path).status_code, 400)
        self.assertEqual(self.post(path).location, "/")
        self.assertIn("Minha conta", self.client.get("/").text)
        self.assertEqual(self.client.get("/auth/logout").status_code, 405)
        self.post("/auth/logout", form_path="/")
        self.assertIn("visitante", self.client.get("/").text)

    def test_confirmed_user_cannot_manage_other_accounts(self):
        with self.app.app_context():
            owner = User(name="Ana", username="ana", email="ana@example.com", confirmed=True)
            other = User(name="Bia", username="bia", email="bia@example.com", confirmed=True)
            owner.password = other.password = "senha-teste"
            db.session.add_all([owner, other])
            db.session.commit()
            other_id = other.id
        self.post("/auth/login", {"email": "ana@example.com", "password": "senha-teste"})
        self.assertNotIn("bia@example.com", self.client.get("/").text)
        self.assertEqual(self.client.get(f"/editar/{other_id}").status_code, 403)
        self.assertEqual(self.post(f"/excluir/{other_id}", form_path="/").status_code, 403)

    def test_token_tampering_and_email_change(self):
        with self.app.app_context():
            user = User(id=1, name="Ana", username="ana", email="ana@example.com")
            user.password = "senha-teste"
            token = user.generate_confirmation_token()
            self.assertFalse(user.confirm(token + "invalid"))
            user.email = "novo@example.com"
            self.assertFalse(user.confirm(token))
            self.assertFalse(user.confirmed)
