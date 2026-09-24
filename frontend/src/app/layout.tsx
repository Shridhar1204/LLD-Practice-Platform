import './globals.css';
import Link from 'next/link';
export default function RootLayout({children}:{children:React.ReactNode}){return <><header className="nav"><div className="navin"><Link className="brand" href="/">DesignLoop</Link><nav className="navlinks"><Link href="/">Problems</Link><Link href="/attempts">Attempts</Link></nav></div></header>{children}</>}
