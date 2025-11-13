"""
MCP Server for Dental Insurance Data Access

This module implements the Model Context Protocol (MCP) server that exposes
insurance data access tools to the LangChain agent.
"""
import json
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from models import (
    Member, Dependent, Claim, Coverage, Procedure, 
    IDCard, BenefitUsage, ClaimStatus, CoverageType
)


class InsuranceDataStore:
    """
    Simulated data store for insurance information.
    In production, this would connect to actual databases.
    """
    
    def __init__(self):
        self.members: Dict[str, Member] = {}
        self.dependents: Dict[str, List[Dependent]] = {}
        self.claims: Dict[str, List[Claim]] = {}
        self.coverages: Dict[str, List[Coverage]] = {}
        self.procedures: Dict[str, Procedure] = {}
        self.id_cards: Dict[str, IDCard] = {}
        self.benefit_usage: Dict[str, BenefitUsage] = {}
        
    def add_member(self, member: Member):
        self.members[member.member_id] = member
        
    def add_dependent(self, dependent: Dependent):
        if dependent.primary_member_id not in self.dependents:
            self.dependents[dependent.primary_member_id] = []
        self.dependents[dependent.primary_member_id].append(dependent)
        
    def add_claim(self, claim: Claim):
        if claim.member_id not in self.claims:
            self.claims[claim.member_id] = []
        self.claims[claim.member_id].append(claim)
        
    def add_coverage(self, coverage: Coverage, member_id: str):
        if member_id not in self.coverages:
            self.coverages[member_id] = []
        self.coverages[member_id].append(coverage)
        
    def add_procedure(self, procedure: Procedure):
        self.procedures[procedure.procedure_code] = procedure
        
    def add_id_card(self, id_card: IDCard):
        self.id_cards[id_card.member_id] = id_card
        
    def add_benefit_usage(self, benefit_usage: BenefitUsage):
        self.benefit_usage[benefit_usage.member_id] = benefit_usage


class MCPInsuranceTools:
    """
    MCP Tools for accessing insurance data.
    These tools will be exposed to the LangChain agent.
    """
    
    def __init__(self, data_store: InsuranceDataStore):
        self.data_store = data_store
        
    def get_member_info(self, member_id: str) -> Dict[str, Any]:
        """
        Get member information by member ID.
        
        Args:
            member_id: The member's unique identifier
            
        Returns:
            Dictionary containing member information
        """
        member = self.data_store.members.get(member_id)
        if not member:
            return {"error": f"Member {member_id} not found"}
        
        return {
            "member_id": member.member_id,
            "name": f"{member.first_name} {member.last_name}",
            "date_of_birth": member.date_of_birth.isoformat(),
            "group_number": member.group_number,
            "plan_id": member.plan_id,
            "effective_date": member.effective_date.isoformat(),
            "email": member.email,
            "phone": member.phone
        }
    
    def get_dependents(self, member_id: str) -> List[Dict[str, Any]]:
        """
        Get all dependents for a member.
        
        Args:
            member_id: The primary member's unique identifier
            
        Returns:
            List of dependent information dictionaries
        """
        dependents = self.data_store.dependents.get(member_id, [])
        return [
            {
                "dependent_id": dep.dependent_id,
                "name": f"{dep.first_name} {dep.last_name}",
                "relationship": dep.relationship,
                "date_of_birth": dep.date_of_birth.isoformat(),
                "effective_date": dep.effective_date.isoformat()
            }
            for dep in dependents
        ]
    
    def get_claims(
        self, 
        member_id: str, 
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get claims for a member with optional filtering.
        
        Args:
            member_id: The member's unique identifier
            status: Optional claim status filter
            start_date: Optional start date (YYYY-MM-DD)
            end_date: Optional end date (YYYY-MM-DD)
            
        Returns:
            List of claim information dictionaries
        """
        claims = self.data_store.claims.get(member_id, [])
        
        # Filter by status if provided
        if status:
            claims = [c for c in claims if c.status == status]
        
        # Filter by date range if provided
        if start_date:
            start = datetime.fromisoformat(start_date).date()
            claims = [c for c in claims if c.service_date >= start]
        
        if end_date:
            end = datetime.fromisoformat(end_date).date()
            claims = [c for c in claims if c.service_date <= end]
        
        return [
            {
                "claim_id": claim.claim_id,
                "patient_name": claim.patient_name,
                "service_date": claim.service_date.isoformat(),
                "procedure": claim.procedure_description,
                "procedure_code": claim.procedure_code,
                "billed_amount": claim.billed_amount,
                "covered_amount": claim.covered_amount,
                "patient_responsibility": claim.patient_responsibility,
                "status": claim.status,
                "provider": claim.provider_name
            }
            for claim in claims
        ]
    
    def get_coverage_details(self, member_id: str) -> List[Dict[str, Any]]:
        """
        Get coverage details for a member's plan.
        
        Args:
            member_id: The member's unique identifier
            
        Returns:
            List of coverage information dictionaries
        """
        coverages = self.data_store.coverages.get(member_id, [])
        return [
            {
                "coverage_type": cov.coverage_type,
                "annual_maximum": cov.annual_maximum,
                "deductible": cov.deductible,
                "coinsurance": f"{cov.coinsurance_percentage}%",
                "frequency_limit": cov.frequency_limit or "No limit",
                "waiting_period": f"{cov.waiting_period_days} days" if cov.waiting_period_days > 0 else "No waiting period"
            }
            for cov in coverages
        ]
    
    def get_procedure_info(self, procedure_code: str) -> Dict[str, Any]:
        """
        Get information about a specific dental procedure.
        
        Args:
            procedure_code: The procedure code (e.g., D0120)
            
        Returns:
            Dictionary containing procedure information
        """
        procedure = self.data_store.procedures.get(procedure_code)
        if not procedure:
            return {"error": f"Procedure {procedure_code} not found"}
        
        return {
            "procedure_code": procedure.procedure_code,
            "name": procedure.procedure_name,
            "description": procedure.description,
            "coverage_type": procedure.coverage_type,
            "typical_cost": procedure.typical_cost
        }
    
    def get_id_card(self, member_id: str) -> Dict[str, Any]:
        """
        Get ID card information for a member.
        
        Args:
            member_id: The member's unique identifier
            
        Returns:
            Dictionary containing ID card information
        """
        id_card = self.data_store.id_cards.get(member_id)
        if not id_card:
            return {"error": f"ID card not found for member {member_id}"}
        
        return {
            "member_name": id_card.member_name,
            "member_id": id_card.member_id_display,
            "group_number": id_card.group_number,
            "plan_name": id_card.plan_name,
            "effective_date": id_card.effective_date.isoformat(),
            "customer_service": id_card.customer_service_phone,
            "claims_address": id_card.claims_address
        }
    
    def get_benefit_usage(self, member_id: str) -> Dict[str, Any]:
        """
        Get benefit usage information for a member.
        
        Args:
            member_id: The member's unique identifier
            
        Returns:
            Dictionary containing benefit usage information
        """
        usage = self.data_store.benefit_usage.get(member_id)
        if not usage:
            return {"error": f"Benefit usage not found for member {member_id}"}
        
        return {
            "plan_year": usage.plan_year,
            "annual_maximum": usage.annual_maximum,
            "used_amount": usage.used_amount,
            "remaining_amount": usage.remaining_amount,
            "deductible": usage.deductible,
            "deductible_met": usage.deductible_met,
            "deductible_remaining": usage.deductible_remaining,
            "last_updated": usage.last_updated.isoformat()
        }
    
    def search_procedures(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for procedures by name or description.
        
        Args:
            search_term: The term to search for
            
        Returns:
            List of matching procedure information dictionaries
        """
        search_lower = search_term.lower()
        matching_procedures = [
            proc for proc in self.data_store.procedures.values()
            if search_lower in proc.procedure_name.lower() 
            or search_lower in proc.description.lower()
        ]
        
        return [
            {
                "procedure_code": proc.procedure_code,
                "name": proc.procedure_name,
                "description": proc.description,
                "coverage_type": proc.coverage_type,
                "typical_cost": proc.typical_cost
            }
            for proc in matching_procedures
        ]


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get MCP tool definitions for the LangChain agent.
    
    Returns:
        List of tool definition dictionaries
    """
    return [
        {
            "name": "get_member_info",
            "description": "Get member information by member ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_id": {
                        "type": "string",
                        "description": "The member's unique identifier"
                    }
                },
                "required": ["member_id"]
            }
        },
        {
            "name": "get_dependents",
            "description": "Get all dependents for a member",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_id": {
                        "type": "string",
                        "description": "The primary member's unique identifier"
                    }
                },
                "required": ["member_id"]
            }
        },
        {
            "name": "get_claims",
            "description": "Get claims for a member with optional filtering by status and date range",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_id": {
                        "type": "string",
                        "description": "The member's unique identifier"
                    },
                    "status": {
                        "type": "string",
                        "description": "Optional claim status filter (submitted, processing, approved, denied, paid)"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Optional start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Optional end date in YYYY-MM-DD format"
                    }
                },
                "required": ["member_id"]
            }
        },
        {
            "name": "get_coverage_details",
            "description": "Get coverage details for a member's plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_id": {
                        "type": "string",
                        "description": "The member's unique identifier"
                    }
                },
                "required": ["member_id"]
            }
        },
        {
            "name": "get_procedure_info",
            "description": "Get information about a specific dental procedure by code",
            "parameters": {
                "type": "object",
                "properties": {
                    "procedure_code": {
                        "type": "string",
                        "description": "The procedure code (e.g., D0120)"
                    }
                },
                "required": ["procedure_code"]
            }
        },
        {
            "name": "get_id_card",
            "description": "Get ID card information for a member",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_id": {
                        "type": "string",
                        "description": "The member's unique identifier"
                    }
                },
                "required": ["member_id"]
            }
        },
        {
            "name": "get_benefit_usage",
            "description": "Get benefit usage information showing how much of annual maximum and deductible has been used",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_id": {
                        "type": "string",
                        "description": "The member's unique identifier"
                    }
                },
                "required": ["member_id"]
            }
        },
        {
            "name": "search_procedures",
            "description": "Search for dental procedures by name or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The term to search for in procedure names and descriptions"
                    }
                },
                "required": ["search_term"]
            }
        }
    ]
