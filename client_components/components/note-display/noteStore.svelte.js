export const selectedNote = $state({
  content: "",
  title: undefined,
  type: undefined,
  ajaxNoteEndpoint: undefined,
  selectedNoteId: undefined,
  csrfToken: undefined,
  isSaving: false,
});
