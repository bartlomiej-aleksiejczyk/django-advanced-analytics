<script>
  import { noteStoreService } from "../services/noteStoreService.svelte.js";
  import { selectedNote } from "../noteStore.svelte.js";
  // TODO: ADD TOOLTIPS FOR MOBILE AND DESKTOP
  const { saveNoteContent } = noteStoreService();

  let debounceTimer = null;

  function debounceSave() {
    selectedNote.content = serializeTodos(todos);
    selectedNote.isSaving = true;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(saveNoteContent, 1000);
  }

  function parseTodos(content) {
    return content.split("\n").map((line) => {
      const isChecked = line.startsWith("[x]");
      return { text: line.replace(/^\[.\] /, ""), done: isChecked };
    });
  }

  function serializeTodos(todos) {
    return todos
      .map((todo) => `[${todo.done ? "x" : " "}] ${todo.text}`)
      .join("\n");
  }

  let todos = $state(parseTodos(selectedNote.content));

  function toggleTodo(index) {
    debounceSave();
  }

  function addTodo(index) {
    todos.splice(index + 1, 0, { text: "", done: false });
    debounceSave();
    setTimeout(() => {
      document
        .querySelector("note-display")
        .shadowRoot.querySelector(`.todo-text[data-index="${index + 1}"]`)
        .focus();
    }, 50);
  }

  function updateText(index, event) {
    todos[index].text = event.target.value;
    debounceSave();
  }

  function handleKeydown(index, event) {
    if (event.key === "Enter") {
      event.preventDefault();
      addTodo(index);
    }
  }

  function removeTodo(index) {
    if (todos.length > 1) {
      todos.splice(index, 1);
      debounceSave();
    }
  }

  let draggedIndex = $state();

  function handleDragStart(event, index) {
    draggedIndex = index;
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", index);
    event.target.classList.add("dragging");
  }

  function handleDragOver(event, index) {
    event.preventDefault();
    const draggingElement = document
      .querySelector("note-display")
      .shadowRoot.querySelector(".dragging");

    if (draggingElement && index !== draggedIndex) {
      todos.splice(index, 0, todos.splice(draggedIndex, 1)[0]);
      draggedIndex = index;
      debounceSave();
    }
  }

  function handleDragEnd(event) {
    draggedIndex = null;
    event.target.classList.remove("dragging");
  }

  function handleTouchStart(event, index) {
    draggedIndex = index;
    event.target.classList.add("dragging");
  }

  function handleTouchMove(event) {
    event.preventDefault();
    const touch = event.touches[0];
    const element = document.elementFromPoint(touch.clientX, touch.clientY);
    if (element && element.dataset.index) {
      const newIndex = Number(element.dataset.index);
      if (newIndex !== draggedIndex) {
        todos.splice(newIndex, 0, todos.splice(draggedIndex, 1)[0]);
        draggedIndex = newIndex;
        debounceSave();
      }
    }
  }

  function handleTouchEnd(event) {
    event.target.classList.remove("dragging");
  }
</script>

<div class="todo-list">
  {#each todos as todo, index}
    <div
      class="todo-item"
      draggable="true"
      ondragstart={(e) => handleDragStart(e, index)}
      ondragover={(e) => handleDragOver(e, index)}
      ondragend={handleDragEnd}
      ontouchstart={(e) => handleTouchStart(e, index)}
      ontouchmove={handleTouchMove}
      ontouchend={handleTouchEnd}
      data-index={index}
      class:dragged={index === draggedIndex}
    >
      <span class="drag-handle">☰</span>
      <input
        type="checkbox"
        bind:checked={todo.done}
        onchange={() => toggleTodo(index)}
      />
      <input
        type="text"
        class="todo-text"
        bind:value={todo.text}
        oninput={(e) => updateText(index, e)}
        onkeydown={(e) => handleKeydown(index, e)}
        placeholder="New task..."
        data-index={index}
        class:completed={todo.done}
      />
      <button class="delete-todo" onclick={() => removeTodo(index)}>✕</button>
    </div>
  {/each}
  <button class="add-todo" onclick={() => addTodo(todos.length - 1)}
    >+ Add Task</button
  >
</div>

<style>
  .todo-list {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    background: var(--color-main-text-area);
  }

  .todo-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    background: var(--color-background-light-contrast);
    cursor: grab;
    outline: 0px dashed #ccc;
    transition: background-color 1s ease-out;
  }

  .todo-item.dragging {
    opacity: 0.5;
  }

  .drag-handle {
    cursor: grab;
    padding: 0.5rem;
    font-size: 1.2rem;
    color: var(--color-text-secondary);
  }

  .todo-text {
    flex: 1;
    border: none;
    padding: 0.5rem;
    background: transparent;
    color: var(--color-main-text);
    outline: none;
    font-size: 1rem;
  }

  .todo-text:focus {
    outline: 1px solid var(--color-accent);
  }

  .todo-text.completed {
    text-decoration: line-through;
    color: var(--color-text-secondary);
  }

  .delete-todo {
    background: var(--color-negative);
    color: white;
    border: none;
    padding: 0.3rem 0.6rem;
    margin-left: 0.5rem;
    cursor: pointer;
    font-size: 1rem;
  }

  .delete-todo:hover {
    background: var(--color-negative-darker);
  }

  .add-todo {
    margin-top: 0.5rem;
    padding: 0.5rem;
    border: none;
    cursor: pointer;
  }

  .add-todo:hover {
    background: var(--color-accent-hover);
  }
  .dragged {
    outline: 2px dashed #ccc;
    background: #f8f8f8;
    margin: 4px 0;
  }
  input,
  input[type="checkbox"] {
    width: 1.75rem;
    height: 1.75rem;
    margin: 0;
    display: inline;
  }
  input[type="checkbox"]:checked {
    background-color: var(--color-primary);
    accent-color: var(--color-primary);
  }
</style>
