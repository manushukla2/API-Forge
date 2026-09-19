import { ArrowRight, ArrowUpRight, PlayCircle, Sparkles, Upload, FlaskConical, Code2 } from 'lucide-react'

export default function HomeScreen({ navigate }) {
  return (
    <div style={{ padding: '48px', display: 'flex', flexDirection: 'column', gap: '32px', maxWidth: '1440px' }}>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <h1 style={{ fontSize: '30px', fontWeight: '700', letterSpacing: '-0.5px', margin: 0 }}>Good morning</h1>
          <p style={{ color: 'var(--muted-foreground)', fontSize: '14px', margin: 0 }}>Choose a workspace to get started.</p>
        </div>
        <span style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '999px', padding: '4px 12px', fontSize: '12px', color: 'var(--muted-foreground)' }}>v0.1.0</span>
      </div>

      {/* Hero */}
      <div style={{ borderRadius: '16px', background: 'linear-gradient(120deg, rgba(124,58,237,0.22), rgba(29,78,216,0.16), #18181b)', border: '1px solid var(--border)', padding: '32px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxWidth: '600px' }}>
          <span style={{ fontSize: '11px', fontWeight: '700', letterSpacing: '3px', textTransform: 'uppercase', color: 'var(--primary)' }}>API QUALITY + GENERATION</span>
          <h2 style={{ fontSize: '36px', fontWeight: '700', letterSpacing: '-0.5px', margin: 0, lineHeight: 1.2 }}>Build better APIs.<br />Test with confidence.</h2>
          <p style={{ color: 'var(--muted-foreground)', fontSize: '15px', margin: 0 }}>From raw documentation to production-ready contracts and evidence.</p>
        </div>

        {/* Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          {[
            { icon: FlaskConical, title: 'QA Engineer', desc: 'Discover, test, and prove every endpoint.', btn: 'Open QA workspace', route: 'qa_home' },
            { icon: Code2, title: 'Developer Studio', desc: 'Turn requirements into a complete API foundation.', btn: 'Open Developer Studio', route: 'dev_home' },
          ].map(({ icon: Icon, title, desc, btn, route }) => (
            <div key={route} style={{ background: 'rgba(24,24,27,0.8)', border: '1px solid var(--border)', borderRadius: '12px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(124,58,237,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon size={24} color="var(--primary)" />
                </div>
                <ArrowUpRight size={18} color="var(--muted-foreground)" />
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <h3 style={{ fontSize: '20px', fontWeight: '700', margin: 0 }}>{title}</h3>
                <p style={{ color: 'var(--muted-foreground)', fontSize: '14px', margin: 0 }}>{desc}</p>
              </div>
              <button onClick={() => navigate(route)} style={{ background: 'var(--primary)', color: 'white', border: 'none', borderRadius: '8px', padding: '10px 16px', fontSize: '14px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                {btn} <ArrowRight size={16} />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px' }}>
        {[['7', 'Input Types'], ['5', 'AI Agents'], ['3', 'Export Formats'], ['∞', 'Test Scenarios']].map(([val, lbl]) => (
          <div key={lbl} style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <span style={{ fontSize: '30px', fontWeight: '700' }}>{val}</span>
            <span style={{ color: 'var(--muted-foreground)', fontSize: '14px' }}>{lbl}</span>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h2 style={{ fontSize: '16px', fontWeight: '700', margin: 0 }}>Recent activity</h2>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {[
            { icon: PlayCircle, name: 'Petstore API test run', time: '2 min ago', badge: 'Passed', badgeColor: '#34d399', badgeBg: 'rgba(52,211,153,0.15)' },
            { icon: Sparkles,   name: 'RAG service scaffold',  time: '1 hour ago', badge: 'Generated', badgeColor: 'var(--primary)', badgeBg: 'rgba(124,58,237,0.15)' },
            { icon: Upload,     name: 'Payments API import',   time: 'Yesterday',  badge: 'Ready', badgeColor: 'var(--muted-foreground)', badgeBg: 'var(--card)' },
          ].map(({ icon: Icon, name, time, badge, badgeColor, badgeBg }, i, arr) => (
            <div key={name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 0', borderBottom: i < arr.length - 1 ? '1px solid var(--border)' : 'none' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <div style={{ width: '36px', height: '36px', borderRadius: '8px', background: 'rgba(124,58,237,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon size={16} color="var(--primary)" />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                  <span style={{ fontSize: '14px', fontWeight: '500' }}>{name}</span>
                  <span style={{ fontSize: '12px', color: 'var(--muted-foreground)' }}>{time}</span>
                </div>
              </div>
              <span style={{ background: badgeBg, color: badgeColor, border: `1px solid ${badgeColor}33`, borderRadius: '6px', padding: '3px 10px', fontSize: '12px', fontWeight: '600' }}>{badge}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  )
}