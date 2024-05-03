function scrollToBottom() {
  let objDiv = document.getElementById("messageBody");
  objDiv.scrollTop = objDiv.scrollHeight;
}

scrollToBottom();

const roomName = JSON.parse(document.getElementById("room-name").textContent);
const userName = JSON.parse(document.getElementById("user_name").textContent);

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

// function s() {
//   var i = document.getElementById("input");
//   if (i.value == "") {
//     document.getElementById("submit").disabled = true;
//   } else document.getElementById("submit").disabled = false;
// }

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  // document.querySelector('#user-hello').innerHTML = (data.tester)
  if (data.message) {
    document.querySelector("#messageBody").innerHTML +=
      '<li>' +
      '<div class="msg-recived msg-container">' +
      '<div class="avatar">' +
      '<div class="send-time">Just Now</div>' +
      '</div>' +
      '<div class="msg-box" id="message-text">' +
      '<div class="inner-box">' +
      '<div class="name"><b>' + data.message + '</b></div>' +
      '<div class="meg">' + data.message +
      '</div>' +
      '</div>' +
      '</div>' +
      '</div>' +
      '</li>';
    // data.username + ": " + data.message + "<br>";
    scrollToBottom();
  } else {
    // alert("This Message is Empty");
  }
  // scrollToBottom();
};

document.querySelector("#submit").onclick = function (e) {
  console.log("clicked")
  const messageInputDom = document.querySelector("#input");
  const message = messageInputDom.value;
  chatSocket.send(
    JSON.stringify({
      message: message,
      username: userName,
      room: roomName,
    })
  );
  messageInputDom.value = "";
};

input.addEventListener("keyup", function (e) {
  var i = document.getElementById("input");
  if (i.value == "" && e.keyCode === 13) {
    alert("This Message is Empty!");
  } else {
    if (e.keyCode === 13) {
      const messageInputDom = document.querySelector("#input");
      const message = messageInputDom.value;
      chatSocket.send(
        JSON.stringify({
          message: message,
          username: userName,
          room: roomName,
        })
      );
      messageInputDom.value = "";
    }
  }
});
