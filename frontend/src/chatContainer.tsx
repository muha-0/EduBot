import {useEffect, useRef, useState} from 'react';
// @ts-ignore
import {BeatLoader} from 'react-spinners';
import umn from './assets/umn.png';
import axios from "axios";
import ChatMessage from "./message";

// @ts-ignore
const ChatWindow = ({onClose}) => {
    const [inputValue, setInputValue] = useState('');
    const [messages, setMessages] = useState([{
        message: "I'm The Educational AI Assistant.\nHow Can I help you? 😊",
        isAI: true
    }]);
    const [isLoading, setLoading] = useState(false);

    async function sendQuery(query: string) {
        const data = {
            message: query,
            user_id: sessionStorage.getItem('sessionID')
        }

        try {
            // @ts-ignore
            setMessages([...messages, {message: query}]);
            setLoading(true)

            await axios.post(`http://localhost:2000/generate`, data)
                .then(
                    (response) => {
                        // @ts-ignore
                        setMessages([...messages, {message: query}, {message: response.data, isAI: true}])
                    }
                );
            // @ts-ignore
            setLoading(false)

        } catch (error) {
            return new Promise((resolve) => {
                setTimeout(() => {
                    resolve(sendQuery(query)); // Recursive call with incremented attempt
                }, 10000); // Exponential backoff (optional)
            });
        }

    }

    const messageRef = useRef(null);
    useEffect(() => {
        // @ts-ignore
        messageRef.current.scrollTo({
            // @ts-ignore
            top: messageRef.current.scrollHeight,
            behavior: 'smooth', // Add smooth scrolling for better UX
        });
    }, [messages]);


    useEffect(() => {
        sessionStorage.setItem("chat", JSON.stringify(messages))
    }, [messages]);

    return (
        <div className="chat-window">
            <div className="chat-window-head">
                <img className={"image-frame"} src={umn}/>
                <p className={"title"}>EduBot</p>
                <p className={"subtitle"}>Educational AI Assistant</p>
                <button className="close-button" onClick={onClose}>X</button>
            </div>
            <div ref={messageRef} className="chat-container">
                {messages.map((message) => (
                    // @ts-ignore
                    <ChatMessage key={message.message} message={message.message} isAI={message.isAI}/>
                ))}
            </div>

            <div className="input-container">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={
                        (evt) => {
                            // @ts-ignore
                            if (evt.key === 'Enter' && inputValue !== '' && !isLoading) { // Check for Enter key and non-empty input
                                // @ts-ignore
                                sendQuery(inputValue)
                                setInputValue(''); // Clear input after Enter press
                            }
                        }
                    }
                />
                {isLoading ? <BeatLoader color={'#872539'}/> : <button onClick={() => {
                    if (inputValue !== '') {
                        // @ts-ignore
                        sendQuery(inputValue)
                        setInputValue('')
                    }
                }}> Send </button>}
            </div>
        </div>
    );
};

export default ChatWindow;