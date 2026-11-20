import { X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Button } from './components/loom/button.tsx'
import { FormField } from './components/loom/form-field.tsx'
import type { Dimension, Term } from './glossary.ts'
import { asPrompt, asSpec, keyOf, type Line } from './sheet.ts'

export function SpecSheet({
  subject,
  onSubject,
  lines,
  onRemove,
}: {
  subject: string
  onSubject: (value: string) => void
  lines: Line[]
  onRemove: (dimension: Dimension, term: Term) => void
}) {
  const empty = lines.length === 0 && !subject.trim()
  return (
    <aside className="sheet" aria-labelledby="sheet-title">
      <h2 id="sheet-title" className="text-title-sm">
        Spec sheet
      </h2>
      <FormField>
        <label className="label" data-size="sm" htmlFor="subject">
          Subject
        </label>
        <textarea
          id="subject"
          className="textarea"
          data-size="sm"
          rows={2}
          placeholder="What the image is of"
          value={subject}
          onChange={(e) => onSubject(e.target.value)}
        />
      </FormField>
      {lines.length === 0 ? (
        <p className="sheet__empty text-body-sm">Check a term to add it here.</p>
      ) : (
        <dl className="sheet__lines">
          {lines.map(({ dimension, terms }) => (
            <div key={dimension.id} className="sheet__line">
              <dt className="text-label-md">{keyOf(dimension)}</dt>
              {terms.map((term) => (
                <dd key={term.id} className="sheet__value text-body-sm">
                  <span>{term.name}</span>
                  <Button
                    type="button"
                    variant="ghost"
                    color="inherit"
                    size="sm"
                    iconOnly
                    aria-label={`Remove ${term.name}`}
                    onClick={() => onRemove(dimension, term)}
                  >
                    <X aria-hidden="true" />
                  </Button>
                </dd>
              ))}
            </div>
          ))}
        </dl>
      )}
      <div className="sheet__copy">
        <CopyButton label="Copy spec" text={asSpec(subject, lines)} disabled={empty} />
        <CopyButton label="Copy prompt" text={asPrompt(subject, lines)} disabled={empty} />
      </div>
    </aside>
  )
}

function CopyButton({ label, text, disabled }: { label: string; text: string; disabled: boolean }) {
  const [state, setState] = useState<'idle' | 'copied' | 'failed'>('idle')

  useEffect(() => {
    if (state === 'idle') return
    const timer = setTimeout(() => setState('idle'), 1500)
    return () => clearTimeout(timer)
  }, [state])

  return (
    <Button
      type="button"
      variant="outline"
      size="sm"
      disabled={disabled}
      onClick={() =>
        navigator.clipboard.writeText(text).then(
          () => setState('copied'),
          () => setState('failed'),
        )
      }
    >
      <span aria-live="polite">{state === 'copied' ? 'Copied' : state === 'failed' ? 'Copy failed' : label}</span>
    </Button>
  )
}
