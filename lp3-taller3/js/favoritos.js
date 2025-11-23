const API_URL_FAVORITOS = "http://127.0.0.1:8000/api/favoritos/";
const API_URL_USUARIOS = "http://127.0.0.1:8000/api/usuarios/";
const API_URL_PELICULAS = "http://127.0.0.1:8000/api/peliculas/";

export async function cargarFavoritos() {
  const main = document.getElementById("contenido-principal");
  main.innerHTML = "<h2>Favoritos</h2><p>Cargando favoritos...</p>";

  try {
    const response = await fetch(API_URL_FAVORITOS);
    const favoritos = await response.json();

    const lista = document.createElement("ul");
    favoritos.forEach((f) => {
      const item = document.createElement("li");
      item.textContent = `🎬 Película ID: ${f.id_pelicula} (Usuario ID: ${f.id_usuario})`;
      lista.appendChild(item);
    });

    main.innerHTML = "<h2>Favoritos</h2>";
    main.appendChild(lista);
  } catch (error) {
    main.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
}

export async function mostrarFormularioFavorito() {
  const main = document.getElementById("contenido-principal");
  main.innerHTML = "<h2>Agregar favorito</h2><p>Cargando datos...</p>";

  try {
    const [usuariosRes, peliculasRes] = await Promise.all([
      fetch(API_URL_USUARIOS),
      fetch(API_URL_PELICULAS),
    ]);

    const usuarios = await usuariosRes.json();
    const peliculas = await peliculasRes.json();

    const form = document.createElement("form");
    form.id = "form-favorito";
    form.innerHTML = `
      <label>Usuario:
        <select name="id_usuario" required>
          ${usuarios.map(u => `<option value="${u.id}">${u.nombre}</option>`).join("")}
        </select>
      </label>
      <label>Película:
        <select name="id_pelicula" required>
          ${peliculas.map(p => `<option value="${p.id}">${p.titulo}</option>`).join("")}
        </select>
      </label>
      <button type="submit">Guardar</button>
    `;

    main.innerHTML = "<h2>Agregar favorito</h2>";
    main.appendChild(form);

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const datos = Object.fromEntries(new FormData(form));

      try {
        const res = await fetch(API_URL_FAVORITOS, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(datos),
        });

        alert("Favorito guardado exitosamente");
        cargarFavoritos();
      } catch (error) {
        alert("Error: " + error.message);
      }
    });
  } catch (error) {
    main.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
}