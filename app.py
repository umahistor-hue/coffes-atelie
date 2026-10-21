from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile, subprocess, shutil, re, uuid

app = FastAPI(title="CarimboLab STL Generator — Teste grátis", version="0.2.0")
MAX_UPLOAD = 5 * 1024 * 1024
ALLOWED = {"image/png", "image/jpeg", "image/svg+xml", "image/webp"}

def clean_text(s: str) -> str:
    s = re.sub(r"[\x00-\x1f\x7f]", " ", s)
    return s.replace("\\", "\\\\").replace('"', '\\"')[:90]

def bounded(v: float, lo: float, hi: float, label: str) -> float:
    if not lo <= v <= hi:
        raise HTTPException(422, f"{label} deve ficar entre {lo} e {hi} mm")
    return float(v)

def run_scad(scad: Path, out: Path):
    exe = shutil.which("openscad")
    if not exe:
        raise HTTPException(503, "OpenSCAD não está instalado no servidor")
    try:
        p = subprocess.run([exe, "-o", str(out), str(scad)], capture_output=True, text=True, timeout=45)
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "Tempo limite ao gerar STL")
    if p.returncode != 0 or not out.exists() or out.stat().st_size < 100:
        raise HTTPException(422, "Falha ao gerar STL: " + (p.stderr[-500:] or p.stdout[-500:]))
    return out

@app.get("/health")
def health():
    return {"ok": True, "openscad_installed": bool(shutil.which("openscad"))}

@app.post("/generate")
async def generate(
    text: str = Form("Meu carimbo"),
    shape: str = Form("round"),
    width_mm: float = Form(25),
    base_mm: float = Form(3),
    relief_mm: float = Form(1),
    relief_mode: str = Form("stamp_raised"),
    handle: str = Form("knob"),
    border: bool = Form(True),
    art: UploadFile | None = File(None),
    authorization: str | None = Header(None),
):
    # Protótipo local: validar JWT e aplicar rate limit antes de expor publicamente.
    width = bounded(width_mm, 15, 45, "largura")
    base = bounded(base_mm, 2, 8, "base")
    relief = bounded(relief_mm, 0.4, 2.4, "relevo")
    if shape not in {"round", "oval", "square"}: raise HTTPException(422, "Formato inválido")
    if relief_mode not in {"stamp_raised", "stamp_recessed"}: raise HTTPException(422, "Relevo inválido")
    if handle not in {"knob", "flat", "cylinder"}: raise HTTPException(422, "Cabo inválido")
    if art and art.filename:
        if art.content_type not in ALLOWED: raise HTTPException(415, "Formato não permitido")
        data = await art.read()
        if len(data) > MAX_UPLOAD: raise HTTPException(413, "Imagem deve ter até 5 MB")
        raise HTTPException(501, "Upload recebido, mas a vetorização de PNG/JPG/SVG ainda não está ativada nesta versão de teste.")
    txt = clean_text(text)
    if shape == "round":
        base_expr = f"cylinder(h={base}, d={width}, $fn=96);"
    elif shape == "oval":
        base_expr = f"linear_extrude(height={base}) scale([1,0.72]) circle(d={width}, $fn=96);"
    else:
        base_expr = f"linear_extrude(height={base}) offset(r=2) square([{width-4},{width-4}], center=true);"
    # Espelhamento proposital na geometria exportada, não apenas na prévia.
    if relief_mode == "stamp_raised":
        art_expr = f'translate([0,0,{base}]) mirror([1,0,0]) linear_extrude(height={relief}) text("{txt}", size={max(3,width*0.105)}, halign="center", valign="center", font="Liberation Sans:style=Bold");'
        face = f"union() {{ BASE(); {art_expr} }}"
    else:
        art_expr = f'translate([0,0,{base-relief}]) mirror([1,0,0]) linear_extrude(height={relief+0.15}) text("{txt}", size={max(3,width*0.105)}, halign="center", valign="center", font="Liberation Sans:style=Bold");'
        face = f"difference() {{ BASE(); {art_expr} }}"
    grip = ""
    if handle != "flat":
        gd = width * (0.36 if handle == "knob" else 0.28)
        gh = max(10, width * 0.6)
        grip = f"translate([0,0,{base}]) cylinder(h={gh}, d1={gd}, d2={gd*0.82}, $fn=64);"
    rim = ""
    if border and shape == "round":
        rim = f"translate([0,0,{base}]) difference() {{ cylinder(h={relief},d={width*0.88},$fn=96); translate([0,0,-0.1]) cylinder(h={relief+0.2},d={width*0.82},$fn=96); }}"
    source = f"$fn=96; module BASE() {{ {base_expr} }} union() {{ {face} {grip} {rim} }}"
    with tempfile.TemporaryDirectory() as td:
        scad, out = Path(td)/"stamp.scad", Path(td)/"stamp.stl"
        scad.write_text(source, encoding="utf-8")
        run_scad(scad, out)
        return FileResponse(out, media_type="model/stl", filename=f"carimbo-teste-{uuid.uuid4().hex[:8]}.stl")
