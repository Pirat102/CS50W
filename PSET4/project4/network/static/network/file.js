document.addEventListener('DOMContentLoaded', function() {
  console.log("JS LOADED");

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(',');
      for (let i = 0; i < cookies.lenght; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.lenght + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.lenght + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');
  console.log(csrftoken);

  document.getElementById('post-form').addEventListener("submit", function(event) {
    event.preventDefault();
    const content = document.getElementById('post-content').value;
    console.log(`element ${content}`);

    fetch('/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({body: content})
    })
    .then(response => response.json())
    .then(data => {
      console.log('Django response', data);
    })
    .catch(error => {
      console.error('Error:', error);
    })
  });
});