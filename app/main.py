from fastapi import FastAPI, HTTPException
from app.schemas import OTPRequest, OTPVerify
from app.otp_service import create_otp, verify_otp, OTPResult
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OTP Microservice", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/otp/generate")
def generate_otp(req: OTPRequest):
    result, otp = create_otp(req.mobile)

    if result == OTPResult.SUCCESS:
        return {
            "message": "OTP generated",
            "otp": otp   # 🔹 demo visibility
        }

    if result == OTPResult.RATE_LIMITED:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later."
        )

    if result == OTPResult.REDIS_UNAVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="OTP service temporarily unavailable"
        )


@app.post("/otp/verify")
def verify(req: OTPVerify):
    result = verify_otp(req.mobile, req.otp)
    return {"valid": result}
