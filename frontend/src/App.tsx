import {useState} from 'react';
import './App.css';
import ChatWindow from "./chatContainer";
import bot from './assets/bot.svg';
import bg from './assets/bg.png'
import Notification from './notify'


function App() {
    const [isOpen, setIsOpen] = useState(false);
    const [isNotified, setNotified] = useState(false)

    return (
        <>
            <img src={bg} className="bg-image"/>
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