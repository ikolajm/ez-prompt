// What every capture shares: the browser, the pacing, the keyboard moves and
// the timeline each take writes to takes/<name>.timeline.json, beside OBS's recordings.
import { writeFile } from 'node:fs/promises'
import { chromium, type Locator, type Page } from 'playwright'

// Setup

const SCREEN = 'http://localhost:5173/ez-prompt/'
// Wide enough to keep the sheet beside the glossary: at 72rem and below it moves underneath.
export const VIEWPORT = { width: 1280, height: 720 }

// Pacing, in milliseconds

const FOCUS_HOLD = 600
export const HOLD = { short: 1200, read: 3000 }

export const pause = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// A take that cannot be used: the screen showed other than the captions say, or
// a control was not where the script expects it.
export class TakeError extends Error {}

export type Mark = (name: string) => void

// Keyboard

function isFocused(locator: Locator): Promise<boolean> {
  return locator.evaluate((el) => el === document.activeElement)
}

// Focuses the control straight off, past every stop between, scrolling it into view.
export async function focusOn(locator: Locator) {
  await locator.focus()
  if (!(await isFocused(locator))) throw new TakeError(`${locator} did not take focus.`)
  await pause(FOCUS_HOLD)
}

// The run

// Loads the screen, hands the take its page and its mark, and writes the
// timeline once the take ends, with whatever the take returns beside the steps.
// A take that cannot be used writes none.
export async function capture(
  name: string,
  take: (page: Page, mark: Mark) => Promise<Record<string, unknown> | void>,
) {
  const steps: { name: string; ms: number }[] = []
  let start = 0
  const mark: Mark = (step) => steps.push({ name: step, ms: Math.round(performance.now() - start) })

  // An app window: no tab strip or address bar, only the title bar OBS's Client Area drops.
  // '' gives the persistent context a throwaway profile.
  const context = await chromium.launchPersistentContext('', {
    headless: false,
    args: [`--app=${SCREEN}`],
    viewport: VIEWPORT,
    reducedMotion: 'no-preference',
    permissions: ['clipboard-read', 'clipboard-write'],
  })
  try {
    const page = context.pages()[0] ?? (await context.newPage())
    await page.goto(SCREEN)
    start = performance.now()
    mark('load')
    const extra = (await take(page, mark)) ?? {}
    mark('end')

    const timeline = new URL(`./takes/${name}.timeline.json`, import.meta.url)
    await writeFile(
      timeline,
      JSON.stringify({ capture: name, viewport: VIEWPORT, ...extra, steps }, null, 2) + '\n',
    )
    console.log(`Timeline written: ${steps.length} steps over ${steps.at(-1)?.ms} ms.`)
  } catch (error) {
    if (!(error instanceof TakeError)) throw error
    console.error(`Take not usable: ${error.message}`)
    process.exitCode = 1
  } finally {
    await context.close()
  }
}
