const form = document.querySelector('#segment-form');
const result = document.querySelector('#result');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const values = new FormData(form);
  const tenure = values.get('relationship_tenure_months');
  const payload = {
    customer_id: values.get('customer_id'),
    account_type: values.get('account_type'),
    product_codes: values.get('product_codes').split(',').map((v) => v.trim()).filter(Boolean),
    relationship_tenure_months: tenure ? Number(tenure) : null,
    interaction_text: values.get('interaction_text') || null,
  };
  result.innerHTML = '<p>Classifying…</p>';
  try {
    const response = await fetch('/v1/segment', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error('The request could not be processed.');
    const data = await response.json();
    result.innerHTML = `<p class="label">SEGMENT</p><h2>${data.segment}</h2><p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</p><p><strong>Mode:</strong> ${data.scoring_mode}</p><p class="rationale">${data.rationale.join(' · ')}</p>`;
  } catch (error) {
    result.innerHTML = `<p class="error">${error.message}</p>`;
  }
});
