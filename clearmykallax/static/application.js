document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('fieldset.foldable').forEach(fieldset => {
    function toggle() {
      fieldset.classList.toggle('folded');
    }
    fieldset.querySelector('legend').addEventListener('click', (event) => {toggle()});
    if (fieldset.classList.contains('initially-folded')) {
      fieldset.classList.remove('initially-folded');
      toggle();
    }
  })
});
