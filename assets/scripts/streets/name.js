/* global street, app */
/* global _unifyUndoStack, _updatePageUrl, _saveStreetToServerIfNecessary */

import { msg } from '../app/messages'
import { updatePageTitle } from '../app/page_title'
import { getElAbsolutePos } from '../util/helpers'
import { updateStreetMetadata } from './metadata'
import { StreetName, normalizeStreetName } from './name_sign'

// The following are only for the main street name
// We can cache selectors outside the functions here.
const streetNameCanvasEl = document.getElementById('street-name-canvas')
const streetNameEl = document.getElementById('street-name')

// Reference to the main street name instance
let streetName

// This is called everywhere.
// TODO: Create a specific init / create function?
// TODO: Updating the street name as a response to events?
export function updateStreetName () {
  streetName = new StreetName(streetNameEl, street.name)
  streetName.text = street.name

  resizeStreetName()

  updateStreetMetadata(street)
  updateStreetNameCanvasPos()

  _unifyUndoStack()
  _updatePageUrl()
  updatePageTitle()
}

function askForStreetName () {
  const newName = window.prompt(msg('PROMPT_NEW_STREET_NAME'), street.name)

  if (newName) {
    street.name = normalizeStreetName(newName)

    updateStreetName()
    updateStreetNameCanvasPos()

    _saveStreetToServerIfNecessary()
  }
}

function resizeStreetName () {
  const streetNameCanvasWidth = streetNameCanvasEl.offsetWidth
  const streetNameWidth = streetName.textEl.scrollWidth

  if (streetNameWidth > streetNameCanvasWidth) {
    streetName.el.style.width = streetNameCanvasWidth + 'px'
  } else {
    streetName.el.style.width = 'auto'
  }
}

function updateStreetNameCanvasPos () {
  const menuEl = document.querySelector('.menu-bar-right')
  const menuElPos = getElAbsolutePos(menuEl)
  const streetNameElPos = getElAbsolutePos(streetName.el)

  streetNameCanvasEl.classList.add('no-movement')
  if (streetNameElPos[0] + streetNameEl.offsetWidth > menuElPos[0]) {
    streetNameCanvasEl.classList.add('move-down-for-menu')
  } else {
    streetNameCanvasEl.classList.remove('move-down-for-menu')
  }

  window.setTimeout(function () {
    streetNameCanvasEl.classList.remove('no-movement')
  }, 50)
}

// Add window listeners to resize and reposition the street name when it resizes
// Only do this after everything is loaded because you don't want to
// fire it before the street name is ready
window.addEventListener('stmx:everything_loaded', function (e) {
  window.addEventListener('resize', (e) => {
    resizeStreetName()
    updateStreetNameCanvasPos()
  })
})

// Add prompt event to main street name
if (!app.readOnly) {
  streetNameEl.addEventListener('pointerdown', askForStreetName)
}

