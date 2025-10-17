document.getElementById('inspectionForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const responseMsg = document.getElementById('formResponse');
  responseMsg.textContent = 'Sending...';

  const data = new FormData(form);

  const res = await fetch('/send', {
    method: 'POST',
    body: data
  });

  const result = await res.json();
  responseMsg.textContent = result.message;
  responseMsg.style.color = result.success ? 'green' : 'red';

  if (result.success) form.reset();
});
