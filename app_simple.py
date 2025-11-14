"""
Flask Web Application for Dental Insurance Chatbot (Simplified)
This version works without RAG to avoid model download issues
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Import for sample data
from models import Member
from mcp_server import InsuranceDataStore
from sample_data import initialize_sample_data

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dental-insurance-chatbot-secret-key-' + str(uuid.uuid4()))
CORS(app)

# Initialize LLM and data store
llm = None
data_store = None
conversation_history = {}  # Store per member
current_member_id = "MEM001"  # Default member

def initialize_system():
    """Initialize the LLM connection and sample data"""
    global llm, data_store
    print("🚀 Initializing system...")
    
    # Initialize data store with sample data
    data_store = InsuranceDataStore()
    initialize_sample_data(data_store)
    print("✅ Sample data loaded")
    
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        model="llama-3-8b-instruct",
        temperature=0.2,
        streaming=False
    )
    print("✅ LLM initialized")
    print("🌐 Web application ready!")


@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')


@app.route('/api/members', methods=['GET'])
def get_members():
    """Get list of all members and dependents"""
    try:
        members_list = []
        
        # Get all members
        for member_id, member in data_store.members.items():
            members_list.append({
                'id': member.member_id,
                'name': f"{member.first_name} {member.last_name}",
                'type': 'Primary Member'
            })
            
            # Get dependents for this member
            if member_id in data_store.dependents:
                for dependent in data_store.dependents[member_id]:
                    members_list.append({
                        'id': dependent.dependent_id,
                        'name': f"{dependent.first_name} {dependent.last_name}",
                        'type': f"Dependent ({dependent.relationship})"
                    })
        
        return jsonify({
            'members': members_list,
            'current_member': current_member_id
        })
    except Exception as e:
        print(f"❌ Error getting members: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/select-member', methods=['POST'])
def select_member():
    """Select a member for the conversation"""
    global current_member_id
    try:
        data = request.json
        member_id = data.get('member_id')
        
        if not member_id:
            return jsonify({'error': 'No member_id provided'}), 400
        
        # Verify member exists
        if member_id not in data_store.members and not any(
            member_id == dep.dependent_id 
            for deps in data_store.dependents.values() 
            for dep in deps
        ):
            return jsonify({'error': 'Invalid member_id'}), 400
        
        current_member_id = member_id
        
        # Clear conversation history for new member
        if member_id in conversation_history:
            conversation_history[member_id] = []
        
        # Get member info
        if member_id in data_store.members:
            member = data_store.members[member_id]
            member_name = f"{member.first_name} {member.last_name}"
        else:
            # Find dependent
            for deps in data_store.dependents.values():
                for dep in deps:
                    if dep.dependent_id == member_id:
                        member_name = f"{dep.first_name} {dep.last_name}"
                        break
        
        return jsonify({
            'status': 'success',
            'member_id': member_id,
            'member_name': member_name
        })
    except Exception as e:
        print(f"❌ Error selecting member: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/claim/<claim_id>', methods=['GET'])
def get_claim_details(claim_id):
    """Get detailed information for a specific claim"""
    try:
        # Find the claim
        claim = None
        for member_claims in data_store.claims.values():
            for c in member_claims:
                if c.claim_id == claim_id:
                    claim = c
                    break
            if claim:
                break
        
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404
        
        # Format claim details
        claim_details = {
            'claim_id': claim.claim_id,
            'member_id': claim.member_id,
            'patient_name': claim.patient_name,
            'provider_name': claim.provider_name,
            'provider_npi': claim.provider_npi,
            'service_date': claim.service_date.strftime('%B %d, %Y'),
            'submission_date': claim.submission_date.strftime('%B %d, %Y at %I:%M %p'),
            'procedure_code': claim.procedure_code,
            'procedure_description': claim.procedure_description,
            'billed_amount': f"${claim.billed_amount:,.2f}",
            'allowed_amount': f"${claim.allowed_amount:,.2f}",
            'covered_amount': f"${claim.covered_amount:,.2f}",
            'patient_responsibility': f"${claim.patient_responsibility:,.2f}",
            'status': claim.status.value,
            'payment_date': claim.payment_date.strftime('%B %d, %Y') if claim.payment_date else 'Pending'
        }
        
        return jsonify({
            'status': 'success',
            'claim': claim_details
        })
        
    except Exception as e:
        print(f"❌ Error fetching claim details: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    global current_member_id
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize conversation history for this member if needed
        if current_member_id not in conversation_history:
            conversation_history[current_member_id] = []
        
        # Add user message to history
        conversation_history[current_member_id].append(HumanMessage(content=user_message))
        
        # Keep only last 10 messages to avoid context overflow
        if len(conversation_history[current_member_id]) > 10:
            conversation_history[current_member_id].pop(0)
        
        # Check if this is a claims-related query
        is_claims_query = any(keyword in user_message.lower() for keyword in ['claim', 'claims', 'submitted', 'paid', 'processing'])
        
        # Get member info for context
        member_context = ""
        member_name = ""
        claims_data_context = ""
        
        if current_member_id in data_store.members:
            member = data_store.members[current_member_id]
            member_name = f"{member.first_name} {member.last_name}"
            member_context = f"\n\nCurrent member: {member_name} (ID: {member.member_id})"
        else:
            # Find dependent
            for deps in data_store.dependents.values():
                for dep in deps:
                    if dep.dependent_id == current_member_id:
                        member_name = f"{dep.first_name} {dep.last_name}"
                        member_context = f"\n\nCurrent dependent: {member_name} (ID: {dep.dependent_id}, Relationship: {dep.relationship})"
                        break
        
        # If claims query, get ALL claims data and pass to LLM for intelligent filtering
        all_claims = []
        if is_claims_query:
            # For dependents, get claims from the primary member (MEM001)
            claims_member_id = "MEM001"
            
            if claims_member_id in data_store.claims:
                claims = data_store.claims[claims_member_id]
                # Filter claims for current member by patient name
                for claim in claims:
                    if claim.patient_name == member_name:
                        all_claims.append(claim)
                
                # Build claims data context for LLM
                if all_claims:
                    claims_data_context = "\n\nAVAILABLE CLAIMS DATA FOR THIS MEMBER:\n"
                    for claim in sorted(all_claims, key=lambda c: c.service_date, reverse=True):
                        claims_data_context += f"""
- Claim ID: {claim.claim_id}
  Status: {claim.status.value}
  Date: {claim.service_date.strftime('%m/%d/%y')}
  Amount: ${claim.billed_amount}
  Covered: ${claim.covered_amount}
  Your Cost: ${claim.patient_responsibility}
  Procedure: {claim.procedure_code} - {claim.procedure_description}
  Provider: {claim.provider_name}
  Submitted: {claim.submission_date.strftime('%m/%d/%y')}
"""
                    claims_data_context += """
INSTRUCTIONS: Based on the user's question, decide which claims to show:
- If they ask for "paid claims" or "claims that are paid", only include claims with Status: PAID
- If they ask for "not paid", "unpaid", "not yet paid", "pending", include claims with Status: APPROVED, PROCESSING, or DENIED (anything except PAID)
- If they ask for "approved claims", only include claims with Status: APPROVED and APPR
- If they ask for "processing" or "in process", only include claims with Status: PROCESSING
- If they ask for "denied claims", only include claims with Status: DENIED
- If they ask for "recent" or "last month", only include recent claims
- If they ask for "expensive" or "over $X", filter by amount
- If they ask for specific procedures (cleanings, crowns, fillings), filter by procedure description
- If they just ask "show my claims" or "all claims", include ALL claims listed above

Respond with ONLY:
1. A brief 1-2 sentence introduction
2. On a new line, write: SHOW_CLAIMS: followed by comma-separated claim IDs you want displayed
   Example: SHOW_CLAIMS: CLM001, CLM005, CLM002

Do not create any tables or lists yourself. Just provide the intro and SHOW_CLAIMS line.
"""
        
        # System message for dental insurance context
        system_msg = SystemMessage(content=f"""You are a helpful dental insurance assistant. 
        
Common dental insurance coverage:
- Preventive care: Cleanings, exams (typically 100% covered)
- Basic procedures: Fillings, extractions (typically 80% covered)
- Major procedures: Crowns, bridges (typically 50% covered)
- Annual maximums typically range from $1,500 to $3,000
- Waiting periods may apply for major procedures

{member_context}
{claims_data_context}

CRITICAL INSTRUCTIONS FOR CLAIMS:
- You are currently helping {member_name}.
- When the user asks about claims, you have access to all their claims data above.
- Based on their question, decide which claims to show using the SHOW_CLAIMS format explained above.
- Provide a brief 1-2 sentence introduction, then the SHOW_CLAIMS line with the claim IDs.
- DO NOT create tables, lists, or include specific claim details in your text.
- If the user wants claims for a different family member, tell them to use the dropdown menu.

For non-claims questions, provide helpful, accurate information about dental insurance plans, coverage, and procedures.""")
        
        # Get response from LLM
        messages = [system_msg] + conversation_history[current_member_id]
        response = llm.invoke(messages)
        
        # Extract response content
        assistant_message = response.content
        
        # Debug: Print the LLM response
        print(f"\n🤖 LLM Response:\n{assistant_message}\n")
        
        # Parse LLM response to extract claim IDs to show
        claims_html = ""
        if is_claims_query and "SHOW_CLAIMS:" in assistant_message:
            # Extract the claim IDs the LLM selected
            lines = assistant_message.split('\n')
            show_claims_line = None
            clean_message = []
            
            for line in lines:
                if line.strip().startswith("SHOW_CLAIMS:"):
                    show_claims_line = line
                    print(f"📋 Found SHOW_CLAIMS line: {line}")
                else:
                    clean_message.append(line)
            
            # Remove the SHOW_CLAIMS line from the message
            assistant_message = '\n'.join(clean_message).strip()
            
            # Extract claim IDs
            if show_claims_line:
                claim_ids_str = show_claims_line.split("SHOW_CLAIMS:")[1].strip()
                selected_claim_ids = [cid.strip() for cid in claim_ids_str.split(',')]
                print(f"✅ Selected claim IDs: {selected_claim_ids}")
                
                # Filter claims to only those selected by LLM
                selected_claims = [c for c in all_claims if c.claim_id in selected_claim_ids]
                print(f"📊 Found {len(selected_claims)} matching claims")
                
                if selected_claims:
                    claims_html = "\n\n" + format_claims_table(selected_claims, current_member_id)
                else:
                    claims_html = "\n\n<p class='no-claims'>No matching claims found.</p>"
        
        # Append claims table if available
        if claims_html:
            assistant_message += claims_html
        
        return jsonify({
            'response': assistant_message,
            'status': 'success',
            'member_id': current_member_id
        })
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


def format_claims_table(claims, member_id):
    """Format claims data as an HTML table"""
    if not claims:
        return ""
    
    # Get member name and determine if filtering by patient is needed
    member_name = ""
    patient_filter = None
    
    if member_id in data_store.members:
        member = data_store.members[member_id]
        member_name = f"{member.first_name} {member.last_name}"
        patient_filter = member_name  # Filter claims by this patient name
    else:
        # Find dependent
        for deps in data_store.dependents.values():
            for dep in deps:
                if dep.dependent_id == member_id:
                    member_name = f"{dep.first_name} {dep.last_name}"
                    patient_filter = member_name  # Filter claims by this patient name
                    break
    
    # Filter claims by patient name if this is a dependent or specific member
    filtered_claims = [c for c in claims if c.patient_name == patient_filter] if patient_filter else claims
    
    if not filtered_claims:
        return f"\n\nNo claims found for {member_name}."
    
    # Sort claims by service date (most recent first)
    sorted_claims = sorted(filtered_claims, key=lambda c: c.service_date, reverse=True)
    print(sorted_claims)
    # Add header with member info
    html = '<div class="claims-header">'
    html += f'<h4>Claims for {member_name}</h4>'
    html += f'<p class="member-id-info">Member ID: <strong>{member_id}</strong></p>'
    html += '</div>'
    
    html += '<table class="claims-table">'
    html += '<thead><tr>'
    html += '<th>Claim #</th>'
    html += '<th>Date</th>'
    html += '<th>Amount</th>'
    html += '<th>Procedure</th>'
    html += '</tr></thead><tbody>'
    
    for claim in sorted_claims:
        status_class = claim.status.value.lower()
        # Main row
        html += f'<tr class="claim-row" onclick="toggleClaimDetails(\'{claim.claim_id}\')">'
        html += f'<td class="claim-id-cell">'
        html += f'<a href="javascript:void(0)" class="claim-link" onclick="event.stopPropagation(); openClaimModal(\'{claim.claim_id}\')">{claim.claim_id}</a>'
        html += f'<span class="claim-status-badge {status_class}">{claim.status.value[:4].upper()}</span>'
        html += f'</td>'
        html += f'<td>{claim.service_date.strftime("%m/%d/%y")}</td>'
        html += f'<td class="amount-cell">${claim.billed_amount:,.0f}</td>'
        html += f'<td class="procedure-cell">'
        html += f'<span class="procedure-code">{claim.procedure_code}</span>'
        html += f'<span class="procedure-desc">{claim.procedure_description[:25]}...</span>'
        html += f'</td>'
        html += '</tr>'
        
        # Details row (hidden by default)
        html += f'<tr class="claim-details-row" id="details-{claim.claim_id}" style="display: none;">'
        html += '<td colspan="4" class="claim-details-cell">'
        html += '<div class="claim-details-content">'
        html += f'<div class="detail-item"><span class="detail-label">Patient:</span> {claim.patient_name}</div>'
        html += f'<div class="detail-item"><span class="detail-label">Provider:</span> {claim.provider_name}</div>'
        html += f'<div class="detail-item"><span class="detail-label">Submitted:</span> {claim.submission_date.strftime("%m/%d/%y")}</div>'
        html += f'<div class="detail-item"><span class="detail-label">Your Cost:</span> ${claim.patient_responsibility:,.2f}</div>'
        html += '</div>'
        html += '</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    
    return html


@app.route('/api/reset', methods=['POST'])
def reset_chat():
    """Reset the conversation"""
    global current_member_id
    if current_member_id in conversation_history:
        conversation_history[current_member_id] = []
    return jsonify({'status': 'success', 'message': 'Conversation reset'})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'llm_initialized': llm is not None
    })


if __name__ == '__main__':
    # Initialize system
    initialize_system()
    
    # Run Flask app
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
