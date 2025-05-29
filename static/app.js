async function fetchEvents() {
    const response = await fetch('/list_events');
    const events = await response.json();
    const list = document.getElementById('events-list');
    list.innerHTML = '';
    events.forEach(event => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>Start:</strong> ${event.start}
            <strong>Stop:</strong> ${event.stop || ''}
            <strong>Tags:</strong> ${event.tags.join(', ')}
            <button onclick="deleteEvent('${event.tags[0]}')">Delete by tag</button>
        `;
        list.appendChild(li);
    });
}

async function addEvent(e) {
    e.preventDefault();
    const start = document.getElementById('start').value;
    const stop = document.getElementById('stop').value;
    const tags = document.getElementById('tags').value.split(',').map(t => t.trim()).filter(Boolean);
    await fetch('/add_event', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({start: Number(start), stop: stop ? Number(stop) : null, tags})
    });
    document.getElementById('event-form').reset();
    fetchEvents();
}

async function deleteEvent(tag) {
    await fetch(`/remove_events?tags=${tag}`, {method: 'DELETE'});
    fetchEvents();
}

document.getElementById('event-form').onsubmit = addEvent;
fetchEvents();
