(() => {
  const PER_PAGE = 3;
  const items = [...document.querySelectorAll('#order-list > article')];
  const pager = document.getElementById('orders-pager');
  const pages = Math.ceil(items.length / PER_PAGE);
  if (pages <= 1) return pager.remove();

  const btn = (label, page, { active, disabled } = {}) => `
    <button type="button" data-page="${page}" ${disabled ? 'disabled' : ''} ${active ? 'aria-current="page"' : ''}
      class="h-9 min-w-9 rounded-button border border-border px-3 disabled:opacity-40 ${active ? 'bg-secondary text-white' : 'text-foreground'}">${label}</button>`;

  const show = (p) => {
    items.forEach((el, i) => el.classList.toggle('hidden', Math.floor(i / PER_PAGE) !== p - 1));
    pager.innerHTML =
      btn('<<', 1, { disabled: p === 1 }) +
      Array.from({ length: pages }, (_, i) => btn(i + 1, i + 1, { active: i + 1 === p })).join('') +
      btn('>>', pages, { disabled: p === pages });
  };

  pager.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-page]');
    if (b) show(+b.dataset.page);
  });

  show(1);
})();