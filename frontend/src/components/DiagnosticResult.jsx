/**
 * DiagnosticResult — Renders structured diagnosis with safety banners.
 */
export default function DiagnosticResult({ text }) {
  if (!text) return null

  // Safety detection
  const isSafetyCritical =
    text.includes('PROFESSIONAL SERVICE REQUIRED') ||
    text.includes('🚨') ||
    text.includes('Critical Severity') ||
    text.includes('High Severity') ||
    text.includes('brakes') ||
    text.includes('steering') ||
    text.includes('airbag')

  // Split into sections based on emoji markers or headers
  const sections = []
  let currentHeader = ''
  let currentContent = []

  const lines = text.split('\n')

  lines.forEach((line) => {
    const trimmed = line.trim()
    if (!trimmed) return

    // Simple heuristic for headers based on common emojis or labels
    const headerMatch = trimmed.match(/^(🔍|📋|🔧|🧩|🛠️|⚠️|✅|🚨|📖|💰|⏱️)\s*(.*)/)
    const labelMatch = trimmed.match(/^([A-Z\s]+):$/)

    if (headerMatch || labelMatch) {
      if (currentContent.length > 0) {
        sections.push({ header: currentHeader, content: currentContent.join('\n') })
      }
      currentHeader = headerMatch ? headerMatch[0] : labelMatch[1]
      currentContent = []
    } else if (/^━+$/.test(trimmed) || /^={3,}$/.test(trimmed)) {
      // Skip separators
    } else {
      currentContent.push(line)
    }
  })

  // Add final section
  if (currentContent.length > 0 || currentHeader) {
    sections.push({ header: currentHeader, content: currentContent.join('\n') })
  }

  return (
    <div className="diag-result">
      {/* ── Safety Banner ── */}
      {isSafetyCritical && (
        <div className="safety-banner">
          <span className="safety-banner-icon">🚨</span>
          <div>
            <div style={{ fontSize: '0.85rem', textTransform: 'uppercase', marginBottom: '2px' }}>Safety Warning</div>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>
              This issue requires immediate professional attention. Do not attempt DIY repairs for safety-critical systems.
            </div>
          </div>
        </div>
      )}

      {/* ── Structured Sections ── */}
      {sections.length > 0 ? (
        sections.map((sec, idx) => (
          <div key={idx} className="diag-section">
            {sec.header && <div className="diag-label">{sec.header}</div>}
            <div className="diag-content" style={{ whiteSpace: 'pre-wrap' }}>
              {sec.content}
            </div>
          </div>
        ))
      ) : (
        <div className="diag-content" style={{ whiteSpace: 'pre-wrap' }}>{text}</div>
      )}
    </div>
  )
}
