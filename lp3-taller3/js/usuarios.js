const API_URL = "http://127.0.0.1:8000/api/usuarios/";

export async function cargarUsuarios() {
  const main = document.getElementById("contenido-principal");
  main.innerHTML = "<h2>Usuarios</h2><p>Cargando usuarios...</p>";

  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Error al obtener usuarios");

    const usuarios = await response.json();

    if (usuarios.length === 0) {
      main.innerHTML = "<h2>Usuarios</h2><p>No hay usuarios registrados.</p>";
      return;
    }

    let html = '<h2>Usuarios Registrados</h2><div class="lista-usuarios">';

    usuarios.forEach((u) => {
      html += `
        <div class="usuario-card">
          <h3>${u.nombre}</h3>
          <p><strong>Correo:</strong> ${u.correo}</p>
          <p><strong>Fecha registro:</strong> ${new Date(u.fecha_registro).toLocaleDateString('es-ES')}</p>
        </div>
      `;
    });

    html += '</div>';
    main.innerHTML = html;
  } catch (error) {
    main.innerHTML = `<h2>Usuarios</h2><p style="color:red;">Error: ${error.message}</p>`;
  }
}