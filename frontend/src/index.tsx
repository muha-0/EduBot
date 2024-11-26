import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import {v4 as uuidv4} from "uuid";

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);

const sessionId = uuidv4();
sessionStorage.setItem('sessionID', sessionId);

root.render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>
);
