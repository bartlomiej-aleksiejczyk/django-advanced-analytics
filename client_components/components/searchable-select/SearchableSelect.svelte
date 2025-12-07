<svelte:options
  customElement={{
    tag: "searchable-select",
    shadow: "none",
  }}
/>

<script>
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";

  let { emptyLabel, options, selectedOptionId } = $props();

  let filteredOptions = $state([]);
  let isDropdownOpen = $state(false);
  let searchText = $state(undefined);
  let highlightedIndex = $state(-1);
  let dropdownRef;
  let selectedOption = $state(undefined);
  let maxDropdownHeight = $state("150px");

  function toggleDropdown() {
    adjustDropdownHeight();

    isDropdownOpen = !isDropdownOpen;

    if (isDropdownOpen) {
      // requestAnimationFrame(() => {});
      searchText = "";
      filterOptions();
      highlightedIndex = filteredOptions.findIndex(
        (option) => option[1] == selectedOptionId
      );
    } else {
      searchText = selectedOption[0] ?? "";
    }
  }

  function filterOptions() {
    filteredOptions = JSON.parse(options).filter((option) =>
      option[0].toLowerCase().includes(searchText.toLowerCase())
    );
    highlightedIndex = -1;
  }

  function onSelectOption(option) {
    if (!option) return;
    searchText = option[0] ?? emptyLabel;
    isDropdownOpen = false;
    location.href = "?directory=" + option[1];
  }

  function handleClickOutside(event) {
    if (!dropdownRef) return;

    if (!dropdownRef.contains(event.composedPath()[0])) {
      isDropdownOpen = false;
      searchText = selectedOption[0] ?? emptyLabel;
    }
  }

  function handleKeyDown(event) {
    if (!isDropdownOpen) return;
    const maxItemIndex = filteredOptions.length - 1;
    if (event.key === "ArrowDown") {
      const incrementedIndex = highlightedIndex + 1;
      highlightedIndex =
        incrementedIndex > maxItemIndex ? -1 : incrementedIndex;
    } else if (event.key === "ArrowUp") {
      const decrementedIndex = highlightedIndex - 1;
      highlightedIndex =
        decrementedIndex < -1 ? maxItemIndex : decrementedIndex;
    } else if (event.key === "Enter" && highlightedIndex !== -1) {
      onSelectOption(filteredOptions[highlightedIndex]);
    }
  }

  function adjustDropdownHeight() {
    if (!dropdownRef) return;

    const rect = dropdownRef.getBoundingClientRect();
    const spaceBelow = window.innerHeight - rect.bottom;
    maxDropdownHeight = `${Math.min(spaceBelow - 10, 600)}px`;
  }

  onMount(() => {
    selectedOption = JSON.parse(options).filter(
      (option) => option[1] == selectedOptionId
    )[0];
    searchText = selectedOption[0];
    document.removeEventListener("click", handleClickOutside);
    document.removeEventListener("keydown", handleKeyDown);
    document.addEventListener("click", handleClickOutside);
    document.addEventListener("keydown", handleKeyDown);
  });
</script>

<!-- Component Markup -->
<div class="searchable-select" id="myObject">
  <div class="dropdown" bind:this={dropdownRef}>
    <input
      type="text"
      bind:value={searchText}
      oninput={filterOptions}
      onclick={toggleDropdown}
      placeholder="Select an option..."
      class="searchable-dropdown-input"
    />
    <div class="chevron {isDropdownOpen ? 'open' : ''}">▼</div>
    {#if isDropdownOpen}
      <div
        class="dropdown-list"
        transition:slide
        style:max-height={maxDropdownHeight}
      >
        {#each filteredOptions as option, i}
          <div
            class="dropdown-item {i === highlightedIndex ? 'highlighted' : ''}"
            onclick={() => onSelectOption(option)}
          >
            {option[0]}
          </div>
        {/each}
        {#if filteredOptions.length === 0}
          <div class="dropdown-item empty">No results found</div>
        {/if}
      </div>
    {/if}
  </div>
</div>

<!-- Component Styles -->
<style>
  .searchable-select {
    margin: 0rem calc(1rem + 2px) 0.3rem;
    align-self: stretch;
    display: flex;
    position: sticky;
    padding-bottom: 0.5rem;
    background-color: var(--color-background);
    top: 0;
  }

  .dropdown {
    position: relative;
    flex-grow: 1;
    font-family: monospace;
  }

  .searchable-dropdown-input {
    width: 100%;
    padding: 8px;
    border: 2px solid var(--color-secondary-darker);
    border-radius: var(--border-radius-medium);
    background: var(--color-text-on-primary);
    color: var(--color-main-text);
    font-size: 0.8rem;
    outline: none;
    cursor: pointer;
  }

  .dropdown-list {
    position: absolute;
    top: 100%;
    width: 100%;
    border: 2px solid var(--color-secondary-darker);
    border-top: none;
    border-radius: var(--border-radius-medium);
    background: var(--color-main-text-area);
    overflow-y: auto;
    z-index: 10;
  }

  .dropdown-item {
    padding: 8px;
    border-bottom: 1px solid var(--color-main-text);
    cursor: pointer;
    transition: background 0.2s;
  }

  .dropdown-item:hover {
    background-color: var(--color-secondary-lighter);
  }

  .dropdown-item.highlighted {
    background-color: var(--color-secondary);
  }

  .dropdown-item:last-child {
    border-bottom: none;
  }

  .dropdown-item.empty {
    text-align: center;
    font-style: italic;
  }

  .chevron {
    position: absolute;
    right: 12px;
    top: 11%;
    font-size: 16px;
    pointer-events: none;
    transition: transform 0.3s ease;
    color: var(--color-main-text);
  }

  .chevron.open {
    transform: rotate(180deg);
  }
</style>
