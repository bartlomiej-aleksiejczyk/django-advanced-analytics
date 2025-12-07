import "idiomorph";

export function qSwap(target, content, options) {
  const element = document.querySelector(target);
  if (element && options.morph) {
    Idiomorph.morph(element, content);
  } else if (element) {
    element.innerHTML = content;
  }
}
