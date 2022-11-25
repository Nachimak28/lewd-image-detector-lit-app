import React, { useEffect, useState } from "react";
import ScrollToBottom from "react-scroll-to-bottom";
import _ from "lodash";

const convertBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);

    fileReader.onload = () => {
      resolve(fileReader.result);
    };

    fileReader.onerror = (error) => {
      reject(error);
    };
  });
};


function Chat({ socket, username, room }) {
  const [currentMessage, setCurrentMessage] = useState("");
  const [messageList, setMessageList] = useState([]);

  // Create a reference to the hidden file input element
  const hiddenFileInput = React.useRef(null);
  
  // Programatically click the hidden file input element
  // when the Button component is clicked
  const handleClick = event => {
    hiddenFileInput.current.click();
  };
  // Call a function (passed as a prop from the parent component)
  // to handle the user-selected file 
  const handleChange = async (event) => {
    const fileUploaded = event.target.files[0];
    // convert img to b64 string - set it as img
    const fileb64str = await convertBase64(fileUploaded);
    await sendImage(fileb64str);
  };

  const sendImage = async (imgStr) => {
    if (imgStr !== "") {
      const messageData = {
        room: room,
        author: username,
        img: imgStr,
        time:
          new Date(Date.now()).getHours() +
          ":" +
          new Date(Date.now()).getMinutes(),
      };
      await socket.emit("send_message", messageData);
      setMessageList((list) => [...list, messageData]);
      setCurrentMessage("");
    }
  }

  const sendMessage = async () => {
    if (currentMessage !== "") {
      const messageData = {
        room: room,
        author: username,
        message: currentMessage,
        // img: hiddenFileInput,
        time:
          new Date(Date.now()).getHours() +
          ":" +
          new Date(Date.now()).getMinutes(),
      };

      await socket.emit("send_message", messageData);
      setMessageList((list) => [...list, messageData]);
      setCurrentMessage("");
    }
  };

  useEffect(() => {
    socket.on("receive_message", (data) => {
      setMessageList((list) => [...list, data]);
    });
  }, [socket]);

  return (
    <div className="chat-window">
      <div className="chat-header">
        <p>Live Chat</p>
      </div>
      <div className="chat-body">
        <ScrollToBottom className="message-container">
          {messageList.map((messageContent) => {
            return (
              <div
                className="message"
                id={username === messageContent.author ? "you" : "other"}
              >
                <div>
                  {_.get(messageContent, "message", null) !== null ? (
                    <div className="message-content">
                      <p>{messageContent.message}</p>
                    </div>
                  ) : (
                    <img
                      style={{
                        display: "block",
                        width: "100px",
                        height: "auto",
                      }}
                      src={messageContent.img}
                    />
                  )}
                  {/* <div className="message-content">
                    {messageContent.message !== null ? (
                      <p>{messageContent.message}</p>
                    ) : (
                      <img
                        style={{
                          display: "block",
                          width: "100px",
                          height: "auto",
                        }}
                        src={messageContent.img}
                      />
                    )} */}
                    {/* <p>{messageContent.message}</p> */}
                  {/* </div> */}
                  <div className="message-meta">
                    <p id="time">{messageContent.time}</p>
                    <p id="author">{messageContent.author}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </ScrollToBottom>
      </div>
      <div className="chat-footer">
        <input
          type="text"
          value={currentMessage}
          placeholder="Hey..."
          onChange={(event) => {
            setCurrentMessage(event.target.value);
          }}
          onKeyPress={(event) => {
            event.key === "Enter" && sendMessage();
          }}
        />
        <input
          type="file"
          ref={hiddenFileInput}
          onChange={handleChange}
          style={{display: 'none'}}
        />
        <button onClick={sendMessage}>&#9658;</button>
        <button onClick={handleClick}>&#x1F5BC;</button>
      </div>
    </div>
  );
}

export default Chat;
