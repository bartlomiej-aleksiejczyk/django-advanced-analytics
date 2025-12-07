<svelte:options customElement="note-display" />

<script>
  import { onMount } from "svelte";
  import { setupInactivityTimer } from "./services/noteReloadServices";
  import { noteStoreService } from "./services/noteStoreService.svelte";
  import { selectedNote } from "./noteStore.svelte.js";
  import PlaintextNoteRenderer from "./note-renderers/PlaintextNoteRenderer.svelte";
  import UniversalRendererWrapper from "./note-renderers/UniversalRendererWrapper.svelte";
  import TodoNoteRenderer from "./note-renderers/TodoNoteRenderer.svelte";

  let { ajaxNoteEndpoint, selectedNoteId, csrfToken = "" } = $props();

  let { loadDefaultNote, loadNoteContent } = noteStoreService();

  window.addEventListener("beforeunload", function (event) {
    if (selectedNote.isSaving) event.preventDefault();
  });

  onMount(() => {
    selectedNote.ajaxNoteEndpoint = ajaxNoteEndpoint;
    selectedNote.selectedNoteId = selectedNoteId;
    selectedNote.csrfToken = csrfToken;

    if (selectedNoteId === "local~note") {
      selectedNote.title = selectedNoteId;
      selectedNote.type = "PLAINTEXT";
      loadDefaultNote();
    } else {
      document.addEventListener("visibilitychange", handleVisibilityChange);
      loadNoteContent();
      setupInactivityTimer(loadNoteContent);
    }
  });

  function handleVisibilityChange() {
    if (!document.hidden) {
      loadNoteContent();
    }
  }
</script>

<UniversalRendererWrapper>
  {#if selectedNote.type === "PLAINTEXT"}
    <PlaintextNoteRenderer />
  {:else if selectedNote.type === "MARKDOWN"}
    <div></div>
  {:else if selectedNote.type === "TODO"}
    <TodoNoteRenderer />
  {/if}
</UniversalRendererWrapper>
