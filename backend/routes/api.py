from __future__ import annotations
from fastapi import APIRouter, HTTPException, Request
from backend.db import dashboard_stats, record_analysis
from backend.models.schemas import AnalyzeRequest, GenerateRequest
from backend.services.breach_checker import hibp_k_anonymity_check
from backend.services.common_password_checker import load_common_passwords
from backend.services.password_analyzer import analyze_password
from backend.services.password_generator import generate_complex_password, generate_passphrase
from backend.services.policy_checker import Policy

router = APIRouter(prefix="/api")
COMMON_PASSWORDS = load_common_passwords()

# Simple per-process rate limiter for the educational deployment.
_BUCKET: dict[str, list[float]] = {}
WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 300


def _rate_limit(request: Request) -> None:
    import time
    host = request.client.host if request.client else "unknown"
    now = time.monotonic()
    recent = [t for t in _BUCKET.get(host, []) if now - t < WINDOW_SECONDS]
    if len(recent) >= MAX_REQUESTS_PER_WINDOW:
        raise HTTPException(status_code=429, detail="Too many analysis requests. Please slow down.")
    recent.append(now)
    _BUCKET[host] = recent


@router.get("/health")
def health():
    return {"status": "ok", "service": "password-strength-analyzer"}


@router.post("/analyze")
def api_analyze(payload: AnalyzeRequest, request: Request):
    _rate_limit(request)
    context = payload.context.model_dump() if payload.context else None
    policy = payload.policy
    policy_obj = Policy(
        minimum_length=policy.minimum_length if policy else 15,
        common_password_check=policy.common_password_check if policy else True,
        personal_info_check=policy.personal_info_check if policy else True,
        maximum_length=policy.maximum_length if policy else 128,
    )
    result = analyze_password(
        payload.password,
        common_passwords=COMMON_PASSWORDS,
        context=context,
        breach_hashes=None,
        policy=policy_obj,
        include_breach=False,
    )
    # Local demo breach check is explicit and does not send data externally.
    if payload.check_local_breach:
        from backend.services.breach_checker import load_breach_hashes, local_breach_check
        demo_hashes = load_breach_hashes()
        result["breach_check"] = local_breach_check(payload.password, demo_hashes)
        if result["breach_check"]["compromised"]:
            result["findings"].append({"type": "breach_exposure", "severity": "critical", "description": "The password matched the local demonstration breach hash set."})
            result["score"] = 0
            result["classification"] = "VERY WEAK"
            result["suggestions"] = list(dict.fromkeys(result["suggestions"] + ["Change a password immediately when there is evidence it has been compromised."]))[:8]
    else:
        result["breach_check"] = {"checked": False, "compromised": False, "source": "disabled"}

    analysis_id = record_analysis(result)
    result["analysis_id"] = analysis_id
    return result


@router.post("/generate")
def api_generate(payload: GenerateRequest):
    if payload.mode == "complex":
        value = generate_complex_password(payload.length, payload.uppercase, payload.lowercase, payload.numbers, payload.symbols)
    else:
        value = generate_passphrase(payload.words)
    return {"password": value, "mode": payload.mode, "stored": False}


@router.post("/breach-check")
def api_remote_breach_check(payload: AnalyzeRequest, request: Request):
    _rate_limit(request)
    # This endpoint is intentionally separate from real-time analysis.
    if not payload.password:
        return {"checked": False, "compromised": False, "source": "none"}
    try:
        return hibp_k_anonymity_check(payload.password)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Remote breach check unavailable") from None


@router.get("/dashboard/stats")
def api_dashboard_stats():
    return dashboard_stats()
