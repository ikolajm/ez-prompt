// The shape src/ez_prompt/extract.py writes to public/glossary.json.

export interface Term {
  id: string
  name: string
  section: string
  group: string | null
  what: string | null
  effect: string
  pairs: string[]
  conflicts: string[]
  example: string | null
  extras: Record<string, string>
}

export interface Group {
  id: string
  name: string
  section: string
  note: string | null
}

export interface Dimension {
  id: string
  label: string
  source: string
  groups: Group[]
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

export function sections(terms: Term[]): [string, Term[]][] {
  const sections = new Map<string, Term[]>()
  for (const term of terms) {
    const list = sections.get(term.section) ?? []
    list.push(term)
    sections.set(term.section, list)
  }
  return [...sections]
}
