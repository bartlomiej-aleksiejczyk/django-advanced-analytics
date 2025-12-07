let inactivityTimeout;

export function setupInactivityTimer(loadNoteContent) {
  resetInactivityTimer(loadNoteContent);
  ["mousemove", "keydown", "scroll", "click", "touchstart"].forEach((event) => {
    document.addEventListener(event, () =>
      resetInactivityTimer(loadNoteContent)
    );
  });
}
//TODO: extract variable to config file
export function resetInactivityTimer(loadNoteContent) {
  clearTimeout(inactivityTimeout);
  inactivityTimeout = setTimeout(() => {
    loadNoteContent();
  }, 60000);
}
