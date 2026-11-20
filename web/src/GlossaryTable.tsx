import { ChevronDown, Minus, Plus } from 'lucide-react'
import { type ReactNode, useState } from 'react'
import type { Group, Term } from './glossary.ts'

export function GlossaryTable({ terms, groups }: { terms: Term[]; groups: Group[] }) {
  const [open, setOpen] = useState<ReadonlySet<string>>(new Set())
  const byId = new Map(groups.map((g) => [g.id, g]))

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
            group={term.group ? byId.get(term.group) : undefined}
            open={open.has(term.id)}
            onToggle={() => toggle(term.id)}
          />
        ))}
      </tbody>
    </table>
  )
}

function TermRows({
  term,
  group,
  open,
  onToggle,
}: {
  term: Term
  group: Group | undefined
  open: boolean
  onToggle: () => void
}) {
  const detailId = `term-${term.id}`
  return (
    <>
      {/* The row takes the click; the button is the keyboard and screen-reader target, and its click bubbles here. */}
      <tr className="glossary__row" data-open={open || undefined} onClick={onToggle}>
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
        <td colSpan={2}>
          <TermDetail term={term} group={group} />
        </td>
      </tr>
    </>
  )
}

function TermDetail({ term, group }: { term: Term; group: Group | undefined }) {
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
      {group?.note && (
        <Field label={group.name}>
          <p>{group.note}</p>
        </Field>
      )}
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
