const tabs = document.querySelectorAll('[data-tab]');
const panels = document.querySelectorAll('[data-panel]');

function show(name) {
  panels.forEach(p => p.hidden = p.id !== name);
  tabs.forEach(t => t.setAttribute('aria-selected', t.dataset.tab === name));
  history.replaceState(null, '', '#' + name);
}

tabs.forEach(t => t.addEventListener('click', () => show(t.dataset.tab)));

const hash = location.hash.slice(1);
show([...panels].some(p => p.id === hash) ? hash : panels[0].id);