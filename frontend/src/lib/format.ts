import type { RiskLevel } from '@/types'

/**
 * Format timestamp / Date strings into readable text.
 */
export function formatTime(isoString: string): string {
  try {
    const date = new Date(isoString)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  } catch {
    return isoString
  }
}

/**
 * Capitalizes string inputs.
 */
export function capitalize(str: string): string {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

/**
 * Returns color classes for confidence levels.
 */
export function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.95) return 'text-status-active'
  if (confidence >= 0.85) return 'text-status-warning'
  return 'text-status-error'
}

/**
 * Returns status mapping based on decision states.
 */
export function getDecisionBadgeStyles(decision: string): {
  textColor: string
  bgColor: string
  borderColor: string
} {
  switch (decision) {
    case 'APPROVED':
      return {
        textColor: 'text-status-active',
        bgColor: 'bg-status-active/10',
        borderColor: 'border-status-active/20',
      }
    case 'FLAGGED':
      return {
        textColor: 'text-status-warning',
        bgColor: 'bg-status-warning/10',
        borderColor: 'border-status-warning/20',
      }
    case 'BLOCKED':
      return {
        textColor: 'text-status-error',
        bgColor: 'bg-status-error/10',
        borderColor: 'border-status-error/20',
      }
    case 'ESCALATED':
      return {
        textColor: 'text-risk-high',
        bgColor: 'bg-risk-high/10',
        borderColor: 'border-risk-high/20',
      }
    case 'REVIEW_REQUIRED':
    case 'AWAITING_REVIEW':
      return {
        textColor: 'text-status-warning',
        bgColor: 'bg-status-warning/10',
        borderColor: 'border-status-warning/20',
      }
    case 'DENIED':
      return {
        textColor: 'text-status-error',
        bgColor: 'bg-status-error/10',
        borderColor: 'border-status-error/20',
      }
    default:
      return {
        textColor: 'text-text-muted',
        bgColor: 'bg-bg-overlay/50',
        borderColor: 'border-border',
      }
  }
}

/**
 * Returns icon color mapping for Risk levels.
 */
export function getRiskColor(level: RiskLevel): string {
  switch (level) {
    case 'critical':
      return 'text-risk-critical'
    case 'high':
      return 'text-risk-high'
    case 'medium':
      return 'text-risk-medium'
    case 'low':
      return 'text-risk-low'
    default:
      return 'text-text-muted'
  }
}
