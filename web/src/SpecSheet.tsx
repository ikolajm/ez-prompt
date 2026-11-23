import { X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Button } from './components/loom/button.tsx'
import { byPart, type Dimension, headedParts, partLabel, type Term } from './glossary.ts'
import { asPrompt, asSpec, type Line } from './sheet.ts'

export function SpecSheet({
  dimensions,
  lines,
  onRemove,
}: {
  dimensions: Dimension[]
  lines: Line[]
  onRemove: (dimension: Dimension, term: Term) => void
}) {
  const empty = lines.length === 0
  const headed = headedParts(dimensions)
  return (
    <aside className="sheet" aria-labelledby="sheet-title">
      <h2 id="sheet-title" className="text-title-sm">
        Spec sheet
      </h2>
      {empty ? (
        <p className="sheet__empty text-body-sm">Check a term to add it here.</p>
      ) : (
        <div className="sheet__parts">
          {byPart(lines, (line) => line.dimension.part).map(([part, partLines]) => (
              <section key={part} aria-labelledby={headed.has(part) ? `sheet-part-${part}` : undefined}>
                {headed.has(part) && (
                  <h3 className="sheet__part-label text-label-md" id={`sheet-part-${part}`}>
                    {partLabel(part)}
                  </h3>
                )}
                <dl className="sheet__lines">
                  {partLines.map(({ dimension, terms }) => (
                    <div key={dimension.id} className="sheet__line">
                      <dt className="text-label-md">{dimension.label}</dt>
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
              </section>
          ))}
        </div>
      )}
      <div className="sheet__copy">
        <CopyButton label="Copy spec" text={asSpec(lines)} disabled={empty} />
        <CopyButton label="Copy prompt" text={asPrompt(lines)} disabled={empty} />
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
