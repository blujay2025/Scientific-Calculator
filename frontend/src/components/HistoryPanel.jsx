export default function HistoryPanel({ items, onReuse, onClear, onDelete }) {
  return (
    <aside className="history-panel">
      <div className="history-header">
        <h2>History</h2>
        <button type="button" className="ghost-btn" onClick={onClear}>Clear</button>
      </div>
      <div className="history-list">
        {items.length === 0 ? (
          <p className="muted">Your saved calculations will appear here.</p>
        ) : (
          items.map((item) => (
            <div className="history-item" key={item.id}>
              <button type="button" className="history-main" onClick={() => onReuse(item)}>
                <span>{item.expression}</span>
                <strong>= {item.result}</strong>
                <small>{item.angle_mode}</small>
              </button>
              <button type="button" className="history-delete" onClick={() => onDelete(item.id)}>✕</button>
            </div>
          ))
        )}
      </div>
    </aside>
  );
}
