/**
 * Module 25: Print Receipt & Table CSV Quick Export
 * Features:
 * - One-click window.print() trigger with media print styles
 * - Client-side table to CSV export generator and direct download
 */

import { showToast } from './toast.js';

export function exportTableToCSV(table, filename = 'rocketbank_transactions.csv') {
  if (!table) {
    return;
  }

  const rows = Array.from(table.querySelectorAll('tr'));
  const csvLines = [];

  rows.forEach((row) => {
    const cells = Array.from(row.querySelectorAll('th, td'));
    if (!cells.length) {
      return;
    }

    const line = cells.map((cell) => {
      // Clean inner text, ignore nested hidden action buttons if any
      let text = cell.innerText.trim();
      text = text.replace(/\n+/g, ' ');
      // Escape double quotes and enclose in quotes if comma or quotes present
      if (text.includes('"') || text.includes(',') || text.includes(';')) {
        text = `"${text.replace(/"/g, '""')}"`;
      }
      return text;
    }).join(',');

    csvLines.push(line);
  });

  const csvContent = '\uFEFF' + csvLines.join('\r\n'); // Add BOM for Excel UTF-8 compatibility
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.display = 'none';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);

  showToast(`Exported ${csvLines.length - 1} rows to CSV!`, 'success');
}

export function initExportPrint() {
  document.addEventListener('click', (e) => {
    // Print trigger
    const printBtn = e.target.closest('[data-print-trigger], .btn-print, [data-print-receipt]');
    if (printBtn) {
      e.preventDefault();
      window.print();
      return;
    }

    // CSV export trigger
    const exportBtn = e.target.closest('[data-export-csv], .btn-export-csv');
    if (exportBtn) {
      e.preventDefault();
      const targetSelector = exportBtn.dataset.exportCsv || exportBtn.dataset.targetTable || 'table';
      const table = document.querySelector(targetSelector) || exportBtn.closest('.card')?.querySelector('table');
      const filename = exportBtn.dataset.filename || `rocketbank_export_${new Date().toISOString().slice(0, 10)}.csv`;

      if (table) {
        exportTableToCSV(table, filename);
      } else {
        showToast('No table found to export', 'warning');
      }
    }
  });
}
