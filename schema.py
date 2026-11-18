"""Pydantic models for the single Gemini JSON response."""
from typing import List, Literal

from pydantic import BaseModel, Field


class SuspiciousPhrase(BaseModel):
    phrase: str = Field(description="Exact substring copied from extracted_text")
    reason: str = Field(description="Short reason this phrase is suspicious")


class UrlIssue(BaseModel):
    url: str
    issue: str = Field(description="Problem with this URL, or 'No obvious issue'")


class Extracted(BaseModel):
    urls: List[UrlIssue]
    phone_numbers: List[str]
    account_numbers: List[str]


class PressureProfile(BaseModel):
    urgency: int = Field(ge=0, le=100)
    fear: int = Field(ge=0, le=100)
    authority: int = Field(ge=0, le=100)
    greed: int = Field(ge=0, le=100)
    secrecy: int = Field(ge=0, le=100)


class HowThisScamWorks(BaseModel):
    hook: str
    pressure: str
    payment: str


class RealVsFake(BaseModel):
    genuine_example: str = Field(
        description="Generic illustration of a genuine message from this type of organization"
    )
    real_org_never_asks: List[str]


class RecoveryTriage(BaseModel):
    clicked_link: List[str]
    shared_otp_or_pin: List[str]
    sent_money: List[str]
    installed_app: List[str]


class ScamReport(BaseModel):
    extracted_text: str
    scam_probability: int = Field(ge=0, le=100)
    verdict: Literal["Safe", "Suspicious", "Likely Scam"]
    scam_type: str
    impersonating: str
    impersonation_reason: str
    explanation_simple: str
    explanation_roman_urdu: str
    red_flags: List[str]
    suspicious_phrases: List[SuspiciousPhrase]
    extracted: Extracted
    pressure_profile: PressureProfile
    how_this_scam_works: HowThisScamWorks
    what_to_do: List[str]
    safe_reply: str
    family_warning_roman_urdu: str
    real_vs_fake: RealVsFake
    recovery_triage: RecoveryTriage
    report_text: str
    confidence_note: str
