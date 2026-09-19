import { Upload, Plus, Search, MoreHorizontal, Layers3, CircleCheck, FileOutput } from 'lucide-react'
import { useState } from 'react'

const SESSIONS = [
  { name: 'Petstore API',         time: 'Today, 10:42 AM',    endpoints: 18, status: 'passed' },
  { name: 'Payments Gateway',     time: 'Yesterday, 4:18 PM', endpoints: 32, status: 'progress' },
  { name: 'User Identity Service',time: 'Mar 08, 2025',       endpoints: 11, status: 'passed' },
  { name: 'Inventory API',        time: 'Mar 06, 2025',       endpoints: 24, status: 'failed' },
]

const STATUS = {
  passed:   { color: '#34d399', bg: 'rgba(52,211,153,0.12)',  dot: '#34d399', label: 'Passed',      action: 'View' },
  progress: { color: '#fbbf24', bg: 'rgba(251,191,36,0.12)',  dot: '#fbbf24', label: 'In progress',  action: 'Open' },
  failed:   { color: '#f87171', bg: 'rgba(248,113,113,0.12)', dot: '#f87171', label: 'Failed',       action: 'Review' },
}

function StatCard({ label, value, sub, subColor, icon: Icon, iconColor, iconBg }) {
  return (
    <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <span style={{ color: 'var(--muted-foreground)', fontSize: '14px' }}>{label}</span>
          <span style={{ fontSize: '30px', fontWeight: '700' }}>{value}</span>
        </div>
        <div style={{ background: iconBg, borderRadius: '8px', padding: '8px' }}>
          <Icon size={20} color={iconColor} />
        </div>
      </div>
      <span style={{ fontSize: '14px', color: subColor || 'var(--muted-foreground)' }}>{sub}</span>
    </div>
  )
}

export default function QADashboard({ navigate }) {
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('all')

  const filtered = SESSIONS.filter(s => {
    const matchSearch = s.name.toLowerCase().includes(search.toLowerCase())
    const matchFilter = filter === 'all' || s.status === filter
    return matchSearch && matchFilter
  })

  return (
    <div style={{ padding: '48px', display: 'flex', flexDirection: 'column', gap: '32px', maxWidth: '1440px' }}>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <h1 style={{ fontSize: '28px', fontWeight: '700', letterSpacing: '-0.5px', margin: 0 }}>QA Dashboard</h1>
          <p style={{ color: 'var(--muted-foreground)', fontSize: '14px', margin: 0 }}>Monitor your API testing workspace.</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button onClick={() => navigate('doc_input')} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '9px 16px', background: 'transparent', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--foreground)', fontSize: '14px', fontWeight: '500', cursor: 'pointer' }}>
            <Upload size={16} /> Import API
          </button>
          <button onClick={() => navigate('doc_input')} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '9px 16px', background: 'var(--primary)', border: 'none', borderRadius: '8px', color: 'white', fontSize: '14px', fontWeight: '600', cursor: 'pointer' }}>
            <Plus size={16} /> New test session
          </button>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px' }}>
        <StatCard label="Total sessions" value="24" sub="+12%  this month" subColor="#34d399" icon={Layers3} iconColor="var(--primary)" iconBg="rgba(124,58,237,0.15)" />
        <StatCard label="Completed" value="18" sub="75% completion rate" icon={CircleCheck} iconColor="#34d399" iconBg="rgba(52,211,153,0.15)" />
        <StatCard label="Export formats" value="3" sub="HTML, JSON, PDF" icon={FileOutput} iconColor="#fbbf24" iconBg="rgba(251,191,36,0.15)" />
      </div>

      {/* Sessions Table */}
      <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ fontSize: '16px', fontWeight: '700', margin: 0 }}>Recent sessions</h2>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <div style={{ position: 'relative' }}>
              <Search size={14} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--muted-foreground)' }} />
              <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search sessions..." style={{ paddingLeft: '32px', paddingRight: '12px', height: '36px', background: 'var(--background)', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--foreground)', fontSize: '14px', width: '220px', outline: 'none' }} />
            </div>
            <select value={filter} onChange={e => setFilter(e.target.value)} style={{ height: '36px', padding: '0 12px', background: 'var(--background)', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--foreground)', fontSize: '14px', cursor: 'pointer', outline: 'none' }}>
              <option value="all">All statuses</option>
              <option value="passed">Passed</option>
              <option value="progress">In progress</option>
              <option value="failed">Failed</option>
            </select>
          </div>
        </div>

        {/* Table Header */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1.4fr 0.8fr 1fr 0.6fr', padding: '10px 16px', borderBottom: '1px solid var(--border)', color: 'var(--muted-foreground)', fontSize: '12px', fontWeight: '600', letterSpacing: '0.8px', textTransform: 'uppercase' }}>
          <span>API Name</span><span>Last Run</span><span>Endpoints</span><span>Status</span><span>Actions</span>
        </div>

        {/* Rows */}
        {filtered.map((s, i) => {
          const st = STATUS[s.status]
          return (
            <div key={i} style={{ display: 'grid', gridTemplateColumns: '2fr 1.4fr 0.8fr 1fr 0.6fr', padding: '16px', borderBottom: i < filtered.length - 1 ? '1px solid var(--border)' : 'none', alignItems: 'center', fontSize: '14px' }}>
              <span style={{ fontWeight: '500' }}>{s.name}</span>
              <span style={{ color: 'var(--muted-foreground)' }}>{s.time}</span>
              <span>{s.endpoints}</span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: st.color }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: st.dot, display: 'inline-block' }} />
                {st.label}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <button onClick={() => navigate('evidence')} style={{ background: 'none', border: 'none', color: 'var(--primary)', fontSize: '14px', cursor: 'pointer', padding: 0, fontWeight: '500' }}>{st.action}</button>
                <MoreHorizontal size={16} color="var(--muted-foreground)" style={{ cursor: 'pointer' }} />
              </span>
            </div>
          )
        })}
      </div>

      {/* Pipeline Health */}
      <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h2 style={{ fontSize: '16px', fontWeight: '700', margin: 0 }}>Pipeline health</h2>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
          <span style={{ fontWeight: '600' }}>86%</span>
          <span style={{ color: 'var(--muted-foreground)' }}>Overall pipeline health</span>
        </div>
        <div style={{ background: 'var(--border)', borderRadius: '999px', height: '8px', overflow: 'hidden' }}>
          <div style={{ background: 'var(--primary)', width: '86%', height: '100%', borderRadius: '999px' }} />
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', fontSize: '13px', color: 'var(--muted-foreground)' }}>
          <span>Import</span><span style={{ textAlign: 'center' }}>Discover</span><span style={{ textAlign: 'center' }}>Test</span><span style={{ textAlign: 'right' }}>Evidence</span>
        </div>
      </div>

    </div>
  )
}