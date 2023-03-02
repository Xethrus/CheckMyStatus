
async function get_status(link) {
  let response = await fetch(link);
  if (response.ok) {
    let data = await response.json();
    return data.status;
  } else {
    throw new Error("HTTP-ERROR: " + response.status);
  }
}

async function check_availability() {
  link = "http://REDACTED:80/get_status";
  var status = get_status(link);
  var isAvailable;
  if(status == "busy") {
    isAvailable = false;
  } else {
    isAvailable = true;
  }
  return isAvailable;
}
