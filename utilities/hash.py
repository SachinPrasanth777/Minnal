import jwt
import bcrypt
from dotenv import load_dotenv
import os
import datetime
from schema.models import UserSignUp

load_dotenv()


class Hash:
    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def generate_token(self, email: str) -> str:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        payload = {"sub": email, "exp": expiration}
        return jwt.encode(payload, os.getenv("SECRET"), algorithm="HS256")
