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
  const editButtons = document.querySelectorAll('.edit-button')
  if (editButtons) {
    editButtons.forEach(button => {
      button.addEventListener('click', () => {
        toggleEdit(button);
      });
    });
  }
  // Toogle between Edit/Save on user's posts
  function toggleEdit(button) {
    const postId = button.getAttribute('data-post-id')
    const postElement = document.querySelector(`.post[data-post-id='${postId}']`)
    const postBody = postElement.querySelector('.post-body')
    if (button.textContent.trim() === 'Edit') {
      postBody.style.display = 'none'
      // Create textarea and add text to it
      const textArea = document.createElement('textarea')
      textArea.value = `${postBody.textContent}`

      // Add new element, after original element
      postBody.insertAdjacentElement('afterend', textArea)
      // Focus cursor on the end of existing text
      textArea.focus();
      textArea.selectionStart = textArea.selectionEnd = textArea.value.length
      button.textContent = 'Save';
    } else {
      // Get value from new element, add it to the original element
      // Deleted new element and show updated element
      const editedBody = postElement.querySelector('textarea')
      postBody.textContent = editedBody.value
      postBody.style.display = ""
      editedBody.remove()
      button.textContent = 'Edit';
      console.log(postId)

    // Post new data to Django
    fetch('/edit_post/', {
      method: 'POST',
      body: JSON.stringify({
        body: postBody.textContent,
        post_id: postId
      })
    })


    }    


  }



  
});
  