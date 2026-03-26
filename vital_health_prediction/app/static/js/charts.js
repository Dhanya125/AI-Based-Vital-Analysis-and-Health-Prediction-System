/**
 * VitalHealth AI - Charts Module
 * For ECG waveform and vital trends visualization
 */

class VitalHealthCharts {
    constructor() {
        this.ecgChart = null;
        this.heartRateChart = null;
        this.spo2Chart = null;
        this.tempChart = null;
        this.ecgData = [];
        this.maxDataPoints = 200;
    }

    /**
     * Initialize ECG Waveform Chart
     */
    initECGChart(canvasId) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        this.ecgChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array(this.maxDataPoints).fill(''),
                datasets: [{
                    label: 'ECG Signal',
                    data: Array(this.maxDataPoints).fill(0),
                    borderColor: '#ef4444',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.2,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                animation: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                scales: {
                    x: { display: false },
                    y: { 
                        min: 0, 
                        max: 4095,
                        title: { display: true, text: 'ADC Value' }
                    }
                }
            }
        });
        
        return this.ecgChart;
    }

    /**
     * Update ECG Chart with new data point
     */
    updateECG(value) {
        if (!this.ecgChart) return;
        
        this.ecgData.push(value);
        if (this.ecgData.length > this.maxDataPoints) {
            this.ecgData.shift();
        }
        
        this.ecgChart.data.datasets[0].data = this.ecgData;
        this.ecgChart.update();
    }

    /**
     * Clear ECG Chart
     */
    clearECG() {
        this.ecgData = [];
        if (this.ecgChart) {
            this.ecgChart.data.datasets[0].data = Array(this.maxDataPoints).fill(0);
            this.ecgChart.update();
        }
    }

    /**
     * Create Heart Rate Trend Chart
     */
    createHeartRateChart(elementId, data) {
        const ctx = document.getElementById(elementId).getContext('2d');
        
        this.heartRateChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: [{
                    label: 'Heart Rate (BPM)',
                    data: data.values || [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Heart Rate: ${context.raw} BPM`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 40,
                        max: 200,
                        title: { display: true, text: 'BPM' }
                    }
                }
            }
        });
        
        return this.heartRateChart;
    }

    /**
     * Create SpO2 Trend Chart
     */
    createSpO2Chart(elementId, data) {
        const ctx = document.getElementById(elementId).getContext('2d');
        
        this.spo2Chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: [{
                    label: 'SpO₂ (%)',
                    data: data.values || [],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 70,
                        max: 100,
                        title: { display: true, text: '%' }
                    }
                }
            }
        });
        
        return this.spo2Chart;
    }

    /**
     * Create Temperature Trend Chart
     */
    createTemperatureChart(elementId, data) {
        const ctx = document.getElementById(elementId).getContext('2d');
        
        this.tempChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: [{
                    label: 'Temperature (°C)',
                    data: data.values || [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 35,
                        max: 40,
                        title: { display: true, text: '°C' }
                    }
                }
            }
        });
        
        return this.tempChart;
    }

    /**
     * Add data point to chart
     */
    addDataPoint(chartName, value, label) {
        let chart;
        switch(chartName) {
            case 'heartRate':
                chart = this.heartRateChart;
                break;
            case 'spo2':
                chart = this.spo2Chart;
                break;
            case 'temp':
                chart = this.tempChart;
                break;
            default:
                return;
        }
        
        if (chart) {
            chart.data.datasets[0].data.push(value);
            if (chart.data.datasets[0].data.length > 20) {
                chart.data.datasets[0].data.shift();
                chart.data.labels.shift();
            }
            chart.data.labels.push(label);
            chart.update();
        }
    }
}

// Create global instance
const vitalCharts = new VitalHealthCharts();