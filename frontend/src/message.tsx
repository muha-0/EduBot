import React from 'react';

// @ts-ignore
function parseTextForLinks(text: String) {
    const urlRegex = /https?:\/\/[^\s]+/g; // Matches URLs with optional protocol
    const textSegments = [];

    let lastIndex = 0;

    const matches = text.toString().matchAll(urlRegex)
    for (const match of matches) {
        const urlStart = match.index;
        // @ts-ignore
        const urlEnd = urlStart + match[0].length;

        // Add text segment before the URL
        // @ts-ignore
        if (urlStart > lastIndex) {
            textSegments.push(text.slice(lastIndex, urlStart));
        }

        // Add the URL as a link
        textSegments.push(<a className={"link"} href={match[0]}>{match[0]}</a>);

        lastIndex = urlEnd;
    }

    // Add any remaining text after the last URL
    if (lastIndex < text.length) {
        textSegments.push(text.slice(lastIndex));
    }

    return textSegments;
}

//@ts-ignore
const TextWithLinks = ({text}) => {
    const textSegments = parseTextForLinks(text);

    return (
        <div>
            {textSegments.map((segment) => (
                typeof segment === 'string' ? (
                    <span key={segment}>{segment.split('\n').map((item: any) => (<>{item}<br/></>))}</span>
                ) : (
                    segment
                )
            ))}
        </div>
    );
};

//@ts-ignore
const ChatMessage = ({message, isAI = false}) => {
    // Define base styles for both user and bot messages
    const baseStyles = {
        padding: '20px',
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
            {<TextWithLinks text={message}/>}
        </div>
    );
};

export default ChatMessage;
