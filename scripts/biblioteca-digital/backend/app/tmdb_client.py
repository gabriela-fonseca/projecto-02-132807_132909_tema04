import os
import httpx
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG = "https://image.tmdb.org/t/p/w342"
LANG = "pt-PT"

GENEROS_MAP = {
    28: "action", 12: "action", 35: "comedy", 80: "thriller",
    18: "drama", 27: "horror", 878: "scifi", 53: "thriller",
    9648: "thriller", 10749: "drama", 10752: "action",
}


async def pesquisar_filmes(titulo: str) -> list[dict]:
    if not TMDB_KEY:
        return []
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{TMDB_BASE}/search/movie",
            params={"api_key": TMDB_KEY, "query": titulo, "language": LANG},
            timeout=10,
        )
        resp.raise_for_status()
        resultados = resp.json().get("results", [])
        return [
            {
                "tmdb_id": m["id"],
                "titulo": m["title"],
                "ano": m["release_date"][:4] if m.get("release_date") else None,
                "nota": round(m["vote_average"], 1) if m.get("vote_average") else None,
                "cartaz_url": f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
            }
            for m in resultados[:8]
        ]


def _extrair_trailer(videos_resultados: list[dict]) -> Optional[str]:
    """Procura primeiro um Trailer; se não houver, aceita um Teaser. Ambos têm de estar no YouTube."""
    candidatos_youtube = [v for v in videos_resultados if v.get("site") == "YouTube"]

    trailer = next((v for v in candidatos_youtube if v.get("type") == "Trailer"), None)
    if trailer:
        return f"https://www.youtube.com/embed/{trailer['key']}"

    teaser = next((v for v in candidatos_youtube if v.get("type") == "Teaser"), None)
    if teaser:
        return f"https://www.youtube.com/embed/{teaser['key']}"

    return None


async def obter_detalhes_filme(tmdb_id: int) -> Optional[dict]:
    if not TMDB_KEY:
        return None
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{TMDB_BASE}/movie/{tmdb_id}",
            params={
                "api_key": TMDB_KEY,
                "language": LANG,
                "append_to_response": "videos",
            },
            timeout=10,
        )
        resp.raise_for_status()
        m = resp.json()

        genero_id = m["genres"][0]["id"] if m.get("genres") else None
        genero_nome = m["genres"][0]["name"] if m.get("genres") else None

        videos_resultados = m.get("videos", {}).get("results", [])
        trailer_url = _extrair_trailer(videos_resultados)

        # Se não houver vídeo em português, repete o pedido sem filtro de idioma
        if not trailer_url:
            resp_en = await client.get(
                f"{TMDB_BASE}/movie/{tmdb_id}",
                params={"api_key": TMDB_KEY, "append_to_response": "videos"},
                timeout=10,
            )
            m_en = resp_en.json()
            videos_en = m_en.get("videos", {}).get("results", [])
            trailer_url = _extrair_trailer(videos_en)

        return {
            "tmdb_id": m["id"],
            "titulo": m["title"],
            "titulo_original": m.get("original_title"),
            "ano": int(m["release_date"][:4]) if m.get("release_date") else None,
            "nota": round(m["vote_average"], 1) if m.get("vote_average") else None,
            "votos": m.get("vote_count"),
            "popularidade": m.get("popularity"),
            "genero": GENEROS_MAP.get(genero_id, "other") if genero_id else None,
            "genero_nome": genero_nome,
            "cartaz_url": f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
            "sinopse": m.get("overview"),
            "duracao_min": m.get("runtime"),
            "trailer_url": trailer_url,
        }
