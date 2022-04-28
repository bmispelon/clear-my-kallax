document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('fieldset.foldable').forEach(fieldset => {
    fieldset.querySelector('legend').addEventListener('click', (event) => {
      fieldset.classList.toggle('folded');
    });
  })
});
