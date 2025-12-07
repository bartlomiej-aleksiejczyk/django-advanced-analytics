const qSelect = (function () {
  class qSelectWrapper {
    constructor(elements) {
      this.elements = Array.isArray(elements) ? elements : [elements];
    }

    css(property, value) {
      if (typeof property === "object") {
        this.elements.forEach((el) => {
          Object.entries(property).forEach(([key, val]) => {
            el.style[key] = val;
          });
        });
      } else if (value !== undefined) {
        this.elements.forEach((el) => (el.style[property] = value));
      } else {
        return getComputedStyle(this.elements[0])[property];
      }
      return this;
    }

    hide() {
      return this.css("display", "none");
    }

    show(displayType = "block") {
      return this.css("display", displayType);
    }

    addClass(className) {
      this.elements.forEach((el) => el.classList.add(className));
      return this;
    }

    removeClass(className) {
      this.elements.forEach((el) => el.classList.remove(className));
      return this;
    }

    toggleClass(className) {
      this.elements.forEach((el) => el.classList.toggle(className));
      return this;
    }

    on(event, handler) {
      this.elements.forEach((el) => el.addEventListener(event, handler));
      return this;
    }

    off(event, handler) {
      this.elements.forEach((el) => el.removeEventListener(event, handler));
      return this;
    }

    html(content) {
      if (content === undefined) {
        return this.elements[0].innerHTML;
      }
      this.elements.forEach((el) => (el.innerHTML = content));
      return this;
    }

    text(content) {
      if (content === undefined) {
        return this.elements[0].textContent;
      }
      this.elements.forEach((el) => (el.textContent = content));
      return this;
    }

    each(callback) {
      this.elements.forEach((el, idx) => callback(el, idx));
      return this;
    }

    find(selector) {
      let found = [];
      this.elements.forEach((el) => {
        found = found.concat(Array.from(el.querySelectorAll(selector)));
      });
      return new qSelectWrapper(found);
    }

    parent() {
      const parents = this.elements
        .map((el) => el.parentElement)
        .filter((el) => el !== null);
      return new qSelectWrapper([...new Set(parents)]);
    }

    is(selector) {
      return this.elements.some((el) => el.matches(selector));
    }

    get(index) {
      return index !== undefined ? this.elements[index] : this.elements;
    }
  }

  return {
    one(selector) {
      const el = document.querySelector(selector);
      if (!el) throw new Error(`Element "${selector}" not found.`);
      return new qSelectWrapper(el);
    },

    any(selector) {
      const els = Array.from(document.querySelectorAll(selector));
      return new qSelectWrapper(els);
    },

    ready(fn) {
      if (document.readyState !== "loading") {
        fn();
      } else {
        document.addEventListener("DOMContentLoaded", fn);
      }
    },
  };
})();
