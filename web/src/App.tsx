import { ChevronDown } from 'lucide-react'
import { useEffect, useState } from 'react'
import './app.css'
import { Button } from './components/loom/button.tsx'
import { type Glossary, loadGlossary, sections } from './glossary.ts'
import { GlossaryTable } from './GlossaryTable.tsx'

type Load = { state: 'loading' } | { state: 'failed'; error: string } | { state: 'ready'; glossary: Glossary }

interface Place {
  dimension: string
  section: string
}

export default function App() {
  const [load, setLoad] = useState<Load>({ state: 'loading' })
  const [place, setPlace] = useState<Place | null>(null)
  // Null until the first toggle: the dimension being shown starts open.
  const [expanded, setExpanded] = useState<ReadonlySet<string> | null>(null)

  useEffect(() => {
    loadGlossary().then(
      (glossary) => setLoad({ state: 'ready', glossary }),
      (error: unknown) => setLoad({ state: 'failed', error: String(error) }),
    )
  }, [])

  if (load.state === 'loading') return <p className="status">Loading the glossary…</p>
  if (load.state === 'failed') return <p className="status">Could not load the glossary. {load.error}</p>

  const { dimensions } = load.glossary
  const dimension = dimensions.find((d) => d.id === place?.dimension) ?? dimensions[0]
  const sectionList = sections(dimension.terms)
  const [section, terms] = sectionList.find(([name]) => name === place?.section) ?? sectionList[0]
  const open = expanded ?? new Set([dimension.id])

  function toggle(id: string) {
    const next = new Set(open)
    if (!next.delete(id)) next.add(id)
    setExpanded(next)
  }

  return (
    <div className="app">
      <nav className="rail" aria-label="Glossary">
        <p className="rail__title text-title-sm">ez-prompt</p>
        <ul className="rail__list">
          {dimensions.map((d) => {
            const current = d.id === dimension.id
            const names = sections(d.terms).map(([name]) => name)
            const leaf = names.length === 1
            const isOpen = !leaf && open.has(d.id)
            const listId = `sections-${d.id}`
            return (
              <li key={d.id}>
                {/* A dimension with one section is that section; one with several only opens and closes. */}
                <Button
                  type="button"
                  variant="ghost"
                  color="inherit"
                  className="rail__dimension"
                  aria-expanded={leaf ? undefined : isOpen}
                  aria-controls={leaf ? undefined : listId}
                  aria-current={leaf && current ? 'true' : undefined}
                  data-active={(!leaf && current) || undefined}
                  trailingIcon={leaf ? undefined : <ChevronDown className="chevron" aria-hidden="true" />}
                  onClick={() => (leaf ? setPlace({ dimension: d.id, section: names[0] }) : toggle(d.id))}
                >
                  {d.label}
                </Button>
                {isOpen && (
                  <ul id={listId} className="rail__sections">
                    {names.map((name) => (
                      <li key={name}>
                        <button
                          type="button"
                          className="rail__section interactive text-body-sm"
                          aria-current={current && name === section ? 'true' : undefined}
                          onClick={() => setPlace({ dimension: d.id, section: name })}
                        >
                          {name}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            )
          })}
        </ul>
      </nav>
      <main className="main">
        <header className="main__header">
          <p className="text-label-md text-on-surface-variant">{dimension.label}</p>
          <h1 className="text-title-lg">{section}</h1>
        </header>
        <GlossaryTable key={`${dimension.id}/${section}`} terms={terms} groups={dimension.groups} />
      </main>
    </div>
  )
}
