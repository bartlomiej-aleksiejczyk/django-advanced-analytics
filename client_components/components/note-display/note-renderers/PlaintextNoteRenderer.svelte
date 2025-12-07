<script>
  import { noteStoreService } from "../services/noteStoreService.svelte.js";
  import { selectedNote } from "../noteStore.svelte.js";

  const { saveNoteContent } = noteStoreService();

  let debounceTimer = null;

  function debounceSave() {
    selectedNote.isSaving = true;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(saveNoteContent, 1000);
  }
</script>

<div class="notes-display__content">
  <textarea
    bind:value={selectedNote.content}
    class="notes-display__textarea"
    oninput={debounceSave}
  ></textarea>
</div>

<style>
  .notes-display__textarea {
    padding-left: 3rem;
    overflow: auto;
    resize: none;
    white-space: pre;
    outline: none;
    background-color: var(--color-main-text-area);
    color: var(--color-main-text);
    border: none;
    margin: 0;
    justify-content: start;
    flex: 1;

    &:focus {
      outline-color: transparent;
    }
  }

  .notes-display__content {
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: start;
    flex: 1;
    align-self: stretch;
  }
</style>
