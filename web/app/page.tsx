'use client';
import {useState} from 'react';
export default function Home(){
 const [text,setText]=useState('Feito com amor'),[shape,setShape]=useState('round'),[relief,setRelief]=useState('stamp_raised');
 const [width,setWidth]=useState(25),[depth,setDepth]=useState(1),[handle,setHandle]=useState('knob'),[border,setBorder]=useState(true);
 const [file,setFile]=useState<File|null>(null),[notice,setNotice]=useState(''),[busy,setBusy]=useState(false);
 async function generate(){
  setBusy(true);setNotice('');
  try{
   const fd=new FormData();
   fd.set('text',text);fd.set('shape',shape);fd.set('width_mm',String(width));fd.set('base_mm','3');fd.set('relief_mm',String(depth));fd.set('relief_mode',relief);fd.set('handle',handle);fd.set('border',String(border));if(file)fd.set('art',file);
   const api=process.env.NEXT_PUBLIC_GENERATOR_API_URL||'http://localhost:8000';
   const r=await fetch(api+'/generate',{method:'POST',body:fd});
   if(!r.ok){const j=await r.json().catch(()=>({}));throw new Error(j.detail||'Não foi possível gerar o STL. Verifique se o gerador está configurado.')}
   const url=URL.createObjectURL(await r.blob()),a=document.createElement('a');a.href=url;a.download='meu-carimbo-brigadeiro.stl';a.click();URL.revokeObjectURL(url);
   setNotice('Arquivo STL baixado. Abra no Cura ou OrcaSlicer e confira o modelo antes de imprimir.');
  }catch(e){setNotice(e instanceof Error?e.message:'Erro inesperado')}finally{setBusy(false)}
 }
 return <main><header><div><b className="logo">Carimbo<span>Lab 3D</span></b><small>Grátis · sem cadastro · sem cobrança</small></div></header>
 <section className="hero"><p className="eyebrow">CRIADOR DE CARIMBOS PERSONALIZADOS</p><h1>Crie seu carimbo para brigadeiro</h1><p>Personalize seu carimbo, gere o arquivo STL e baixe para impressão 3D. Sem login, sem senha e sem pagamento.</p></section>
 <div className="grid"><section className="card"><h2>Personalize seu carimbo</h2>
 <label>Nome ou frase<textarea value={text} maxLength={90} onChange={e=>setText(e.target.value)}/></label>
 <label>Enviar imagem (opcional)<input type="file" accept=".png,.jpg,.jpeg,.svg,.webp" onChange={e=>setFile(e.target.files?.[0]||null)}/><small>O envio de imagens ainda precisa da função de vetorização para virar parte do STL. Nesta versão, use texto para testar.</small></label>
 <label>Formato<select value={shape} onChange={e=>setShape(e.target.value)}><option value="round">Redondo</option><option value="oval">Oval</option><option value="square">Quadrado</option></select></label>
 <label>Tipo de marca<select value={relief} onChange={e=>setRelief(e.target.value)}><option value="stamp_raised">Marca afundada no doce (arte saliente no carimbo)</option><option value="stamp_recessed">Marca saltada no doce (arte cavada no carimbo)</option></select></label>
 <label>Largura: {width} mm<input type="range" min="15" max="45" value={width} onChange={e=>setWidth(+e.target.value)}/></label>
 <label>Profundidade: {depth.toFixed(1)} mm<input type="range" min="0.4" max="2.4" step="0.1" value={depth} onChange={e=>setDepth(+e.target.value)}/></label>
 <label>Cabo<select value={handle} onChange={e=>setHandle(e.target.value)}><option value="knob">Pegador redondo</option><option value="cylinder">Cabo alto</option><option value="flat">Sem cabo</option></select></label>
 <label className="check"><input type="checkbox" checked={border} onChange={e=>setBorder(e.target.checked)}/> Adicionar borda</label>
 <button disabled={busy} onClick={generate}>{busy?'Gerando…':'Gerar e baixar STL grátis'}</button>{notice&&<p className="notice">{notice}</p>}</section>
 <section className="card preview"><h2>Prévia da ideia</h2><div className="stamp"><div className="rim"><div className="art">{text||'Seu texto'}</div></div></div><p>O texto aparece espelhado no carimbo para sair legível no brigadeiro.</p><small>Prévia ilustrativa; ainda não é uma visualização 3D exata.</small></section></div>
 <footer>CarimboLab 3D · teste grátis e sem cadastro. Confira o STL no fatiador antes de imprimir.</footer></main>
}
