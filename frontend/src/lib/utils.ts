import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Merges class names with Tailwind conflict resolution.
 * Uses clsx for conditional logic + tailwind-merge to handle conflicts.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDuration(ms: number | null | undefined): string {
  if (ms === null || ms === undefined) return '0ms'
  if (ms >= 1000) {
    return `${(ms / 1000).toFixed(2)}s`
  }
  return `${Math.round(ms)}ms`
}

export function formatPercent(val: number | null | undefined): string {
  if (val === null || val === undefined) return '0%'
  const pct = val <= 1 && val > 0 ? val * 100 : val
  return `${Math.round(pct)}%`
}

export function formatCost(usd: number | null | undefined): string {
  if (usd === null || usd === undefined) return '$0.000'
  if (usd === 0) return '$0.000'
  if (usd < 0.001) {
    return `$${usd.toFixed(4)}`
  }
  return `$${usd.toFixed(3)}`
}

