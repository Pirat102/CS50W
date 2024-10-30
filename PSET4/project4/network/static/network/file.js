document.addEventListener('DOMContentLoaded', function() {
  // Check if element exist. This is the way to handle multiple HTML files
  const postForm = document.getElementById('post-form');
  if (postForm) {
    // Create new post
    postForm.addEventListener('submit', function(event) {
      event.preventDefault();
    // Get input
    const content = document.getElementById('post-content').value;
    console.log(`element ${content}`);

    fetch('/create', {
      method: 'POST',
      body: JSON.stringify({body: content})
    })
    .then(response => response.json())
    .then(data => {
      console.log('Django response:', data);
      // Clear textarea
      document.getElementById('post-content').value = '';
      // Refresh the page
      location.reload();
    })
    .catch(error => {
      console.error('Error:', error);
    })
  });
  };


  // Follow/Unfollow
  const followBtn = document.querySelectorAll('#follow')
  if (followBtn) {
    followBtn.forEach(button =>{
      button.addEventListener('click', function() {
        console.log('Clicked');
        const userId = button.getAttribute('data-user-id');
        fetch(`/is_following/${userId}`,{
          method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
          console.log('Django response:', data);
          if (data.status === "success") {
            button.innerHTML = data.is_following ? "Unfollow" : "Follow";
          } else {
              console.error("Error updating follow status");
          }
        })
        .catch(error => {
          console.error('Error:', error);
        })
      });
    });
  };

  // Edit post
  const editPost = document.querySelectorAll('#edit-post')
  if (editPost) {
    editPost.forEach(button => {
      button.addEventListener('click', () => {
        console.log('Clicked')
      })
    })
  }

  
});
  