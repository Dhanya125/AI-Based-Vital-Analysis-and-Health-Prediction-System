/**
 * VitalHealth AI - Main JavaScript Module
 */

// Global variables
let wsConnection = null;
let simulationInterval = null;
let isSimulating = false;

// DOM Elements
const elements = {
    connectBtn: document.getElementById('connect-btn'),
    statusIndicator: document.getElementById('status-indicator'),
    statusText: document.getElementById('status-text'),
    liveHR: document.getElementById('live-hr'),
    liveSpO2: document.getElementById('live-spo2'),
    liveTemp: document.getElementById('live-temp'),
    lastHR: document.getElementById('last-hr'),
    lastSpO2: document.getElementById('last-spo2'),
    lastTemp: document.getElementById('last-temp'),
    riskLevel: document.getElementById('risk-level'),
    ecgCanvas: document.getElementById('ecg-canvas')
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initEventListeners();
    initCharts();
    refreshDashboardData();
    
    // Auto-refresh dashboard every 10 seconds
    if (window.location.pathname.includes('dashboard')) {
        setInterval(refreshDashboardData, 10000);
    }
});

/**
 * Initialize Event Listeners
 */
function initEventListeners() {
    if (elements.connectBtn) {
        elements.connectBtn.addEventListener('click', toggleConnection);
    }
}

/**
 * Initialize Charts
 */
function initCharts() {
    if (elements.ecgCanvas) {
        vitalCharts.initECGChart('ecg-canvas');
    }
}

/**
 * Toggle ESP32 Connection
 */
function toggleConnection() {
    if (wsConnection && wsConnection.readyState === WebSocket.OPEN) {
        disconnectESP32();
    } else {
        connectESP32();
    }
}

/**
 * Connect to ESP32 via WebSocket
 */
function connectESP32() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    wsConnection = new WebSocket(wsUrl);
    
    wsConnection.onopen = function() {
        updateConnectionStatus(true);
        showToast('Connected to ESP32 sensor', 'success');
        
        if (elements.connectBtn) {
            elements.connectBtn.innerHTML = '<i class="fas fa-times"></i> Disconnect';
            elements.connectBtn.classList.remove('btn-gradient');
            elements.connectBtn.classList.add('btn-outline-gradient');
        }
    };
    
    wsConnection.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleSensorData(data);
    };
    
    wsConnection.onclose = function() {
        updateConnectionStatus(false);
        showToast('Disconnected from ESP32', 'warning');
        
        if (elements.connectBtn) {
            elements.connectBtn.innerHTML = '<i class="fas fa-plug"></i> Connect to ESP32';
            elements.connectBtn.classList.remove('btn-outline-gradient');
            elements.connectBtn.classList.add('btn-gradient');
        }
    };
    
    wsConnection.onerror = function(error) {
        console.error('WebSocket error:', error);
        showToast('Connection error', 'error');
    };
}

/**
 * Disconnect from ESP32
 */
function disconnectESP32() {
    if (wsConnection) {
        wsConnection.close();
        wsConnection = null;
    }
}

/**
 * Update Connection Status UI
 */
function updateConnectionStatus(connected) {
    if (elements.statusIndicator) {
        elements.statusIndicator.style.backgroundColor = connected ? '#10b981' : '#ef4444';
    }
    
    if (elements.statusText) {
        elements.statusText.innerHTML = connected ? 'Connected to ESP32' : 'Disconnected';
    }
}

/**
 * Handle Incoming Sensor Data
 */
function handleSensorData(data) {
    // Update live displays
    if (elements.liveHR) elements.liveHR.innerHTML = data.heart_rate || '--';
    if (elements.liveSpO2) elements.liveSpO2.innerHTML = data.spo2 || '--';
    if (elements.liveTemp) elements.liveTemp.innerHTML = data.temperature || '--';
    
    // Update ECG chart
    if (data.ecg_sample) {
        vitalCharts.updateECG(data.ecg_sample);
    }
    
    // Send to backend for prediction
    sendDataToBackend(data);
    
    // Check for critical alerts
    checkCriticalAlerts(data);
}

/**
 * Send Data to Backend
 */
function sendDataToBackend(data) {
    fetch('/api/sensor-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success' && result.prediction) {
            // Update risk level if on dashboard
            if (elements.riskLevel && result.prediction.risk_level) {
                elements.riskLevel.innerHTML = result.prediction.risk_level;
                let color = '#10b981';
                if (result.prediction.risk_level === 'High') color = '#ef4444';
                else if (result.prediction.risk_level === 'Moderate') color = '#f59e0b';
                elements.riskLevel.style.color = color;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Check for Critical Alerts
 */
function checkCriticalAlerts(data) {
    const alerts = [];
    
    if (data.heart_rate > 120) {
        alerts.push(`⚠️ Critical: Heart rate is ${data.heart_rate} BPM (high)`);
    } else if (data.heart_rate < 50) {
        alerts.push(`⚠️ Critical: Heart rate is ${data.heart_rate} BPM (low)`);
    }
    
    if (data.spo2 < 90) {
        alerts.push(`⚠️ Critical: Oxygen saturation is ${data.spo2}% (low)`);
    }
    
    if (data.temperature > 38.5) {
        alerts.push(`⚠️ Critical: Temperature is ${data.temperature}°C (high fever)`);
    } else if (data.temperature < 35.0) {
        alerts.push(`⚠️ Critical: Temperature is ${data.temperature}°C (hypothermia)`);
    }
    
    if (alerts.length > 0) {
        alerts.forEach(alert => showToast(alert, 'warning'));
        
        // Try to send browser notification
        if (Notification.permission === 'granted') {
            new Notification('VitalHealth Alert', {
                body: alerts.join('\n'),
                icon: '/static/images/icon.png'
            });
        }
    }
}

/**
 * Show Toast Notification
 */
function showToast(message, type = 'info') {
    let toastContainer = document.querySelector('.toast-container');
    
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast-custom toast-${type}`;
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <div class="flex-grow-1">
                <i class="fas fa-${getToastIcon(type)} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-sm" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Get Toast Icon
 */
function getToastIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

/**
 * Refresh Dashboard Data
 */
function refreshDashboardData() {
    fetch('/api/historical-data?limit=1')
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                const latest = data[0];
                if (elements.lastHR) elements.lastHR.innerHTML = latest.heart_rate || '--';
                if (elements.lastSpO2) elements.lastSpO2.innerHTML = latest.spo2 || '--';
                if (elements.lastTemp) elements.lastTemp.innerHTML = latest.temperature || '--';
            }
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Start Simulation (for testing without ESP32)
 */
function startSimulation() {
    if (isSimulating) return;
    isSimulating = true;
    
    simulationInterval = setInterval(() => {
        const data = {
            heart_rate: Math.floor(Math.random() * 80) + 60,
            spo2: Math.floor(Math.random() * 10) + 90,
            temperature: (Math.random() * 2) + 36.5,
            ecg_sample: Math.floor(Math.random() * 4095)
        };
        
        handleSensorData(data);
    }, 2000);
    
    showToast('Simulation started', 'info');
}

/**
 * Stop Simulation
 */
function stopSimulation() {
    if (simulationInterval) {
        clearInterval(simulationInterval);
        simulationInterval = null;
    }
    isSimulating = false;
    showToast('Simulation stopped', 'info');
}

// Request notification permission on load
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}