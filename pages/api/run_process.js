// pages/api/run_process.js
export default async function handler(req, res) {
    try {
        const flaskResponse = await fetch('http://localhost:5000/run_process');
        const data = await flaskResponse.json();
        res.status(200).json(data);
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}
