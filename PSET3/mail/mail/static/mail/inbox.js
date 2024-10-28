document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  // Clear email view, because it's appending elements with each API request
  document.querySelector('#email-view').innerHTML = '';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Clear email view, because it's appending elements with each API request
  document.querySelector('#email-view').innerHTML = '';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    emails.forEach(email => {
      const div = document.createElement('div');
      const button = document.createElement('button');
      button.style.display = 'none'
      div.innerHTML = `
      <span>Subject: ${email.subject}</span><br>
      <span>From: ${email.sender}</span><br>
      <span class="timestamp">${email.timestamp}</span><br>
      <button class="reply-btn"> Reply </button>
      `;

      const replyButton = div.querySelector('.reply-btn');
      replyButton.addEventListener('click', function(event){
        event.stopPropagation();
        compose_email()
        document.querySelector('#compose-recipients').value = email.recipients;
        document.querySelector('#compose-subject').value = `Re:${email.subject}`;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;

      })

      // Archive/Unarchive
      if (mailbox != 'sent') {
        button.style.display = 'inline-block'
        button.innerHTML = email.archived ? "Unarchive" : "Archive";
        button.addEventListener('click', function(event) {
        event.stopPropagation();
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        })
        .then(() => load_mailbox('inbox'))
        })
      } 

      // Add event listener for each email and load email content on click
      div.addEventListener('click', function() {
        load_email(email.id)
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
      });
      // Change background color if email was read
      div.style.backgroundColor = email.read ? "grey" : "white";



    div.appendChild(button)
    document.querySelector('#emails-view').append(div);
    
    });
  })
}


function send_email() {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    })
    return false;
  };


function load_email(emailId) {
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
  console.log(email);
  const div = document.createElement('div');
      div.innerHTML = `
      <table> <tr>
          <td> From:&nbsp;${email.sender}  </td>
          <td class="timestamp"> ${email.timestamp} </td> </tr>
        <tr> <td> To:&nbsp;${email.recipients} </td> </tr>
      </table>
      <br>
      <div class="body-wrapper">
       <h2> ${email.subject}</h2>
        <div class="mail-body">
        ${email.body}
        </div>
      </div>
      `;

  // Disable emails-view, append email div
  document.querySelector('#emails-view').style.display = "none";
  document.querySelector('#email-view').append(div);
  });
}
