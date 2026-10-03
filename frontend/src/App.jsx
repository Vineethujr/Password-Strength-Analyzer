import { useEffect, useMemo, useState } from 'react'

const labels = ['VERY WEAK', 'WEAK', 'MODERATE', 'STRONG', 'VERY STRONG']
const demoValues = [
  ['Very weak', '123456'],
  ['Weak', 'Password123!'],
  ['Weak', 'aaaaaaaaaaaaaaaa'],
  ['Weak', 'qwerty2026!'],
]

function classificationClass(value = '') {
  return value.toLowerCase().replaceAll(' ', '-')
}

function App() {
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [context, setContext] = useState({ first_name: '', birth_year: '', company_or_college: '' })
  const [result, setResult] = useState(null)
  const [tab, setTab] = useState('analyzer')
  const [generated, setGenerated] = useState('')
  const [generatorMode, setGeneratorMode] = useState('complex')
  const [generatorLength, setGeneratorLength] = useState(20)
  const [remoteBreach, setRemoteBreach] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [dashboard, setDashboard] = useState(null)

  const barWidth = useMemo(() => `${result ? Math.max(0, result.score) : 0}%`, [result])

  useEffect(() => {
    const timer = setTimeout(async () => {
      if (!password) {
        setResult(null)
        setError('')
        return
      }
      setLoading(true)
      try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ password, context, check_local_breach: true })
        })
        const json = await response.json()
        if (!response.ok) throw new Error(json.detail || 'Analysis failed')
        setResult(json)
        setError('')
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }, 250)
    return () => clearTimeout(timer)
  }, [password, context])

  async function generate() {
    setError('')
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: generatorMode, length: generatorLength })
      })
      const json = await response.json()
      if (!response.ok) throw new Error(json.detail || 'Generation failed')
      setGenerated(json.password)
      setRemoteBreach(null)
    } catch (e) {
      setError(e.message)
    }
  }

  async function copyGenerated() {
    if (generated && navigator.clipboard) await navigator.clipboard.writeText(generated)
  }

  async function checkRemoteBreach() {
    setRemoteBreach(null)
    try {
      const response = await fetch('/api/breach-check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      })
      const json = await response.json()
      if (!response.ok) throw new Error(json.detail || 'Remote check unavailable')
      setRemoteBreach(json)
    } catch (e) {
      setRemoteBreach({ checked: false, compromised: false, error: e.message })
    }
  }

  async function loadDashboard() {
    try {
      const response = await fetch('/api/dashboard/stats')
      setDashboard(await response.json())
    } catch (e) {
      setError('Could not load dashboard.')
    }
  }

  function selectDemo(value) {
    setPassword(value)
    setTab('analyzer')
  }

  return (
    <div className="page">
      <header className="hero">
        <div>
          <div className="eyebrow">DEFENSIVE CYBERSECURITY PROJECT</div>
          <h1>Password Security Lab</h1>
          <p>Analyze password length, predictability and patterns locally, then turn findings into actionable security guidance.</p>
        </div>
        <div className="privacy-badge">🔒 No plaintext password storage</div>
      </header>

      <nav className="tabs">
        <button className={tab === 'analyzer' ? 'active' : ''} onClick={() => setTab('analyzer')}>Analyzer</button>
        <button className={tab === 'generator' ? 'active' : ''} onClick={() => setTab('generator')}>Generator</button>
        <button className={tab === 'education' ? 'active' : ''} onClick={() => setTab('education')}>Education</button>
        <button className={tab === 'dashboard' ? 'active' : ''} onClick={() => { setTab('dashboard'); loadDashboard() }}>Dashboard</button>
      </nav>

      {error && <div className="error">{error}</div>}

      {tab === 'analyzer' && (
        <main className="grid">
          <section className="card input-card">
            <h2>Live Analyzer</h2>
            <label>Optional demo context</label>
            <div className="three-col">
              <input aria-label="Demo first name" placeholder="First name" value={context.first_name} onChange={e => setContext({ ...context, first_name: e.target.value })} />
              <input aria-label="Demo birth year" placeholder="Birth year" inputMode="numeric" maxLength="4" value={context.birth_year} onChange={e => setContext({ ...context, birth_year: e.target.value })} />
              <input aria-label="Demo company or college" placeholder="Company / college" value={context.company_or_college} onChange={e => setContext({ ...context, company_or_college: e.target.value })} />
            </div>
            <label>Password</label>
            <div className="password-wrap">
              <input
                aria-label="Password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="new-password"
                spellCheck="false"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="Type a synthetic demo password…"
              />
              <button className="ghost" onClick={() => setShowPassword(!showPassword)}>{showPassword ? '🙈 Hide' : '👁 Show'}</button>
            </div>
            <p className="muted">The field is processed for analysis only. This demo does not use localStorage or sessionStorage for passwords.</p>

            <div className="demo-row">
              {demoValues.map(([name, value]) => <button key={value} className="demo-btn" onClick={() => selectDemo(value)}>{name}</button>)}
            </div>
          </section>

          <section className="card result-card">
            <div className="result-head">
              <div>
                <div className="muted">Strength</div>
                <h2 className={classificationClass(result?.classification)}>{result?.classification || '—'}</h2>
              </div>
              <div className="score">{result?.score ?? 0}<span>/100</span></div>
            </div>
            <div className="meter"><div style={{ width: barWidth }} /></div>
            {loading && <div className="muted">Analyzing locally…</div>}
            {result && <>
              <div className="stat-grid">
                <div><span>Length</span><b>{result.metrics.length}</b><small>{result.metrics.length_band}</small></div>
                <div><span>Unique ratio</span><b>{Math.round(result.metrics.unique_character_ratio * 100)}%</b><small>{result.metrics.unique_character_count} unique</small></div>
                <div><span>Entropy-style</span><b>{result.metrics.theoretical_entropy_bits}</b><small>bits, illustrative</small></div>
                <div><span>Weaknesses</span><b>{result.findings.length}</b><small>detected signals</small></div>
              </div>

              <h3>Findings</h3>
              {result.findings.length === 0 ? <div className="good">✓ No tracked weakness signals detected.</div> : <div className="findings">{result.findings.map((f, i) => <div className={`finding ${f.severity}`} key={i}><span>⚠</span><div><b>{f.type.replaceAll('_', ' ')}</b><p>{f.description}</p></div></div>)}</div>}

              <h3>Security Suggestions</h3>
              <ul className="suggestions">{result.suggestions.map((s, i) => <li key={i}>💡 {s}</li>)}</ul>

              <div className="policy-box"><div><b>{result.policy.passed ? 'POLICY PASS' : 'POLICY REVIEW'}</b><span>{result.policy.note}</span></div><button className="secondary" onClick={checkRemoteBreach}>Run privacy-preserving online breach check</button></div>
              {remoteBreach && <div className="remote-result">{remoteBreach.compromised ? `⚠ Found ${remoteBreach.exposure_count} time(s) in the remote breach corpus.` : '✓ No match found in the remote breach corpus.'}<small>Only a 5-character SHA-1 hash prefix is sent for this explicit check.</small></div>}
            </>}
          </section>
        </main>
      )}

      {tab === 'generator' && (
        <main className="grid single">
          <section className="card">
            <h2>Secure Password Generator</h2>
            <p className="muted">Uses Python <code>secrets</code> on the backend. Generated values are not stored.</p>
            <div className="form-row">
              <label>Mode<select value={generatorMode} onChange={e => setGeneratorMode(e.target.value)}><option value="complex">Random characters</option><option value="passphrase">Random-word passphrase</option></select></label>
              <label>Length<select value={generatorLength} onChange={e => setGeneratorLength(Number(e.target.value))}><option value="16">16</option><option value="20">20</option><option value="24">24</option></select></label>
            </div>
            <button className="primary" onClick={generate}>Generate</button>
            {generated && <div className="generated"><code>{generated}</code><div><button className="secondary" onClick={copyGenerated}>Copy</button><button className="secondary" onClick={() => { setPassword(generated); setTab('analyzer') }}>Use in Analyzer</button></div></div>}
            <div className="info"><b>Passphrase guidance</b><p>Long passphrases made from independently random words can be easier to remember. Do not reuse any example or generated value from screenshots.</p></div>
          </section>
        </main>
      )}

      {tab === 'education' && (
        <main className="grid two">
          <section className="card">
            <h2>Password vs. Passphrase</h2>
            <p><b>Password:</b> a secret string used for authentication.</p>
            <p><b>Passphrase:</b> a longer secret composed of multiple words. Random word selection can help make length practical without relying on forced symbol substitutions.</p>
            <div className="callout">Do not copy famous quotations or the examples shown in this app.</div>
          </section>
          <section className="card">
            <h2>10 Password Security Rules</h2>
            <ol className="rules">
              <li>Use a unique password for each important account.</li>
              <li>Prefer longer passwords or random-word passphrases.</li>
              <li>Avoid names, dates, company/college terms and other predictable context.</li>
              <li>Avoid common or previously compromised passwords.</li>
              <li>Do not reuse passwords across services.</li>
              <li>Use a password manager.</li>
              <li>Enable MFA where available.</li>
              <li>Never share passwords with other people.</li>
              <li>Be cautious of phishing and fake login pages.</li>
              <li>Change a password when compromise is suspected or confirmed.</li>
            </ol>
          </section>
          <section className="card wide">
            <h2>Why entropy is only one signal</h2>
            <p>The simplified estimate is <code>L × log2(N)</code>, where <code>L</code> is length and <code>N</code> is an assumed character pool. It is useful for teaching the concept of search-space size, but human-created passwords usually do not behave like independent random characters. This project therefore combines the estimate with blocklists, pattern detection, length, and context.</p>
            <div className="callout">Password strength cannot be perfectly determined by one formula.</div>
          </section>
          <section className="card wide">
            <h2>Real-world login security</h2>
            <p>Password strength is only one layer. Real systems also need secure password hashing, MFA, rate limiting, abuse detection, session security, phishing resistance, secure recovery, and monitoring. Passwords themselves are not phishing-resistant.</p>
          </section>
        </main>
      )}

      {tab === 'dashboard' && (
        <main className="grid two">
          {!dashboard ? <section className="card"><h2>Dashboard</h2><p className="muted">Loading aggregate metadata…</p></section> : <>
            <section className="card dashboard-main">
              <h2>Aggregate Demo Dashboard</h2>
              <div className="stat-grid">
                <div><span>Total analyses</span><b>{dashboard.total_analyses}</b></div>
                <div><span>Average score</span><b>{dashboard.average_score}</b></div>
                <div><span>Very weak</span><b>{dashboard.strength_distribution['VERY WEAK']}</b></div>
                <div><span>Very strong</span><b>{dashboard.strength_distribution['VERY STRONG']}</b></div>
              </div>
              <h3>Strength distribution</h3>
              <div className="bars">{labels.map(label => <div className="bar-row" key={label}><span>{label}</span><div><i style={{ width: `${Math.min(100, dashboard.strength_distribution[label] * 12)}%` }} /></div><b>{dashboard.strength_distribution[label]}</b></div>)}</div>
              <h3>Weakness frequency</h3>
              <div className="bars">{dashboard.weakness_frequency.slice(0, 8).map(item => <div className="bar-row" key={item.type}><span>{item.type.replaceAll('_', ' ')}</span><div><i style={{ width: `${Math.min(100, item.count * 12)}%` }} /></div><b>{item.count}</b></div>)}</div>
            </section>
            <section className="card">
              <h2>Safe Local History</h2>
              <p className="muted">Only metadata is shown; the password itself is never stored.</p>
              <div className="history">{dashboard.recent_history.map(row => <div className="history-row" key={row.analysis_id}><b>{row.classification}</b><span>{row.score}/100</span><span>len {row.password_length}</span><span>{row.weakness_count} findings</span></div>)}</div>
            </section>
          </>}
        </main>
      )}

      <footer>Educational defensive-security project • No credential harvesting • No cracking • No password persistence</footer>
    </div>
  )
}

export default App
