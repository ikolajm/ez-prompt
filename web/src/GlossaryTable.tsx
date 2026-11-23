import { ChevronDown, Minus, Plus } from 'lucide-react'
import { type ReactNode, useState } from 'react'
import { Checkbox } from './components/loom/checkbox.tsx'
import type { Term } from './glossary.ts'

export function GlossaryTable({
  terms,
  picked,
  onPick,
}: {
  terms: Term[]
  picked: ReadonlySet<string>
  onPick: (term: Term) => void
}) {
  const [open, setOpen] = useState<ReadonlySet<string>>(new Set())

  function toggle(id: string) {
    setOpen((current) => {
      const next = new Set(current)
      if (!next.delete(id)) next.add(id)
      return next
    })
  }

  return (
    <table className="table glossary" data-size="lg">
      <thead>
        <tr>
          <th scope="col" className="glossary__pick">
            <span className="visually-hidden">On the sheet</span>
          </th>
          <th scope="col">Term</th>
          <th scope="col" className="glossary__effect">
            Effect
          </th>
        </tr>
      </thead>
      <tbody>
        {terms.map((term) => (
          <TermRows
            key={term.id}
            term={term}
            open={open.has(term.id)}
            onToggle={() => toggle(term.id)}
            picked={picked.has(term.id)}
            onPick={() => onPick(term)}
          />
        ))}
      </tbody>
    </table>
  )
}

function TermRows({
  term,
  open,
  onToggle,
  picked,
  onPick,
}: {
  term: Term
  open: boolean
  onToggle: () => void
  picked: boolean
  onPick: () => void
}) {
  const detailId = `term-${term.id}`
  return (
    <>
      {/* The row takes the click; the button is the keyboard and screen-reader target, and its click bubbles here. */}
      <tr className="glossary__row" data-open={open || undefined} onClick={onToggle}>
        {/* Stops here, so checking a term never opens its row. */}
        <td className="glossary__pick" onClick={(e) => e.stopPropagation()}>
          <Checkbox
            aria-label={`${term.name} on the sheet`}
            checked={picked}
            onChange={onPick}
          />
        </td>
        <th scope="row">
          <button type="button" className="glossary__name" aria-expanded={open} aria-controls={detailId}>
            <ChevronDown className="chevron" aria-hidden="true" />
            {term.name}
          </button>
        </th>
        <td className="glossary__effect">
          <div className="glossary__clamp">{term.effect}</div>
        </td>
      </tr>
      <tr id={detailId} className="glossary__detail" hidden={!open}>
        <td colSpan={3}>
          <TermDetail term={term} />
        </td>
      </tr>
    </>
  )
}

function TermDetail({ term }: { term: Term }) {
  return (
    <div className="detail">
      <Field label="Effect" open>
        <p>{term.effect}</p>
      </Field>
      {term.what && (
        <Field label="What it is">
          <p>{term.what}</p>
        </Field>
      )}
      {term.pairs.length > 0 && (
        <Field label="Pairs well with">
          <List items={term.pairs} />
        </Field>
      )}
      {term.conflicts.length > 0 && (
        <Field label="Conflicts with">
          <List items={term.conflicts} />
        </Field>
      )}
      {term.example && (
        <Field label="Example">
          <p>{term.example}</p>
        </Field>
      )}
      {Object.entries(term.extras).map(([label, text]) => (
        <Field key={label} label={label}>
          <p>{text}</p>
        </Field>
      ))}
    </div>
  )
}

function Field({ label, open, children }: { label: string; open?: boolean; children: ReactNode }) {
  return (
    <details className="detail__field" open={open}>
      <summary className="text-label-lg">
        <Plus className="detail__icon detail__icon--closed" aria-hidden="true" />
        <Minus className="detail__icon detail__icon--open" aria-hidden="true" />
        {label}
      </summary>
      <div className="detail__body">{children}</div>
    </details>
  )
}

/* "Backlit subjects — rim light around hair": the term before the first dash, its reason after. */
function List({ items }: { items: string[] }) {
  return (
    <ul className="pairs">
      {items.map((item, index) => {
        const split = item.indexOf(' — ')
        if (split === -1) return <li key={index}>{item}</li>
        return (
          <li key={index}>
            <span className="pairs__term">{item.slice(0, split)}</span>
            <span className="pairs__reason">{item.slice(split + 3)}</span>
          </li>
        )
      })}
    </ul>
  )
}
