from fastapi import FastAPI, HTTPException
from app.schemas import OTPRequest, OTPVerify
from app.otp_service import create_otp, verify_otp, OTPResult


app = FastAPI(title="OTP Microservice", version="1.0")

@app.post("/otp/generate")
def generate_otp(req: OTPRequest):
    result = create_otp(req.mobile)

    if result == OTPResult.SUCCESS:
        return {"message": "OTP sent successfully"}

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
