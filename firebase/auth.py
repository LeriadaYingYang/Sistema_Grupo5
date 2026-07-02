import requests

API_KEY = "https://iisem-1f66d-default-rtdb.firebaseio.com/"

def iniciar_sesion_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

    datos = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    respuesta = requests.post(url, json=datos)

    if respuesta.status_code == 200:
        resultado = respuesta.json()
        return {
            "uid": resultado["localId"],
            "email": resultado["email"],
            "id_token": resultado["idToken"]
        }

    return None