import type { Metadata } from 'next';
import './style.css';
export const metadata: Metadata={title:'CarimboLab 3D — Teste grátis',description:'Teste a criação de carimbos personalizados para brigadeiros.'};
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="pt-BR"><body>{children}</body></html>; }
