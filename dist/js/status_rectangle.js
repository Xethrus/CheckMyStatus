
async function get_status(link) {
  console.log(link);
  let response = await fetch(link);
  if (response.ok) {
    let data = await response.json();
    return data.status;
  } else {
    throw new Error("HTTP-ERROR: " + response.status);
  }
}

async function check_availability() {
  link = "http://107.131.124.5:8000/get_status";
  var status = await get_status(link);
  var isAvailable;
  if(status == "busy") {
    console.log("STATUS BUSY")
    isAvailable = false;
  } else {
    console.log("STATUS AVAILABLE")
    isAvailable = true;
  }
  return isAvailable;
}
