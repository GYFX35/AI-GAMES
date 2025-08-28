import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse
from typing import List
import jwt

app = FastAPI()

# The 'uploads' directory is at the root of the project.
# The API is run from the 'api' directory.
# So we need to go one level up.
UPLOADS_DIR = "../uploads"

@app.post("/models", status_code=201)
async def upload_model(file: UploadFile = File(...)):
    """
    Upload a 3D model file.
    """
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

    file_path = os.path.join(UPLOADS_DIR, file.filename)

    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail="File with this name already exists.")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()


    return {"filename": file.filename, "content_type": file.content_type}

@app.get("/models", response_model=List[str])
async def list_models():
    """
    Get a list of all available 3D models.
    """
    if not os.path.exists(UPLOADS_DIR):
        return []
    return os.listdir(UPLOADS_DIR)

@app.get("/models/{model_name}")
async def download_model(model_name: str):
    """
    Download a 3D model file.
    """
    file_path = os.path.join(UPLOADS_DIR, model_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found.")
    return FileResponse(file_path)

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """
    Delete a 3D model file.
    """
    file_path = os.path.join(UPLOADS_DIR, model_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found.")
    os.remove(file_path)
    return {"message": f"Model '{model_name}' deleted successfully."}

@app.post("/api/verify_purchase")
async def verify_purchase(request: Request):
    """
    Verify the purchase with Facebook.
    """
    data = await request.json()
    signed_request = data.get('signedRequest')

    if not signed_request:
        raise HTTPException(status_code=400, detail="signedRequest not provided.")

    # You must get your App Secret from your Facebook Developer Dashboard
    app_secret = "YOUR_APP_SECRET" # IMPORTANT: Replace with your actual App Secret

    try:
        # The signed request is a JWT. The first part is the signature, the second is the payload.
        # We need to decode it to get the payment information.
        # Note: Facebook's signed_request is a bit different from a standard JWT.
        # It's in the format `signature.payload`, where both are base64-url-encoded.
        # The signature is an HMAC-SHA256 hash of the payload, using your app secret as the key.
        # The PyJWT library expects the format `header.payload.signature`.
        # We will need to parse this manually.

        parts = signed_request.split('.')
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail="Invalid signedRequest format.")

        encoded_sig, payload = parts

        # The payload is a base64-url encoded JSON string.
        decoded_payload = jwt.utils.base64url_decode(payload)

        # The signature needs to be verified against the payload.
        # The `jwt.decode` function can do this, but it expects a full JWT.
        # We can construct a dummy JWT to use the library's verification logic.
        # The algorithm used by Facebook is HMAC-SHA256.

        # A proper implementation would look something like this:
        import hmac
        import hashlib
        import base64

        # The signature is a HMAC-SHA256 hash of the payload, using your app secret as the key.
        expected_sig = hmac.new(app_secret.encode(), msg=payload.encode(), digestmod=hashlib.sha256).digest()

        # The provided signature is base64-url-encoded. It needs to be decoded.
        # Add padding if necessary.
        try:
            provided_sig = base64.urlsafe_b64decode(encoded_sig + '==')
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid signature encoding.")

        if not hmac.compare_digest(expected_sig, provided_sig):
            raise HTTPException(status_code=400, detail="Signature validation failed.")

        # If the signature is valid, we can now decode the payload.
        payload_data = jwt.decode(payload + ".", options={"verify_signature": False}) # Signature already verified


        if payload_data.get('status') == 'completed':
            return {"status": "completed"}
        else:
            return {"status": "failed", "detail": payload_data.get('status')}

    except jwt.PyJWTError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JWT: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
