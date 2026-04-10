import { useEffect, useMemo, useState } from 'react';
import api from '../api';

const baseButtons = [
  ['toggle-angle', 'Deg/Rad'],
  ['toggle-inv', 'Inv'],
  ['x!', 'x!'],
  ['(', '('],
  [')', ')'],
  ['%', '%'],
  ['AC', 'AC'],
  ['sin', 'sin'],
  ['ln', 'ln'],
  ['7', '7'],
  ['8', '8'],
  ['9', '9'],
  ['÷', '÷'],
  ['π', 'π'],
  ['cos', 'cos'],
  ['log', 'log'],
  ['4', '4'],
  ['5', '5'],
  ['6', '6'],
  ['×', '×'],
  ['e', 'e'],
  ['tan', 'tan'],
  ['√', '√'],
  ['1', '1'],
  ['2', '2'],
  ['3', '3'],
  ['-', '-'],
  ['Ans', 'Ans'],
  ['EXP', 'EXP'],
  ['^', 'xʸ'],
  ['0', '0'],
  ['.', '.'],
  ['=', '='],
  ['+', '+'],
];

function getDisplayLabel(value, invEnabled) {
  if (!invEnabled) return value;
  if (value === 'sin') return 'sin⁻¹';
  if (value === 'cos') return 'cos⁻¹';
  if (value === 'tan') return 'tan⁻¹';
  return value;
}

export default function Calculator({ expression, setExpression, onHistoryRefresh }) {
  const [display, setDisplay] = useState(expression || '0');
  const [angleMode, setAngleMode] = useState('DEG');
  const [invEnabled, setInvEnabled] = useState(false);
  const [ans, setAns] = useState('0');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const buttons = useMemo(() => baseButtons, []);

  const appendToken = (token) => {
    setDisplay((prev) => {
      const next = prev === '0' ? token : prev + token;
      setExpression?.(next);
      return next;
    });
  };

  useEffect(() => {
    if (expression !== undefined && expression !== display) {
      setDisplay(expression || '0');
    }
  }, [expression, display]);

  const handleButton = async (value) => {
    setError('');

    if (value === 'toggle-angle') {
      setAngleMode((prev) => (prev === 'DEG' ? 'RAD' : 'DEG'));
      return;
    }

    if (value === 'toggle-inv') {
      setInvEnabled((prev) => !prev);
      return;
    }

    if (value === 'AC') {
      setDisplay('0');
      setExpression?.('0');
      return;
    }

    if (value === '=') {
      setLoading(true);
      try {
        const response = await api.post('/calculator/evaluate', {
          expression: display,
          angle_mode: angleMode,
          ans,
          save_history: true,
        });
        setDisplay(response.data.result);
        setExpression?.(response.data.result);
        setAns(response.data.result);
        await onHistoryRefresh();
      } catch (err) {
        setError(err?.response?.data?.message || 'Unable to evaluate expression.');
      } finally {
        setLoading(false);
      }
      return;
    }

    if (value === 'x!') {
      appendToken('!');
      return;
    }

    if (value === '%') {
      appendToken('/100');
      return;
    }

    if (['sin', 'cos', 'tan'].includes(value)) {
      const fn = invEnabled ? `a${value}` : value;
      appendToken(`${fn}(`);
      return;
    }

    if (value === 'ln' || value === 'log') {
      appendToken(`${value}(`);
      return;
    }

    if (value === '√') {
      appendToken('√(');
      return;
    }

    if (value === '^') {
      appendToken('^');
      return;
    }

    if (value === 'EXP') {
      appendToken('EXP');
      return;
    }

    appendToken(value);
  };

  const backspace = () => {
    setDisplay((prev) => {
      if (prev.length <= 1) {
        setExpression?.('0');
        return '0';
      }
      const next = prev.slice(0, -1);
      setExpression?.(next);
      return next;
    });
  };

  return (
    <div className="calculator-card">
      <div className="calculator-display">
        <div className="display-meta">
          <span>{angleMode}</span>
          <button type="button" className="ghost-btn" onClick={backspace}>⌫</button>
        </div>
        <div className="display-value">{display}</div>
        <div className="display-subtext">Ans: {ans}</div>
      </div>

      {error && <p className="error-text calc-error">{error}</p>}

      <div className="calculator-grid">
        {buttons.map(([value, label]) => (
          <button
            key={`${value}-${label}`}
            type="button"
            className={`calc-btn ${value === '=' ? 'equal-btn' : ''}`}
            onClick={() => handleButton(value)}
            disabled={loading}
          >
            {label === 'Deg/Rad' ? angleMode : getDisplayLabel(label, invEnabled)}
          </button>
        ))}
      </div>
    </div>
  );
}
