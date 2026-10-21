# CarimboLab 3D — versão simples sem login

Esta versão remove cadastro, login, banco de dados e salvamento de projetos. A pessoa entra, configura o carimbo e tenta baixar o STL sem criar conta. Não existe checkout ou cobrança.

## O que ainda é necessário
- Publicar a interface Next.js e configurar `NEXT_PUBLIC_GENERATOR_API_URL` para apontar ao servidor gerador.
- Publicar o gerador FastAPI com OpenSCAD instalado.
- A vetorização de imagens PNG/JPG/SVG ainda não está implementada; por enquanto, use texto.
- A prévia é ilustrativa. Teste o STL no Cura/OrcaSlicer e valide uma impressão antes de uso real.
- Configure limites de uso e proteção contra abuso antes de abrir ao público.

## Rodar localmente
Veja as instruções abaixo e em `generator/`. O gerador deve estar ativo e acessível ao navegador; `localhost` só funciona quando o servidor está rodando no mesmo computador.

Este pacote ainda não é um site publicado.
