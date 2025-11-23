const API_URL = "http://127.0.0.1:8000/api/estadisticas/";

export async function cargarEstadisticas() {
  const main = document.getElementById("contenido-principal");
  main.innerHTML = "<h2>Estadísticas</h2><p>Cargando datos...</p>";

  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Error al obtener estadísticas");

    const stats = await response.json();

    main.innerHTML = `
      <h2>📊 Estadísticas</h2>
      <ul>
        <li>Total de usuarios: ${stats.total_usuarios}</li>
        <li>Total de películas: ${stats.total_peliculas}</li>
        <li>Total de favoritos: ${stats.total_favoritos}</li>
        <li>Película más popular: ${stats.pelicula_mas_popular}</li>
        <li>Usuario más activo: ${stats.usuario_mas_activo}</li>
      </ul>
    `;
  } catch (error) {
    main.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
}