<script>
  const { children } = $props();
  import { selectedNote } from "../noteStore.svelte.js";
</script>

<div class="notes-display">
  {#if selectedNote.title && selectedNote.selectedNoteId}
    <div class="notes-display__header">
      <h3>{selectedNote.title}</h3>
    </div>
    {@render children()}
  {:else}
    <div class="notes-display__no-content">
      <h3>Select a note to see details.</h3>
    </div>
  {/if}
</div>

<style>
  .notes-display {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    flex-grow: 1;
    align-self: stretch;
  }

  .notes-display__header {
    padding: 1.25rem 1rem 1.5rem;
    display: flex;
    justify-content: center;
    background-color: var(--color-main-text-area);
    color: var(--color-main-text);
    border: none;
  }

  .notes-display__no-content {
    justify-content: center;
    display: flex;
    align-items: center;
    flex: 1;
    align-self: stretch;
    text-align: center;
  }
</style>
