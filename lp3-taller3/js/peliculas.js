const API_URL = "http://127.0.0.1:8000/api/peliculas/";

export async function cargarPeliculas() {
  const main = document.getElementById("contenido-principal");
  main.innerHTML = "<h2>Películas</h2><p>Cargando películas...</p>";

  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Error al obtener películas");

    const peliculas = await response.json();

    if (peliculas.length === 0) {
      main.innerHTML = "<p>No hay películas registradas.</p>";
      return;
    }

    const contenedor = document.createElement("div");
    contenedor.classList.add("lista-peliculas");

    peliculas.forEach((p) => {
      const tarjeta = document.createElement("div");
      tarjeta.classList.add("pelicula");

      tarjeta.innerHTML = `
        <h3>${p.titulo} (${p["año"]})</h3>
        <p><strong>Director:</strong> ${p.director}</p>
        <p><strong>Género:</strong> ${p.genero}</p>
        <p><strong>Duración:</strong> ${p.duracion} min</p>
        <p><strong>Clasificación:</strong> ${p.clasificacion}</p>
        <p><strong>Sinopsis:</strong> ${p.sinopsis}</p>
      `;

      contenedor.appendChild(tarjeta);
    });

    main.innerHTML = "<h2>Películas</h2>";
    main.appendChild(contenedor);
  } catch (error) {
    main.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
}

export function mostrarFormularioPelicula() {
  const main = document.getElementById("contenido-principal");
  main.innerHTML = `
    <h2>Agregar nueva película</h2>
    <form id="form-pelicula">
      <input type="text" name="titulo" placeholder="Título" required />
      <input type="text" name="director" placeholder="Director" required />
      <input type="text" name="genero" placeholder="Género" required />
      <input type="number" name="duracion" placeholder="Duración (min)" required />
      <input type="number" name="año" placeholder="Año de estreno" required />
      <input type="text" name="clasificacion" placeholder="Clasificación" required />
      <textarea name="sinopsis" placeholder="Sinopsis" required></textarea>
      <button type="submit">Guardar</button>
    </form>
  `;

  document.getElementById("form-pelicula").addEventListener("submit", async (e) => {
    e.preventDefault();
    const datos = Object.fromEntries(new FormData(e.target));

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      });

      if (!response.ok) throw new Error("Error al guardar película");

      alert("Película guardada exitosamente");
      cargarPeliculas();
    } catch (error) {
      alert("Error: " + error.message);
    }
  });
}