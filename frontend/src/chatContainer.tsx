import {useEffect, useRef, useState} from 'react';
// @ts-ignore
import {BeatLoader} from 'react-spinners';
import CIS from './CIS.png';
import axios from "axios";
import ChatMessage from "./message";


// @ts-ignore
const ChatWindow = ({onClose}) => {
    const [inputValue, setInputValue] = useState('');
    const [start, setStart] = useState(true)
    const [messages, setMessages] = useState([{
        message: "I'm The Faculty of Computing and Information Sciences AI Assistant.\nHow Can I help you? 😊",
        isAI: true
    }]);
    const [isLoading, setLoading] = useState(false);

    if (start) {
        if (sessionStorage.getItem("chat")) {
            // @ts-ignore
            setMessages(JSON.parse(sessionStorage.getItem("chat")))
        }
        setStart(false)
    }

    async function sendQuery(query: string) {
        const data = {
            msg: query,
        }

        try {
            // @ts-ignore
            setMessages([...messages, {message: query}]);
            setLoading(true)

            const response = await axios.post(`http://localhost:2000/generate`, data);
            // @ts-ignore
            setMessages([...messages, {message: query}, {message: response.data, isAI: true}])
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
                <img className={"image-frame"} src={CIS}/>
                <p className={"title"}>CIS Chatbot</p>
                <p className={"subtitle"}>Computing and Information Sciences AI Assistant</p>
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
                {isLoading ? <BeatLoader color={'#4d79b6'}/> : <button onClick={() => {
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