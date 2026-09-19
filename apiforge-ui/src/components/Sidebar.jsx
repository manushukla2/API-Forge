import { BarChart3, Download, FileCheck2, Home, Laptop, LayoutDashboard, Lightbulb, ListChecks, Network, PlayCircle, Upload, Workflow, Braces, ChevronsUpDown } from 'lucide-react'

const NAV_QA = [
  { icon: Home, label: 'Home', route: 'home' },
  { icon: LayoutDashboard, label: 'Dashboard', route: 'qa_home' },
  { icon: Upload, label: 'Import API', route: 'doc_input' },
  { icon: Workflow, label: 'API Flow', route: 'flow' },
  { icon: PlayCircle, label: 'Run Tests', route: 'test_runner' },
  { icon: FileCheck2, label: 'Evidence', route: 'evidence' },
  { icon: BarChart3, label: 'Reports', route: 'reports' },
]

const NAV_DEV = [
  { icon: Laptop, label: 'Dev Dashboard', route: 'dev_home' },
  { icon: ListChecks, label: 'Requirements', route: 'requirements' },
  { icon: Lightbulb, label: 'Stack Advisor', route: 'stack' },
  { icon: Network, label: 'Architecture', route: 'architecture' },
  { icon: Download, label: 'Export', route: 'export' },
]

function NavItem({ icon: Icon, label, route, active, navigate }) {
  const isActive = active === route
  const base = { width:'100%', display:'flex', alignItems:'center', gap:'12px', padding:'10px 12px', borderRadius:'8px', fontSize:'14px', border:'none', cursor:'pointer', textAlign:'left', transition:'all 0.15s' }
  const activeStyle = { ...base, background:'var(--primary)', color:'white', fontWeight:'600' }
  const inactiveStyle = { ...base, background:'transparent', color:'var(--muted-foreground)', fontWeight:'400' }
  return (
    <button onClick={() => navigate(route)} style={isActive ? activeStyle : inactiveStyle}
      onMouseEnter={e => { if (!isActive) { e.currentTarget.style.background='var(--sidebar-accent)'; e.currentTarget.style.color='var(--foreground)' }}}
      onMouseLeave={e => { if (!isActive) { e.currentTarget.style.background='transparent'; e.currentTarget.style.color='var(--muted-foreground)' }}}>
      <Icon size={16} />{label}
    </button>
  )
}

export default function Sidebar({ active, navigate }) {
  return (
    <aside style={{ width:'248px', flexShrink:0, display:'flex', flexDirection:'column', height:'100vh', position:'sticky', top:0, background:'var(--sidebar)', borderRight:'1px solid var(--sidebar-border)', padding:'24px' }}>
      <div style={{ display:'flex', flexDirection:'column', gap:'32px', height:'100%' }}>

        <div style={{ display:'flex', alignItems:'center', gap:'8px' }}>
          <div style={{ width:'32px', height:'32px', borderRadius:'8px', background:'var(--primary)', display:'flex', alignItems:'center', justifyContent:'center' }}>
            <Braces size={16} color="white" />
          </div>
          <span style={{ fontWeight:'700', fontSize:'18px' }}>APIForge</span>
        </div>

        <div style={{ borderRadius:'8px', background:'var(--sidebar-accent)', border:'1px solid var(--sidebar-border)', padding:'10px 12px', display:'flex', alignItems:'center', justifyContent:'space-between', cursor:'pointer' }}>
          <div style={{ display:'flex', flexDirection:'column', gap:'2px' }}>
            <span style={{ color:'var(--muted-foreground)', fontSize:'11px' }}>Workspace</span>
            <span style={{ fontWeight:'600', fontSize:'14px' }}>QA Engineer</span>
          </div>
          <ChevronsUpDown size={16} color="var(--muted-foreground)" />
        </div>

        <nav style={{ display:'flex', flexDirection:'column', gap:'32px' }}>
          <div style={{ display:'flex', flexDirection:'column', gap:'8px' }}>
            <span style={{ color:'var(--muted-foreground)', fontSize:'11px', fontWeight:'600', letterSpacing:'1.5px', textTransform:'uppercase', padding:'0 12px' }}>QA</span>
            <div style={{ display:'flex', flexDirection:'column', gap:'2px' }}>
              {NAV_QA.map(item => <NavItem key={item.route} {...item} active={active} navigate={navigate} />)}
            </div>
          </div>
          <div style={{ display:'flex', flexDirection:'column', gap:'8px' }}>
            <span style={{ color:'var(--muted-foreground)', fontSize:'11px', fontWeight:'600', letterSpacing:'1.5px', textTransform:'uppercase', padding:'0 12px' }}>Developer</span>
            <div style={{ display:'flex', flexDirection:'column', gap:'2px' }}>
              {NAV_DEV.map(item => <NavItem key={item.route} {...item} active={active} navigate={navigate} />)}
            </div>
          </div>
        </nav>

        <div style={{ marginTop:'auto', paddingTop:'16px', borderTop:'1px solid var(--sidebar-border)', display:'flex', alignItems:'center', justifyContent:'space-between', fontSize:'12px', color:'var(--muted-foreground)' }}>
          <span>v0.1.0</span>
          <span style={{ display:'flex', alignItems:'center', gap:'6px' }}>
            <span style={{ width:'8px', height:'8px', borderRadius:'50%', background:'#34d399', display:'inline-block' }} />
            Pipeline ready
          </span>
        </div>

      </div>
    </aside>
  )
}