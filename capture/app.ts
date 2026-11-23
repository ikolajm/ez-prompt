// The app capture: a close-up, a low angle, golden hour and film grain picked
// from the glossary into the sheet, one card opened on the way, and the prompt
// copied, by keyboard.
//
//   node app.ts
//
// Needs the app running (`npm run dev` in web/). The copied prompt is written
// into the timeline, so its caption is the text the app really produced.
import type { Page } from 'playwright'
import { capture, focusOn, HOLD, pause, TakeError, type Mark } from './take.ts'

// Each pick: the rail key it sits under, the term, and its first cue, which the
// copied prompt has to carry.
const PICKS = [
  { key: 'Shot Size', term: 'Close-Up (CU)', cue: 'close-up shot' },
  { key: 'Angle', term: 'Low Angle (Looking Up)', cue: 'low angle shot looking up' },
  { key: 'Time of Day', term: 'Golden Hour', cue: 'golden hour light' },
  { key: 'Image Texture', term: 'Film Grain', cue: 'visible film grain' },
]

async function openKey(page: Page, key: string) {
  await focusOn(page.getByRole('navigation', { name: 'Glossary' }).getByRole('button', { name: key, exact: true }))
  await page.keyboard.press('Enter')
  await page.locator('.main__header').filter({ hasText: key }).waitFor()
  await pause(HOLD.short)
}

async function pick(page: Page, term: string) {
  await focusOn(page.getByRole('checkbox', { name: `${term} on the sheet` }))
  await page.keyboard.press('Space')
  await page.locator('.sheet__value').filter({ hasText: term }).waitFor()
  await pause(HOLD.short)
}

async function take(page: Page, mark: Mark) {
  await page.locator('.glossary').waitFor()
  await pause(HOLD.short)

  const [first, ...rest] = PICKS

  mark('shot-size')
  await openKey(page, first.key)

  mark('card')
  const name = page.locator('.glossary__name').filter({ hasText: first.term })
  await focusOn(name)
  await page.keyboard.press('Enter')
  await page.locator('.glossary__detail:not([hidden])').waitFor()
  await pause(HOLD.read)
  await page.keyboard.press('Enter')
  await page.locator('.glossary__detail:not([hidden])').waitFor({ state: 'detached' })
  await pause(HOLD.short)

  mark('pick-close-up')
  await pick(page, first.term)

  for (const { key, term } of rest) {
    mark(`key-${key}`)
    await openKey(page, key)
    mark(`pick-${term}`)
    await pick(page, term)
  }
  await pause(HOLD.short)

  mark('copy')
  await focusOn(page.getByRole('button', { name: 'Copy prompt' }))
  await page.keyboard.press('Enter')
  // The button renames itself to report the result, so it is found again by its new name.
  const result = page.getByRole('button', { name: /^(Copied|Copy failed)$/ })
  await result.waitFor()
  if ((await result.textContent())?.trim() !== 'Copied') throw new TakeError('The copy failed.')
  const prompt = await page.evaluate(() => navigator.clipboard.readText())
  for (const { term, cue } of PICKS) {
    if (!prompt.includes(cue)) throw new TakeError(`The copied prompt is missing ${term}'s cue "${cue}".`)
  }
  await pause(HOLD.read)

  return { prompt }
}

await capture('app', take)
