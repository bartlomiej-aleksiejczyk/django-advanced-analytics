/**
 * MobileDragAndDrop - A lightweight, headless drag-and-drop library for mobile and desktop environments.
 *
 * Features:
 * - Supports multiple containers for flexible drag-and-drop operations.
 * - Compatible with Shadow DOM to work inside web components.
 * - Configurable using attributes or CSS selectors.
 * - Provides event hooks for key drag-and-drop lifecycle events.
 * - Internal tracking for container enter/leave detection.
 * - Stores references to event listeners for efficient cleanup.
 * - Includes a `destroy()` method to remove all event listeners when no longer needed.
 *
 * Configuration Options:
 * @param {Object} config - Configuration object.
 * @param {HTMLElement[]} [config.containers] - Array of container elements.
 * @param {string} [config.containerSelector="[data-drag-container]"] - Selector for drag containers.
 * @param {string} [config.draggableSelector="[data-draggable]"] - Selector for draggable elements.
 * @param {string} [config.handleSelector="[data-drag-handle]"] - Selector for drag handles.
 * @param {HTMLElement|Document} [config.root=document] - Root element (document or Shadow DOM root).
 *
 * Event Hooks:
 * - `onDragStart(info)`: Triggered when a drag operation begins.
 * - `onDragEnter(info)`: Fired when a draggable enters a new container.
 * - `onDragLeave(info)`: Fired when a draggable leaves a container.
 * - `onDragMove(info)`: Fired continuously while dragging.
 * - `onDrop(info)`: Fired when a draggable is dropped.
 *
 * Example Usage:
 * ```javascript
 * class MyComponent extends HTMLElement {
 *   constructor() {
 *     super();
 *     this.attachShadow({ mode: "open" });
 *     this.shadowRoot.innerHTML = `
 *       <div data-drag-container>
 *         <div data-draggable data-dragitem-index="1">Item 1</div>
 *         <div data-draggable data-dragitem-index="2">Item 2</div>
 *       </div>
 *     `;
 *   }
 *
 *   connectedCallback() {
 *     this.dnd = new MobileDragAndDrop({ root: this.shadowRoot });
 *     MobileDragAndDrop.enable(null, this.dnd);
 *
 *     this.dnd.onDragStart = (info) => console.log("Drag started", info);
 *     this.dnd.onDragEnter = (info) => console.log("Entered container", info);
 *     this.dnd.onDragLeave = (info) => console.log("Left container", info);
 *     this.dnd.onDragMove = (info) => console.log("Dragging...", info);
 *     this.dnd.onDrop = (info) => console.log("Dropped", info);
 *   }
 *
 *   disconnectedCallback() {
 *     this.dnd.destroy();
 *   }
 * }
 * customElements.define("my-component", MyComponent);
 * ```
 */

class MobileDragAndDrop {
  /**
   * @param {Object} config - Configuration object.
   * @param {HTMLElement[]} [config.containers] - Array of container elements.
   * @param {string} [config.containerSelector="[data-drag-container]"] - CSS selector for containers.
   * @param {string} [config.draggableSelector="[data-draggable]"] - CSS selector for draggable elements.
   * @param {string} [config.handleSelector="[data-drag-handle]"] - CSS selector for drag handles.
   * @param {HTMLElement|Document} [config.root=document] - The root element (document or shadowRoot).
   */
  constructor(config = {}) {
    this.config = Object.assign(
      {
        containerSelector: "[data-drag-container]",
        draggableSelector: "[data-draggable]",
        handleSelector: "[data-drag-handle]",
        root: document,
        containers: null,
      },
      config
    );

    this.root = this.config.root;
    this.containers =
      this.config.containers ||
      Array.from(this.root.querySelectorAll(this.config.containerSelector));

    this.draggingEl = null;
    this.offsetX = 0;
    this.offsetY = 0;
    this.scrollInterval = null;
    this.currentContainer = null; // Track current container for enter/leave events
    this.draggableListeners = []; // To store references for cleanup

    // External event hooks (callbacks)
    this.onDragStart = null;
    this.onDragEnter = null;
    this.onDragLeave = null;
    this.onDragMove = null;
    this.onDrop = null;

    // Bind event handlers for proper removal later.
    this.pointerMoveHandler = this.pointerMoveHandler.bind(this);
    this.pointerUpHandler = this.pointerUpHandler.bind(this);
  }

  /**
   * Attaches draggable behavior to elements.
   * If a CSS selector is provided, it overrides the default attribute-based selector.
   * @param {string|null} [selector] - Optional CSS selector for draggable elements.
   * @param {MobileDragAndDrop} instance - An instance of MobileDragAndDrop.
   */
  static enable(selector, instance) {
    const configSelector = selector || instance.config.draggableSelector;
    const draggableItems = instance.root.querySelectorAll(configSelector);
    draggableItems.forEach((item) => {
      item.style.touchAction = "none"; // Prevent default gestures

      const pointerDownCallback = (e) => {
        // If a drag handle is defined, ensure the event originated from it.
        if (instance.config.handleSelector) {
          if (!e.target.closest(instance.config.handleSelector)) {
            return;
          }
        }
        instance.pointerDownHandler(e, item);
      };

      // Store listener references for later removal.
      instance.draggableListeners.push({ item, pointerDownCallback });
      item.addEventListener("pointerdown", pointerDownCallback);
      item.addEventListener("touchstart", pointerDownCallback, {
        passive: false,
      });
    });
  }

  /**
   * Handles the start of a drag event.
   * @param {Event} e - The event object.
   * @param {HTMLElement} item - The element being dragged.
   */
  pointerDownHandler(e, item) {
    if (e.touches && e.touches.length > 1) return; // Ignore multi-touch

    this.draggingEl = item;
    const rect = item.getBoundingClientRect();
    const clientX = e.clientX ?? e.touches[0].clientX;
    const clientY = e.clientY ?? e.touches[0].clientY;

    this.offsetX = clientX - rect.left;
    this.offsetY = clientY - rect.top;

    document.addEventListener("pointermove", this.pointerMoveHandler);
    document.addEventListener("pointerup", this.pointerUpHandler);
    document.addEventListener("touchmove", this.pointerMoveHandler, {
      passive: false,
    });
    document.addEventListener("touchend", this.pointerUpHandler);

    e.preventDefault();

    if (this.onDragStart) {
      this.onDragStart({
        element: this.draggingEl,
        originalX: clientX,
        originalY: clientY,
      });
    }
  }

  /**
   * Handles the movement of the dragged element.
   * Detects container enter/leave events and provides continuous drag move feedback.
   * @param {Event} e - The event object.
   */
  pointerMoveHandler(e) {
    if (!this.draggingEl) return;

    const clientX = e.clientX ?? (e.touches ? e.touches[0].clientX : 0);
    const clientY = e.clientY ?? (e.touches ? e.touches[0].clientY : 0);
    const targetElement = e.target;

    // Determine current container using the closest matching container.
    let newContainer = targetElement.closest(this.config.containerSelector);
    if (!newContainer && this.containers.length) {
      newContainer = this.containers.find((cont) =>
        cont.contains(targetElement)
      );
    }

    // Trigger onDragLeave if the container has changed.
    if (this.currentContainer !== newContainer) {
      if (this.currentContainer && this.onDragLeave) {
        this.onDragLeave({
          element: this.draggingEl,
          container: this.currentContainer,
        });
      }
      if (newContainer && this.onDragEnter) {
        this.onDragEnter({ element: this.draggingEl, container: newContainer });
      }
      this.currentContainer = newContainer;
    }

    // Determine hovered draggable element, if any.
    const hoverElement = targetElement.closest(this.config.draggableSelector);
    const hoverIndex = hoverElement
      ? hoverElement.getAttribute("data-dragitem-index")
      : null;

    if (this.onDragMove) {
      this.onDragMove({
        element: this.draggingEl,
        x: clientX - this.offsetX,
        y: clientY - this.offsetY,
        hoverElement: hoverElement,
        hoverIndex: hoverIndex,
        container: this.currentContainer,
      });
    }

    this.handleAutoScroll(e);
  }

  /**
   * Handles the end of the drag event and triggers the drop event.
   * @param {Event} e - The event object.
   */
  pointerUpHandler(e) {
    document.removeEventListener("pointermove", this.pointerMoveHandler);
    document.removeEventListener("pointerup", this.pointerUpHandler);
    document.removeEventListener("touchmove", this.pointerMoveHandler);
    document.removeEventListener("touchend", this.pointerUpHandler);

    clearInterval(this.scrollInterval);

    const finalX =
      e.clientX ?? (e.changedTouches ? e.changedTouches[0].clientX : 0);
    const finalY =
      e.clientY ?? (e.changedTouches ? e.changedTouches[0].clientY : 0);

    // Determine drop target.
    const dropTarget = this.getDropTarget(finalX, finalY);

    if (this.onDrop) {
      this.onDrop({
        element: this.draggingEl,
        dropTarget: dropTarget,
        finalX: finalX,
        finalY: finalY,
      });
    }

    // Reset state.
    this.draggingEl = null;
    if (this.currentContainer && this.onDragLeave) {
      this.onDragLeave({ element: null, container: this.currentContainer });
    }
    this.currentContainer = null;
  }

  /**
   * Determines the drop target based on the final pointer coordinates.
   * @param {number} x - The final x coordinate.
   * @param {number} y - The final y coordinate.
   * @returns {HTMLElement|null} - The container element where the drop occurred.
   */
  getDropTarget(x, y) {
    const target = this.getElementFromPoint(x, y);
    return target ? target.closest(this.config.containerSelector) : null;
  }

  /**
   * Returns the element under the given coordinates, supporting Shadow DOM.
   * @param {number} x - X coordinate.
   * @param {number} y - Y coordinate.
   * @returns {HTMLElement|null} - The element under the coordinates.
   */
  getElementFromPoint(x, y) {
    let el = document.elementFromPoint(x, y);
    if (el && el.shadowRoot) {
      return el.shadowRoot.elementFromPoint(x, y) || el;
    }
    return el;
  }

  /**
   * Handles auto-scrolling when dragging near the screen edges.
   * @param {Event} e - The event object.
   */
  handleAutoScroll(e) {
    const scrollMargin = 50;
    const maxScrollSpeed = 20;
    const minScrollSpeed = 5;

    clearInterval(this.scrollInterval);
    const clientY = e.clientY ?? (e.touches ? e.touches[0].clientY : 0);

    if (clientY < scrollMargin) {
      const speed = Math.max(
        maxScrollSpeed * (1 - clientY / scrollMargin),
        minScrollSpeed
      );
      this.scrollInterval = setInterval(() => window.scrollBy(0, -speed), 20);
    } else if (clientY > window.innerHeight - scrollMargin) {
      const speed = Math.max(
        maxScrollSpeed *
          ((clientY - (window.innerHeight - scrollMargin)) / scrollMargin),
        minScrollSpeed
      );
      this.scrollInterval = setInterval(() => window.scrollBy(0, speed), 20);
    }
  }

  /**
   * Destroys the instance by removing all event listeners from draggable elements
   * and any global listeners attached during dragging.
   */
  destroy() {
    this.draggableListeners.forEach(({ item, pointerDownCallback }) => {
      item.removeEventListener("pointerdown", pointerDownCallback);
      item.removeEventListener("touchstart", pointerDownCallback);
    });
    this.draggableListeners = [];
    document.removeEventListener("pointermove", this.pointerMoveHandler);
    document.removeEventListener("pointerup", this.pointerUpHandler);
    document.removeEventListener("touchmove", this.pointerMoveHandler);
    document.removeEventListener("touchend", this.pointerUpHandler);
    clearInterval(this.scrollInterval);
  }
}
