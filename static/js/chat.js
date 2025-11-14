// Chat Modal State
let isChatOpen = false;
let isProcessing = false;
let currentMemberId = null;

// DOM Elements
const chatModal = document.getElementById('chatModal');
const chatIcon = document.getElementById('chatIcon');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const chatNotification = document.getElementById('chatNotification');
const memberSelect = document.getElementById('memberSelect');
const claimModal = document.getElementById('claimModal');
const claimModalBody = document.getElementById('claimModalBody');

// Toggle Chat Modal
function toggleChat() {
    isChatOpen = !isChatOpen;
    
    if (isChatOpen) {
        openChat();
    } else {
        closeChat();
    }
}

function openChat() {
    chatModal.classList.add('open');
    chatIcon.style.display = 'none';
    chatNotification.classList.remove('show');
    isChatOpen = true;
    
    // Load members if not already loaded
    if (!memberSelect.options.length || memberSelect.options[0].value === '') {
        loadMembers();
    }
    
    // Focus on input
    setTimeout(() => {
        chatInput.focus();
    }, 300);
}

function closeChat() {
    chatModal.classList.remove('open');
    chatIcon.style.display = 'flex';
    isChatOpen = false;
}

// Auto-resize textarea
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
});

// Handle Enter key (send message)
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Add message to chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Convert markdown-style formatting to HTML
    const formattedContent = formatMessage(content);
    messageContent.innerHTML = formattedContent;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

// Format message content (basic markdown support)
function formatMessage(text) {
    // Replace newlines with <br>
    text = text.replace(/\n/g, '<br>');
    
    // Bold text **text**
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text *text*
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Code blocks ```code```
    text = text.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');
    
    // Inline code `code`
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Convert bullet points
    text = text.replace(/^- (.*?)$/gm, '<li>$1</li>');
    if (text.includes('<li>')) {
        text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    return text;
}

// Scroll chat to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
}

// Hide typing indicator
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Send message to backend
async function sendMessage() {
    const message = chatInput.value.trim();
    
    if (!message || isProcessing) {
        return;
    }
    
    // Add user message to chat
    addMessage(message, true);
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // Disable input while processing
    isProcessing = true;
    chatInput.disabled = true;
    sendButton.disabled = true;
    showTypingIndicator();
    
    try {
        // Send request to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add bot response to chat
        hideTypingIndicator();
        addMessage(data.response, false);
        
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', false);
    } finally {
        // Re-enable input
        isProcessing = false;
        chatInput.disabled = false;
        sendButton.disabled = false;
        chatInput.focus();
    }
}

// Reset conversation
async function resetChat() {
    if (!confirm('Are you sure you want to reset the conversation?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Clear chat messages
            chatMessages.innerHTML = '';
            
            // Add welcome message
            addMessage(`Hello! I'm your dental insurance assistant. I can help you with:

- Checking your coverage and claims
- Finding procedure costs
- Viewing your ID card
- Answering questions about your dental insurance

What would you like to know?`, false);
            
            console.log('Conversation reset successfully');
        } else {
            throw new Error('Failed to reset conversation');
        }
    } catch (error) {
        console.error('Error resetting chat:', error);
        alert('Failed to reset conversation. Please try again.');
    }
}

// Show notification badge
function showNotification() {
    if (!isChatOpen) {
        chatNotification.classList.add('show');
    }
}

// Load members list
async function loadMembers() {
    try {
        const response = await fetch('/api/members');
        if (!response.ok) {
            throw new Error('Failed to load members');
        }
        
        const data = await response.json();
        
        // Clear existing options
        memberSelect.innerHTML = '';
        
        // Add members to dropdown
        data.members.forEach(member => {
            const option = document.createElement('option');
            option.value = member.id;
            option.textContent = `${member.name} - ${member.type}`;
            memberSelect.appendChild(option);
        });
        
        // Set current member
        if (data.current_member) {
            memberSelect.value = data.current_member;
            currentMemberId = data.current_member;
        }
        
    } catch (error) {
        console.error('Error loading members:', error);
        memberSelect.innerHTML = '<option value="">Error loading members</option>';
    }
}

// Handle member selection change
async function handleMemberChange() {
    const selectedMemberId = memberSelect.value;
    
    if (!selectedMemberId || selectedMemberId === currentMemberId) {
        return;
    }
    
    try {
        const response = await fetch('/api/select-member', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ member_id: selectedMemberId })
        });
        
        if (!response.ok) {
            throw new Error('Failed to select member');
        }
        
        const data = await response.json();
        currentMemberId = data.member_id;
        
        // Clear chat and show new welcome message
        chatMessages.innerHTML = '';
        addMessage(`Hello! I'm now assisting ${data.member_name}. I can help you with:

- Checking coverage and claims
- Finding procedure costs
- Viewing ID card information
- Answering questions about your dental insurance

What would you like to know?`, false);
        
    } catch (error) {
        console.error('Error selecting member:', error);
        alert('Failed to switch member. Please try again.');
        // Revert selection
        if (currentMemberId) {
            memberSelect.value = currentMemberId;
        }
    }
}

// Open claim detail modal
async function openClaimModal(claimId) {
    claimModal.classList.add('open');
    claimModalBody.innerHTML = '<div class="loading-spinner">Loading claim details...</div>';
    
    try {
        const response = await fetch(`/api/claim/${claimId}`);
        if (!response.ok) {
            throw new Error('Failed to load claim details');
        }
        
        const data = await response.json();
        const claim = data.claim;
        
        // Build claim details HTML
        claimModalBody.innerHTML = `
            <div class="claim-detail-section">
                <h4>Claim Information</h4>
                <div class="claim-detail-grid">
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Claim ID</div>
                        <div class="claim-detail-value">${claim.claim_id}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Member ID</div>
                        <div class="claim-detail-value">${claim.member_id}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Patient Name</div>
                        <div class="claim-detail-value">${claim.patient_name}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Status</div>
                        <div class="claim-detail-value">
                            <span class="claim-status ${claim.status.toLowerCase()}">${claim.status.toUpperCase()}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="claim-detail-section">
                <h4>Service Details</h4>
                <div class="claim-detail-grid">
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Service Date</div>
                        <div class="claim-detail-value">${claim.service_date}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Submission Date</div>
                        <div class="claim-detail-value">${claim.submission_date}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Procedure Code</div>
                        <div class="claim-detail-value">${claim.procedure_code}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Procedure</div>
                        <div class="claim-detail-value">${claim.procedure_description}</div>
                    </div>
                </div>
            </div>

            <div class="claim-detail-section">
                <h4>Provider Information</h4>
                <div class="claim-detail-grid">
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Provider Name</div>
                        <div class="claim-detail-value">${claim.provider_name}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Provider NPI</div>
                        <div class="claim-detail-value">${claim.provider_npi}</div>
                    </div>
                </div>
            </div>

            <div class="claim-detail-section">
                <h4>Financial Details</h4>
                <div class="claim-detail-grid">
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Billed Amount</div>
                        <div class="claim-detail-value amount">${claim.billed_amount}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Allowed Amount</div>
                        <div class="claim-detail-value amount">${claim.allowed_amount}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Covered Amount</div>
                        <div class="claim-detail-value amount">${claim.covered_amount}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Your Responsibility</div>
                        <div class="claim-detail-value amount">${claim.patient_responsibility}</div>
                    </div>
                    <div class="claim-detail-item">
                        <div class="claim-detail-label">Payment Date</div>
                        <div class="claim-detail-value">${claim.payment_date}</div>
                    </div>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading claim details:', error);
        claimModalBody.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--error);">
                <p>Failed to load claim details. Please try again.</p>
            </div>
        `;
    }
}

// Close claim detail modal
function closeClaimModal() {
    claimModal.classList.remove('open');
}

// Toggle claim details row
function toggleClaimDetails(claimId) {
    const detailsRow = document.getElementById(`details-${claimId}`);
    if (detailsRow) {
        if (detailsRow.style.display === 'none') {
            detailsRow.style.display = 'table-row';
        } else {
            detailsRow.style.display = 'none';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dental Insurance Chatbot initialized');
    
    // Add welcome message
    addMessage(`Hello! I'm your dental insurance assistant. I can help you with:

- Checking your coverage and claims
- Finding procedure costs
- Viewing your ID card
- Answering questions about your dental insurance

What would you like to know?`, false);
    
    // Show welcome notification after 3 seconds
    setTimeout(() => {
        showNotification();
    }, 3000);
});

// Handle clicks outside chat modal to close it
document.addEventListener('click', function(event) {
    if (isChatOpen && 
        !chatModal.contains(event.target) && 
        !chatIcon.contains(event.target)) {
        // Don't close if clicking inside modal or on chat icon
        // This is handled by the close button
    }
});

// Prevent chat modal clicks from closing it
chatModal.addEventListener('click', function(event) {
    event.stopPropagation();
});
