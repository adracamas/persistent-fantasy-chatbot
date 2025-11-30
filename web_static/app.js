// Fantasy Chatbot Web Interface JavaScript

class FantasyChatbotUI {
    constructor() {
        this.ws = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.currentSessionId = null;
        
        this.initializeElements();
        this.initializeEventListeners();
        this.connectWebSocket();
        this.loadInitialData();
    }
    
    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.chatForm = document.getElementById('chat-form');
        this.loadingOverlay = document.getElementById('loading-overlay');
        
        // Status elements
        this.connectionStatus = document.getElementById('connection-status');
        this.wsStatus = document.getElementById('ws-status');
        this.memoryCount = document.getElementById('memory-count');
        
        // Sidebar elements
        this.memorySearch = document.getElementById('memory-search');
        this.memoryList = document.getElementById('memory-list');
        this.worldState = document.getElementById('world-state');
        this.sessionStats = document.getElementById('session-stats');
        
        // Stats elements
        this.procTime = document.getElementById('proc-time');
        this.memoriesUsed = document.getElementById('memories-used');
    }
    
    initializeEventListeners() {
        // Chat form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Memory search
        this.memorySearch.addEventListener('input', (e) => {
            this.searchMemories(e.target.value);
        });
        
        // Enter key handling for message input
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea if needed (for future multiline input)
        this.messageInput.addEventListener('input', (e) => {
            this.autoResizeInput(e.target);
        });
    }
    
    connectWebSocket() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
            
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.connected = true;
                this.updateConnectionStatus(true);
                this.hideLoading();
                this.reconnectAttempts = 0;
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleWebSocketMessage(data);
                } catch (e) {
                    console.error('Error parsing WebSocket message:', e);
                }
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.connected = false;
                this.updateConnectionStatus(false);
                this.attemptReconnect();
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.connected = false;
                this.updateConnectionStatus(false);
            };
            
        } catch (e) {
            console.error('Failed to connect WebSocket:', e);
            this.updateConnectionStatus(false);
            this.hideLoading();
        }
    }
    
    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'chat_response':
                this.displayMessage(data.user_input, data.response);
                this.updateSessionStats(data.processing_time, data.memories_used);
                this.refreshSidebarData();
                break;
                
            case 'broadcast':
                // Handle broadcast messages (shared sessions)
                console.log('Broadcast:', data.message);
                break;
                
            case 'error':
                this.showError(data.error);
                break;
                
            default:
                console.log('Unknown message type:', data.type);
        }
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connectWebSocket();
            }, this.reconnectDelay * this.reconnectAttempts);
        }
    }
    
    updateConnectionStatus(connected) {
        if (connected) {
            this.connectionStatus.textContent = 'Connected';
            this.connectionStatus.className = 'status online';
            this.wsStatus.className = 'ws-status connected';
        } else {
            this.connectionStatus.textContent = 'Disconnected';
            this.connectionStatus.className = 'status offline';
            this.wsStatus.className = 'ws-status';
        }
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.connected) return;
        
        // Clear input
        this.messageInput.value = '';
        
        // Show user message immediately
        this.displayMessage(message, '', true);
        
        // Send via WebSocket
        const messageData = {
            type: 'chat_message',
            message: message,
            timestamp: new Date().toISOString()
        };
        
        try {
            this.ws.send(JSON.stringify(messageData));
        } catch (e) {
            console.error('Failed to send message:', e);
            this.showError('Failed to send message');
        }
    }
    
    displayMessage(userInput, aiResponse = '', isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'ai'}`;
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="message-content">${this.escapeHtml(userInput)}</div>
                <div class="message-time">${this.formatTime(new Date())}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">${this.formatMessage(aiResponse)}</div>
                <div class="message-time">${this.formatTime(new Date())}</div>
            `;
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    formatMessage(message) {
        // Convert line breaks to paragraphs
        return message.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .map(line => `<p>${this.escapeHtml(line)}</p>`)
            .join('');
    }
    
    updateSessionStats(processingTime, memoriesUsed) {
        this.procTime.textContent = `${processingTime.toFixed(2)}s`;
        this.memoriesUsed.textContent = memoriesUsed;
    }
    
    async loadInitialData() {
        try {
            // Load memories
            await this.loadMemories();
            
            // Load world state
            await this.loadWorldState();
            
            // Load stats
            await this.loadStats();
            
        } catch (e) {
            console.error('Failed to load initial data:', e);
        }
    }
    
    async loadMemories() {
        try {
            const response = await fetch('/memories');
            const data = await response.json();
            
            this.displayMemories(data.memories);
            this.memoryCount.textContent = `${data.memories.length} memories`;
            
        } catch (e) {
            console.error('Failed to load memories:', e);
        }
    }
    
    displayMemories(memories) {
        this.memoryList.innerHTML = '';
        
        memories.slice(0, 10).forEach(memory => {
            const memoryItem = document.createElement('div');
            memoryItem.className = 'memory-item';
            memoryItem.innerHTML = `
                <div class="memory-type">${memory.type}</div>
                <div class="memory-name">${this.escapeHtml(memory.name || 'Unknown')}</div>
                <div class="memory-content">${this.escapeHtml(memory.content)}</div>
            `;
            
            memoryItem.addEventListener('click', () => {
                this.insertMemoryIntoChat(memory);
            });
            
            this.memoryList.appendChild(memoryItem);
        });
    }
    
    async searchMemories(query) {
        if (!query.trim()) {
            this.loadMemories();
            return;
        }
        
        try {
            const response = await fetch('/search-memories', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });
            
            const data = await response.json();
            this.displayMemories(data.results);
            
        } catch (e) {
            console.error('Failed to search memories:', e);
        }
    }
    
    async loadWorldState() {
        try {
            const response = await fetch('/world-state');
            const data = await response.json();
            
            this.displayWorldState(data.world_state);
            
        } catch (e) {
            console.error('Failed to load world state:', e);
        }
    }
    
    displayWorldState(worldState) {
        this.worldState.innerHTML = '';
        
        worldState.slice(-10).reverse().forEach(state => {
            const stateItem = document.createElement('div');
            stateItem.className = 'world-item';
            stateItem.innerHTML = `
                <span class="world-key">${this.escapeHtml(state.key)}</span>
                <span class="world-value">${this.escapeHtml(state.value)}</span>
            `;
            
            this.worldState.appendChild(stateItem);
        });
    }
    
    async loadStats() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.memory_stats) {
                this.updateStats(data.memory_stats);
            }
            
        } catch (e) {
            console.error('Failed to load stats:', e);
        }
    }
    
    updateStats(memoryStats) {
        // Update memory count
        this.memoryCount.textContent = `${memoryStats.total_memories} memories`;
    }
    
    insertMemoryIntoChat(memory) {
        const message = `Tell me more about ${memory.name || memory.type}: ${memory.content}`;
        this.messageInput.value = message;
        this.messageInput.focus();
    }
    
    refreshSidebarData() {
        // Refresh sidebar data after each message
        setTimeout(() => {
            this.loadMemories();
            this.loadWorldState();
        }, 1000);
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message ai';
        errorDiv.innerHTML = `
            <div class="message-content" style="color: #f44336;">
                <strong>Error:</strong> ${this.escapeHtml(message)}
            </div>
            <div class="message-time">${this.formatTime(new Date())}</div>
        `;
        
        this.chatMessages.appendChild(errorDiv);
        this.scrollToBottom();
    }
    
    showLoading() {
        this.loadingOverlay.style.display = 'flex';
    }
    
    hideLoading() {
        this.loadingOverlay.style.display = 'none';
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    autoResizeInput(input) {
        // Auto-resize for future multiline input support
        input.style.height = 'auto';
        input.style.height = input.scrollHeight + 'px';
    }
    
    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Fantasy Chatbot UI...');
    
    // Show loading screen
    const loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.style.display = 'flex';
    
    // Initialize the UI
    const app = new FantasyChatbotUI();
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            console.log('Page hidden - pausing connections');
        } else {
            console.log('Page visible - resuming connections');
            if (!app.connected) {
                app.connectWebSocket();
            }
        }
    });
    
    // Handle online/offline status
    window.addEventListener('online', () => {
        console.log('Back online - reconnecting');
        app.connectWebSocket();
    });
    
    window.addEventListener('offline', () => {
        console.log('Gone offline');
        app.updateConnectionStatus(false);
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to send message
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            app.sendMessage();
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            app.messageInput.value = '';
            app.messageInput.focus();
        }
    });
    
    // Prevent form submission on refresh
    window.addEventListener('beforeunload', (e) => {
        if (app.messageInput.value.trim()) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
    
    console.log('Fantasy Chatbot UI initialized successfully!');
});

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Note: Service worker would need to be implemented separately
        console.log('Service Worker support detected');
    });
}