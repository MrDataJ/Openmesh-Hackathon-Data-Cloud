import React, { useState, useEffect } from 'react';

const DataDisplay = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        // Implement WebSocket connection and set data
        const ws = new WebSocket('ws://localhost:6789');
        ws.onmessage = (event) => {
            setData(JSON.parse(event.data));
        };

        return () => {
            ws.close();
        };
    }, []);

    return (
        <div>
            <h1>Real-time Data</h1>
            {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>Loading...</p>}
        </div>
    );
};

export default DataDisplay;
