from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from team3_chassis.security.securityprovider import SecurityProvider


class AutenticationMiddleware(BaseHTTPMiddleware):    
    def __init__(self, app, valid_routes=None, ask_for_keys:bool= None, generate_keys:bool= None, client_microservice_ip:str= None, client_microservice_port:int= None, role:str=None):
        super().__init__(app)
        # Permite personalizar las rutas válidas, con un valor por defecto
        self.valid_routes = valid_routes
        self.ask_for_keys = ask_for_keys
        self.generate_keys = generate_keys
        self.client_microservice_ip = client_microservice_ip
        self.client_microservice_port = client_microservice_port
        self.role = role
        

    async def dispatch(self, request: Request, call_next):
        for route_method, route_path in self.valid_routes:
            if route_path == request.url.path and (route_method is None or route_method == request.method):
                print("Valid route")
                return await call_next(request)
        try:
            security_service = await SecurityProvider.create(self.generate_keys, self.ask_for_keys, self.client_microservice_ip, self.client_microservice_port)
            # Extrae el token del encabezado Authorization
            auth: HTTPAuthorizationCredentials = request.headers.get("Authorization")

            if not auth or not auth.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

            token = auth.split(" ")[1]  # Obtiene el token después de 'Bearer'

            # Decodifica el token
            payload = security_service.decode_token(token)

            # Verifica la fecha de expiración
            if security_service.validar_fecha_expiracion(payload):
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})

            # Verifica si el usuario es admin (si es necesario)
            if not security_service.validate_role(payload, self.role):
                return JSONResponse(status_code=403, content={"detail": "Insufficient permissions"})

            response = await call_next(request)
            return response

        except HTTPException as exc:
            # Puedes personalizar aquí aún más el manejo de excepciones
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

        except Exception as exc:
            # Manejo de otras excepciones no previstas
            print(exc)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
