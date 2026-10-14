/**
 * Module 20: Financial Analytics Chart (Chart.js Integration)
 * Fetches monthly financial summary from /api/v1/analytics/monthly-summary/
 * and renders an interactive multi-dataset comparison chart.
 */

import { http } from '../api/http.js';
import { formatCurrency } from '../utils.js';

async function loadChartJs() {
  if (window.Chart) {
    return window.Chart;
  }

  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js';
    script.async = true;
    script.onload = () => resolve(window.Chart);
    script.onerror = () => reject(new Error('Failed to load Chart.js'));
    document.head.appendChild(script);
  });
}

export async function initAnalyticsChart() {
  const canvas = document.getElementById('monthlyAnalyticsChart') || document.querySelector('[data-analytics-chart]');
  if (!canvas) {
    return;
  }

  try {
    const [Chart, data] = await Promise.all([
      loadChartJs(),
      http.get('/api/v1/analytics/monthly-summary/'),
    ]);

    const ctx = canvas.getContext('2d');
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

    const textColor = isDark ? '#94a3b8' : '#64748b';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.months,
        datasets: [
          {
            label: 'Income',
            data: data.income,
            backgroundColor: 'rgba(16, 185, 129, 0.75)',
            borderColor: '#10b981',
            borderWidth: 1.5,
            borderRadius: 6,
          },
          {
            label: 'Expenses',
            data: data.expenses,
            backgroundColor: 'rgba(239, 68, 68, 0.75)',
            borderColor: '#ef4444',
            borderWidth: 1.5,
            borderRadius: 6,
          },
          {
            label: 'Net Savings',
            data: data.savings,
            type: 'line',
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99, 102, 241, 0.15)',
            borderWidth: 2.5,
            tension: 0.35,
            fill: true,
            pointBackgroundColor: '#6366f1',
            pointRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: textColor,
              font: {
                family: 'system-ui, -apple-system, sans-serif',
                size: 12,
              },
            },
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.dataset.label || '';
                return `${label}: ${formatCurrency(context.parsed.y, data.currency || 'KZT')}`;
              },
            },
          },
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor },
          },
          y: {
            grid: { color: gridColor },
            ticks: {
              color: textColor,
              callback: (val) => `${(val / 1000).toFixed(0)}k`,
            },
          },
        },
      },
    });
  } catch (err) {
    console.warn('[AnalyticsChart] Unable to load or render chart:', err);
    if (canvas && canvas.parentNode) {
      canvas.parentNode.innerHTML += `
        <div class="text-center p-md text-muted font-mono" style="font-size: var(--font-size-xs);">
          Financial analytics graph requires network access.
        </div>
      `;
    }
  }
}
