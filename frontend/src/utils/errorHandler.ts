/**
 * Error Handler Utility
 * Converts technical errors into user-friendly messages
 * Logs technical details for developers while showing friendly messages to users
 */

export interface UserFriendlyError {
  message: string;
  canRetry: boolean;
  suggestedAction?: string;
}

// Error message configuration map
const ERROR_MESSAGES: Record<string, UserFriendlyError> = {
  // Client Errors (4xx)
  'CLIENT_ERROR': {
    message: 'Invalid information provided.',
    canRetry: false,
    suggestedAction: 'Please check your inputs and try again.'
  },
  '404': {
    message: 'The requested information could not be found.',
    canRetry: false,
    suggestedAction: 'Please refresh the page and try again.'
  },
  '429': {
    message: 'You\'ve made too many requests.',
    canRetry: true,
    suggestedAction: 'Please wait a moment and try again.'
  },
  
  // Processing Errors
  'PROCESSING_ERROR': {
    message: 'We couldn\'t process your request at this time.',
    canRetry: true,
    suggestedAction: 'Please try again in a moment.'
  },
  
  // Server Errors (5xx)
  'SERVER_ERROR': {
    message: 'Our service is experiencing issues.',
    canRetry: true,
    suggestedAction: 'Our team has been notified. Please try again in a few minutes.'
  },
  
  // Timeout/Connection Errors
  'TIMEOUT_ERROR': {
    message: 'The request took too long.',
    canRetry: true,
    suggestedAction: 'Please check your connection and try again.'
  },
  
  // Network Errors
  'NETWORK_ERROR': {
    message: 'Unable to connect to our service.',
    canRetry: true,
    suggestedAction: 'Please check your internet connection and try again.'
  },
  
  // Cancelled
  'CANCELLED': {
    message: 'The request was cancelled.',
    canRetry: true,
    suggestedAction: 'Please try again if needed.'
  },
  
  // Default
  'DEFAULT': {
    message: 'Something unexpected happened.',
    canRetry: true,
    suggestedAction: 'Please try again. If the problem persists, contact support.'
  }
};

/**
 * Convert any error into a user-friendly message
 */
export function handleError(error: any, context: string = 'processing your request'): UserFriendlyError {
  // Log technical details for developers
  console.group(`🔴 Error while ${context}`);
  console.error('Technical details:', error);
  if (error.response) {
    console.error('Response status:', error.response.status);
    console.error('Response data:', error.response.data);
  }
  if (error.stack) console.error('Stack trace:', error.stack);
  console.groupEnd();

  // Backend provided user-friendly message? Use it!
  if (error.response?.data?.detail) {
    return {
      message: error.response.data.detail,
      canRetry: true,
      suggestedAction: 'Please try again.'
    };
  }

  // Check HTTP status code
  const status = error.response?.status;
  if (status === 404) return ERROR_MESSAGES['404'];
  if (status === 422) return ERROR_MESSAGES['PROCESSING_ERROR'];
  if (status === 429) return ERROR_MESSAGES['429'];
  if (status >= 400 && status < 500) return ERROR_MESSAGES['CLIENT_ERROR'];
  if (status >= 500) return ERROR_MESSAGES['SERVER_ERROR'];

  // Check error code
  if (error.code === 'ERR_CANCELED') return ERROR_MESSAGES['CANCELLED'];
  if (error.code === 'ERR_NETWORK') return ERROR_MESSAGES['NETWORK_ERROR'];
  if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
    return ERROR_MESSAGES['TIMEOUT_ERROR'];
  }

  // No response = network error
  if (!error.response) return ERROR_MESSAGES['NETWORK_ERROR'];

  // Default fallback
  return ERROR_MESSAGES['DEFAULT'];
}

/**
 * Format error for display in UI
 */
export function formatErrorForDisplay(errorInfo: UserFriendlyError): string {
  return errorInfo.suggestedAction 
    ? `${errorInfo.message} ${errorInfo.suggestedAction}`
    : errorInfo.message;
}
