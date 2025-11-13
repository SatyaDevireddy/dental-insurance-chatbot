"""
Data models for dental insurance system
"""
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ClaimStatus(str, Enum):
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    APPROVED = "approved"
    DENIED = "denied"
    PAID = "paid"


class CoverageType(str, Enum):
    PREVENTIVE = "preventive"
    BASIC = "basic"
    MAJOR = "major"
    ORTHODONTIC = "orthodontic"


class Member(BaseModel):
    """Member information"""
    member_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: str
    phone: str
    address: str
    group_number: str
    plan_id: str
    effective_date: date
    is_primary: bool = True
    primary_member_id: Optional[str] = None  # For dependents


class Dependent(BaseModel):
    """Dependent information"""
    dependent_id: str
    primary_member_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    relationship: str  # spouse, child, etc.
    effective_date: date


class Procedure(BaseModel):
    """Dental procedure information"""
    procedure_code: str
    procedure_name: str
    description: str
    coverage_type: CoverageType
    typical_cost: float


class Coverage(BaseModel):
    """Coverage details for a plan"""
    plan_id: str
    coverage_type: CoverageType
    annual_maximum: float
    deductible: float
    coinsurance_percentage: int  # e.g., 80 means 80% covered
    frequency_limit: Optional[str] = None  # e.g., "twice per year"
    waiting_period_days: int = 0


class Claim(BaseModel):
    """Insurance claim"""
    claim_id: str
    member_id: str
    patient_name: str  # Could be member or dependent
    provider_name: str
    provider_npi: str
    service_date: date
    submission_date: datetime
    procedure_code: str
    procedure_description: str
    billed_amount: float
    allowed_amount: float
    covered_amount: float
    patient_responsibility: float
    status: ClaimStatus
    denial_reason: Optional[str] = None
    payment_date: Optional[date] = None


class IDCard(BaseModel):
    """Member ID card information"""
    member_id: str
    member_name: str
    group_number: str
    plan_id: str
    plan_name: str
    effective_date: date
    member_id_display: str
    customer_service_phone: str
    claims_address: str


class BenefitUsage(BaseModel):
    """Benefit usage tracking"""
    member_id: str
    plan_year: int
    annual_maximum: float
    used_amount: float
    remaining_amount: float
    deductible: float
    deductible_met: float
    deductible_remaining: float
    last_updated: datetime


class PlanDocument(BaseModel):
    """Plan documents for RAG"""
    document_id: str
    plan_id: str
    document_type: str  # policy, benefits_summary, provider_directory, etc.
    title: str
    content: str
    last_updated: date
