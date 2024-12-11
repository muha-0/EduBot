import React from 'react';
import {marked} from 'marked'; // Import marked library

// @ts-ignore
const MarkdownViewer = ({markdownText}) => {
    const htmlContent = marked(markdownText);

    return (
        <div
            className="markdown-content"
            // @ts-ignore
            dangerouslySetInnerHTML={{__html: htmlContent}} // Set the HTML content
        />
    );
};


//@ts-ignore
const ChatMessage = ({message, isAI = false}) => {
    // Define base styles for both user and bot messages
    const baseStyles = {
        padding: '12px',
        borderRadius: '30px',
        boxShadow: '0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-start',
        maxWidth: '70%',
        marginBottom: '16px',
        color: "white"
    };

    const userStyles = {
        ...baseStyles,
        backgroundColor: '#e1b953', // Lighter material background
        alignSelf: 'flex-end',
        justifyContent: 'flex-start', // Text alignment to the left
        marginRight: '16px', // Margin for user messages
    };

    const botStyles = {
        ...baseStyles,
        backgroundColor: '#872539', // Slightly darker material background
        alignSelf: 'flex-start',
        justifyContent: 'flex-end', // Text alignment to the right
        marginLeft: '16px', // Margin for bot messages
    };

    const messageStyles = isAI ? botStyles : userStyles;

    return (
        <div style={messageStyles}>
            {message && <MarkdownViewer markdownText={message}/>}
        </div>
    );
};

export default ChatMessage;
