// App.js
import React, { useEffect, useState } from 'react';

function App() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchInbox = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/inbox');
      const data = await res.json();
      setEmails(data);
    } catch (err) {
      console.error("Failed to fetch inbox", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInbox();
  }, []);

  const urgencyColor = (urgency) => {
    switch (urgency) {
      case 'High': return 'red';
      case 'Medium': return 'orange';
      default: return 'gray';
    }
  };

  return (
    <div style={{ maxWidth: '700px', margin: '30px auto', fontFamily: 'Arial' }}>
      <h2>📧 Inbox Zero AI Assistant</h2>
      {loading ? (
        <p>Loading inbox...</p>
      ) : (
        emails.map(email => (
          <div key={email.id} style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '15px', borderRadius: '5px' }}>
            <h3>{email.subject}</h3>
            <p><strong>From:</strong> {email.from}</p>
            <p><strong>Summary:</strong> {email.summary}</p>
            <p><strong>Action:</strong> {email.action}</p>
            <span style={{ color: urgencyColor(email.urgency), fontWeight: 'bold' }}>
              Urgency: {email.urgency}
            </span>
          </div>
        ))
      )}
    </div>
  );
}

export default App;
