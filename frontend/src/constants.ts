/**
 * Frontend application constants
 */

// Priority levels for recommendations
export const PRIORITY_LEVELS = {
  CRITICAL: 'critical',
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low'
} as const;

// Priority order for sorting (lower number = higher priority)
export const PRIORITY_ORDER: Record<string, number> = {
  [PRIORITY_LEVELS.CRITICAL]: 1,
  [PRIORITY_LEVELS.HIGH]: 2,
  [PRIORITY_LEVELS.MEDIUM]: 3,
  [PRIORITY_LEVELS.LOW]: 4
};

// Implementation difficulty levels
export const DIFFICULTY_LEVELS = {
  EASY: 'easy',
  MODERATE: 'moderate',
  DIFFICULT: 'difficult'
} as const;

// Difficulty order for sorting
export const DIFFICULTY_ORDER: Record<string, number> = {
  [DIFFICULTY_LEVELS.EASY]: 1,
  [DIFFICULTY_LEVELS.MODERATE]: 2,
  [DIFFICULTY_LEVELS.DIFFICULT]: 3
};

// Default values
export const DEFAULT_DIFFICULTY = DIFFICULTY_LEVELS.MODERATE;

// Formatting
export const CURRENCY_LOCALE = 'de-DE';
export const DATE_LOCALE = 'de-DE';
