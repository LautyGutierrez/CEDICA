/**
 * Default timeout for toast notifications.
 */
export const DEFAULT_TOAST_TIMEOUT = 3000;

/**
 * Base URL for the backend.
 * @type {string}
 */
export const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL || 'http://localhost:5000';

/**
 * API URL for the backend.
 */
export const BACKEND_API_URL = `${BACKEND_BASE_URL}/api`;


export const DEFAULT_API_MAINTEINANCE_ERROR = 'toast';
