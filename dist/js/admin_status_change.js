function set_status(status, duration, token) {
  console.log("making set status request");
  fetch('/set_status', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'token': token;
    },
    body: JSON.stringify({'status': status, 'duration': duration})
  })
  .then(response => {
    if(response.ok) {
      return response.text();
    } else {
      throw new Error('Network Response Not Ok');
    }
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('FETCH FAILED:', error);
  });
}
