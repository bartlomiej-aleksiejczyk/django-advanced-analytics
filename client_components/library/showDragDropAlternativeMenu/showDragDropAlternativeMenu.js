/**
 * Displays a headless modal for selecting an index and a group as an alternative to drag and drop.
 *
 * @param {Object} options - Configuration options for the modal.
 * @param {string} [options.title="Choose Position and Group"] - The title displayed on the modal.
 * @param {string} [options.indexLabel="Select Index:"] - Label for the index dropdown.
 * @param {string} [options.groupLabel="Select Group:"] - Label for the group dropdown.
 * @param {string} [options.confirmText="Confirm"] - Text for the confirm button.
 * @param {string} [options.cancelText="Cancel"] - Text for the cancel button.
 * @param {Array<number|string>} [options.indices=[1, 2, 3, 4, 5]] - List of indices available for selection.
 * @param {Array<string>} [options.groups=["Group A", "Group B", "Group C"]] - List of groups available for selection.
 * @param {Function} [options.callback] - Function to be called when the user confirms the selection.
 *        The callback receives two arguments: selected index and selected group.
 */
function showDragDropAlternativeMenu(options) {
  // TODO: use popover api
  const {
    title = "Choose Position and Group",
    indexLabel = "Select Index:",
    groupLabel = "Select Group:",
    confirmText = "Confirm",
    cancelText = "Cancel",
    indices = [1, 2, 3, 4, 5],
    groups = ["Group A", "Group B", "Group C"],
    callback = (index, group) => console.log("Selected:", index, group),
  } = options;

  const modal = document.createElement("div");
  modal.setAttribute("popover", "");
  modal.classList.add("global-popover");

  const titleElement = document.createElement("h3");
  titleElement.textContent = title;
  modal.appendChild(titleElement);

  const indexLabelElement = document.createElement("label");
  indexLabelElement.textContent = indexLabel;
  modal.appendChild(indexLabelElement);

  const indexSelect = document.createElement("select");
  indices.forEach((idx) => {
    const option = document.createElement("option");
    option.value = idx;
    option.textContent = idx;
    indexSelect.appendChild(option);
  });
  modal.appendChild(indexSelect);
  modal.appendChild(document.createElement("br"));

  const groupLabelElement = document.createElement("label");
  groupLabelElement.textContent = groupLabel;
  modal.appendChild(groupLabelElement);

  const groupSelect = document.createElement("select");
  groups.forEach((group) => {
    const option = document.createElement("option");
    option.value = group;
    option.textContent = group;
    groupSelect.appendChild(option);
  });
  modal.appendChild(groupSelect);
  modal.appendChild(document.createElement("br"));

  const confirmButton = document.createElement("button");
  confirmButton.textContent = confirmText;
  confirmButton.style.marginTop = "10px";
  confirmButton.onclick = () => {
    callback(indexSelect.value, groupSelect.value);
    document.body.removeChild(modal);
  };
  modal.appendChild(confirmButton);

  const cancelButton = document.createElement("button");
  cancelButton.textContent = cancelText;
  cancelButton.style.marginLeft = "10px";
  cancelButton.onclick = () => {
    document.body.removeChild(modal);
  };
  modal.appendChild(cancelButton);

  document.body.appendChild(modal);
}
