import {useEffect, useState} from 'react';
import './App.css';
import ChatWindow from "./chatContainer";
import bot from './assets/bot.svg';
import bg from './assets/bg.png'
import Notification from './notify'


function App() {
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const handleBeforeUnload = () => {
            const url = 'http://localhost:2000/delete-user';
            // @ts-ignore
            const data = {user_id: sessionStorage.getItem('sessionID')};
            navigator.sendBeacon(url, JSON.stringify(data));
        };

        // Attach event listener to beforeunload
        window.addEventListener('beforeunload', handleBeforeUnload);

        // Cleanup on component unmount
        return () => {
            window.removeEventListener('beforeunload', handleBeforeUnload);
        };
    }, []);

    return (
        <>
            <img src={bg} className="bg-image"/>
            {!sessionStorage.getItem("notified") && <Notification onClick={() => {
                sessionStorage.setItem("notified", "Notified")
            }}/>}
            {!isOpen &&
                <button className="chat-button" onClick={() => {
                    sessionStorage.setItem("notified", "Notified")
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