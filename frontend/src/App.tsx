import {useState} from 'react';
import './App.css';
import ChatWindow from "./chatContainer";
import bot from './bot.svg';
import test from './test.png'
import Notification from './notify'


function App() {
    const [isOpen, setIsOpen] = useState(false);
    const [isNotified, setNotified] = useState(false)

    return (
        <>
            <img src={test} className="bg"/>
            {!sessionStorage.getItem("notified") && <Notification onClick={() => {
                sessionStorage.setItem("notified", "Notified")
                setNotified(true)
            }}/>}
            {!isOpen &&
                <button className="chat-button" onClick={() => {
                    sessionStorage.setItem("notified", "Notified")
                    setNotified(true)
                    setIsOpen(true)
                }}>
                    <img src={bot} alt="Button Icon" height={40}/>
                </button>
            }
            {isOpen && <ChatWindow onClose={() => setIsOpen(false)}/>}
        </>
    );
}

export default App;