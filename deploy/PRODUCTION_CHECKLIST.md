# Checklist de publicação — versão sem login

- [ ] Publicar `web/` em um serviço de hospedagem compatível com Next.js.
- [ ] Publicar `generator/` em um servidor com OpenSCAD instalado.
- [ ] Definir `NEXT_PUBLIC_GENERATOR_API_URL` com a URL HTTPS do gerador.
- [ ] Configurar CORS para aceitar apenas o domínio do site.
- [ ] Adicionar limite de tamanho de arquivos e rate limiting antes de liberar publicamente.
- [ ] Implementar vetorização de imagens; atualmente upload de imagem não é convertido em geometria.
- [ ] Testar o STL no fatiador e conferir espelhamento, dimensões e integridade da malha.
