const API_URL = "http://127.0.0.1:8000/api/usuarios/";

export async function cargarUsuarios() {
  const main = document.getElementById("contenido-principal");
  main.innerHTML = "<h2>Usuarios</h2><p>Cargando usuarios...</p>";

  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Error al obtener usuarios");

    const usuarios = await response.json();

    if (usuarios.length === 0) {
      main.innerHTML = "<p>No hay usuarios registrados.</p>";
      return;
    }

    const lista = document.createElement("ul");
    usuarios.forEach((u) => {
      const item = document.createElement("li");
      item.textContent = `${u.nombre} (${u.email})`;
      lista.appendChild(item);
    });

    main.innerHTML = "<h2>Usuarios</h2>";
    main.appendChild(lista);
  } catch (error) {
    main.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
}