import os

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
from datetime import datetime, timedelta
import json



class SecurityProvider:
    public_key=None
    private_key=None
    private_pem=None
    public_pem=None
    client_microservice_ip=None
    client_microservice_port=None

    @classmethod
    async def create(cls, generate_keys: bool, ask_for_keys: bool, client_microservice_ip: str= None, client_microservice_port: int= None):
        self = SecurityProvider()
        if generate_keys:
            self.generate_keys()
            
        if ask_for_keys: 
            self.client_microservice_ip = client_microservice_ip
            self.client_microservice_port = client_microservice_port
            self.public_key = self.get_public_key()
            
        return self

    def get_public_key(self):
        response= requests.get(f"http://{self.client_microservice_ip}:{self.client_microservice_port}/client/get/key")
        data = json.loads(response.text.strip('"').replace("\n", "\n"))
        public_key = data['public_key']
        return public_key

    @staticmethod
    def load_private_key():
        try:
            with open("private_key.pem", "rb") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Private key file not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the private key: {e}")

    @staticmethod
    def load_public_key():
        try:
            with open("public_key.pem", "rb") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Public key file not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the public key: {e}")


    def generate_keys(self):
        if os.path.exists("private_key.pem") and os.path.exists("public_key.pem"):
            print("Keys already exist. Skipping key generation.")
            return

        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        self.private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open("private_key.pem", "wb") as f:
            f.write(self.private_pem)

        self.public_key = self.private_key.public_key()
        self.public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open("public_key.pem", "wb") as f:
            f.write(self.public_pem)

        print("Keys generated successfully.")


    def create_token(self,data: dict, expires_delta: timedelta = timedelta(hours=3)):
        """Creates a JWT token with the given data and expiration."""
        private_key = self.load_private_key()
        data.update({"exp": datetime.utcnow() + expires_delta})
        headers = {
            "alg": "RS256",
            "typ": "JWT"
        }

        return jwt.encode(data, private_key, algorithm="RS256", headers=headers)


    def decode_token(self,token: str):
        """Decodes a JWT token and returns its payload."""
        
        if self.public_key is None:
            self.public_key = self.load_public_key()
            
        try:
            payload = jwt.decode(token, self.public_key, algorithms=["RS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")

    @staticmethod
    def validate_role(payload: dict, role: str) -> bool:
        """Checks if the user has admin privileges."""
        return payload.get("role") == role or payload.get("role") == "admin"

    @staticmethod
    def validar_fecha_expiracion(payload: dict) -> bool:
        # Obtiene la fecha de expiración del token
        exp_timestamp_str = payload.get("fecha_expiracion")
        if not exp_timestamp_str:
            return False

        exp_timestamp_datetime = datetime.fromisoformat(exp_timestamp_str)
        exp_timestamp = exp_timestamp_datetime.timestamp()
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp)

        # Comprueba si el token ha expirado
        return exp_datetime <= datetime.utcnow()