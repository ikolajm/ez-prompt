import type { Dimension, Term } from './glossary.ts'

// Picks per dimension id, each list in the order picked.
export type Sheet = Record<string, Term[]>

// Every other key holds one term, and a new pick replaces it.
const STACKING = new Set(['light', 'composition', 'image-texture'])

export function keyOf(dimension: Dimension): string {
  return dimension.id.replace(/-/g, ' ')
}

export function toggle(sheet: Sheet, dimension: Dimension, term: Term): Sheet {
  const current = sheet[dimension.id] ?? []
  const next = current.some((t) => t.id === term.id)
    ? current.filter((t) => t.id !== term.id)
    : STACKING.has(dimension.id)
      ? [...current, term]
      : [term]
  return { ...sheet, [dimension.id]: next }
}

export interface Line {
  dimension: Dimension
  terms: Term[]
}

// In the glossary's dimension order, not the order picked.
export function lines(sheet: Sheet, dimensions: Dimension[]): Line[] {
  return dimensions
    .map((dimension) => ({ dimension, terms: sheet[dimension.id] ?? [] }))
    .filter((line) => line.terms.length > 0)
}

export function asSpec(sheetLines: Line[]): string {
  return sheetLines
    .map(({ dimension, terms }) => `${keyOf(dimension)}: ${terms.map((t) => t.name).join(', ')}`)
    .join('\n')
}

// A term's cues are what the image models read; a term without cues falls back to its name.
export function asPrompt(sheetLines: Line[]): string {
  return sheetLines
    .flatMap(({ terms }) => terms.flatMap((t) => (t.cues.length > 0 ? t.cues : [t.name])))
    .join(', ')
}
