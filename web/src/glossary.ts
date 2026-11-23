// The shape src/ez_prompt/extract.py writes to public/glossary.json.

export interface Term {
  id: string
  name: string
  section: string
  what: string | null
  effect: string
  pairs: string[]
  conflicts: string[]
  example: string | null
  cues: string[]
  extras: Partial<Record<string, string>>
}

export interface Dimension {
  id: string
  label: string
  part: string
  terms: Term[]
}

export interface Glossary {
  dimensions: Dimension[]
}

export async function loadGlossary(): Promise<Glossary> {
  const response = await fetch(`${import.meta.env.BASE_URL}glossary.json`)
  if (!response.ok) throw new Error(`glossary.json: ${response.status}`)
  return (await response.json()) as Glossary
}

// Runs of items sharing a part, in the order given.
export function byPart<T>(items: T[], partOf: (item: T) => string): [string, T[]][] {
  const parts: [string, T[]][] = []
  for (const item of items) {
    const last = parts.at(-1)
    if (last && last[0] === partOf(item)) last[1].push(item)
    else parts.push([partOf(item), [item]])
  }
  return parts
}

// A part holding one key is that key, so only parts with several take a heading.
export function headedParts(dimensions: Dimension[]): Set<string> {
  return new Set(byPart(dimensions, (d) => d.part).flatMap(([part, keys]) => (keys.length > 1 ? [part] : [])))
}

export function partLabel(part: string): string {
  return part.charAt(0).toUpperCase() + part.slice(1)
}

export function sections(terms: Term[]): [string, Term[]][] {
  const sections = new Map<string, Term[]>()
  for (const term of terms) {
    const list = sections.get(term.section) ?? []
    list.push(term)
    sections.set(term.section, list)
  }
  return [...sections]
}
