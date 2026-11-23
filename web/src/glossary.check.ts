// Holds the extract's output to the types the app reads it through: a field the extract
// renames or drops fails `tsc`. Nothing imports this file, so it never reaches the bundle.
import data from '../public/glossary.json'
import type { Glossary } from './glossary.ts'

data satisfies Glossary
