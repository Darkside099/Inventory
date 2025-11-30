// Client side helpers
console.log('Cloud Inventory Hub scripts loaded');

// Example: dismiss flash messages after 6s
setTimeout(() => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(a => a.classList.remove('show'));
}, 6000);
