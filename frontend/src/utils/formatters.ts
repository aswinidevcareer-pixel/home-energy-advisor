import { CURRENCY_LOCALE, DATE_LOCALE } from '../constants';

/**
 * Format currency value to EUR
 */
export function formatCurrency(value: number | undefined): string {
  if (value === undefined || value === null) return '€0';
  return `€${value.toLocaleString(CURRENCY_LOCALE, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

/**
 * Format date to readable string
 */
export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString(DATE_LOCALE, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Format category for display
 */
export function formatCategory(category: string): string {
  return category
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

/**
 * Get priority badge color
 */
export function getPriorityColor(priority: string): string {
  const colors: Record<string, string> = {
    'critical': '#d32f2f',
    'high': '#f57c00',
    'medium': '#fbc02d',
    'low': '#388e3c'
  };
  return colors[priority.toLowerCase()] || '#757575';
}

/**
 * Get difficulty badge color
 */
export function getDifficultyColor(difficulty: string): string {
  const colors: Record<string, string> = {
    'easy': '#4caf50',
    'moderate': '#ff9800',
    'difficult': '#f44336'
  };
  return colors[difficulty.toLowerCase()] || '#9e9e9e';
}
