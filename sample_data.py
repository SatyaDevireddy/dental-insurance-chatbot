"""
Sample data initialization for testing the chatbot
"""
from datetime import date, datetime, timedelta
from models import (
    Member, Dependent, Claim, Coverage, Procedure, 
    IDCard, BenefitUsage, ClaimStatus, CoverageType
)
from mcp_server import InsuranceDataStore


def initialize_sample_data(data_store: InsuranceDataStore):
    """
    Initialize the data store with sample insurance data.
    
    Args:
        data_store: InsuranceDataStore instance to populate
    """
    # Create first sample member - John Smith
    member = Member(
        member_id="MEM001",
        first_name="John",
        last_name="Smith",
        date_of_birth=date(1985, 3, 15),
        email="john.smith@example.com",
        phone="555-123-4567",
        address="123 Main St, Anytown, ST 12345",
        group_number="GRP12345",
        plan_id="PLAN001",
        effective_date=date(2024, 1, 1),
        is_primary=True
    )
    data_store.add_member(member)
    
    # Create second sample member - Sarah Johnson
    member2 = Member(
        member_id="MEM002",
        first_name="Sarah",
        last_name="Johnson",
        date_of_birth=date(1990, 8, 22),
        email="sarah.johnson@example.com",
        phone="555-234-5678",
        address="456 Oak Ave, Springfield, ST 67890",
        group_number="GRP12346",
        plan_id="PLAN001",
        effective_date=date(2024, 1, 1),
        is_primary=True
    )
    data_store.add_member(member2)
    
    # Create third sample member - Robert Davis
    member3 = Member(
        member_id="MEM003",
        first_name="Robert",
        last_name="Davis",
        date_of_birth=date(1978, 11, 5),
        email="robert.davis@example.com",
        phone="555-345-6789",
        address="789 Pine Rd, Riverside, ST 11223",
        group_number="GRP12347",
        plan_id="PLAN001",
        effective_date=date(2024, 1, 1),
        is_primary=True
    )
    data_store.add_member(member3)
    
    # Create sample dependents
    spouse = Dependent(
        dependent_id="DEP001",
        primary_member_id="MEM001",
        first_name="Jane",
        last_name="Smith",
        date_of_birth=date(1987, 7, 22),
        relationship="spouse",
        effective_date=date(2024, 1, 1)
    )
    data_store.add_dependent(spouse)
    
    child1 = Dependent(
        dependent_id="DEP002",
        primary_member_id="MEM001",
        first_name="Emily",
        last_name="Smith",
        date_of_birth=date(2015, 5, 10),
        relationship="child",
        effective_date=date(2024, 1, 1)
    )
    data_store.add_dependent(child1)
    
    child2 = Dependent(
        dependent_id="DEP003",
        primary_member_id="MEM001",
        first_name="Michael",
        last_name="Smith",
        date_of_birth=date(2018, 9, 3),
        relationship="child",
        effective_date=date(2024, 1, 1)
    )
    data_store.add_dependent(child2)
    
    # Create sample coverage
    coverages = [
        Coverage(
            plan_id="PLAN001",
            coverage_type=CoverageType.PREVENTIVE,
            annual_maximum=999999,  # No limit for preventive
            deductible=0,
            coinsurance_percentage=100,
            frequency_limit="Twice per year",
            waiting_period_days=0
        ),
        Coverage(
            plan_id="PLAN001",
            coverage_type=CoverageType.BASIC,
            annual_maximum=2000,
            deductible=50,
            coinsurance_percentage=80,
            frequency_limit=None,
            waiting_period_days=0
        ),
        Coverage(
            plan_id="PLAN001",
            coverage_type=CoverageType.MAJOR,
            annual_maximum=2000,
            deductible=50,
            coinsurance_percentage=50,
            frequency_limit=None,
            waiting_period_days=180
        ),
        Coverage(
            plan_id="PLAN001",
            coverage_type=CoverageType.ORTHODONTIC,
            annual_maximum=2000,  # Lifetime maximum
            deductible=0,
            coinsurance_percentage=50,
            frequency_limit=None,
            waiting_period_days=365
        )
    ]
    
    for coverage in coverages:
        data_store.add_coverage(coverage, "MEM001")
    
    # Create sample procedures
    procedures = [
        Procedure(
            procedure_code="D0120",
            procedure_name="Periodic Oral Evaluation",
            description="Regular dental checkup and examination",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=75.00
        ),
        Procedure(
            procedure_code="D0150",
            procedure_name="Comprehensive Oral Evaluation",
            description="Complete examination for new patients",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=150.00
        ),
        Procedure(
            procedure_code="D0210",
            procedure_name="Intraoral X-rays (Complete Series)",
            description="Full mouth X-rays",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=125.00
        ),
        Procedure(
            procedure_code="D0220",
            procedure_name="Intraoral X-ray (First Film)",
            description="First periapical X-ray",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=25.00
        ),
        Procedure(
            procedure_code="D0274",
            procedure_name="Bitewing X-rays (Four Films)",
            description="Four bitewing X-rays",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=50.00
        ),
        Procedure(
            procedure_code="D1110",
            procedure_name="Prophylaxis - Adult",
            description="Routine teeth cleaning for adults",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=100.00
        ),
        Procedure(
            procedure_code="D1120",
            procedure_name="Prophylaxis - Child",
            description="Routine teeth cleaning for children",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=75.00
        ),
        Procedure(
            procedure_code="D1208",
            procedure_name="Fluoride Treatment",
            description="Topical fluoride application",
            coverage_type=CoverageType.PREVENTIVE,
            typical_cost=35.00
        ),
        Procedure(
            procedure_code="D2140",
            procedure_name="Amalgam Filling (One Surface)",
            description="Silver filling for one tooth surface",
            coverage_type=CoverageType.BASIC,
            typical_cost=150.00
        ),
        Procedure(
            procedure_code="D2150",
            procedure_name="Amalgam Filling (Two Surfaces)",
            description="Silver filling for two tooth surfaces",
            coverage_type=CoverageType.BASIC,
            typical_cost=180.00
        ),
        Procedure(
            procedure_code="D2391",
            procedure_name="Composite Filling (One Surface)",
            description="Tooth-colored filling for one surface",
            coverage_type=CoverageType.BASIC,
            typical_cost=175.00
        ),
        Procedure(
            procedure_code="D3310",
            procedure_name="Root Canal - Anterior Tooth",
            description="Root canal therapy for front tooth",
            coverage_type=CoverageType.BASIC,
            typical_cost=800.00
        ),
        Procedure(
            procedure_code="D3320",
            procedure_name="Root Canal - Bicuspid",
            description="Root canal therapy for bicuspid tooth",
            coverage_type=CoverageType.BASIC,
            typical_cost=900.00
        ),
        Procedure(
            procedure_code="D3330",
            procedure_name="Root Canal - Molar",
            description="Root canal therapy for molar tooth",
            coverage_type=CoverageType.BASIC,
            typical_cost=1200.00
        ),
        Procedure(
            procedure_code="D2740",
            procedure_name="Crown - Porcelain Fused to Metal",
            description="Crown with metal base and porcelain coating",
            coverage_type=CoverageType.MAJOR,
            typical_cost=1200.00
        ),
        Procedure(
            procedure_code="D2750",
            procedure_name="Crown - Porcelain",
            description="All-porcelain crown",
            coverage_type=CoverageType.MAJOR,
            typical_cost=1300.00
        ),
        Procedure(
            procedure_code="D6010",
            procedure_name="Surgical Placement of Implant",
            description="Dental implant surgery",
            coverage_type=CoverageType.MAJOR,
            typical_cost=2500.00
        ),
        Procedure(
            procedure_code="D5110",
            procedure_name="Complete Upper Denture",
            description="Full denture for upper jaw",
            coverage_type=CoverageType.MAJOR,
            typical_cost=1500.00
        ),
        Procedure(
            procedure_code="D5120",
            procedure_name="Complete Lower Denture",
            description="Full denture for lower jaw",
            coverage_type=CoverageType.MAJOR,
            typical_cost=1500.00
        ),
        Procedure(
            procedure_code="D8080",
            procedure_name="Comprehensive Orthodontic Treatment",
            description="Full orthodontic treatment (braces)",
            coverage_type=CoverageType.ORTHODONTIC,
            typical_cost=5000.00
        )
    ]
    
    for procedure in procedures:
        data_store.add_procedure(procedure)
    
    # Create sample claims
    claims = [
        Claim(
            claim_id="CLM001",
            member_id="MEM001",
            patient_name="John Smith",
            provider_name="Dr. Sarah Johnson, DDS",
            provider_npi="1234567890",
            service_date=date(2024, 6, 15),
            submission_date=datetime(2024, 6, 16, 10, 30),
            procedure_code="D1110",
            procedure_description="Prophylaxis - Adult",
            billed_amount=100.00,
            allowed_amount=100.00,
            covered_amount=100.00,
            patient_responsibility=0.00,
            status=ClaimStatus.PAID,
            payment_date=date(2024, 6, 25)
        ),
        Claim(
            claim_id="CLM002",
            member_id="MEM001",
            patient_name="John Smith",
            provider_name="Dr. Sarah Johnson, DDS",
            provider_npi="1234567890",
            service_date=date(2024, 6, 15),
            submission_date=datetime(2024, 6, 16, 10, 30),
            procedure_code="D0120",
            procedure_description="Periodic Oral Evaluation",
            billed_amount=75.00,
            allowed_amount=75.00,
            covered_amount=75.00,
            patient_responsibility=0.00,
            status=ClaimStatus.PAID,
            payment_date=date(2024, 6, 25)
        ),
        Claim(
            claim_id="CLM003",
            member_id="MEM001",
            patient_name="Jane Smith",
            provider_name="Dr. Sarah Johnson, DDS",
            provider_npi="1234567890",
            service_date=date(2024, 7, 10),
            submission_date=datetime(2024, 7, 11, 14, 15),
            procedure_code="D2391",
            procedure_description="Composite Filling (One Surface)",
            billed_amount=175.00,
            allowed_amount=175.00,
            covered_amount=140.00,  # 80% after deductible
            patient_responsibility=35.00,
            status=ClaimStatus.PAID,
            payment_date=date(2024, 7, 20)
        ),
        Claim(
            claim_id="CLM004",
            member_id="MEM001",
            patient_name="Emily Smith",
            provider_name="Dr. Michael Lee, DDS",
            provider_npi="0987654321",
            service_date=date(2024, 8, 5),
            submission_date=datetime(2024, 8, 6, 9, 0),
            procedure_code="D1120",
            procedure_description="Prophylaxis - Child",
            billed_amount=75.00,
            allowed_amount=75.00,
            covered_amount=75.00,
            patient_responsibility=0.00,
            status=ClaimStatus.PAID,
            payment_date=date(2024, 8, 15)
        ),
        Claim(
            claim_id="CLM005",
            member_id="MEM001",
            patient_name="John Smith",
            provider_name="Dr. Sarah Johnson, DDS",
            provider_npi="1234567890",
            service_date=date(2024, 9, 20),
            submission_date=datetime(2024, 9, 21, 11, 45),
            procedure_code="D2740",
            procedure_description="Crown - Porcelain Fused to Metal",
            billed_amount=1200.00,
            allowed_amount=1200.00,
            covered_amount=600.00,  # 50% after deductible
            patient_responsibility=600.00,
            status=ClaimStatus.APPROVED,
            payment_date=None
        ),
        Claim(
            claim_id="CLM006",
            member_id="MEM001",
            patient_name="Michael Smith",
            provider_name="Dr. Michael Lee, DDS",
            provider_npi="0987654321",
            service_date=date(2024, 10, 12),
            submission_date=datetime(2024, 10, 13, 8, 30),
            procedure_code="D1208",
            procedure_description="Fluoride Treatment",
            billed_amount=35.00,
            allowed_amount=35.00,
            covered_amount=35.00,
            patient_responsibility=0.00,
            status=ClaimStatus.PROCESSING,
            payment_date=None
        )
    ]
    
    for claim in claims:
        data_store.add_claim(claim)
    
    # Create sample ID card
    id_card = IDCard(
        member_id="MEM001",
        member_name="John Smith",
        group_number="GRP12345",
        plan_id="PLAN001",
        plan_name="Comprehensive Dental PPO",
        effective_date=date(2024, 1, 1),
        member_id_display="MEM001-001",
        customer_service_phone="1-800-DENTAL-1 (1-800-336-8251)",
        claims_address="Dental Insurance Claims, PO Box 12345, Insurance City, ST 54321"
    )
    data_store.add_id_card(id_card)
    
    # Create sample benefit usage
    benefit_usage = BenefitUsage(
        member_id="MEM001",
        plan_year=2024,
        annual_maximum=2000.00,
        used_amount=915.00,  # Sum of non-preventive covered amounts
        remaining_amount=1085.00,
        deductible=50.00,
        deductible_met=50.00,
        deductible_remaining=0.00,
        last_updated=datetime(2024, 10, 13, 8, 30)
    )
    data_store.add_benefit_usage(benefit_usage)
